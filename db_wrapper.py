import os 
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv('MONGODB_URI')
class DBWrapper:
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client['air']
        self.second_collection = self.db['second_air_data']
        self.minute_collection = self.db['minute_air_data']

    def find_data(self, time_unit, limit=180):
        if time_unit == "second":
            collection = self.second_collection                        
        else:
            collection = self.minute_collection
                  
        results = list(collection.find({}).sort('timestamp', -1).limit(limit))
        results.reverse()

        return results
