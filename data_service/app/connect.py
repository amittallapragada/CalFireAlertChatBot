from pymongo import MongoClient
import os
DB_HOST = os.environ.get("MONGODB_HOST")
DB_NAME = os.environ.get("MONGODB_DATABASE")
DB_USERNAME = os.environ.get("MONGODB_USERNAME")
DB_PASSWORD = os.environ.get("MONGODB_PASSWORD")


class Database:
    def __init__(self, db_name=DB_NAME, db_host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD, collection_name=None):
        client = MongoClient(db_host, username=username, password=password, authMechanism='SCRAM-SHA-256')
        db = client[db_name]
        self.coll = db[collection_name]

    def put_item(self, Item=None):
        try:
            self.coll.insert_one(Item)
        except Exception as e:
            print(e)
            raise e 
    
    def query(self, key=None, value=None):
        try:
            documents = self.coll.find({key:value})
            response = [doc for doc in documents]
            print(response)
            return {"Items": response}
        except Exception as e:
            print(e)
            return e



