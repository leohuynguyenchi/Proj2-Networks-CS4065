import socket
import threading

# Globals
clients = [] # List of connected clients
message_board = [] # List of messages
client_usernames = {} # Dictionary to map client sockets to client usernames
#lock for thread-safe operations
lock = threading.Lock()

# Broadcast a message to all connected clients
def broadcast_message(message):
    with lock:
        for client in clients:
            try:
                # Send the message to the client
                client.send(message.encode('utf-8'))
            except:
                pass

# Handle individual client communication
def handle_client(client_socket):
    try:
        # Receive username from client
        username = client_socket.recv(1024).decode('utf-8')
        with lock:
            # Store the username and add the client to the list
            client_usernames[client_socket] = username
            clients.append(client_socket)
        # Notify all clients that a new user has joined
        broadcast_message(f"{username} has joined the group.")

        # Send last 2 messages from the message board
        history = "Last 2 messages:\n"
        with lock:
            for msg in message_board[-2:]:
                history += msg + "\n"
        client_socket.send(history.encode('utf-8'))

        # Communication loop
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.strip() == "%leave":
                broadcast_message(f"{username} has left the group.")
                break
            formatted_message = f"Message from {username}: {message}"
            with lock:
                # Add the message to the message board
                message_board.append(formatted_message)
            broadcast_message(formatted_message)
    except:
        pass
    finally:
        # Remove client from the list
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
            if client_socket in client_usernames:
                username = client_usernames.pop(client_socket, "Unknown")
                # Notify all clients that the user has left
                broadcast_message(f"{username} has left the group.")
        #Close the client socket
        client_socket.close()

# Start the server
def main():
    host = '127.0.0.1'
    port = 8080

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port)) # Bind the socket to the address and port
    server_socket.listen(5) #Listen for incoming connections

    print(f"Server is running on {host}:{port}...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()
