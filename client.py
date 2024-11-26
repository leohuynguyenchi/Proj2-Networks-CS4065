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
    server_address = ('127.0.0.1', 8080) #Define server address and a port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket
    # Attempt to connect to the server
    try:
        client_socket.connect(server_address)
        print("Connected to the server.")
    except:
        print("Connection failed.")
        return

    username = input("Enter your username: ") # Enter username
    client_socket.send(username.encode('utf-8')) # Send the username to the server

    # Start a thread to listen for messages from server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Command loop -> send commands to the server
    while True:
        command = input("> ")
        # Send leave command to the server and break the loop
        if command.lower() == "%leave":
            client_socket.send(command.encode('utf-8'))
            break
        else:
            #Send other commands to the server
            client_socket.send(command.encode('utf-8'))
    #close the client socket
    client_socket.close()
    print("Disconnected from the server.")

if __name__ == "__main__":
    main()
