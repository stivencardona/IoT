# Import standard python modules
import time
import os
import sys
import threading

# Import Adafruit IO Client.
from Adafruit_IO import Client

# Class for params into instance for Threading call
class messageSendControl():
	def __init__(self, message):
		self.message=message

# Define Functions for Threading
def send_message(aioClient, feedInstance, messageInstance):
	while True:
		if(messageInstance.message!=""):
			if(messageInstance.message.isdigit()):
				aioClient.send(feedInstance.key, int(messageInstance.message))
			else:
				print("El dato '{}' no es apto para el envio".format(messageInstance.message))
			time.sleep(10)

if __name__ == "__main__":
	if(len(sys.argv)!=4):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey $AdafruitIOFeedKey\n'.format(sys.argv[0]))
		os._exit(1)

	AdafruitIOFeedUsername=sys.argv[1]
	AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
	AdafruitIOFeedKey=sys.argv[3] # Feed key where data is received

	# Connect to Adafruit IO Server
	aio=Client(username=AdafruitIOFeedUsername, key=AdafruitIOKey)

	# Link to feeds
	feedInstance=aio.feeds(AdafruitIOFeedKey)

	# Create messageSendControl instance
	messageInstance=messageSendControl("")
	
	# Setup Threading, to publish message every 10 seconds
	hilo0=threading.Thread(target=send_message, args=(aio, feedInstance, messageInstance,))
	hilo0.start()

	# Mod publish value
	while messageInstance.message!="x": # char 'x' to exit
		messageInstance.message=input("Ingrese nuevo valor para el tanque\n")