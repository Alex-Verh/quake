# For now just have a single thread that reads sensor data together
import time
import humidity
import accel
import dd_sensor

# Constants
DHT_PIN = 4
FLAME_PIN = 4
MQ2_PIN = 4
MQ9_PIN = 4


# Accelerometer previous values
prev_acc_x = 0
prev_acc_y = 0
prev_acc_z = 0

while True:

    # Read humidity
    humidity, temperature = humidity.read_humidity_temperature(4)

    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading from ASM2302.')


    # Read acceleration
    # Note that we don't define pins for the MPU6050 because it can work only with GPIO 2 (SDA) and GPIO 3 (SCL)
    acc_x, acc_y, acc_z = accel.read_raw_acceleration()

    # Calculate changes in acceleration
    delta_x = abs(acc_x - prev_acc_x)
    delta_y = abs(acc_y - prev_acc_y)
    delta_z = abs(acc_z - prev_acc_z)

    # Update accelerometer previous values
    prev_acc_x = acc_x
    prev_acc_y = acc_y
    prev_acc_z = acc_z

    print("delta_x: ", delta_x, " delta_y: ", delta_y, " delta_z: ", delta_z)

    # Check for sharp movement
    sharp_movement_detected = delta_x > accel.SHARP_MOVEMENT_THRESHOLD or delta_y > accel.SHARP_MOVEMENT_THRESHOLD or delta_z > accel.SHARP_MOVEMENT_THRESHOLD
    if sharp_movement_detected:
        print("Sharp movement detected")


    # Read flame
    flame = dd_sensor.read_dd(FLAME_PIN)
    print('Flame status (0 - good; 1 - bad): ', input)

    # Read MQ2
    mq2 = dd_sensor.read_dd(MQ2_PIN)
    print('Gas status (0 - bad; 1 - good): ', mq2)

    # Read MQ9
    mq9 = dd_sensor.read_dd(MQ9_PIN)
    print('Gas status (0 - bad; 1 - good): ', mq9)

    time.sleep(1)