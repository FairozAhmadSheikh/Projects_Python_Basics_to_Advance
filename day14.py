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
