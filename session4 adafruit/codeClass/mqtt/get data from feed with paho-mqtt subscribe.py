# Import standard Python Modules
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
# AdafruitIOGroupKey=sys.argv[3] # Group where Feed From
AdafruitIOFeedKey=sys.argv[3]# complete Feed key where data receive

# Define callback functions which will be called when certain events happen.
def on_connect(client, userdata, flags, rc):
	# Connected function will be called when the client connects.
	print("Conectado con codigo resultante:  "+str(rc))
	
	# Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
	client.subscribe(AdafruitIOFeedUsername+"/feeds/"+AdafruitIOFeedKey)

def on_message(client, userdata, message):
	# Message function will be called when a subscribed feed has a new value.
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)

if __name__ == "__main__":
	# Create an MQTT client instance.
	client = mqtt.Client()
	
	# Setup the callback functions
	client.on_message = on_message
	client.on_connect = on_connect
	
	# Setup Credentials
	client.username_pw_set(username=AdafruitIOFeedUsername, password=AdafruitIOKey)

	# Connect to the Adafruit IO server.
	print("Conectando al broker")
	client.connect(host="io.adafruit.com", port=1883, keepalive=60)
	client.loop_forever()