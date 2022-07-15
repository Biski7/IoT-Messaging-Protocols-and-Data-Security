import pcapy
from struct import *
import csv
from os.path import exists
from os import system as com

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

CLIENT_IP = '1921681235'

devices = pcapy.findalldevs()
loopback = devices[devices.index('lo')]


# all_breaker = False
loopback_breaker = False

# initialize global variables
total_bytes_loopback = 0
finack_counter_loopback = 0
total_seconds_out = 0

count_loopback = 0

# create live capture instance
cap_loopback  = pcapy.open_live(loopback, 1024, 1, 5)

def next_packet_loopback():
    global cap_loopback, CLIENT_IP
    while True:
        header, payload = cap_loopback.next()

        while header == None:
            print('invalid packet ho, next garyo')
            (header, payload) = cap_loopback.next()

        if (len(payload) >= 54):
            ip_header = unpack('!BBHHHBBHBBBBBBBB', payload[14:34])
            src_ip_str = str(ip_header[8]) + str(ip_header[9]) + str(ip_header[10]) + str(ip_header[11])
            src_ip_int = int(src_ip_str)
            dst_ip_str = str(ip_header[12]) + str(ip_header[13]) + str(ip_header[14]) + str(ip_header[15])
            dst_ip_int = int(dst_ip_str)
            if (dst_ip_str == '127001' and src_ip_str == '127001'):
                # print('ip milyo')
                break
            # else:
            #     print('ip milena')
        else:
            # print('length pugena')
            continue
    return (header, payload)
    

while True:
    header_loopback, payload_loopback = next_packet_loopback()

    # Get timestamp to record time between each packets
    epoch_loopback, microsecond_loopback = header_loopback.getts()

    total_seconds = epoch_loopback + (microsecond_loopback * (10**(-6)))

    if count_loopback == 0:
        total_seconds_out = total_seconds

    tcp_header_loopback = unpack('!HHLLBBHHH', payload_loopback[34:54])

    source_port_loopback = tcp_header_loopback[0]

    destination_port_loopback = tcp_header_loopback[1]

    sequence_number_loopback = tcp_header_loopback[2]

    acknowledgement_number_loopback = tcp_header_loopback[3]

    offset_loopback = tcp_header_loopback[4] >> 4

    mqtt_tcp_length_loopback = len(payload_loopback) - 34

    reserved_loopback = tcp_header_loopback[4] & 0xF

    flags_loopback = tcp_header_loopback[5]

    C_W_R_loopback = flags_loopback >> 7

    ECN_echo_loopback = flags_loopback & 0x40

    ECN_echo_loopback >>= 6

    Urgent_loopback = flags_loopback & 0x20

    Urgent_loopback >>= 5

    Ack_loopback = flags_loopback & 0x10

    Ack_loopback >>= 4

    Push_loopback = flags_loopback & 0x8

    Push_loopback >>= 3


    Reset_loopback = flags_loopback & 0x4


    Reset_loopback >>= 2

    Sync_loopback = flags_loopback & 0x2

    Sync_loopback >>= 1

    Finish_loopback = flags_loopback & 0x1

    if (Finish_loopback == 1 and Ack_loopback == 1):
        finack_counter_loopback+=1
    # else:
    #     continue



    window_loopback = tcp_header_loopback[6]

    checksum_loopback = tcp_header_loopback[7]

    pointer_loopback = tcp_header_loopback[8]

    total_bytes_loopback+= mqtt_tcp_length_loopback

    with open('log_loopback.csv', 'a') as csvf:
        writer = csv.writer(csvf, dialect= csv.excel)
        writer.writerow([total_seconds, source_port_loopback, destination_port_loopback, sequence_number_loopback, acknowledgement_number_loopback, offset_loopback, C_W_R_loopback, ECN_echo_loopback, Urgent_loopback, Ack_loopback, Push_loopback, Reset_loopback, Sync_loopback, Finish_loopback, window_loopback, checksum_loopback, pointer_loopback])

    if (exists('server_end_loopback.lock') == True and finack_counter_loopback == 2 and Ack_loopback == 1 and Finish_loopback == 0):
        diff_total_seconds = total_seconds - total_seconds_out - 1
        with open('log_loopback.csv', 'a') as csvf:
            writer = csv.writer(csvf, dialect= csv.excel)
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', (total_bytes_loopback)])
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',(diff_total_seconds)])
        
        
        finack_counter_loopback = 0
        # loopback_breaker = True
        # com("rm client_end_loopback.lock")
        break

    # if (loopback_breaker == True):
    #     com("rm client_end_loopback.lock")
    #     break

    count_loopback+=1
