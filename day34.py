import socket
import threading

# Server settings
HOST = '127.0.0.1'  # localhost
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)
# Handle client
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'🚪 {nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break
# Receive connections
def receive():
    print('🖥️ Server is running...')
    while True:
        client, address = server.accept()
        print(f"✅ Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"👤 Nickname: {nickname}")
        broadcast(f'📢 {nickname} joined the chat!'.encode('utf-8'))
        client.send('🛡️ Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()


# Client Code 

import socket
import threading

# Server settings
HOST = '127.0.0.1'
PORT = 55555

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Listen to server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("❌ An error occurred!")
            client.close()
            break

# Send messages
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# Start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
