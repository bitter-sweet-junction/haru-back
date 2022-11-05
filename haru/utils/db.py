import os

import pymongo

_client = None
_db = None


def init_database():
    global _client, _db

    uri = os.environ.get("MONGODB_URI")
    _client = pymongo.MongoClient(uri)
    _db = _client.haru


def get_database():
    global _db
    return _db
