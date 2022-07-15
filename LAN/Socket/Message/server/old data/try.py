import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pcapy
from struct import *
import csv
from os.path import exists
import os

import socket
SERVER = socket.gethostbyname(socket.gethostname())

# CLIENT_IP = '1921681178'
CLIENT_IP = '1921681211'

devices = pcapy.findalldevs()
# ind = devices.index('wlan0')
loopback = devices[devices.index('wlp2s0')]

# initialize global variables
# finack_checker = False
# breaker = False
total_bytes = 0
temp_time_g = 0
count = 0
temp_time_gl = 0
total_time = 0


################
src_ip_str = ''
dst_ip_str = ''
######

# create live capture instance
cap  = pcapy.open_live(loopback, 1024, 1, 1)

while True:
    (header, payload) = cap.next()

    while header == None:
        (header, payload) = cap.next()

    # Unpacking TCP packet
    if (len(payload) >= 34):
        ip_header = unpack('!BBHHHBBHBBBBBBBB', payload[14:34])
        src_ip_str = str(ip_header[8]) + str(ip_header[9]) + str(ip_header[10]) + str(ip_header[11])
        src_ip_int = int(src_ip_str)
        dst_ip_str = str(ip_header[12]) + str(ip_header[13]) + str(ip_header[14]) + str(ip_header[15])
        dst_ip_int = int(dst_ip_str)
    else:
        pass

    if (len(payload) >= 54):
        tcp_header = unpack('!HHLLBBHHH', payload[34:54])
    else:
        pass


    # print(src_ip_int, dst_ip_int)
    
    if (src_ip_str == CLIENT_IP or dst_ip_str == CLIENT_IP):
        
        # Get timestamp to record time between each packets
        epoch, millisecond = header.getts()
        e_str, ms_str = str(epoch), str(millisecond)
        ems_str = e_str+'.'+ms_str
        ems_fl = float(ems_str)
        if count == 0:
            temp_time_g = ems_fl
        temp_time_gl = ems_fl
        source_port = tcp_header[0]
        destionation_port = tcp_header[1]
        sequence_number = tcp_header[2]
        acknowledgement_number = tcp_header[3]
        offset = tcp_header[4] >> 4

        reserved = tcp_header[4] & 0xF
        flags = tcp_header[5]

        C_W_R = flags >> 7
        ECN_echo = flags & 0x40
        ECN_echo >>= 6
        Urgent = flags & 0x20
        Urgent >>= 5
        Ack = flags & 0x10
        Ack >>= 4

        Push = flags & 0x8
        Push >>= 3
        Reset = flags & 0x4
        Reset >>= 2
        Sync = flags & 0x2
        Sync >>= 1
        Finish = flags & 0x1


        window = tcp_header[6]
        checksum = tcp_header[7]
        pointer = tcp_header[8]
        total_bytes+=offset

        # if(Finish == 0 and Ack == 1):
        #     breaker = True
        # else:
        #     breaker = False
        
        # if (Finish == 1 and Ack ==1):
        #     finack_checker = True


        with open('log.csv', 'a') as csvf:
            writer = csv.writer(csvf, dialect= csv.excel)
            writer.writerow([ems_fl, source_port, destionation_port, sequence_number, acknowledgement_number, offset, C_W_R, ECN_echo, Urgent, Ack, Push, Reset, Sync, Finish, window, checksum, pointer])


        if (exists('server_end.lock') == True and Ack == 1 and Finish == 0):
            total_time = temp_time_gl - temp_time_g
            with open('log.csv', 'a') as csvf:
                writer = csv.writer(csvf, dialect= csv.excel)
                writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', total_bytes])
                writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',total_time - 2])

            os.system('rm server_end.lock')

            break

        count+=1
    
    else:
        pass

os.system('touch loop_end.lock')
