import pcapy
from struct import *
import csv
from os.path import exists
from os import system as com

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

devices = pcapy.findalldevs()
# ind = devices.index('wlan0')
loopback = devices[devices.index('lo')]

# initialize global variables
total_bytes = 0
finack_counter = 0
temp_time_g = 0.0
count = 0
temp_time_gl = 0.0
total_time = 0.0
ack_counter = 0

# create live capture instance
cap  = pcapy.open_live(loopback, 1024, 1, 10)

while True:
    (header, payload) = cap.next()

    while header == None:
        (header, payload) = cap.next()

    # Get timestamp to record time between each packets
    epoch, millisecond = header.getts()
    e_str, ms_str = str(epoch), str(millisecond)
    ems_str = e_str+'.'+ms_str
    ems_fl = float(ems_str)
    if count == 0:
        temp_time_g = ems_fl

    # if temp_time_gl == ems_fl:
    #     continue

    temp_time_gl = ems_fl

    # Unpacking TCP packet
    tcp_header = unpack('!HHLLBBHHH', payload[34:54])
    source_port = tcp_header[0]
    destination_port = tcp_header[1]
    sequence_number = tcp_header[2]
    acknowledgement_number = tcp_header[3]
    offset = tcp_header[4] >> 4

    mqtt_tcp_length = len(payload) - 34

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

    if (Finish == 1 and Ack == 1):
        finack_counter+=1
        print('finack counter: ', finack_counter)


    window = tcp_header[6]
    checksum = tcp_header[7]
    pointer = tcp_header[8]
    total_bytes+= mqtt_tcp_length

    if finack_counter >= 2 and Ack == 1 and Finish == 0:
        ack_counter+=1
        print('ack counter: ',ack_counter )
    
    with open('log.csv', 'a') as csvf:
        writer = csv.writer(csvf, dialect= csv.excel)
        writer.writerow([ems_fl, source_port, destination_port, sequence_number, acknowledgement_number, offset, C_W_R, ECN_echo, Urgent, Ack, Push, Reset, Sync, Finish, window, checksum, pointer])

    if (exists('server_end.lock') == True and finack_counter == 4 and Ack == 1 and Finish == 0 and ack_counter == 2):
        total_time = temp_time_gl - temp_time_g
        with open('log.csv', 'a') as csvf:
            writer = csv.writer(csvf, dialect= csv.excel)
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', (total_bytes - 1000)])
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', (total_time)])

        com("rm server_end.lock")
        finack_counter = 0

        break

    count+=1
