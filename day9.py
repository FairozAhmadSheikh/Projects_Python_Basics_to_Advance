import pymongo
from datetime import datetime

def connect_db():
    """Connects to MongoDB and returns a collection."""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["TaskManager"]
    return db["tasks"]