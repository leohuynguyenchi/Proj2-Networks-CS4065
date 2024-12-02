"""
Simple Chat Client

This script implements a command-line chat client that connects to a chat server.
It supports various commands to interact with the server and other users.

Commands:
    %connect <address> <port> - Connect to the chat server
    %join - Join the server with a username
    %post <message> - Send a message to all users
    %users - Get the list of users connected to the server
    %leave - Disconnect from the server
    %exit - Exit the chat client
    %message <message_id> - Retrieve a specific message by ID
    %groups - List available groups
    %groupjoin <group_names> - Join specified groups
    %grouppost <group> <message> - Send a message to a group
    %groupusers <group> - List users in a group
    %groupleave <group> - Leave a group
    %groupmessage <group> <message_id> - Retrieve a message from a group

Usage:
    Run the script and enter commands as prompted.
"""

import socket     # For networking operations
import threading  # For handling concurrent threads

def receive_messages(sock):
    # Function to continuously receive messages from the server
    while True:
        try:
            # Receive data from the server
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            # If an error occurs, notify and exit the loop
            print("Connection closed.")
            break

def main():
    client_socket = None  # Initialize the client socket
    # Command loop to process user inputs
    while True:
        command = input("> ").strip()  # Read command from user

        # Handle %connect command to connect to the server
        if command.startswith("%connect"):
            # Parse the address and port from the command
            _, address, port = command.split()
            server_address = (address, int(port))
            # Create a new socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect(server_address)
                print("Connected to the server.")
                # Start a new thread to receive messages from the server
                threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            except:
                # If connection fails, notify user and reset client_socket
                print("Connection failed.")
                client_socket = None

        # Handle %join command to join the server with a username
        elif command.startswith("%join"):
            if client_socket:
                username = input("Enter your username: ")
                # Send the username to the server
                client_socket.send(username.encode('utf-8'))
                client_socket.send("%users".encode('utf-8')) # Request the list of users
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %post command to send a message to the server
        elif command.startswith("%post"):
            if client_socket:
                # Extract the message content after the command
                _, content = command.split(maxsplit=1)
                message = f"{content}"
                client_socket.send(message.encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %users command to request the list of users from the server
        elif command.startswith("%users"):
            if client_socket:
                client_socket.send("%users".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %leave command to disconnect from the server
        elif command.startswith("%leave"):
            if client_socket:
                # Notify the server about leaving
                client_socket.send("%leave".encode('utf-8'))
                client_socket.close()
                client_socket = None
                print("Disconnected from the server.")
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %exit command to exit the client application
        elif command.startswith("%exit"):
            if client_socket:
                client_socket.send("%leave".encode('utf-8'))
                client_socket.close()
            print("Exiting the client.")
            break  # Exit the command loop and terminate the program

        # Handle %message command to retrieve a specific message by ID
        elif command.startswith("%message"):
            if client_socket:
                _, message_id = command.split(maxsplit=1)
                client_socket.send(f"%message {message_id}".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %groups command to list available groups on the server
        elif command.startswith("%groups"):
            if client_socket:
                client_socket.send("%groups".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %groupjoin command to join specified groups
        elif command.startswith("%groupjoin"):
            if client_socket:
                _, groups = command.split(maxsplit=1)
                client_socket.send(f"%groupjoin {groups}".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %grouppost command to send a message to a group
        elif command.startswith("%grouppost"):
            if client_socket:
                _, group, content = command.split(maxsplit=2)
                message = f"%grouppost {group} {content}"
                client_socket.send(message.encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %groupusers command to list users in a specific group
        elif command.startswith("%groupusers"):
            if client_socket:
                _, group = command.split(maxsplit=1)
                client_socket.send(f"%groupusers {group}".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %groupleave command to leave a specific group
        elif command.startswith("%groupleave"):
            if client_socket:
                _, group = command.split(maxsplit=1)
                client_socket.send(f"%groupleave {group}".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # Handle %groupmessage command to retrieve a specific message from a group
        elif command.startswith("%groupmessage"):
            if client_socket:
                _, group, message_id = command.split(maxsplit=2)
                client_socket.send(f"%groupmessage {group} {message_id}".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")

        # If command is not recognized, notify the user
        else:
            print("Unknown command. Please use one of the specified commands.")

if __name__ == "__main__":
    main()
