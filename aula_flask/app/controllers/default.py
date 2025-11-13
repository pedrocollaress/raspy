import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
from flask import render_template 
from app import app

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

led_vermelho, led_verde = 11, 12

pin_t, pin_e = 15, 16

lixeira = 20

pin_dht = 4

dht_sensor = dht.DHT11

status_vermelho = ""
status_verde = ""

gpio.setup(led_vermelho, gpio.OUT)
gpio.setup(led_verde, gpio.OUT)
gpio.setup(pin_t, gpio.OUT)
gpio.setup(pin_e, gpio.IN)

gpio.output(led_vermelho, gpio.LOW)
gpio.output(led_verde, gpio.LOW)

def status_led_vermelho():
    if gpio.input(led_vermelho) == 1:
        status_vermelho = "LED vermelho ON"
    else:
        status_vermelho = "LED vermelho OFF"
        
    return status_vermelho

def status_led_verde():
    if gpio.input(led_verde) == 1:
        status_verde = "LED verde ON"
    else:
        status_verde = "LED verde OFF"
        
    return status_verde

def umid_temp():
    umid, temp = dht.read(dht_sensor, pin_dht)
    if umid is not None:
        umidade = ('{0:0.0f}%'.format(umid))
    else:
        umidade = 'Erro ao ler sensor'

    if temp is not None:
        temperatura = ('{0:0.0f}*C'.format(temp))
    else:
        temperatura = 'Erro ao ler sensor'
        
    return umidade, temperatura

def ocupacao_lixeira ():
    gpio.output(pin_t, True)
    delay.sleep(0.000001)
    gpio.output(pin_t, False)

    init_time = delay.time()
    final_time = delay.time()
    
    while gpio.input(pin_e) == False:
        init_time = delay.time()
    while gpio.input(pin_e) == True:
        final_time = delay.time()
        
    distance_time = final_time - init_time
    distance = (distance_time * 34300) / 2 
    ocupacao_l = (distance/lixeira) * 100
    if ocupacao_l < 0:
        ocupacao_f = 0    
    ocupacao_f = 100 - ocupacao_l
    
    ocupacao_lixeira = ('(0:0.0f)%'.format(ocupacao_f))
    return ocupacao_lixeira

@app.route("/")
def index():
    templateData = {
        "led_vermelho": status_led_vermelho(),
        "led_verde": status_led_verde(),
        "umid": umid_temp()[0],
        "temp": umid_temp()[1],
        "ocup_lixeira": ocupacao_lixeira()
    } 
    return render_template("index.html", **templateData)

@app.route("/led_vermelho/<action>")
def led_vermelho_route(action):
    if action == "on":
        gpio.output(led_vermelho, gpio.HIGH)
    elif action == "off":
        gpio.output(led_vermelho, gpio.LOW)

    templateData = {
        "led_vermelho": status_led_vermelho(),
        "led_verde": status_led_verde(),
        "umid": umid_temp()[0],
        "temp": umid_temp()[1],
        "ocup_lixeira": ocupacao_lixeira()
    }
    return render_template("index.html", **templateData)

@app.route("/led_verde/<action>")
def led_verde_route(action):
    if action == "on":
        gpio.output(led_verde, gpio.HIGH)
    elif action == "off":
        gpio.output(led_verde, gpio.LOW)

    templateData = {
        "led_verde": status_led_verde(),
        "led_verde": status_led_verde(),
        "umid": umid_temp()[0],
        "temp": umid_temp()[1],
        "ocup_lixeira": ocupacao_lixeira()
    }
    return render_template("index.html", **templateData)
