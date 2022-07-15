import socket
import time
import os 
# IP = socket.gethostbyname(socket.gethostname())
# print(IP)
IP = '192.168.1.211'
PORT = 5050
DISCONNECT_MESSAGE = '!END'
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 128

def main():
    # time.sleep(0.3)
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # print('COnnected')
    """ Connecting to the server. """
    client.connect(ADDR)

    u_inp = 'a'*1
    client.sendall(u_inp.encode(FORMAT))
    print("Data Sent by Client")
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    print('Client closed')



    """ Closing the connection from the server. """
    # print('Client closed')

    time.sleep(1)
    os.system('touch client_end.lock')

if __name__ == "__main__":
    main()  
