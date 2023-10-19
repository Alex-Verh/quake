# FILE OBSOLETED BY main_threads.py

# For now just have a single thread that reads sensor data together
import dht      # humidity sensor
import accel
import dd_sensor
import time
import datetime

# Constants
DHT_PIN = 4
FLAME_PIN = 26
MQ2_PIN = 4
MQ9_PIN = 4

# Sensor enable control
enable_dht = True
enable_accel = False
enable_flame = True
enable_mq2 = False
enable_mq9 = False

# Sensor data dictionaries for each sensor
# The first entry in each dictionary is the time() when the data was recorded
sensor_data = {
    "humidity": [],         # datetime (sql datetime), humidity (float), temperature (float)
    "acceleration": [],     # datetime (sql datetime), delta_x (float), delta_y (float), delta_z (float)
    "flame": [],            # datetime (sql datetime), digital_signal (0 - good; 1 - bad)
    "mq2": [],              # datetime (sql datetime), digital_signal (0 - bad; 1 - good)
    "mq9": [],              # datetime (sql datetime), digital_signal (0 - bad; 1 - good)
}

# Accelerometer previous values
prev_acc_x = 0
prev_acc_y = 0
prev_acc_z = 0

def get_current_sql_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

while True:
    

    # Read humidity
    if (enable_dht):
        humidity, temperature = dht.read_humidity_temperature(DHT_PIN)

        if humidity is not None and temperature is not None:
            print('Humidity={1:0.1f}%  Temp={0:0.1f}*'.format(humidity, temperature))
            sensor_data["humidity"].append((get_current_sql_time(), humidity, temperature))
        else:
            print('Failed to get reading from ASM2302.')

    # Read acceleration
    if (enable_accel):
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
        sharp_threshold_passed = (
            delta_x > accel.SHARP_MOVEMENT_THRESHOLD 
            or delta_y > accel.SHARP_MOVEMENT_THRESHOLD 
            or delta_z > accel.SHARP_MOVEMENT_THRESHOLD
        )
        if sharp_threshold_passed:
            print("Sharp movement detected. RING ALARM RING ALARM RING ALARM RING ALARM RING ALARM")
        sensor_data["acceleration"].append((get_current_sql_time(), delta_x, delta_y, delta_z, sharp_threshold_passed))


    # Read flame
    if (enable_flame):
        flame = dd_sensor.read_dd(FLAME_PIN)
        print('Flame status (0 - good; 1 - bad): ', flame)
        sensor_data["flame"].append((get_current_sql_time(), flame))

    # Read MQ2
    if (enable_mq2):
        mq2 = dd_sensor.read_dd(MQ2_PIN)
        print('Gas status (0 - bad; 1 - good): ', mq2)
        sensor_data["mq2"].append((get_current_sql_time(), mq2))

    # Read MQ9
    if (enable_mq9):
        mq9 = dd_sensor.read_dd(MQ9_PIN)
        print('Gas status (0 - bad; 1 - good): ', mq9)
        sensor_data["mq9"].append((get_current_sql_time(), mq9))

    print("\ndata: ", sensor_data, "\n")

    time.sleep(1)