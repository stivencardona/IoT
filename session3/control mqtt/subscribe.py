# Import standard Python Modules
import sys
import os
import time
import RPi.GPIO as GPIO

# Import paho MQTT Client
import paho.mqtt.client as mqtt


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