import socket
import threading
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")
file_handler = logging.FileHandler("_server.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{",datefmt="%Y-%m-%d %H:%M")
file_handler.setLevel("DEBUG")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clients = list()
usernames = list()

def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        username = data.decode('ascii').replace('USERNAME: ', '')
        usernames.append(username)
        client_index = get_client_index(conn, clients)
        broadcast(f'{username} entered the chat.'.encode('ascii'), client_index)

        while True:
            logger.debug("Inside handle connection")
            logger.debug("Client index: "+ str(get_client_index(conn, clients)))
            logger.debug("Conn: " + str(conn))
            logger.debug("Addr: " + str(addr))
            logger.debug("Clients: "+ str(clients))
            try:
                data = conn.recv(1024)
                logger.debug('User name: '+ str(usernames))
                logger.debug("Data: " + data.decode('ascii'))
            except ConnectionResetError:
                print("client closed connection by force")
                client_index = get_client_index(conn, clients)
                broadcast(f'{username} left the chat.'.encode('ascii'), client_index)
                del clients[client_index]
                del usernames[client_index]
                logger.debug('User name: '+ str(usernames))
                break
            client_index = get_client_index(conn, clients)
            logger.debug("Client index: "+ str(client_index))
            broadcast(data, client_index)

def broadcast(data, client_index):
    logger.debug("Inside broadcast")
    logger.debug("Data: " + data.decode('ascii'))
    logger.debug("Client index: "+ str(client_index))
    for index, client in enumerate(clients):
        if not index == client_index:
            client.sendall(data)


def get_client_index(conn, clients):
    for index, client in enumerate(clients):
        if client == conn:
            return index

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        logger.debug("Inside main")
        logger.debug("Conn: " + str(conn))
        logger.debug("Addr: " + str(addr))
        clients.append(conn)
        logger.debug("Clients: "+ str(clients))
        t = threading.Thread(target=handle_connection, args=(conn, addr))
        t.start()
