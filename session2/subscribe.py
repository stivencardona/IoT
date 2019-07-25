# Import standard Python Modules
import sys
import os

# Import paho MQTT Client
import paho.mqtt.client as mqtt

# Define callback functions which will be called when certain events happen.
def on_connect(client, userdata, flags, rc):
	# Connected function will be called when the client connects.
	print("Conectado con codigo resultante:  "+str(rc))
	
	if rc == 0:
		# Subscribing in on_connect() means that if we lose the connection and
		# reconnect then subscriptions will be renewed.
		topic = 'edgr6/#'
		print("Suscribiendose al topic ->{0}".format(topic))
		client.subscribe(topic)
	else:
		print("NO SE PUDO ESTABLECER LA CONEXION")

def on_message(client, userdata, message):
	# Message function will be called when a subscribed feed has a new value.
	print("message received " ,str(message.payload.decode("utf-8")))
	print("message topic=",message.topic)

if __name__ == "__main__":
	piso =0
	cantRooms = 0
	cantBombillos = 0#asu
	if(len(sys.argv)!=5):
		sys.stderr.write('Usage: "{0}" $hostAddress  piso habitacion cantlucesxhabitacion\n'.format(sys.argv[0]))
		os._exit(1)
	
	
	# Create an MQTT client instance.
	print("Creando instancia MQTT")
	client = mqtt.Client()
	
	client.piso = int(sys.argv[2])#cantidad de pisos que tiene el edificio
	client.cantRooms = int(sys.argv[3])#cantidad de habitaciones que tiene el edificio
	client.cantBombillos = int(sys.argv[4])#canidad de bombillos que tiene el edificio
	
	#garantizamos almenos un piso, una habitacion y un bombillo
	assert(client.piso > 0)
	assert(client.cantRooms > 0)
	assert(client.cantBombillos > 0)
	
	# Setup the callback functions
	client.on_message = on_message
	client.on_connect = on_connect

	# Connect to the Broker server.
	print("conectando al broker")
	client.connect(host=sys.argv[1], port=1883, keepalive=60)

	client.loop_forever()
