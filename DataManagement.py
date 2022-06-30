# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:02:07 2021

@author: ClaudiaLoisR
"""
import pymongo

class DataManagement:
    
    def __init__(self):
        
        self.client = pymongo.MongoClient("mongodb://sulmongodb:qZmCs9lfEZ0xjPlQ1eZP0ZFHN3zRCHmZ4Pxj9aSguBkMFIRO6DivvTMMx00g3Fz6uPdG1uNrifHTm4BLTeRczg%3D%3D@sulmongodb.mongo.cosmos.azure.com:10255/?authSource=admin&maxIdleTimeMS=120000&appname=MongoDB%20Compass&retryWrites=false&ssl=true")
        self.db=self.client["Usr_ChatBot"]
        
    def store(self,data,collection):
        
        self.data=data
        self.collection=collection
        my_collection=self.db[collection]
        my_collection.insert_one(data)
        
    def insert(self,data):
       my_collection=self.db["Dropouts"]
       self.data=data
       return (my_collection.insert_one(data)).inserted_id
   
    def delete(self,id_):
       my_collection=self.db["Dropouts"]
       self.id_=id_
       my_collection.delete_one({'_id': id_})
   
    def update(self,id_,data):
       self.data=data
       self.id_=id_
       my_collection=self.db["Dropouts"]
       filter_ = { '_id': id_ }
       newvalues = { "$set": data}
       my_collection.update_one(filter_, newvalues)
        
   # def storeData(self,details):
        
        
    def storeMissed(self,missed):
        
        self.missed=missed
        my_collection=self.db["Missed"]
        my_collection.insert_one(missed)
    