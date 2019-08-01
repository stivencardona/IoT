# Import standard Python Modules
import time
import sys

# Import RPi.GPIO Module
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")
	
# Define Function "main", way to manage errors
def main():
	# Setup GPIO setmode
	GPIO.setmode(GPIO.BCM)#con los numeros de 
	
	# List with all GPIO pin numbers
	pinList=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
	
	# Set GPIO pin signal OUT and initial value "shutdown"
	GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)
	
	# Set signal up to all pins one to one in order
	for i in pinList:
		GPIO.output(i, GPIO.HIGH)
		time.sleep(0.5)

	# Set signal down to all pins one to one in reversed order
	for i in reversed(pinList):
		GPIO.output(i, GPIO.LOW)
		time.sleep(0.5)
	GPIO.cleanup()

if __name__ == '__main__':
	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()

