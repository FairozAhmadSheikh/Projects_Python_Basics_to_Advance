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
                        bytes_read = client.recv(min(BUFFER_SIZE, filesize))
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                        filesize -= len(bytes_read)
                broadcast(f"[File Received] {filename}", client)
            else:
                broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            username = usernames[index]
            usernames.remove(username)
            client.close()
            broadcast(f"{username} has left the chat.", None)
            break
# Broadcast messages to all clients
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

# Main server function
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION] {address} connected.")

        client.send("USERNAME".encode('utf-8'))
        username = client.recv(BUFFER_SIZE).decode('utf-8')
        usernames.append(username)
        clients.append(client)
        
        print(f"Username is {username}")
        broadcast(f"{username} has joined the chat!", client)
        client.send("Connected to the server!".encode('utf-8'))