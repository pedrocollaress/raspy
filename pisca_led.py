import RPi.GPIO as gpio
import time as delay

gpio.setmode(gpio.BOARD)

led_vermelho, led_verde = 11, 12

gpio.setup(led_vermelho, gpio.OUT)
gpio.setup(led_verde, gpio.OUT)

while True:
    gpio.output(led_vermelho, True)
    print("LED vermelho aceso")
    delay.sleep(5)
    gpio.output(led_vermelho, False)
    print("LED vermelho apagado")
    
