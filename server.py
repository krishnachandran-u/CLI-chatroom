import socket
import threading

HOST = "127.0.0.1"
PORT = "3005"

def receive_message(client_socket, addr, active_connections):
    while True:

        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "log_out":
                print(f"[CLOSED] : {addr}")
                break
            print(f"[{addr}]: {message}")

        except Exception as receive_message_exception:
            print(f"An exception has occured on receiving message from {addr}: {receive_message_exception}")
    
    active_connections.remove(client_socket)
    print(f"Number of active connections: {len(active_connections)}")

def send_message(client_socket, addr):
    while True:

        try:
            message = input("Type message: ")
            message = "[SERVER]: " + message
            client_socket.send(message.encode('utf-8'))  

        except Exception as send_message_exception:
            print(f"An exception has occured on sending message to {addr}: {send_message_exception}")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(host, port)

    server_socket.listen(5)
    print(f"[LISTENING] {host}:{port}")

    active_connections = []

    while True:

        try:
            client_socket, addr = server_socket.accept()         
            print(f"Connection established with {addr}")

            active_connections.append(client_socket)
            print(f"Number of active connections: {len(active_connections)}")

            receive_thread = threading.Thread(target = receive_message, args = (client_socket, addr, active_connections))
            send_thread = threading.Thread(target = send_message, args = (client_socket, addr))

            receive_thread.start()
            send_thread.start()

        except Exception as server_start_exception:
            print(f"An exception has occured on starting server: {server_start_exception}")

if __name__ == "__main__":  
    host = HOST
    port = PORT

    start_server(host, port)