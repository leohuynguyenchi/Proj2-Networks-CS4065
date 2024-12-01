import socket
import threading

# Globals
clients = []  # List of connected clients
message_boards = {f"g{i}": [] for i in range(1, 6)}  # Dictionary to store messages for each group
message_board = []  # List of messages for the single message board
client_usernames = {}  # Dictionary to map client sockets to client usernames
client_groups = {}  # Dictionary to map client sockets to groups
# Lock for thread-safe operations
lock = threading.Lock()
message_counter = 0  # Global message counter

# Broadcast a message to all connected clients in a message board
def broadcast_message(message):
    with lock:
        for client in clients:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

# Broadcast a message to all connected clients in a group(s)
def broadcast_messages(message, group):
    with lock:
        for client in client_groups:
            if group in client_groups[client]:
                try:
                    # Send the message to the client
                    client.send(message.encode('utf-8'))
                except:
                    pass

# Handle individual client communication
def handle_client(client_socket):
    global message_counter
    try:
        # Receive username from the client
        username = client_socket.recv(1024).decode('utf-8')
        with lock:
            # Store the username
            client_usernames[client_socket] = username
            clients.append(client_socket)
        broadcast_message(f"{username} has joined the public group.")

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
                broadcast_message(f"{username} has left the public group.")
                break

            # Handle %users command -> Retrieve the list of users
            if message.strip() == "%users":
                with lock:
                    users = [client_usernames[client] for client in clients]
                client_socket.send(f"Users: {', '.join(users)}".encode('utf-8'))

            elif message.strip() == "%groups":
                # Send the list of groups to the client
                with lock:
                    groups = list(message_boards.keys())
                client_socket.send(f"Groups: {', '.join(groups)}".encode('utf-8'))

            elif message.startswith("%groupjoin"):
                _, groups = message.split(maxsplit=1)
                with lock:
                    if client_socket not in client_groups:
                        client_groups[client_socket] = []
                    for group in groups:
                        if group not in client_groups[client_socket]:
                            client_groups[client_socket].append(group)
                broadcast_messages(f"{username} has joined {groups}.", group)

            elif message.startswith("%grouppost"):
                _, group, content = message.split(maxsplit=2)
                with lock:
                    message_id = len(message_boards[group])
                    formatted_message = f"Message {message_id} from {username} in {group}: {content}"
                    # Add the message to the group's message board
                    message_boards[group].append(formatted_message)
                    # Broadcast the message to all clients in the group
                    broadcast_messages(formatted_message, group)

            elif message.startswith("%groupusers"):
                _, group = message.split(maxsplit=1)
                with lock:
                    users_in_group = []
                    for client in client_groups:
                        if group in client_groups[client]:
                            users_in_group.append(client_usernames[client])
                    client_socket.send(f"Users in {group}: {', '.join(users_in_group)}".encode('utf-8'))

            elif message.startswith("%groupmessage"):
                _, group, message_id = message.split(maxsplit=2)
                with lock:
                    if int(message_id) < len(message_boards[group]):
                        client_socket.send(message_boards[group][int(message_id)].encode('utf-8'))
                    else:
                        client_socket.send("Message ID not found.".encode('utf-8'))

            elif message.startswith("%groupleave"):
                _, group = message.split(maxsplit=1)
                with lock:
                    if group in client_groups[client_socket]:
                        client_groups[client_socket].remove(group)
                        broadcast_messages(f"{username} has left {group}.", group)

            elif message.startswith("%message"):
                _, message_id = message.split(maxsplit=1)
                with lock:
                    try:
                        message_id = int(message_id)
                        if 0 <= message_id < len(message_board):
                            client_socket.send(message_board[message_id].encode('utf-8'))
                        else:
                            client_socket.send("Message ID not found.".encode('utf-8'))
                    except ValueError:
                        client_socket.send("Invalid message ID.".encode('utf-8'))

            else:
                with lock:
                    formatted_message = f"Message {message_counter} from {username}: {message}"
                    message_board.append(formatted_message)
                    message_counter += 1
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
        # Close the client socket
        client_socket.close()

# Start the server
def main():
    host = 'localhost'
    port = 8080

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen(5)

    print(f"Server is running on {host}:{port}...")

    while True:
        # Accept a new connection
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")
        # Start a new thread to handle the client
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == "__main__":
    main()
