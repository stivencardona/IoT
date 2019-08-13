# Import standard python modules
import time
import sys

# Import GPIO Module
import RPi.GPIO as GPIO
 
# set GPIO Pins Trigger and echo vars
GPIO_TRIGGER = 2
GPIO_ECHO = 3

# Define Function to get data from ultrasonic sensor
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed
    # in the air at 20° 343.6 m/s
    # and divide by 2, because there and back
    distance = (TimeElapsed * 343.59999999999997) / 2
 
    return distance
 
# Define Function "main", way to manage errors
def main():
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    while True:
        dist = distance()
        print ("Measured Distance = %.1f m" % dist)
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main() 
    except:
        print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
        GPIO.cleanup()