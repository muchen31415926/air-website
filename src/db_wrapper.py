import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv('MONGODB_URI')
class DBWrapper:
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client['air']
        self.collection = self.db['air']

    def find_data(self, limit=180):
        results = list(
            self.collection.find({}).sort('timestamp', -1).limit(limit)
        )     

        results.reverse()
        
        return results
