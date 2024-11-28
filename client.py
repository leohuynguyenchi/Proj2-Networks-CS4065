import socket
import threading

def receive_messages(sock):
    while True:
        # Receive messages from the server
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            # If an error occurs, close the connection
            print("Connection closed.")
            break

def main():
    client_socket = None
    # Command loop
    while True:
        command = input("> ").strip()
        # Connect command
        if command.startswith("%connect"):
            _, address, port = command.split()
            server_address = (address, int(port))
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                client_socket.connect(server_address)
                print("Connected to the server.")
                threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            except:
                print("Connection failed.")
                client_socket = None

        # Join command
        elif command.startswith("%join"):
            if client_socket:
                username = input("Enter your username: ")
                client_socket.send(username.encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")
        # Post command
        elif command.startswith("%post"):
            if client_socket:
                _, content = command.split(maxsplit=1)
                message = f"{content}"
                client_socket.send(message.encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")
        # Users command
        elif command.startswith("%users"):
            if client_socket:
                client_socket.send("%users".encode('utf-8'))
            else:
                print("You need to connect to the server first using %connect command.")
        # Leave command
        elif command.startswith("%leave"):
            if client_socket:
                client_socket.send("%leave".encode('utf-8'))
                client_socket.close()
                client_socket = None
                print("Disconnected from the server.")
            else:
                print("You need to connect to the server first using %connect command.")
        # Exit command
        elif command.startswith("%exit"):
            if client_socket:
                client_socket.send("%leave".encode('utf-8'))
                client_socket.close()
            print("Exiting the client.")
            break

        # elif command.startswith("%groups"):
        #     if client_socket:
        #         client_socket.send("%groups".encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        # elif command.startswith("%groupjoin"):
        #     if client_socket:
        #         _, group = command.split(maxsplit=1)
        #         client_socket.send(f"%groupjoin {group}".encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        # elif command.startswith("%grouppost"):
        #     if client_socket:
        #         _, group, subject, content = command.split(maxsplit=3)
        #         message = f"%grouppost {group} {subject}: {content}"
        #         client_socket.send(message.encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        # elif command.startswith("%groupusers"):
        #     if client_socket:
        #         _, group = command.split(maxsplit=1)
        #         client_socket.send(f"%groupusers {group}".encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        # elif command.startswith("%groupleave"):
        #     if client_socket:
        #         _, group = command.split(maxsplit=1)
        #         client_socket.send(f"%groupleave {group}".encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        # elif command.startswith("%groupmessage"):
        #     if client_socket:
        #         _, group, message_id = command.split(maxsplit=2)
        #         client_socket.send(f"%groupmessage {group} {message_id}".encode('utf-8'))
        #     else:
        #         print("You need to connect to the server first using %connect command.")

        else:
            print("Unknown command. Please use one of the specified commands.")

if __name__ == "__main__":
    main()
