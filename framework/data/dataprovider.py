# -*- coding:utf-8 -*-
import pymongo
from settings import settings

def conn():
    return pymongo.MongoClient(host=settings.PLATFORM_MONGODB_HOST, port=settings.PLATFORM_MONGODB_PORT, tz_aware=False)

def _metadb():
    return conn().get_database(settings.PLATFORM_MONGODB_DEFAULT)

def _flow_db():
    return conn().get_database(settings.WORKFLOW_MONGODB_DB)

metadb = _metadb()
flow_db = _flow_db()
