import subprocess

# Function to run rs485.py
def run_rs485():
    subprocess.run(["python3", "rs485.py"])

# Function to run sensor-mqtt-pg.py
def run_sensor_mqtt_pg():
    subprocess.run(["python3", "sensor-mqtt-pg.py"])

# Main function to run both scripts
def main():
    # Start rs485.py in a separate process
    rs485_process = subprocess.Popen(["python3", "rs485.py"])

    # Start sensor-mqtt-pg.py in a separate process
    sensor_mqtt_pg_process = subprocess.Popen(["python3", "sensor-mqtt-pg.py"])

    # Wait for both processes to complete
    rs485_process.wait()
    sensor_mqtt_pg_process.wait()

if __name__ == "__main__":
    main()
