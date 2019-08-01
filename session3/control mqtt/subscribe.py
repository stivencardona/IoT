# Import standard Python Modules
import sys
import os
import time
import RPi.GPIO as GPIO

# Import paho MQTT Client
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)
pinList = [i for i in range(2,28)]
pines = {}

GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)
for p in pinList:

    pines[p] = GPIO.PWM(p, 60)
    pines[p].start(0)
        
def on_connect(client, userdata, flags, rc):

    if rc== 0:

        topic = 'grupo6/#'
        print("Suscribiendose al topic -> {}".format(topic))
        client.subscribe(topic)
    else:
        print("NO SE PUDO ESTABLECER LA CONEXION")

def on_message(client, userdata, message):

    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    msj = str(message.payload.decode("utf-8"))
    leds,porcentaje = msj.split("|")
    print(leds)
    leds = eval(leds)
    print(leds)
    if message.topic == "grupo6/luces":
        print("vamos a prender o apagar luces")

        if porcentaje == "ON":
            print("encender leds..")
            for l in leds :
                print("led ",l)
                pines[l].ChangeDutyCycle(99) 
        elif porcentaje == "OFF":
            print("apagar leds")
            for l in leds :
                print("led", l)
                pines[l].ChangeDutyCycle(0) 
        else:
            print("no se hara nada porcentajes invalidos")

    elif message.topic == "grupo6/iluminacion":
        porcentaje = int(porcentaje)
        print("vamsos a cambiar la luminosidad de las luces")

        for l in leds :
            print("led ",l)
            pines[l].ChangeDutyCycle(porcentaje)
            



def main():

    print("iniciando servidor")
    print("creando instancia MQTT")
    client = mqtt.Client()

    client.on_message = on_message
    client.on_connect = on_connect

    print("conectando al broker")
    client.connect(host = "192.168.26.97", port=1883, keepalive = 60)

    client.loop_forever()


if __name__ == "__main__":

	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()    