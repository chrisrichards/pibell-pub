#!/usr/bin/python

import logging
import paho.mqtt.client as paho
import serial
import time

DEVICE = '/dev/ttyAMA0'
BAUD = 9600

def on_publish(client, userdata, mid):
	print("mid: " + str(mid))

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
# logging.basicConfig(filename='doorbell.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
logging.info('Starting')
print "Starting\n"

client = paho.Client()
client.on_publish = on_publish
client.connect("192.168.0.214", 1883)
logging.info('Connected')
print "Connected\n"
client.loop_start()

last_msg_time = time.time()

ser = serial.Serial(DEVICE, BAUD)
while True:
	msg = ser.read(12)
	logging.info('Received msg:' + msg)

	now = time.time() 
	elapsed = now - last_msg_time

	if msg == "aAB000002A--":
		if elapsed > 3:
			logging.info('Pressed')
			last_msg_time = now
			client.publish("home/doorbell/state", "pressed", qos=1)
	elif msg.startswith("a--BATT"):
			client.publish("home/doorbell/battery", msg[7:11], qos=1)


