import socket
import threading

HOST = "127.0.0.1"
PORT = 3005

def receive_message(client_socket, host, port):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "server_shut_down":
                print(f"[CLOSED]: Server {host}:{port} has shut down ")
            else:
                print(f"[SERVER]: {message}")
        except Exception as receive_message_exception:
            print(f"An exception has occured on receiving message from {host}:{port}: {receive_message_exception}")
        
def send_message(client_socket, host, port):
    while True:
        message = input("Type message: ")
        client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":

    host = HOST
    port = PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    client_socket.connect(server_address)

    receive_thread = threading.Thread(target = receive_message, args = (client_socket, host, port, ))
    send_thread = threading.Thread(target = send_message, args = (client_socket, host, port, ))

    receive_thread.start()
    send_thread.start()
