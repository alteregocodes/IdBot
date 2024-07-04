from pymongo import MongoClient
import config

class Database:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        self.blacklist_collection = self.db["blacklist"]

    def add_to_blacklist(self, name):
        name = name.lower()
        if not self.blacklist_collection.find_one({"name": name}):
            self.blacklist_collection.insert_one({"name": name})

    def load_blacklist(self):
        return [item["name"] for item in self.blacklist_collection.find()]

    def remove_from_blacklist(self, name):
        name = name.lower()
        self.blacklist_collection.delete_one({"name": name})

# Contoh penggunaan:
# db = Database()
# db.add_to_blacklist("spammer")
# print(db.load_blacklist())
