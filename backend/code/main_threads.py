# For now just have a single thread that reads sensor data together
import dht      # humidity sensor
import accel
import dd_sensor

import time
import datetime
import threading
import queue
import sqlite3

# Constants
DHT_PIN = 4
FLAME_PIN = 26
MQ2_PIN = 4
MQ9_PIN = 4

DATA_QUEUE_SIZE = 300

# Sensor enable control
enable_dht = True
enable_accel = False
enable_flame = True
enable_mq2 = False
enable_mq9 = False

# Sensor data dictionaries for each sensor
# Time will be recorded when writing to the db
sensor_data = {
    "humidity": queue.Queue(),         # humidity (float), temperature (float)
    "acceleration": queue.Queue(),     # delta_x (float), delta_y (float), delta_z (float)
    "flame": queue.Queue(),            # digital_signal (0 - good; 1 - bad)
    "mq2": queue.Queue(),              # digital_signal (0 - bad; 1 - good)
    "mq9": queue.Queue(),              # digital_signal (0 - bad; 1 - good)
}

# We will set a maximum queue size of 300
# Sensors will collect data every second -> 5 minutes * 60 seconds = 300 entries
# Data average will be uploaded to the db once every 5 minutes
def ensure_queue_size():
    for key in sensor_data:
        while sensor_data[key].qsize() > DATA_QUEUE_SIZE:
            sensor_data[key].get()


# Function to get the current datetime in sql datetime format
def get_current_sql_time():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# Create a lock object for synchronized access to sensor_data
data_lock = threading.Lock()


# Function to upload the average of collected datat to the db
# The function is tooooo big so another function (below) will be representing the thread
def upload_data_sql():
    # Average values
    avg_humidity = 0
    avg_temperature = 0
    avg_delta_x = 0
    avg_delta_y = 0
    avg_delta_z = 0

    # Values that will indicate if the hazard was detected even once in the time interval between db writes
    # 0 good; 1 bad
    top_flame = 0
    # 0 bad; 1 good
    top_mq2 = 1
    # 0 bad; 1 good
    top_mq9 = 1

    with data_lock:

        # Calculate avg values for the dht sensor
        size_dht = sensor_data["humidity"].qsize()
        if (size_dht == 0): size_dht = 1

        while not sensor_data["humidity"].empty():
            hum, temp = sensor_data["humidity"].get()
            avg_humidity += hum
            avg_temperature += temp
        avg_humidity /= size_dht
        avg_temperature /= size_dht

        # Calculate avg values for the mpu accelerator
        size_mpu = sensor_data["acceleration"].qsize()
        if (size_mpu == 0): size_mpu = 1

        while not sensor_data["acceleration"].empty():
            delta_x, delta_y, delta_z = sensor_data["acceleration"].get()
            avg_delta_x += delta_x
            avg_delta_y += delta_y
            avg_delta_z += delta_z
        avg_delta_x /= size_mpu
        avg_delta_y /= size_mpu
        avg_delta_z /= size_mpu

        # Calculate "top" (most common) value for flame
        flame_zero_counter = 0
        size_flame = sensor_data["flame"].qsize()
        if (size_flame == 0): size_flame = 1

        while not sensor_data["flame"].empty():
            val = sensor_data["flame"].get()
            if (val == 0):
                flame_zero_counter += 1
        if (flame_zero_counter / size_flame >= 0.5):
            top_flame = 0
        else:
            top_flame = 1

        # Calculate the "top" (most common) value for mq2
        mq2_zero_counter = 0
        size_mq2 = sensor_data["mq2"].qsize()
        if (size_mq2 == 0): size_mq2 = 1

        while not sensor_data["mq2"].empty():
            val = sensor_data["mq2"].get()
            if (val == 0):
                mq2_zero_counter += 1
        if (mq2_zero_counter / size_mq2 >= 0.5):
            top_mq2 = 0
        else:
            top_mq2 = 1
        
        # Calculate the "top" (most common) value for mq9
        mq9_zero_counter = 0
        size_mq9 = sensor_data["mq9"].qsize()
        if (size_mq9 == 0): size_mq9 = 1
        
        while not sensor_data["mq9"].empty():
            val = sensor_data["mq9"].get()
            if (val == 0):
                mq9_zero_counter += 1
        if (mq9_zero_counter / size_mq9 >= 0.5):
            top_mq9 = 0
        else:
            top_mq9 = 1

    # Insert into quakeDB.db
    try:
        connection = sqlite3.connect("../db/quakeDB.db")
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO sensor_data (
                timestamp,
                avg_humidity,
                avg_temperature,
                avg_delta_x,
                avg_delta_y,
                avg_delta_z,
                top_flame,
                top_mq2,
                top_mq9
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            get_current_sql_time(),
            avg_humidity,
            avg_temperature,
            avg_delta_x,
            avg_delta_y,
            avg_delta_z,
            top_flame,
            top_mq2,
            top_mq9
        ))

        connection.commit()
        connection.close()

        print("Success on inserting into quakeDB.db!")
    
    except sqlite3.Error as err:
        print("Failed to insert data into sqlite table", err)
    finally:
        if connection:
            connection.close()
            print("The sqlite connection is closed")


# Function to create the upload_data_sql_thread
def upload_data_sql_thread(interval):
    while True:
        time.sleep(interval)
        upload_data_sql()


# Function to read AM2302 data
def read_dht_data(interval):
    print("Reading dht data...")
    while True:
        if enable_dht:
            humidity, temperature = dht.read_humidity_temperature(DHT_PIN)
            if humidity is not None and temperature is not None:
                with data_lock:
                    sensor_data["humidity"].put((humidity, temperature,))
                    ensure_queue_size()
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
                print("Sharp movement detected. RING ALARM RING ALARM RING ALARM RING ALARM RING ALARM")

            with data_lock:
                sensor_data["acceleration"].put((
                        delta_x, 
                        delta_y, 
                        delta_z, 
                        sharp_threshold_passed,
                    ))
                ensure_queue_size()
        time.sleep(interval)

# Function to read KY-026 data
def read_flame_data(interval):
    print("Reading flame data...")
    while True:
        if enable_flame:
            flame = dd_sensor.read_dd(FLAME_PIN)
            # print('Flame status (0 - good; 1 - bad): ', flame)
            with data_lock:
                sensor_data["flame"].put(flame)
                ensure_queue_size()
        time.sleep(interval)


# Function to read MQ-2 data
def read_mq2_data(interval):
    print("Reading mq2 data...")
    while True:
        if enable_mq2:
            mq2 = dd_sensor.read_dd(MQ2_PIN)
            # print('Gas status (0 - bad; 1 - good): ', mq2)
            with data_lock:
                sensor_data["mq2"].put(mq2)
                ensure_queue_size()
        time.sleep(interval)


# Function to read MQ-9 data
def read_mq9_data(interval):
    print("Reading mq9 data...")
    while True:
        if enable_mq9:
            mq9 = dd_sensor.read_dd(MQ9_PIN)
            # print('Gas status (0 - bad; 1 - good): ', mq2)
            with data_lock:
                sensor_data["mq9"].put(mq9)
                ensure_queue_size()
        time.sleep(interval)


if __name__ == '__main__':

    try:
        dht_thread = threading.Thread(target=read_dht_data, name="dht_thread", args=(1,))
        acceleration_thread = threading.Thread(target=read_mpu6050_data, name="acceleration_thread", args=(1,))
        flame_thread = threading.Thread(target=read_flame_data, name="flame_thread", args=(1,))
        mq2_thread = threading.Thread(target=read_mq2_data, name="mq2_thread", args=(1,))
        mq9_thread = threading.Thread(target=read_mq9_data, name="mq9_thread", args=(1,))
        sql_thread = threading.Thread(target=upload_data_sql_thread, name="sql_thread", args=(300,))

        dht_thread.start()
        acceleration_thread.start()
        flame_thread.start()
        mq2_thread.start()
        mq9_thread.start()
        sql_thread.start()


        while True:
            print('----- 5 seconds have passed -----')
            print(sensor_data)
            time.sleep(5)

    except KeyboardInterrupt:
        dht_thread.join()
        acceleration_thread.join()
        flame_thread.join()
        mq2_thread.join()
        mq9_thread.join()