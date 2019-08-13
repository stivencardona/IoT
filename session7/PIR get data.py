# Import standard python modules
import time
import datetime
import sys

# Import GPIO Module
import RPi.GPIO as GPIO

# Setup Sensor pin var
SENSOR_PIN = 4

# Define callback functions which will be called when certain events happen.
def motionPIR(channel):
	# motionPIR function will be called when event
	# RISING and FALLING is detected (GPIO event)
	# In retriggering mode (jumper placed in H) 
	# The event detection can works of the next form:
	# with RISING event (LOW to HIGH) while detect movement
	# with FALLING event (HIGH to LOW) when movement are 
	# stoped (some seconds, depend sensivity value)
	timestamp = time.time()
	stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
	sense=GPIO.input(SENSOR_PIN)
	if(sense==GPIO.HIGH):
		print('Se ha detectado movimiento: {}'.format(stamp))
	elif(sense==GPIO.LOW):
		print('No hay mas movimiento: {}'.format(stamp))

# Define Function "main", way to manage errors
def main():
	# Setup GPIO mode
	GPIO.setmode(GPIO.BCM)
	# Set GPIO pin direction
	GPIO.setup(SENSOR_PIN, GPIO.IN)

	# add event for detection
	GPIO.add_event_detect(SENSOR_PIN , GPIO.BOTH, callback=motionPIR, bouncetime=150)
	while True:
		time.sleep(0.1)

if __name__=="__main__":
	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()