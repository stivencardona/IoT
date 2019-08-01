# Import standard Python Modules
import time
import sys
import os

# Import paho MQTT Client
import paho.mqtt.client as mqtt

# Define callback functions which will be called when certain events happen.
def on_connect(client, userdata, flags, rc):
	# Connected function will be called when the client connects.
	print("Conectado con codigo resultante:  "+str(rc))
	client.connectedFlag=True

def on_disconnect(client):
	# Disconnected function will be called when the client disconnects.
	print("¡Se ha Desconectado!")
	os._exit(1)

def makeDataToSend():
	

	#aqui se haria el control de errores pero se dejara para una proxima ocasion
	tipo = sys.argv[2]
	op = sys.argv[3]

	topic = "grupo6/{}".format(tipo)	
	return topic,op
	

if __name__ == "__main__":
	if(len(sys.argv) != 4): 
		sys.stderr.write('Usage: "{0}" $hostAddress TIPO:luces/iluminacion operacion:[#,#,#,..,#]|ON/ [#,#,#,..#]|porcentaje\n'.format(sys.argv[0]))
		os._exit(1)
		
		
	
	
	#argumentos
	#python publish.py ipbroker piso habitacion l1 [l2 l3 ... ln]
	
	# Setup the callback functions
	client = mqtt.Client()

	# Setup the callback functions
	client.on_connect = on_connect
	client.on_disconnect = on_disconnect

	# Setup Control vars
	client.connectedFlag=False

	# Connect to the Broker server.
	print("conectando al broker")
	client.connect(sys.argv[1], 1883, 60)
	client.loop_start()

	while not client.connectedFlag:
		print("Esperando conexión")
		time.sleep(1)
	
	t,m = makeDataToSend()
	print("Publicando al topic ->'{0}'".format(t), "el siguiente mensaje: ".format(m))
	client.publish(t,m)
	
	
	client.loop_stop()
	client.disconnect()
