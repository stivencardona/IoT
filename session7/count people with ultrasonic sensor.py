# Import standard python modules
import time
import threading
import datetime

# Import GPIO Module
import RPi.GPIO as GPIO


# Define global vars #
# Control of sincronization in Threads
lock = threading.RLock()

# Set GPIO Pins for Trigger and Echo vars
GPIO_TRIGGER = 2
GPIO_ECHO = 3

# setup show data time
showDataTime=20


# Define Classes #
# Define class for instance objects in threading
class DataCount():
	def __init__(self):
		self.countTimes=0


# Define functions #
# Define functions for paralelism
def show_data(peopleCount):
	counted=False
	while True:
		# Show data every 20 seconds and reset countTimes
		if(int(time.time())%showDataTime==0): 
			if(not counted):
				lock.acquire()
				print("{} | Personas contadas {}".format(datetime.datetime.now(), peopleCount.countTimes))
				peopleCount.countTimes=0
				lock.release()
				counted=True
		else:
			counted=False


# Define Function to get data from ultrasonic sensor
def distance_():
	# Set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
 
	# Set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, GPIO.LOW)
 
	StartTime = time.time()
	StopTime = time.time()
 
	# Save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
 
	# Save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
 
	# Time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	"""To calculate distance is
	multiply with the sonic speed in the air at 20° 343.6 m/s and divide
	 by 2, because there and back
	"""
	distance = (TimeElapsed * 343.59999999999997) / 2
 
	return distance
 

# Define Function "main", way to manage errors
def main():
	# Define GPIO Pins vars
	GPIO_COUNT_STATE = 7# LED for alert are in count state
	GPIO_COUNTED = 8# LED to show +1 count

	# GPIO Mode (BOARD / BCM)
	GPIO.setmode(GPIO.BCM)
	
	# set GPIO direction (IN / OUT)
	GPIO.setup([GPIO_TRIGGER, GPIO_COUNT_STATE, GPIO_COUNTED], 
		GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(GPIO_ECHO, GPIO.IN)

	# Control of count system
	countPeople=DataCount()
	maxDistance=1.7
	baseTime=time.time()
	countTemp=0		# Count value while step and interrupt area
	countTempLast=0
	
	# Flags for execute only one time (turn off, turn on)
	counted=False
	countState=False
	countTempLastState=True
	
	countRate=0.3

	# Setup Threading, to show data every 20 seconds
	hilo0=threading.Thread(target=show_data, args=[countPeople,])
	hilo0.start()
	
	while True:
		dist = distance_()
		if(round(dist,1)>=maxDistance):
			baseTime=time.time()
			if(countTemp!=0):
				lock.acquire()
				countPeople.countTimes+=countTemp
				lock.release()
				countTemp=0
			if(countState):
				countState=False
				GPIO.output(GPIO_COUNT_STATE, GPIO.LOW)
		else:
			# Triggered every 19 seconds for update counTimes
			if(int(time.time())%(showDataTime-1)==0):
				if(not counted):
					lock.acquire()
					countPeople.countTimes+=countTemp
					lock.release()
					
					# Update base time with rate residue
					baseTime=time.time()-(time.time()%countRate)
					# Update countTempLast for LED count alert
					continueTime=time.time()-baseTime
					countTempLast=int(continueTime/countRate)

					counted=True
			else:
				counted=False
			continueTime=time.time()-baseTime
			countTemp=int(continueTime/countRate)		# Count rate
			if(not countState):
				countState=True
				GPIO.output(GPIO_COUNT_STATE, GPIO.HIGH)

		# Turn on LED to alert every counted +1 for 1 cycle time
		if(countTempLast!=countTemp):
			countTempLast=countTemp
			countTempLastState=False
			GPIO.output(GPIO_COUNTED, GPIO.HIGH)
		elif(not countTempLastState):
			GPIO.output(GPIO_COUNTED, GPIO.LOW)
			countTempLastState=True
			
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], 
			sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()