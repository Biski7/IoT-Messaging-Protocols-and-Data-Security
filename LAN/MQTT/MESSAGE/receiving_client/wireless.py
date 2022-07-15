import pcapy
from struct import *
import csv
from os.path import exists
from os import system as com

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

CLIENT_IP = '1921681235'

devices = pcapy.findalldevs()
wireless = devices[devices.index('wlp2s0')]

# all_breaker = False
wireless_breaker = False

# initialize global variables
total_bytes_wireless = 0
finack_counter_wireless = 0
total_seconds_out = 0

count_wireless = 0
# create live capture instance
cap_wireless = pcapy.open_live(wireless, 1024, 1, 5)

def next_packet_wireless():
    global cap_wireless, CLIENT_IP
    while True:
        header, payload = cap_wireless.next()

        while header == None:
            print('invalid packet ho, next garyo')
            (header, payload) = cap_wireless.next()

        if (len(payload) >= 34):
            ip_header = unpack('!BBHHHBBHBBBBBBBB', payload[14:34])
            src_ip_str = str(ip_header[8]) + str(ip_header[9]) + str(ip_header[10]) + str(ip_header[11])
            src_ip_int = int(src_ip_str)
            dst_ip_str = str(ip_header[12]) + str(ip_header[13]) + str(ip_header[14]) + str(ip_header[15])
            dst_ip_int = int(dst_ip_str)
            if (dst_ip_str == CLIENT_IP or src_ip_str == CLIENT_IP):
                print('ip milyo wireless ko')
                break
            else:
                print('ip milena wireless ko')
        else:
            # print('length pugena')
            continue
    return (header, payload)


while True:
    header_wireless, payload_wireless = next_packet_wireless()

    # Get timestamp to record time between each packets
    epoch_wireless, microsecond_wireless = header_wireless.getts()
    
    total_seconds = epoch_wireless + (microsecond_wireless * (10**(-6)))

    if count_wireless == 0:
        total_seconds_out = total_seconds

    tcp_header_wireless = unpack('!HHLLBBHHH', payload_wireless[34:54])

    source_port_wireless = tcp_header_wireless[0]

    destination_port_wireless = tcp_header_wireless[1]

    sequence_number_wireless = tcp_header_wireless[2]

    acknowledgement_number_wireless = tcp_header_wireless[3]

    offset_wireless = tcp_header_wireless[4] >> 4

    mqtt_tcp_length_wireless = len(payload_wireless) - 34

    reserved_wireless = tcp_header_wireless[4] & 0xF

    flags_wireless = tcp_header_wireless[5]

    C_W_R_wireless = flags_wireless >> 7

    ECN_echo_wireless = flags_wireless & 0x40

    ECN_echo_wireless >>= 6

    Urgent_wireless = flags_wireless & 0x20

    Urgent_wireless >>= 5

    Ack_wireless = flags_wireless & 0x10

    Ack_wireless >>= 4

    Push_wireless = flags_wireless & 0x8

    Push_wireless >>= 3


    Reset_wireless = flags_wireless & 0x4


    Reset_wireless >>= 2

    Sync_wireless = flags_wireless & 0x2

    Sync_wireless >>= 1

    Finish_wireless = flags_wireless & 0x1


    if (Finish_wireless == 1 and Ack_wireless == 1):
        finack_counter_wireless+=1
        print(finack_counter_wireless)
    # else:
    #     continue

    window_wireless = tcp_header_wireless[6]

    checksum_wireless = tcp_header_wireless[7]

    pointer_wireless = tcp_header_wireless[8]

    total_bytes_wireless+= mqtt_tcp_length_wireless

    with open('log_wireless.csv', 'a') as csvf:
        writer = csv.writer(csvf, dialect= csv.excel)
        writer.writerow([total_seconds, source_port_wireless, destination_port_wireless, sequence_number_wireless, acknowledgement_number_wireless, offset_wireless, C_W_R_wireless, ECN_echo_wireless, Urgent_wireless, Ack_wireless, Push_wireless, Reset_wireless, Sync_wireless, Finish_wireless, window_wireless, checksum_wireless, pointer_wireless])

    if (exists('server_end_wireless.lock') == True and finack_counter_wireless == 2 and Ack_wireless == 1 and Finish_wireless == 0):
        diff_total_seconds = total_seconds - total_seconds_out - 1
        print(diff_total_seconds)
        print(total_bytes_wireless)
        with open('log_wireless.csv', 'a') as csvf:
            writer = csv.writer(csvf, dialect= csv.excel)
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', (total_bytes_wireless - 1)])
            writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',(diff_total_seconds)])
        
        # finack_counter_wireless = 0

        total_bytes_wireless = 0
        finack_counter_wireless = 0
        # temp_time_g_wireless = 0
        # temp_time_gl_wireless = 0
        total_time_wireless = 0

        print('wireless ko criteria pugyo')
        # com("rm client_end_wireless.lock")
        break
    else:
        # print('wireless ko criteria pugena')
        pass

    # if (wireless_breaker == True):
    #     com("rm client_end_wireless.lock")
    #     break

    count_wireless+=1
