import socket
import threading
import os

# Constants
HOST = '127.0.0.1'
PORT = 5555
SEPARATOR = '<SEPARATOR>'
BUFFER_SIZE = 4096

clients = []
usernames = []
# Handle individual client connection
def handle_client(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('utf-8')
            if message.startswith('FILE_SEND'):
                filename, filesize = message.split(SEPARATOR)[1:]
                filename = os.path.basename(filename)
                filesize = int(filesize)
                with open("received_" + filename, "wb") as f:
                    while filesize > 0:
                        