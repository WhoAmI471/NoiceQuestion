from pymongo import MongoClient
client = MongoClient("mongodb+srv://admin:uHVLqOSKXXcH6mSN@cluster0.olzd1kw.mongodb.net/?retryWrites=true&w=majority")

db = client.stats_db

user_stats_collection = db["stats_collection"]