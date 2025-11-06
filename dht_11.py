import RPi.GPIO as gpio
import time as delay
import Adafruit_DHT as dht

gpio.setmode(gpio.BOARD)

# DHT11 sensor setup
pin_sensor = 4
dht_sensor = dht.DHT11

# Ultrasonic sensor setup
trigger, echo = 15, 16
gpio.setup(trigger, gpio.OUT)
gpio.setup(echo, gpio.IN)

# LED setup
led_vermelho, led_verde = 11, 12
gpio.setup(led_vermelho, gpio.OUT)
gpio.setup(led_verde, gpio.OUT)

# Trash configuration
empty_trash = 20

def measure_distance():
    gpio.output(trigger, True)
    delay.sleep(0.000001)
    gpio.output(trigger, False)

    init_time = delay.time()
    final_time = delay.time()
    
    while gpio.input(echo) == False:
        init_time = delay.time()
    while gpio.input(echo) == True:
        final_time = delay.time()
        
    distance_time = final_time - init_time
    distance = (distance_time * 34300) / 2 
    return distance

while True:
    # Read DHT11 sensor
    umid, temp = dht.read(dht_sensor, pin_sensor)
    if umid is not None and temp is not None:
        print("Temperature: {0:0.1f}°C  Humidity: {1:0.1f}%".format(temp, umid))
    else:
        print("Falha na leitura do sensor DHT11")
        continue
    
    # Read distance sensor
    try:
        dist = measure_distance()
    except Exception as e:
        print(f"Erro ao medir distância: {e}")
        continue
    print(f"Distância medida: {dist:.1f} cm")
    av_space = (dist/empty_trash)/100
    print(f"Espaço disponível no lixo: {av_space:.1%}")
    
    # Format temperature and humidity values
    temp = float(format(temp, '.1f'))
    umid = float(format(umid, '.1f'))
    
    # Control LEDs based on temperature and trash level
    trash_full = av_space <= 0.2  # 80% or more full
    
    if trash_full:
        gpio.output(led_vermelho, True)
        gpio.output(led_verde, False)
        print("Atenção: Lixeira está mais de 80% cheia!")
    elif temp > 18:
        # Piscar LED verde quando temperatura > 18°C
        gpio.output(led_vermelho, False)
        gpio.output(led_verde, True)
        delay.sleep(0.5)
        gpio.output(led_verde, False)
        delay.sleep(0.5)
        gpio.output(led_verde, True)
        print("Temperatura acima de 18°C - LED verde piscando")
    else:
        gpio.output(led_vermelho, False)
        gpio.output(led_verde, True)
        print("Condições normais")
    
    # Wait before next reading
    delay.sleep(6)