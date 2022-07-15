from paho.mqtt import client as mqtt
import time
from os.path import exists
from os import system as com

# mqttBroker = '10.0.2.15'
while True:
    # if(exists('server_start.lock') == True):
    client = mqtt.Client("c2")
    client.connect('192.168.1.235', port = 1883)  
    f = open('file_to_send.txt', 'rb')
    data = f.read()
    client.loop_start()
    client.publish(topic="chat", payload= data,qos=0)
    # com('touch client_start.lock')
    time.sleep(1)
    client.loop_stop()
    break



com('touch client_end_wireless.lock')
com('touch client_end_loopback.lock')
