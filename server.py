import socket
import threading

# Globals
clients = []
message_board = []
client_usernames = {}

lock = threading.Lock()

# Broadcast a message to all connected clients
def broadcast_message(message):
    with lock:
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

# Handle individual client communication
def handle_client(client_socket):
    try:
        # Receive username
        username = client_socket.recv(1024).decode('utf-8')
        with lock:
            client_usernames[client_socket] = username
            clients.append(client_socket)
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
            if not message or message.strip() == "%leave":
                break
            formatted_message = f"Message from {username}: {message}"
            with lock:
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
                broadcast_message(f"{username} has left the group.")
        client_socket.close()

# Start the server
def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server is running on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()
