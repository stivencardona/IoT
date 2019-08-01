# Import standard python modules
import threading
import time
import os
import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# "global" Vars
if(len(sys.argv)!=4):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey  $AdafruitIOFeedKey\n'.format(sys.argv[0]))
		os._exit(1)

AdafruitIOFeedUsername=sys.argv[1]
AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
#AdafruitIOGroupKey=sys.argv[3] # Group where Feed From
AdafruitIOFeedKey=sys.argv[3]# Feed key where data receive

# Define callback functions which will be called when certain events happen.
def on_connect(client):
	# Connected function will be called when the client connects.
	pass

def on_disconnect(client):
	# Disconnected function will be called when the client disconnects.
	print("¡Se ha Desconectado de Adafruit IO!")
	os._exit(1)

# Define Functions for Threading
def send_message(client):
	while True:
		if(client.messageSend is not None):
			client.publish(feed_id=AdafruitIOFeedKey, value=client.messageSend, feed_user=AdafruitIOFeedUsername)
			time.sleep(10)

if __name__=="__main__":
	# Create an MQTT client instance.
	client = MQTTClient(username=AdafruitIOFeedUsername, key=AdafruitIOKey)

	# Setup the callback functions
	client.on_connect=on_connect
	client.on_disconnect=on_disconnect

	# Setup Control Vars
	client.messageSend="0"

	# Connect to the Adafruit IO server.
	client.connect()
	client.loop_background()
	while not client.is_connected():
		print("Esperando conexión")
		time.sleep(1)
	
	# Setup Threading, to publish message every 10 seconds
	hilo0=threading.Thread(target=send_message, args=(client,))
	hilo0.start()

	# Mod publish value
	while client.messageSend!="x":# char 'x' to exit
		client.messageSend=input("Nuevo valor para el tanque\n")
	
	client.loop_background(stop=True)
	client.disconnect()
	