import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("Connection closed.")
            break

def main():
    server_address = ('127.0.0.1', 8080)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect(server_address)
        print("Connected to the server.")
    except:
        print("Connection failed.")
        return

    # Enter username
    username = input("Enter your username: ")
    client_socket.send(username.encode('utf-8'))

    # Start a thread to listen for messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    # Command loop
    while True:
        command = input("> ")
        if command.lower() == "%leave":
            client_socket.send(command.encode('utf-8'))
            break
        else:
            client_socket.send(command.encode('utf-8'))

    client_socket.close()
    print("Disconnected from the server.")

if __name__ == "__main__":
    main()
