from cryptography.fernet import Fernet
import json
import os
import getpass
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as file:
        file.write(key)

def load_key():
    return open(KEY_FILE, "rb").read()

if not os.path.exists(KEY_FILE):
    generate_key()

fernet = Fernet(load_key())

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
def encrypt(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()
def add_password():
    service = input("Enter service name: ")
    username = input("Enter username/email: ")
    password = getpass.getpass("Enter password: ")

    data = load_data()
    data[service] = {
        "username": encrypt(username),
        "password": encrypt(password)
    }
    save_data(data)
    print(f"🔐 Password for '{service}' added successfully.")