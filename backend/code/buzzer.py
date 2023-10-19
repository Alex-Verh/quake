import RPi.GPIO as GPIO
import time

# Function to control the buzzer
# The interval will be used to turn off the alarm after specified seconds
def control_buzzer(BUZZER_PIN, status, interval):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    if (status):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)


if __name__ == "__main__":
    try:
        while True:
            print("Buzzer 4 seconds on")
            control_buzzer(24, True)
            time.sleep(4)

            print("Buzzer 2 seconds off")
            control_buzzer(24, False)
            time.sleep(2)
    
    except KeyboardInterrupt:
        GPIO.cleanup()