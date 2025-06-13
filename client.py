import socket
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

user_name = input("Enter user name: ")

session = PromptSession()

def receive_message(s):
    while True:
        data = s.recv(1024)
        print(data.decode('ascii'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(f'{user_name} entered the chat.'.encode('ascii'))

    t2 = threading.Thread(target=receive_message, args=(s,))
    t2.start()

    while True:
        with patch_stdout():
            s.sendall(f'{user_name}: {session.prompt(f"{user_name}: ")}'.encode("ascii"))
