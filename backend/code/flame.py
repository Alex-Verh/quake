import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

Flame_PIN = 26
GPIO.setup(Flame_PIN, GPIO.IN)

try: 
    while True:
        input = GPIO.input(Flame_PIN)
        print('Flame status (0 - good; 1 - bad): ', input)
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()