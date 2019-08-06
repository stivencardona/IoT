# Import standard Python Modules
import time

# Import Adafruit_DHT Module
import Adafruit_DHT

# Tipo de sensor, numero GPIO de pin

if __name__=="__main__":
    while True:
        # Retreive data from DHT11 sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor=Adafruit_DHT.DHT11, pin=4, retries=15, delay_seconds=2)
        
        # Check Retreive Data
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')