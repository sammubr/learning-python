from pymongo import MongoClient
import os

class MongoConfig:
    def __init__(self):
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = MongoClient(self.mongo_url)
        self.db = self.client.test_database
        self._create_indexes()

    def get_database(self):
        return self.db

    def _create_indexes(self):
        self.db.cars.create_index("description", unique=True)