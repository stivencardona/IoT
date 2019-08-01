# Import standard python modules
import time
import os
import sys

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# "global" Vars
if(len(sys.argv)!=4):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey $AdafruitIOFeedKey\n'.format(sys.argv[0]))
		os._exit(1)

AdafruitIOFeedUsername=sys.argv[1]
AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
AdafruitIOFeedKey=sys.argv[3]# Feed key where data receive

# Define callback functions which will be called when certain events happen.
def on_connect(client):
	# Connected function will be called when the client connects.
    
	# Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
	client.subscribe(feed_id=AdafruitIOFeedKey, feed_user=AdafruitIOFeedUsername)

def on_disconnect(client):
	# Disconnected function will be called when the client disconnects.
	print("¡Se ha Desconectado de Adafruit IO!")
	os._exit(1)

def on_message(client, feed_id, payload):
	# Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
	print('Feed {0} ha recibido el valor-> {1}'.format(feed_id, payload))

if __name__=="__main__":
	# Create an MQTT client instance.
	client = MQTTClient(username=AdafruitIOFeedUsername, key=AdafruitIOKey)

	# Setup the callback functions
	client.on_connect=on_connect
	client.on_disconnect=on_disconnect
	client.on_message=on_message

	# Connect to the Adafruit IO server.
	client.connect()
	client.loop_blocking()