import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
UTC_TZ = ZoneInfo("UTC")
TAIPEI_TZ = ZoneInfo("Asia/Taipei")


class DBWrapper:
    def __init__(self):
        self.client = MongoClient(uri, tz_aware=True)
        self.db = self.client["air"]
        self.second_collection = self.db["second_air_data"]
        self.minute_collection = self.db["minute_air_data"]

    def find_data(self, time_unit, limit=180):
        if time_unit == "second":
            collection = self.second_collection
        else:
            collection = self.minute_collection

        results = list(collection.find({}).sort("timestamp", -1).limit(limit))

        results.reverse()
        self._convert_to_taipei_time(results)

        return results

    def delete_docs(self):
        cutoff = datetime.now(UTC_TZ) - timedelta(days=1)

        self.db.second_air_data.delete_many({"timestamp": {"$lt": cutoff}})
        self.db.minute_air_data.delete_many({"timestamp": {"$lt": cutoff}})

    @staticmethod
    def _convert_to_taipei_time(docs):
        for doc in docs:
            doc["timestamp"] = doc["timestamp"].astimezone(TAIPEI_TZ)
