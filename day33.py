# pip install cryptography
from cryptography.fernet import Fernet
import json
import os

# Generate a new key (ONLY ONCE) and save it
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the previously generated key
def load_key():
    return open("secret.key", "rb").read()
# Encrypt and save passwords
def save_password(service, username, password):
    key = load_key()
    fernet = Fernet(key)

    if os.path.exists("passwords.json"):
        with open("passwords.json", "rb") as file:
            data = json.loads(fernet.decrypt(file.read()).decode())
    else:
        data = {}

    data[service] = {"username": username, "password": password}
    encrypted_data = fernet.encrypt(json.dumps(data).encode())

    with open("passwords.json", "wb") as file:
        file.write(encrypted_data)
        # Retrieve passwords
def retrieve_password(service):
    key = load_key()
    fernet = Fernet(key)

    try:
        with open("passwords.json", "rb") as file:
            data = json.loads(fernet.decrypt(file.read()).decode())
        if service in data:
            print(f"Service: {service}")
            print(f"Username: {data[service]['username']}")
            print(f"Password: {data[service]['password']}")
        else:
            print("No details for this service.")
    except Exception as e:
        print("Error reading data:", e)
    def main():
if not os.path.exists("secret.key"):
    generate_key()

while True:
    choice = input("\n1. Save Password\n2. Retrieve Password\n3. Exit\nEnter Choice: ")

    if choice == '1':
        service = input("Service Name: ")
        username = input("Username: ")
        password = input("Password: ")
        save_password(service, username, password)
        print("✅ Password Saved Securely!")

    elif choice == '2':
        service = input("Enter Service Name to Retrieve: ")
        retrieve_password(service)

    elif choice == '3':
        print("🔒 Exiting Password Manager. Stay Safe!")
        break

    else:
        print("❌ Invalid Choice. Try Again.")

if __name__ == "__main__":
main()