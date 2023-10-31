# This code will be used for reading data from both MQ-2 and MQ-9

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

MQ_PIN = 4
GPIO.setup(MQ_PIN, GPIO.IN)

try: 
    while True:
        input = GPIO.input(MQ_PIN)
        print('Gas status (0 - bad; 1 - good): ', input)
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()