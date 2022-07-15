import paho.mqtt.client as mqtt
import time
from os import system as com
from os.path import exists
import csv

ind = False
wait_end_time = 0

def on_message(client, obj, msg):
    while True:
        print("message ayo:")
        global ind, wait_end_time
        wait_end_time = time.time()
        ind = True
        break

def on_dis(cl, ud, rc = 0):
  client.loop_stop()
  print("disconnected")


client = mqtt.Client("c1")
print('1')
client.connect("192.168.1.235", port = 1883, bind_address = '')
print('2')         
client.subscribe("chat", qos=0)
print("Starting")
wait_start_time = time.time()
client.loop_start()
print('waiting message')
# com('touch server_start.lock')
while True:
  client.on_message = on_message
  if ind == True:
    break
client.on_disconnect = on_dis
client.loop_stop()

wait_time = wait_end_time - wait_start_time

with open('log_wireless_delay.csv', 'a') as w:
  writer = csv.writer(w, dialect= csv.excel)
  writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', wait_time])
  
with open('log_loopback_delay.csv', 'a') as w:
  writer = csv.writer(w, dialect= csv.excel)
  writer.writerow(['','', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', wait_time])


com('touch server_end_wireless.lock')
com('touch server_end_loopback.lock')

time.sleep(0.5)