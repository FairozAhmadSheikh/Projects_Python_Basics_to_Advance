import pymongo
from datetime import datetime

def connect_db():
    """Connects to MongoDB and returns a collection."""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["TaskManager"]
    return db["tasks"]
def add_task(collection):
    """Adds a new task to the database."""
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    task = {"title": title, "description": description, "due_date": due_date, "created_at": datetime.now()}
    collection.insert_one(task)
    print("Task added successfully!")