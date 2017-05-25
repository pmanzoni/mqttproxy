import json
import random
import socket
import sys
import threading
import time
import paho.mqtt.client as mqtt 

HOST='localhost'
PORT=1883
DEBUG_MSG_ON = True
SENSOR_NUM = 0

# The callback used when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
	if DEBUG_MSG_ON: sys.stderr.write("[DEBUG:simpleexnode:on_connect] Connected to %s : %d\n" % (client._host, client._port))
	if rc > 0:
		sys.stderr.write("[ERROR:simpleexnode:on_connect]: %d - calling on_connect()\n" % rc)
		sys.exit(2)
	else:
		client.subscribe("global/testing")
		client.subscribe("external/testing")

# The callback used when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
	if DEBUG_MSG_ON: sys.stderr.write("[DEBUG:simpleexnode:on_message] Received: '%s', topic: '%s' (qos=%d)\n" % (msg.payload, msg.topic, msg.qos))
	themsg = json.loads(str(msg.payload))

	if msg.topic.startswith("global"):
		sys.stdout.write("SENSOR "+str(SENSOR_NUM)+": received data from GLOBAL sensor "+str(themsg['Sensor']))
	else: msg.topic.startswith("external"):
		sys.stdout.write("SENSOR "+str(SENSOR_NUM)+": received data from EXTERNAL sensor "+str(themsg['Sensor']))
	else:
		sys.stdout.write("SENSOR "+str(SENSOR_NUM)+": received data from INTERNAL sensor "+str(themsg['Sensor']))
	sys.stdout.write(". Got value "+str(themsg['Value'])+" "+themsg['C_F'])
	sys.stdout.write(" at "+str(themsg['Time'])+"\n")


if __name__ == '__main__':
	client=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol='MQTTv311')
	client.on_connect = on_connect
	client.on_message = on_message

	# Connect to the MQTT broker
	try:
		client.connect(HOST, PORT, keepalive=60)
	except socket.error as serr:
		sys.stderr.write("[ERROR] %s\n" % serr)
		sys.exit(2)

	random.seed(a=None)
	SENSOR_NUM = random.randint(1,100)

	client.loop_forever()

