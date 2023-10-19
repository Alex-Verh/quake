# Required modules are imported and set up
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Here the output pin is declared, to which the LEDs are connected.
LED_Red = 17
LED_Green = 24
LED_Blue = 4

GPIO.setup(LED_Red, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_Green, GPIO.OUT, initial= GPIO.LOW)
GPIO.setup(LED_Blue, GPIO.OUT, initial= GPIO.LOW)
   
print ("LED test [press CTRL+C to exit test]")
  
# main program loop
try:
    while True:
        print("LED RED 3 seconds on")
        GPIO.output(LED_Red,GPIO.HIGH) #LED is turned on
        GPIO.output(LED_Green,GPIO.HIGH) #LED is switched on
        GPIO.output(LED_Blue,GPIO.HIGH) #LED is switched on
        # time.sleep(3) # wait mode for 4 seconds
        # print("LED GREEN 3 seconds on") 
        # GPIO.output(LED_Red,GPIO.LOW) #LED is switched on
        # GPIO.output(LED_Green,GPIO.HIGH) #LED is switched on
        # GPIO.output(LED_Blue,GPIO.LOW) #LED is switched on
        # time.sleep(3) #wait mode for 3 seconds
        # print("LED BLUE 3 seconds on") 
        # GPIO.output(LED_Red,GPIO.LOW) #LED is switched on
        # GPIO.output(LED_Green,GPIO.LOW) #LED is switched on
        # GPIO.output(LED_Blue,GPIO.HIGH) #LED is switched on
        # time.sleep(3) #wait mode for 3 seconds
   
# clean up after the program is finished
except KeyboardInterrupt:
    GPIO.cleanup()