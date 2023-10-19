# For now just have a single thread that reads sensor data together
import dht      # humidity sensor
import accel
import dd_sensor

import time
import datetime
import threading
import sys

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
    "acceleration": [],     # datetime (sql datetime), delta_x (float), delta_y (float), delta_z (float), threshold_passed (boolean)
    "flame": [],            # datetime (sql datetime), digital_signal (0 - good; 1 - bad)
    "mq2": [],              # datetime (sql datetime), digital_signal (0 - bad; 1 - good)
    "mq9": [],              # datetime (sql datetime), digital_signal (0 - bad; 1 - good)
}

def get_current_sql_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# Create a lock object for synchronized access to sensor_data
data_lock = threading.Lock()

# Function to read AM2302 data
def read_dht_data(interval):
    print("Reading dht data...")
    while True:
        if enable_dht:
            humidity, temperature = dht.read_humidity_temperature(DHT_PIN)
            if humidity is not None and temperature is not None:
                with data_lock:
                    sensor_data["humidity"].append((get_current_sql_time(), humidity, temperature,))
        time.sleep(interval)


# Function to read MPU6050 data
def read_mpu6050_data(interval):
    print("Reading accelerator data...")
    # Accelerometer previous values
    prev_acc_x = 0
    prev_acc_y = 0
    prev_acc_z = 0

    while True:
        if enable_accel:
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

            # print("delta_x: ", delta_x, " delta_y: ", delta_y, " delta_z: ", delta_z)

            # Check for sharp movement
            sharp_threshold_passed = (
                delta_x > accel.SHARP_MOVEMENT_THRESHOLD 
                or delta_y > accel.SHARP_MOVEMENT_THRESHOLD 
                or delta_z > accel.SHARP_MOVEMENT_THRESHOLD
            )
            if sharp_threshold_passed:
                print("Sharp movement detected")

            with data_lock:
                sensor_data["acceleration"].append((
                        get_current_sql_time(), 
                        delta_x, 
                        delta_y, 
                        delta_z, 
                        sharp_threshold_passed,
                    ))
        time.sleep(interval)

# Function to read KY-026 data
def read_flame_data(interval):
    print("Reading flame data...")
    while True:
        if enable_flame:
            flame = dd_sensor.read_dd(FLAME_PIN)
            # print('Flame status (0 - good; 1 - bad): ', flame)
            with data_lock:
                sensor_data["flame"].append((get_current_sql_time(), flame))
        time.sleep(interval)


# Function to read MQ-2 data
def read_mq2_data(interval):
    print("Reading mq2 data...")
    while True:
        if enable_mq2:
            mq2 = dd_sensor.read_dd(MQ2_PIN)
            # print('Gas status (0 - bad; 1 - good): ', mq2)
            with data_lock:
                sensor_data["mq2"].append((get_current_sql_time(), mq2))
        time.sleep(interval)


# Function to read MQ-9 data
def read_mq9_data(interval):
    print("Reading mq9 data...")
    while True:
        if enable_mq9:
            mq9 = dd_sensor.read_dd(MQ9_PIN)
            # print('Gas status (0 - bad; 1 - good): ', mq2)
            with data_lock:
                sensor_data["mq9"].append((get_current_sql_time(), mq9))
        time.sleep(interval)


if __name__ == '__main__':

    try:
        dht_thread = threading.Thread(target=read_dht_data, name="dht_thread", args=(1,))
        acceleration_thread = threading.Thread(target=read_mpu6050_data, name="acceleration_thread", args=(1,))
        flame_thread = threading.Thread(target=read_flame_data, name="flame_thread", args=(1,))
        mq2_thread = threading.Thread(target=read_mq2_data, name="mq2_thread", args=(1,))
        mq9_thread = threading.Thread(target=read_mq9_data, name="mq9_thread", args=(1,))

        dht_thread.start()
        acceleration_thread.start()
        flame_thread.start()
        mq2_thread.start()
        mq9_thread.start()


        while True:
            print('----- 5 seconds has passed -----')
            print(sensor_data)
            time.sleep(5)

    except KeyboardInterrupt:
        dht_thread.join()
        acceleration_thread.join()
        flame_thread.join()
        mq2_thread.join()
        mq9_thread.join()