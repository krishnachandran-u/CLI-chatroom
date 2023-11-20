import socket
import threading

HOST = "127.0.0.1"
PORT = 3005

def receive_and_broadcast_message(client_socket, client_address, active_client_sockets, active_client_addresses):
    while True:

        try:

            message = client_socket.recv(1024).decode('utf-8')
            if message == "!logout":
                print(f"[CLOSED] : {client_address}")
                break
            print(f"[{client_address}]: {message}")
            for active_client_socket in active_client_sockets:
                if active_client_socket != client_socket:
                    active_client_socket.send(("[" + str(client_address) + "]: " + message).encode('utf-8'))

        except Exception as receive_message_exception:

            print(f"An exception has occured on receiving message from {client_address}: {receive_message_exception}")
    
    active_client_sockets.remove(client_socket)
    active_client_addresses.remove(client_address)

    client_socket.close()

    print(f"--- ACTIVE CLIENT SOCKETS: {len(active_client_sockets)} ---")

    return

def start_server(host, port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"[LISTENING] {host}:{port}")

    active_client_sockets = []
    active_client_addresses = []

    while True:

        try:

            client_socket, client_address = server_socket.accept()         
            print(f"Connection established with {client_address}")

            active_client_sockets.append(client_socket)
            active_client_addresses.append(client_address)

            print(f"--- ACTIVE CLIENT SOCKETS: {len(active_client_sockets)} ---")

            receive_and_broadcast_thread = threading.Thread(target = receive_and_broadcast_message, args = (client_socket, client_address, active_client_sockets, active_client_addresses))

            receive_and_broadcast_thread.start()

        except Exception as server_start_exception:

            print(f"An exception has occured on starting server: {server_start_exception}")
    return

if __name__ == "__main__":  

    host = HOST
    port = PORT

    start_server(host, port)