import socket
import threading
import os

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

STORAGE_DIR = "storage"
if not os.path.exists(STORAGE_DIR):
    os.mkdir(STORAGE_DIR)

def handle_client(client_socket, address):
    print(f"[+] Connection from {address}")
    while True:
        try:
            command = client_socket.recv(BUFFER_SIZE).decode()
            if not command:
                break

            if command.startswith("UPLOAD"):
                _, filename = command.split(SEPARATOR)
                filepath = os.path.join(STORAGE_DIR, filename)
                with open(filepath, "wb") as f:
                    while True:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if bytes_read == b"DONE":
                            break
                        f.write(bytes_read)
                client_socket.send("Upload complete.".encode())

            elif command.startswith("DOWNLOAD"):
                _, filename = command.split(SEPARATOR)
                filepath = os.path.join(STORAGE_DIR, filename)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        while chunk := f.read(BUFFER_SIZE):
                            client_socket.send(chunk)
                    client_socket.send(b"DONE")
                else:
                    client_socket.send("File not found.".encode())

            elif command.startswith("LIST"):
                files = os.listdir(STORAGE_DIR)
                response = "\n".join(files) if files else "No files found."
                client_socket.send(response.encode())

            elif command.startswith("MKDIR"):
                _, dirname = command.split(SEPARATOR)
                path = os.path.join(STORAGE_DIR, dirname)
                os.makedirs(path, exist_ok=True)
                client_socket.send("Directory created.".encode())

        except Exception as e:
            print(f"[!] Error: {e}")
            break

    print(f"[-] Client {address} disconnected.")
    client_socket.close()

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[+] Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
