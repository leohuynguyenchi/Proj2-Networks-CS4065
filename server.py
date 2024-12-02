import socket
import threading

# Globals
clients = []  # List of connected client sockets
message_boards = {f"g{i}": [] for i in range(1, 6)}  # Dictionary to store messages for each group (g1 to g5)
message_board = []  # List of messages for the public message board
client_usernames = {}  # Dictionary to map client sockets to their usernames
client_groups = {}  # Dictionary to map client sockets to the groups they have joined
# Lock for thread-safe operations
lock = threading.Lock()

# Broadcast a message to all connected clients in the public message board
def broadcast_message(message):
    with lock:
        for client in clients:
            try:
                # Send the message to the client
                client.send(message.encode('utf-8'))
            except:
                # If an error occurs (e.g., client disconnected), ignore and continue
                pass

# Broadcast a message to all connected clients in a specific group
def broadcast_messages(message, group):
    with lock:
        print(f"Broadcasting to group {group}: {message}")  # Debug message
        for client, groups in client_groups.items():
            # Check if the client has joined the specified group
            if group in groups:
                print(f"Sending to client {client}")  # Debug message
                try:
                    # Send the message to the client
                    client.send(f"{message}\n".encode('utf-8'))
                except Exception as e:
                    # If an error occurs, print the error and continue
                    print(f"Error sending to {client}: {e}")

# Handle individual client communication
def handle_client(client_socket):
    try:
        # Receive username from the client
        username = client_socket.recv(1024).decode('utf-8')
        with lock:
            # Store the username associated with the client socket
            client_usernames[client_socket] = username
            clients.append(client_socket)
        # Notify all clients in the public group that a new user has joined
        broadcast_message(f"{username} has joined the public group.")

        history = "Last 2 messages:\n"
        with lock:
            for msg in message_board[-2:]:
                history += msg + "\n"
        client_socket.send(history.encode('utf-8'))

        # Communication loop: listen for messages from the client
        while True:
            # Receive a message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                # If no message is received, client has disconnected
                break

            # Check for special commands
            if message.strip() == "%leave":
                # Client wants to leave the public group
                broadcast_message(f"{username} has left the public group.")
                break

            elif message.strip() == "%users":
                # Client requests the list of users
                with lock:
                    users = [client_usernames[client] for client in clients]
                client_socket.send(f"Users: {', '.join(users)}".encode('utf-8'))

            elif message.strip() == "%groups":
                # Client requests the list of groups
                with lock:
                    groups = list(message_boards.keys())
                client_socket.send(f"Groups: {', '.join(groups)}".encode('utf-8'))

            elif message.startswith("%groupjoin"):
                # Client wants to join one or more groups
                _, groups = message.split(maxsplit=1)
                selected_groups = groups.split(',')

                with lock:
                    if client_socket not in client_groups:
                        # If client is not in any groups yet, add the selected groups
                        client_groups[client_socket] = selected_groups
                    else:
                        # Add the selected groups to the client's group list if not already present
                        for group in selected_groups:
                            if group not in client_groups[client_socket]:
                                client_groups[client_socket].append(group)
                # Notify all clients in the selected groups that the user has joined
                for group in selected_groups:
                    broadcast_messages(f"{username} has joined {group}.", group)

            elif message.startswith("%grouppost"):
                # Client wants to post a message to a group
                _, group, content = message.split(maxsplit=2)
                formatted_message = f"Message from {username} in {group}: {content}"
                with lock:
                    message_boards[group].append(formatted_message)
                broadcast_messages(formatted_message, group)

            elif message.startswith("%groupusers"):
                # Client requests the list of users in a group
                _, group = message.split(maxsplit=1)
                with lock:
                    if group in client_groups.get(client_socket, []):
                        # If the client is a member of the group
                        users_in_group = [
                            client_usernames[client]
                            for client in client_groups
                            if group in client_groups[client]
                        ]
                        client_socket.send(f"Users in {group}: {', '.join(users_in_group)}".encode('utf-8'))
                    else:
                        # If the client is not a member of the group
                        client_socket.send(f"You are not a member of {group}".encode('utf-8'))

            elif message.startswith("%groupmessage"):
                # Client requests a specific message from a group's message board
                _, group, message_id = message.split(maxsplit=2)
                with lock:
                    if int(message_id) < len(message_boards[group]):
                        # If the message ID is valid
                        client_socket.send(message_boards[group][int(message_id)].encode('utf-8'))
                    else:
                        # If the message ID is invalid
                        client_socket.send("Message ID not found.".encode('utf-8'))

            elif message.startswith("%groupleave"):
                # Client wants to leave a group
                _, group = message.split(maxsplit=1)
                with lock:
                    if group in client_groups.get(client_socket, []):
                        client_groups[client_socket].remove(group)
                broadcast_messages(f"{username} has left {group}.", group)

            elif message.startswith("%message"):
                # Client requests a specific message from the public message board
                _, message_id = message.split(maxsplit=1)
                with lock:
                    if int(message_id) < len(message_board):
                        # If the message ID is valid
                        client_socket.send(message_board[int(message_id)].encode('utf-8'))
                    else:
                        # If the message ID is invalid
                        client_socket.send("Message ID not found.".encode('utf-8'))

            else:
                # Treat as a regular message to be added to the public message board
                formatted_message = f"Message from {username}: {message}"
                with lock:
                    # Add the message to the public message board
                    message_board.append(formatted_message)
                # Broadcast the message to all clients in the public message board
                broadcast_message(formatted_message)

            # The following commented code seems to be old or unused
            # else:
            #     formatted_message = f"Message from {username}: {message}"
            #     with lock:
            #         for group in selected_groups:
            #             # Add the message to the group's message board
            #             message_boards[group].append(formatted_message)
            #             # Broadcast the message to all clients in the group
            #             broadcast_messages(formatted_message, group)
    except:
        # Handle any exceptions that occur in the communication loop
        pass
    finally:
        # When the client disconnects or an error occurs
        # Remove client from the list
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
            if client_socket in client_usernames:
                # Remove the client's username
                username = client_usernames.pop(client_socket, "Unknown")
                # Notify all clients in the public group that the user has left
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
    # Listen for incoming connections, with a maximum backlog of 5
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
