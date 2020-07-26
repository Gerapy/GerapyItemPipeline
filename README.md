# Gerapy Item Pipeline

This is a package for supporting Item Pipelines in Scrapy, also this
package is a module in [Gerapy](https://github.com/Gerapy/Gerapy).

## Installation

```shell script
pip3 install gerapy-item-pipeline
```

## Usage

These are all kinds of the storage implemented.

### MongoDB

```python
MONGODB_CONNECTION_STRING = 'localhost'
MONGODB_DATABASE_NAME = 'default'
MONGODB_UPSERT = True
MONGODB_COLLECTION_NAME_FIELD = 'mongodb_collection_name'
MONGODB_COLLECTION_NAME_DEFAULT = 'default'
MONGODB_ITEM_PRIMARY_KEY_FIELD = 'primary_key'
MONGODB_ITEM_PRIMARY_KEY_DEFAULT = 'id'
```

