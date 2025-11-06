import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht

gpio.setmode(gpio.BOARD)

pin_sensor = 4 
dht_sensor = dht.DHT11

pin_t = 15
pin_e = 16
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

ledVermelho = 11
ledVerde = 12
gpio.setup(ledVermelho, gpio.OUT)
gpio.setup(ledVerde, gpio.OUT)


def distancia():
    gpio.output(pin_t, True)
    delay.sleep(0.00001)
    gpio.output(pin_t, False)

    while gpio.input(pin_e) == 0:
        tempo_i = delay.time()
    while gpio.input(pin_e) == 1:
        tempo_f = delay.time()

    tempo_d = tempo_f - tempo_i
    distancia_cm = (tempo_d * 34300) / 2
    return distancia_cm

while True:
    _, temp = dht.read(dht_sensor, pin_sensor)

    if temp is not None:
        print("Temperatura = {0:0.1f}°C".format(temp))
    else:
        print("Falha ao ler o sensor DHT11")

    valor_lido = distancia()
    print("Distância = %.1f cm" % valor_lido)

    if valor_lido < 5:
        gpio.output(ledVermelho, True)
        gpio.output(ledVerde, False)
        print("LED Vermelho Ativado (distância < 5cm)")
    else:
        gpio.output(ledVermelho, False)

        if temp is not None and temp > 18:
            
            gpio.output(ledVerde, True)
            delay.sleep(0.3)
            gpio.output(ledVerde, False)
            delay.sleep(0.3)
            print("LED Verde Piscando (temp > 18°C)")
        else:
            gpio.output(ledVerde, False)
            print("LED Verde Desligado (temp <= 18°C)")

    delay.sleep(1)