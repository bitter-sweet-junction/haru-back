import os

from pymongo import MongoClient
from pymongo.database import Database

_client = None
_db = None


def init_database():
    global _client, _db

    uri = os.environ.get("MONGODB_URI")
    _client = MongoClient(uri)
    _db = _client.haru


def get_database() -> Database:
    global _db
    return _db
