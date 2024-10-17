import pymongo
import json

class MongoClient:
    def __init__(self, db_url: str):
        self.client = pymongo.MongoClient(db_url)

    def insert_sensor(self, data: dict):
        db = self.client["SensorDatabase"]
        db.ApiData.insert_one(data)
    
    def insert_modbus(self, data: dict):
        db = self.client["ModbusDatabase"]
        db.ApiData.insert_one(data)

    def get_all_documents(self):
        db = self.client["SensorDatabase"]
        try:
            documents = list(db.ApiData.find())
            for doc in documents:
                doc['_id'] = str(doc['_id'])
            return json.dumps(documents, indent=4)
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return None