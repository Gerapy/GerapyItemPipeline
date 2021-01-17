import pymongo
from gerapy_item_pipeline.settings import *


class MongoDBPipeline(object):
    
    @classmethod
    def from_crawler(cls, crawler):
        """
        set mongodb settings
        :param crawler: scrapy crawler
        :return:
        """
        cls.connection_string = crawler.settings.get('MONGODB_CONNECTION_STRING', MONGODB_CONNECTION_STRING)
        cls.database_name = crawler.settings.get('MONGODB_DATABASE_NAME', MONGODB_DATABASE_NAME)
        cls.upsert = crawler.settings.get('MONGODB_UPSERT', MONGODB_UPSERT)
        cls.collection_name_field = crawler.settings.get('MONGODB_COLLECTION_NAME_FIELD',
                                                         MONGODB_COLLECTION_NAME_FIELD)
        cls.collection_name_default = crawler.settings.get('MONGODB_COLLECTION_NAME_DEFAULT',
                                                           MONGODB_COLLECTION_NAME_DEFAULT)
        cls.item_primary_key_field = crawler.settings.get('MONGODB_ITEM_PRIMARY_KEY_FIELD',
                                                          MONGODB_ITEM_PRIMARY_KEY_FIELD)
        cls.item_primary_key_default = crawler.settings.get('MONGODB_ITEM_PRIMARY_KEY_DEFAULT',
                                                            MONGODB_ITEM_PRIMARY_KEY_DEFAULT)
        return cls()
    
    def open_spider(self, spider):
        """
        called when spider open
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
    
    def process_item(self, item, spider):
        """
        process item
        :param item: item scraped
        :param spider: spider object
        :return:
        """
        # update collection_name
        if isinstance(item, dict):
            collection_name = item.get(self.collection_name_field,
                                       self.collection_name_default)
        else:
            if hasattr(item, self.collection_name_field):
                collection_name = getattr(item, self.collection_name_field) or self.collection_name_default
            else:
                collection_name = item.get(self.collection_name_field,
                                           self.collection_name_default)
        # update primary_key_field
        if isinstance(item, dict):
            primary_key_field = item.get(self.item_primary_key_field,
                                         self.item_primary_key_default)
        else:
            if hasattr(item, self.item_primary_key_field):
                primary_key_field = getattr(item, self.item_primary_key_field) or self.item_primary_key_default
            else:
                primary_key_field = getattr(item, self.item_primary_key_field) or \
                                    item.get(self.item_primary_key_field,
                                             self.item_primary_key_default)
        if self.upsert:
            self.db[collection_name].update({
                primary_key_field: item.get(primary_key_field)
            }, {
                '$set': item
            }, upsert=True)
        else:
            self.db[collection_name].insert(item)
        return item
    
    def close_spider(self, spider):
        """
        close client when spider closes
        :param spider:
        :return:
        """
        self.client.close()
