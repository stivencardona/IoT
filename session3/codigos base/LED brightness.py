# Import standard python modules
import time
import sys

# Import RPi.GPIO library
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")   

# Define Function "main", way to manage errors
def main():
	# var GPIO pin to show output
	led_pin = 21
	
	# Set GPIO pin mode
	GPIO.setmode(GPIO.BCM)
	# Set GPIO pin direction and initial in Off
	GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)   # Declaring pin 21 as output pin
	
	# Setup PWM instance to led_pin with 100 Hz
	pwm = GPIO.PWM(led_pin, 60)
	
	# start PWM at 0% duty cycle 
	pwm.start(0)
	
	# Change duty cicle 0 to 100
	for x in range(101):
		pwm.ChangeDutyCycle(x)
		time.sleep(0.01)
	   
	# change duty cicle 100 to 0
	for x in range(100,0,-1):
		pwm.ChangeDutyCycle(x)
		time.sleep(0.01)

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
	
	
