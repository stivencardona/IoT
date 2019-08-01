# Import standard python modules
import time
import os
import sys

# Import Adafruit IO Client.
from Adafruit_IO import Client

if __name__ == "__main__":
	if(len(sys.argv)!=4):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey $AdafruitIOFeedKey\n'.format(sys.argv[0]))
		os._exit(1)

	AdafruitIOFeedUsername=sys.argv[1]
	AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
	AdafruitIOFeedKey=sys.argv[3] # Feed key where data is received
	
	aio=Client(username=AdafruitIOFeedUsername, key=AdafruitIOKey)

	# Link to feeds
	fuelPercentageFeed=aio.feeds(AdafruitIOFeedKey)
	lastUpdate=""
	while True:
		# get last data from the feeds, Warning should be have any data, not empty
		fuelPercentageData=aio.receive(fuelPercentageFeed.key)
		if(lastUpdate!=fuelPercentageData.updated_at):
			print("Capacidad en el tanque {}%".format(fuelPercentageData.value))
			lastUpdate=fuelPercentageData.updated_at
		time.sleep(1)