DOWNLOAD_DIR = "client_downloads"

# Create the folder if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

import socket
import os

SERVER_HOST = '18.189.192.27' 
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    return client_socket

def upload_file(filename):
    if not os.path.exists(filename):
        print("File not found.")
        return
    client_socket = connect()
    client_socket.send(f"UPLOAD{SEPARATOR}{os.path.basename(filename)}".encode())
    with open(filename, "rb") as f:
        while chunk := f.read(BUFFER_SIZE):
            client_socket.send(chunk)
    client_socket.send(b"DONE")
    print(client_socket.recv(BUFFER_SIZE).decode())
    client_socket.close()

def download_file(filename):
    client_socket = connect()
    client_socket.send(f"DOWNLOAD{SEPARATOR}{filename}".encode())
    filepath = os.path.join("client_downloads", filename)
    os.makedirs("client_downloads", exist_ok=True)
    with open(filepath, "wb") as f:
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if chunk == b"DONE" or not chunk:
                break
            f.write(chunk)
    print(f"Downloaded {filename} to client_downloads/")
    client_socket.close()

def list_files():
    client_socket = connect()
    client_socket.send("LIST".encode())
    print(client_socket.recv(BUFFER_SIZE).decode())
    client_socket.close()

def make_directory(dirname):
    client_socket = connect()
    client_socket.send(f"MKDIR{SEPARATOR}{dirname}".encode())
    print(client_socket.recv(BUFFER_SIZE).decode())
    client_socket.close()

# Demo (you can replace this with user input if needed)
# upload_file("example.txt")
# download_file("example.txt")
# list_files()
# make_directory("new_folder")
