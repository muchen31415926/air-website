from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from db_wrapper import DBWrapper

TAIPEI_TZ = ZoneInfo("Asia/Taipei")


class SensorManager:
    def __init__(self):
        self.db = DBWrapper()

    def is_online(self):

        now = datetime.now(TAIPEI_TZ)
        ts = self.db.find_data("second", limit=1)[0]["timestamp"]

        return now - ts < timedelta(minutes=5)
