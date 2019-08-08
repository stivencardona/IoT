# Import standard python modules
import time

#obtener la temperatura y humedad del ambiente sensor DHT11
# Import Adafruit_DHT Module
import Adafruit_DHT

#para obtener la humedad de la tierra con el hidrometro
# Import Raspberry Hardware
import board
import busio

# Import ADS1115 module
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import sys
import os
import RPi.GPIO as GPIO
#to get data hidrometro need the next functions

import threading

from Adafruit_IO import MQTTClient

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Control vars
rawValueMin=9000;rawValueMax=26000
rawValueDeltaMax=rawValueMax-rawValueMin

#GPIO.setup([6], GPIO.OUT, initial=GPIO.LOW)

pinsuelo = [9,10,11]

pinhumedad = [25,26,27]
#GPIO.setup(pinsuelo, GPIO.OUT, initial=GPIO.LOW)
pintemp = [17,18,19]

GPIO.setup(pinsuelo + pinhumedad + pintemp, GPIO.OUT, initial=GPIO.LOW)

def getSuelo():
    return 100-((chan.value-rawValueMin)/rawValueDeltaMax)*100

def getNivelSuelo():

    temp = getSuelo()

    if temp < 30:
        return "bajo"
    elif temp > 65:
        return "alto"
    else:
        return "normal"

def getambiente():
    humidity, temperature = Adafruit_DHT.read_retry(sensor=Adafruit_DHT.DHT11, pin=4, retries=15, delay_seconds=2)
    while not validateAmbiente(humidity, temperature):
        humidity, temperature = Adafruit_DHT.read_retry(sensor=Adafruit_DHT.DHT11, pin=4, retries=15, delay_seconds=2)

    return humidity, temperature

def validateAmbiente(h,t):
    # Check Retreive Data
    if h is not None and t is not None:
        return True
    else:
        return False
    
def gethumedadAmbiente(h):

    if h < 60:
        return "bajo"
    elif h > 80:
        return "alto"
    else:
        return "normal"
def getTemperaturaAmbiente(t):

    if t < 15:
        return "bajo"
    elif t > 30:
        return "alto"
    else:
        return "normal"

def changeLeds(nivel, leds):
    #GPIO.output(i, GPIO.LOW)
    for i in leds:
        GPIO.output(i, GPIO.LOW)

    if nivel == "bajo":
        GPIO.output(leds[0], GPIO.HIGH)
    elif nivel == "normal":
        GPIO.output(leds[1], GPIO.HIGH)
    elif nivel  == "alto":
        GPIO.output(leds[2], GPIO.HIGH)
     
#variables glo bales de los sensores y valores


sensores = {"HumedadSuelo" :  0,
    "NivelHumedadSuelo" : "bajo",
    "HumedadAmbiente" : 0,
    "NivelHumedadAmbiente" : "bajo",
    "TemperaturaAmbiente" : 0,
    "NivelTemperaturaAmbiente" : "bajo",
    }


def TimeRealSuelo():
    while True:
        sensores["HumedadSuelo"] = getSuelo()
        sensores["NivelHumedadSuelo"] = getNivelSuelo()
        changeLeds(sensores["NivelHumedadSuelo"],pinsuelo)
        time.sleep(5)
        print("el valor del suelo: {} y su nivel es {}".format(sensores["HumedadSuelo"], sensores["NivelHumedadSuelo"]))





def TimeRealAmbiente():

    while True:
        sensores["HumedadAmbiente"],sensores["TemperaturaAmbiente"] = getambiente()
        sensores["NivelHumedadAmbiente"] = gethumedadAmbiente(sensores["HumedadAmbiente"])
        sensores["NivelTemperaturaAmbiente"] = getTemperaturaAmbiente(sensores["TemperaturaAmbiente"])
        changeLeds(sensores["NivelTemperaturaAmbiente"],pintemp)
        changeLeds(sensores["NivelHumedadAmbiente"],pinhumedad)
        print("el valor de la temperatura del ambiente es: {} y su nivel es {}.\nel valor de la humedad ambiente es: {} y su nivel es: {}".format(sensores["TemperaturaAmbiente"],sensores["NivelTemperaturaAmbiente"],sensores["HumedadAmbiente"],sensores["NivelHumedadAmbiente"]))


feeds = {"feedHumSuelo" : "humedad-suelo",
    "feedHumAmb" : "humedad-ambiente",
    "feedTmpAmb" : "temperatura-ambiente"}

def on_connect(client):
    pass

def on_disconnect(client):
    print("!Se desconecto amiguito")
    os._exit(1)

def send_message():
    while True:
        feeds["client"].publish(feed_id = feeds["feedHumSuelo"], value=sensores["HumedadSuelo"], feed_user =feeds["username"] )
        feeds["client"].publish(feed_id = feeds["feedHumAmb"], value=sensores["HumedadAmbiente"], feed_user =feeds["username"] )
        feeds["client"].publish(feed_id = feeds["feedTmpAmb"], value=sensores["TemperaturaAmbiente"], feed_user =feeds["username"] )

        print("PUBLICANDO ::: suelo: {} , humedad: {} , temperatura : {}".format(sensores["HumedadSuelo"],sensores["HumedadAmbiente"],sensores["TemperaturaAmbiente"]))
        time.sleep(10)

def main():
    #TimeRealSuelo()
    #TimeRealAmbiente()

    if(len(sys.argv) != 3):

        sys.stderr.write('Usage: "{}" $AdafruitIOusername $AdafruitIOkey , los feed estan quemados en el codigo xD\n'.format(sys.argv[0]))
        os._exit(1)

    #se leen de los sensores
    hiloSuelo = threading.Thread(target=TimeRealSuelo)
    hiloAmbiente = threading.Thread(target=TimeRealAmbiente)

    hiloSuelo.start()
    hiloAmbiente.start()
    #----------------------------------------------

    username = sys.argv[1]
    skey = sys.argv[2]

    feeds["username"] = username
    feeds["skey"] = skey

    client = MQTTClient(username = username, key = skey)
    

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect()
    client.loop_background()

    feeds["client"] = client

    send_message()
    #threading.Thread.join()

if __name__ == '__main__':
    #main()
    try:
        main()
    except:
        print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
        GPIO.cleanup()
        #hiloSuelo.
        
