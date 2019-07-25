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
	print(sys.argv)
	
	#0 1
	# 2 3 4 [5 6 7 8]
	bombillas = sys.argv[5:]
	operation = sys.argv[4]
	
	piso = sys.argv[2]
	habitacion = sys.argv[3]
	try:
		piso = int(sys.argv[2])
		habitacion = int(sys.argv[3])
		
	except:
		sys.stderr.write("HABITACIONES Y PISOS NO SON VALORES VALIDOS")
		os._exit(1)
		
	assert(operation == "ON" or operation == "OFF")
	print("bombillas",bombillas)
	
	topic = "edgr6/piso{}/habitacion{}/luces".format(piso,habitacion)
	aux = str(bombillas)
	msj = "{}|{}".format(aux[1:len(aux)-1],operation)
	
	return topic, msj
	
	
	

if __name__ == "__main__":
	if(len(sys.argv)<6): 
		sys.stderr.write('Usage: "{0}" $hostAddress piso habitacion operation l1 [l2 l3 ... ln]\n'.format(sys.argv[0]))
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
	print("Publicando al topic ->'{0}'".format(t))
	client.publish(t,m)
	"""
	print("Publicando al topic ->'{0}'".format("area0/plant0/temperatura"))
	client.publish("area0/plant0/temperatura","{temperatura: 30}")
	print("Publicando al topic ->'{0}'".format("area0/plant0/humedad"))
	client.publish("area0/plant0/humedad","{humedad: 70}")
	"""
	
	
	client.loop_stop()
	client.disconnect()
