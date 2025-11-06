import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht
from flask import render_template 
from app import app

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)

led_vermelho, led_verde = 11, 12

pin_t, pin_e = 15, 16

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

@app.route("/")
def index():
    templateData = {
        "led_vermelho": status_led_vermelho(),
        "led_verde": status_led_verde()
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
        "led_verde": status_led_verde()
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
        "led_verde": status_led_verde()
    }
    return render_template("index.html", **templateData)