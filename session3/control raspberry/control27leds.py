# Import standard python modules
import time
import sys
import RPi.GPIO as GPIO

tipo = None
try:
    #print(sys.argv[1])
    tipo = int(sys.argv[1]) 
except:
    print("ocurrio un error con el tipo de funcionamiento, no es pwd ni setup")

assert(tipo == 0 or tipo == 1)
print(tipo)
#si es 0 significa que trabajmos con pwm
#si es 1 significa que trabajamos con setup


def getData(p1,p2):

    op = input("ingrese operacion siguiendo el formato: {},{}".format(p1,p2))

    #op = eval(op)
    return op


def mainpwm():
    print("main pwm")
    formato = "[#,#,...,#]|porcentaje de pulso"
    msj = " ese es el porcentaje de iluminacion que tendran los leds de la lista\n"
    GPIO.setmode(GPIO.BCM)
    pinList = [i for i in range(2,28)]
    pines = {}

    GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)
    for p in pinList:

        pines[p] = GPIO.PWM(p, 60)
        pines[p].start(0)

    while True:
        data = getData(formato, msj)
        leds, porcentaje = data.split("|")

        leds = eval(leds)
        porcentaje = int(porcentaje)
        if porcentaje >= 0 and porcentaje <= 100:
            for l in leds:

                pines[l].ChangeDutyCycle(porcentaje)
        else:
            print("porcentaje fuera de los limites")


def mainsetup():
    print("main setup")
    formato = "[#,#,...,#]|acction"
    msj = " numero desde 2 hasta 27, la accion debe ser ON o OFF\n"
    GPIO.setmode(GPIO.BCM)

    pinList = [i for i in range(2,28)]
    GPIO.setup(pinList, GPIO.OUT, initial=GPIO.LOW)

    
    while True:
        data = getData(formato, msj)

        leds, op = data.split("|")

        leds = eval(leds)
        for led in leds:
            if op == "ON":
                GPIO.output(led, GPIO.HIGH)
            elif op == "OFF":
                GPIO.output(led, GPIO.LOW)
            else:
                print("Operacion invalida: {}".format(op))
        




def main():
    
    if tipo:
        mainsetup()
    else:
        mainpwm()


if __name__ == "__main__":
    
    
	try:
		main()
	except:
		print("{} line {}".format(sys.exc_info()[0], sys.exc_info()[-1].tb_lineno))
		GPIO.cleanup()
    