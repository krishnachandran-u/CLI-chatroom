import socket
import threading

HOST = "127.0.0.1"
PORT = "3005"

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(host, port)

    server_socket.listen(10)
    print(f"[LISTENING] {host}:{port}")

    while True:
        try:
            client_socket, addr = server_socket.accept()         
            print(f"Connection established with {addr}")
        except Exception as server_exception:
            print(f"An exception has occured: {e}")

if __name__ == "__main__":  
    host = HOST
    port = PORT

    start_server(host, port)