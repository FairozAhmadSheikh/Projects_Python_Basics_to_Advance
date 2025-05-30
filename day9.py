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
def view_tasks(collection):
    """Displays all tasks."""
    tasks = collection.find()
    for task in tasks:
        print(f"Title: {task['title']}, Due Date: {task['due_date']}, Description: {task['description']}")
def update_task(collection):
    """Updates an existing task."""
    title = input("Enter task title to update: ")
    new_description = input("Enter new description: ")
    result = collection.update_one({"title": title}, {"$set": {"description": new_description}})
    if result.modified_count:
        print("Task updated successfully!")
    else:
        print("Task not found.")

def delete_task(collection):
    """Deletes a task from the database."""
    title = input("Enter task title to delete: ")
    result = collection.delete_one({"title": title})
    if result.deleted_count:
        print("Task deleted successfully!")
    else:
        print("Task not found.")
def main():
    collection = connect_db()
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            add_task(collection)
        elif choice == "2":
            view_tasks(collection)
        elif choice == "3":
            update_task(collection)
        elif choice == "4":
            delete_task(collection)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
if __name__ == "__main__":
    main()