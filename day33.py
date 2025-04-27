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