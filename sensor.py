from datetime import datetime, timedelta, timezone

from db_wrapper import DBWrapper

TZ = timezone(timedelta(hours=8))


class SensorManager:
    def __init__(self):
        self.db = DBWrapper()

    def is_online(self):

        now = datetime.now(TZ)
        ts = self.db.find_data("second", limit=1)[0]["timestamp"]

        return now - ts < timedelta(minutes=5)
