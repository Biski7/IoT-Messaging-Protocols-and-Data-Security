import socket
import time
import os

PORT = 5050

SIZE = 128
DISCONNECT_MESSAGE = '!END'
FORMAT = 'utf-8'
# SERVER = '192.168.1.211'
# SERVER = '192.168.1.235'
SERVER = '192.168.1.178' 
# OR
# SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

def main():
    print("[STARTING] Server is starting...")
    # create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] The server is listening on {SERVER}")
    conn, addr = server.accept()
    while True:
        mes = conn.recv(SIZE).decode(FORMAT)
        if not mes:
            break
        else:
            print(f'Server Side: [CLIENT] {mes}')


    time.sleep(2)
    os.system('touch server_end.lock')

if __name__ == "__main__":
    main()

