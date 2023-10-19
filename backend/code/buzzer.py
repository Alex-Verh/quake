# Required modules are imported and set up
import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BCM)
  
# Here the input pin is declared, to which the sensor is connected.
Buzzer_PIN = 4
GPIO.setup(Buzzer_PIN, GPIO.OUT, initial= GPIO.LOW)

print("Buzzer test [press CTRL+C to exit test]")
 
# main program loop
try:
    while True:
        print("Buzzer 4 seconds on")
        GPIO.output(Buzzer_PIN,GPIO.HIGH) #buzzer is switched on
        time.sleep(4)#wait mode for 4 seconds
        print("Buzzer 2 seconds off")
        GPIO.output(Buzzer_PIN,GPIO.LOW) #buzzer is switched off
        time.sleep(2)#wait mode for another two seconds then LED is off
  
#rearrange after the program has been terminated
except KeyboardInterrupt:
    GPIO.cleanup()