# A general script to read data from digital sensors (such as the flame sensor a the MQ sensors)

import RPi.GPIO as GPIO

def read_dd(INPUT_PIN):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN)

    input = GPIO.input(INPUT_PIN)
    print('DD signal for GPIO ' , INPUT_PIN, ': ', input)