from datetime import datetime, timedelta
from db_wrapper import DBWrapper


class SensorManager:
    def __init__(self):
        self.db = DBWrapper()
    
    def is_online(self):
        now = datetime.now()
        ts = self.db.find_data("second", limit=1)[0]['timestamp']
        if now - ts < timedelta(minutes=5):
            return True
        
        return False
    