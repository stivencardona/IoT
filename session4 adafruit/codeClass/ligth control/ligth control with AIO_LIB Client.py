# Import standard python modules
import time
import os
import sys

# Import RPi.GPIO library
try:
   import RPi.GPIO as GPIO
except RuntimeError:
   print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# Import Adafruit IO Client.
from Adafruit_IO import Client

def main():
	if(len(sys.argv)!=5):
		sys.stderr.write('Usage: "{0}" $AdafruitIOUsername $AdafruitIOKey $AdafruitIOFeedForStateKey $AdafruitIOFeedForIntensityKey \n'.format(sys.argv[0]))
		os._exit(1)
	
	AdafruitIOFeedUsername=sys.argv[1]
	AdafruitIOKey=sys.argv[2]# Beware, your Key is Secret!
	incubatorLigthStateFeedKey=sys.argv[3] # Feed key where data is received
	incubatorLigthIntensityFeedKey=sys.argv[4] # Feed key where data is received

	# var GPIO pin to show output
	led_pin = 21



	# Set GPIO pin mode
	GPIO.setmode(GPIO.BCM)

	# Set GPIO pin direction
	#GPIO.setup(led_pin, GPIO.OUT)
	pinList = [i for i in range(2,28)]
	GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)

	# Setup PWM instance to led_pin with 60 Hz
	pwm = GPIO.PWM(led_pin, 60)
	
	# Connect to Adafruit IO Server
	aio=Client(username=AdafruitIOFeedUsername, key=AdafruitIOKey)

	# Link to feeds
	incubatorLigthStateFeed=aio.feeds(incubatorLigthStateFeedKey)
	incubatorLigthIntensityFeed=aio.feeds(incubatorLigthIntensityFeedKey)
	
	# Control vars
	dutyValue=0
	incubatorLigthStateLastUpdate=""
	incubatorLigthIntensityLastUpdate=""

	try:
		while True:
			# get feeds data from Adafruit IO
			incubatorLigthStateData=aio.receive(incubatorLigthStateFeed.key)
			incubatorLigthIntensityData=aio.receive(incubatorLigthIntensityFeed.key)
		   
			# check if the received data is new
			if(incubatorLigthStateData.updated_at!=incubatorLigthStateLastUpdate):
				# Update datetime update, for execute only one time
				incubatorLigthStateLastUpdate=incubatorLigthStateData.updated_at
				if(incubatorLigthStateData.value=="ON"):
					print("encendido")
					pwm.start(dutyValue)
				elif(incubatorLigthStateData.value=="OFF"):
					print("apagado")
					pwm.ChangeDutyCycle(0)
					pwm.stop()
					
					# Set on dashboard (publish) ligth intensity in 0
					aio.send(incubatorLigthIntensityFeed.key, 0)
			
			# check if the received data is new
			if(incubatorLigthIntensityData.updated_at!=incubatorLigthIntensityLastUpdate):
				# Update datetime update, for execute only one time
				incubatorLigthIntensityLastUpdate=incubatorLigthIntensityData.updated_at

				# Check value is a number, manage errors
				if(incubatorLigthIntensityData.value.isdigit()):
					dutyValue=int(incubatorLigthIntensityData.value)
					print("cambio de intensidad a {}%".format(dutyValue))
				else:
					print("Error en el Duty value, valor recibido -> {}".format(incubatorLigthIntensityData.value))
					
				# check if the actual state for LED is ON
				if(incubatorLigthStateData.value=="ON"):
					# change LED ilumination intensity
					pwm.ChangeDutyCycle(dutyValue)
							
	except KeyboardInterrupt:
		# Set default values in dashboard (publish)
		aio.send(incubatorLigthStateFeed.key, "OFF")
		aio.send(incubatorLigthIntensityFeed.key, 0)
		
		# Stop PWM
		pwm.stop()
		
		# Clean
		GPIO.cleanup()
	

if __name__ == "__main__":
	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()
