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
    mes = conn.recv(SIZE)
    while True:
    
        if not mes:
            break
        else:
            f = open('/home/bishal/Desktop/Research/LAN/Socket/File/server/file_to_receive.txt', 'wb')
            f.write(mes)
            mes = conn.recv(SIZE)

    f.close()

    time.sleep(2)
    os.system('touch server_end.lock')

if __name__ == "__main__":
    main()

