import socket
import time

IP = socket.gethostbyname(socket.gethostname())
# print(IP)
# IP = '192.168.1.131'
PORT = 5050
DISCONNECT_MESSAGE = '!END'
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 128

def main():
    # time.sleep(0.3)
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    # """ Opening and reading the file data. """
    # # file = open("data/sample.uxp", "r")
    # file = open("data/myData.txt", "r")
    # data = file.read()

    # """ Sending the filename to the server. """
    # # client.send('sample.uxp'.encode(FORMAT))
    # client.send('myData.txt'.encode(FORMAT))

    # msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")

    # """ Sending the file data to the server. """
    # client.send(data.encode(FORMAT))
    # msg = client.recv(SIZE).decode(FORMAT)
    # print(f"[SERVER]: {msg}")

    # """ Closing the file. """
    # file.close()

    u_inp = 'a'*1
    client.sendall(u_inp.encode(FORMAT))
    print("Data Sent by Client")
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    print('Client closed')



    """ Closing the connection from the server. """
    # print('Client closed')


if __name__ == "__main__":
    main()