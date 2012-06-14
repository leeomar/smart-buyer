#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo.connection import Connection
from pymongo import DESCENDING, ASCENDING
#from pymongo import objectid
from bson.objectid import ObjectId
from scrapy import log

class MongoClient:
    PRIMARY_KEY = 'uid'
    OBJECTID_KEY = '_id'

    def __init__(self):
        pass

    def connect(self, host, port, dbname, default_collection=None):
        self.dbclient = Connection(host, port)
        self.db = self.dbclient[dbname]
        self.default_collection = default_collection
        log.msg("connect to mongo[%s:%s], db:%s, collection:%s"\
            %(host, port, dbname, default_collection))
        return self

    def create_index(self, feild_name, ascending=True, collection=None): 
        self.get_collection(collection).create_index( \
                [(feild_name, ASCENDING if ascending else DESCENDING),])

    def get_collection(self, collection=None):
        if collection is None:
            collection = self.default_collection

        return self.db[collection]
    
    def get_objectid(self, key):
        return ObjectId(str(key))

    def insert(self, dict_obj, pk=None, collection=None):
        if pk is not None:
            dict_obj[MongoClient.PRIMARY_KEY] = pk 
        self.get_collection(collection).insert(dict_obj)
        log.msg('insert %s, collection:%s' % (dict_obj, collection))
        return dict_obj
    
    def insert_field(self, pk, collection=None, **kws):
        collection = self.get_collection(collection)
        collection.update({MongoClient.PRIMARY_KEY : pk},
            {'$push': kws}, 
            upsert = True)

    def update_field(self, pk, collection=None, **kws):
        collection = self.get_collection(collection)
        collection.update({MongoClient.PRIMARY_KEY : pk},
                {'$set': kws},
                upsert=True)
    
    def find_one(self, pk, collection=None):
        collection = self.get_collection(collection)
        result = collection.find_one({MongoClient.PRIMARY_KEY : pk})
        log.msg('get %s from %s' % (result, collection))
        return result

    def find(self, collection=None, **kws):
        collection = self.get_collection(collection)
        return collection.find(kws)
    
if __name__ == '__main__':
    client = MongoClient().connect('127.0.0.1', 27017, "test", "test")

    key=111
    client.insert({'data' : [{'begin' : 1}]}, key)
    print client.find_one(key)
    print '============='
    client.insert_field(key, data={'price': 127, 'time': 123459} ,
            shop="360buy.com")
    print client.find_one(key)
    print '============='

    client.update_field(key, shop='newegg.com', version=23)
    print client.find_one(key)
    print '============='

    print client.find(shop='newegg.com')
    print client.find(shop='newegg.com')[0]
