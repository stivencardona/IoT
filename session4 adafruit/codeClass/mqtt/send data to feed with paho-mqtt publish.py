# Import standard python modules
import threading
import time
import os
import sys

# Import paho MQTT client.
import paho.mqtt.client as mqtt

# "global" Vars
if(len(sys.argv)!=4):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey $AdafruitIOFeedKey\n'.format(sys.argv[0]))
		os._exit(1)

AdafruitIOFeedUsername=sys.argv[1]
AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
AdafruitIOFeedKey=sys.argv[3]# Complete Feed key where data receive

# Define callback functions which will be called when certain events happen.
def on_connect(client, userdata, flags, rc):
	# Connected function will be called when the client connects.
	print("Conectado con codigo resultante:  "+str(rc))
	client.connectedFlag=True

def on_disconnect(client):
	# Disconnected function will be called when the client disconnects.
	print("¡Se ha Desconectado!")
	os._exit(1)

# Define Functions for Threading
def send_message(client):
	while True:
		if(client.messageSend is not None):
			# publish topic $username/feeds/$groupKey.$feedKey
			client.publish(AdafruitIOFeedUsername+"/feeds/"+AdafruitIOFeedKey, client.messageSend)
			time.sleep(10)
		
if __name__ == "__main__":
	# Setup an MQTT Client Instance
	client = mqtt.Client()

	# Setup Callbacks
	client.on_connect = on_connect
	client.on_disconnect=on_disconnect
	
	# Setup Control Vars
	client.connectedFlag=False
	client.messageSend="0"

	# Setup Credentials
	client.username_pw_set(username=AdafruitIOFeedUsername, password=AdafruitIOKey)

	# Connect to the Broker server.
	print("Conectando al broker")
	client.connect(host="io.adafruit.com", port=1883, keepalive=60)
	client.loop_start()
	while not client.connectedFlag:
		print("Esperando conexión")
		time.sleep(1)
	
	# Setup Threading, to publish message every 10 seconds
	hilo0=threading.Thread(target=send_message, args=(client,))
	hilo0.start()

	# Mod publish value
	while client.messageSend!="x":# char 'x' to exit
		client.messageSend=input("Nuevo valor para el tanque\n")
	client.loop_stop()
	client.disconnect()