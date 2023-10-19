# Required modules are imported and set up
import RPi.GPIO as GPIO
import time

# The red and green LEDs are inverted on the sensor.
LED_Red = 27 #22
LED_Green = 22 #27
LED_Blue = 17


# Function to control led lights
def control_led(LED_RED, LED_GREEN, LED_BLUE, red_status, green_status, blue_status):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_BLUE, GPIO.OUT)

    GPIO.output(LED_Red, red_status)
    GPIO.output(LED_Green, green_status)
    GPIO.output(LED_Blue, blue_status)


# Function to loop leds in a pattern
def loop_led(LED_RED, LED_GREEN, LED_BLUE, iterations):
    for i in range (0, iterations):
        control_led(LED_RED, LED_GREEN, LED_BLUE, True, False, False)
        time.sleep(0.5)
        control_led(LED_RED, LED_GREEN, LED_BLUE, True, False, True)
        time.sleep(0.5)
        control_led(LED_RED, LED_GREEN, LED_BLUE, False, False, True)
        time.sleep(0.25)
        control_led(LED_RED, LED_GREEN, LED_BLUE, True, True, True)
        time.sleep(0.25)

    control_led(LED_RED, LED_GREEN, LED_BLUE, False, False, False)
  

if __name__ == "__main__":

    try:
        loop_led(27, 22, 17, 3)
    
    # clean up after the program is finished
    except KeyboardInterrupt:
        GPIO.cleanup()