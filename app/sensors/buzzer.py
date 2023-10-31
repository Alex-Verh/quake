import time

# Function to control the buzzer
def control_buzzer(BUZZER_PIN, status):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    if (status):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)


# Function to loop buzzer
def loop_buzzer(BUZZER_PIN, iterations):
    for i in range (0, iterations):
        control_buzzer(BUZZER_PIN, True)
        time.sleep(0.3)
        control_buzzer(BUZZER_PIN, False)
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        loop_buzzer(16, 5)

        # while True:
        #     print("Buzzer 4 seconds on")
        #     control_buzzer(16, True, 2)
        #     time.sleep(4)

        #     print("Buzzer 2 seconds off")
        #     control_buzzer(16, False, 2)
        #     time.sleep(2)
    
    except KeyboardInterrupt:
        GPIO.cleanup()