# your chat goes here

import socket
import threading

# Define server settings
HOST = '127.0.0.1'  # Localhost
PORT = 5555         # Port to bind to

# Create a list to store connected clients
clients = []

# Broadcast message to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

# Handle each client connection
def handle_client(client_socket):
    while True:
        try:
            # Receive the message from the client
            message = client_socket.recv(1024)
            if message:
                print(f"Received: {message.decode('utf-8')}")
                broadcast(message, client_socket)  # Send to other clients
            else:
                # If no message, disconnect client
                clients.remove(client_socket)
                client_socket.close()
                break
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Allow up to 5 clients

    print(f"Server started on {HOST}:{PORT}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection: {client_address}")

        clients.append(client_socket)

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
