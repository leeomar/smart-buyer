#!/usr/bin/python
# -*- coding: utf-8 -*-

from pymongo.connection import Connection
from pymongo import DESCENDING, ASCENDING
from pymongo import objectid

class MongoClient:
    PRIMARY_KEY = 'uid'
    OBJECTID_KEY = '_id'

    def __init__(self):
        pass

    def connect(self, host, port, dbname, default_collection_name=None):
        self.dbclient = Connection(host, port)
        self.db = self.dbclient[dbname]
        self.default_collection_name = default_collection_name
        return self

    def create_index(self, feild_name, ascending=True, collection_name=None): 
        self.get_collection(collection_name).create_index( \
                [(feild_name, ASCENDING if ascending else DESCENDING),])

    def get_collection(self, collection_name=None):
        if collection_name is None:
            collection_name = self.default_collection_name

        return self.db[collection_name]
    
    def get_objectid(self, key):
        return objectid.ObjectId(str(key))

    def insert(self, dict_obj, pk=None, collection_name=None):
        if pk is not None:
            dict_obj[MongoClient.PRIMARY_KEY] = pk 
        self.get_collection(collection_name).insert(dict_obj)
        #return str(dict_obj[MongoClient.OBJECTID_KEY])
        return dict_obj
    
    def insert_field(self, pk, collection_name=None, **field_value_pairs):
        collection = self.get_collection(collection_name)
        collection.update({MongoClient.PRIMARY_KEY : pk},
            {'$push': field_value_pairs}, 
            upsert = True)

    def update_field(self, pk, collection_name=None, **field_value_pairs):
        collection = self.get_collection(collection_name)
        collection.update({MongoClient.PRIMARY_KEY : pk},
                {'$set': field_value_pairs},
                upsert=True)
    
    def find_one(self, pk, collection_name=None):
        collection = self.get_collection(collection_name)
        return collection.find_one({MongoClient.PRIMARY_KEY : pk})

    def find(self, collection_name=None, **field_value_pairs):
        collection = self.get_collection(collection_name)
        return collection.find(field_value_pairs)
    
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
