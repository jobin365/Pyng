import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clients = list()

def handle_connection(conn, addr, client_index):
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            for index, client in enumerate(clients):
                if not index == client_index:
                    client.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        client_index = len(clients) - 1
        t = threading.Thread(target=handle_connection, args=(conn, addr, client_index))
        t.start()
