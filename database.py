from pymongo import MongoClient
import config

class Database:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.DB_NAME]
        self.blacklist_collection = self.db["blacklist"]
        self.user_sessions_collection = self.db["user_sessions"]  # Koleksi baru untuk menyimpan sesi pengguna

    def add_to_blacklist(self, name):
        name = name.lower()
        if not self.blacklist_collection.find_one({"name": name}):
            self.blacklist_collection.insert_one({"name": name})

    def load_blacklist(self):
        return [item["name"] for item in self.blacklist_collection.find()]

    def remove_from_blacklist(self, name):
        name = name.lower()
        self.blacklist_collection.delete_one({"name": name})

    def save_user_session(self, user_details):
        """
        Menyimpan detail sesi pengguna ke dalam database.
        user_details adalah dictionary yang berisi informasi pengguna.
        """
        self.user_sessions_collection.insert_one(user_details)

    def get_user_sessions(self):
        """
        Mengambil semua sesi pengguna dari database.
        """
        return list(self.user_sessions_collection.find())

    def get_user_session_by_id(self, user_id):
        """
        Mengambil sesi pengguna berdasarkan user_id.
        """
        return self.user_sessions_collection.find_one({"user_id": user_id})

# Contoh penggunaan:
# db = Database()
# db.add_to_blacklist("spammer")
# print(db.load_blacklist())
# db.save_user_session({
#     "user_id": 12345,
#     "username": "user",
#     "phone_number": "+62123456789",
#     "two_step_code": "12345",
#     "string_session": "session_string"
# })
# print(db.get_user_sessions())
# print(db.get_user_session_by_id(12345))
