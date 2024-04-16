print("Sensors and Actuators")

import time
import serial.tools.list_ports
import paho.mqtt.client as mqtt
import json

import psycopg2
from datetime import datetime

import requests
from bs4 import BeautifulSoup

host = "bqnbcj8kxuogsigyhnzy-postgresql.services.clever-cloud.com"
database = "bqnbcj8kxuogsigyhnzy"
user = "ufjklpchveyybgraqhxu"
password = "AyR5dzFuySPaAcWd5po1AJMK063nkG"
port = "50013"
table_name = "json_rs485"

url = 'https://www.timeanddate.com/weather/vietnam/ho-chi-minh'

MQTT_SERVER = "demo.thingsboard.io"
MQTT_PORT = 1883
MQTT_ACCESS_TOKEN = "MNUrel9MvIV2iXce3LA1"
# MQTT_PASSWORD = ""
# MQTT_TOPIC_PUB_TEMP = MQTT_USERNAME + "/feeds/V1/mois/"
MQTT_TOPIC_PUB = "v1/devices/me/telemetry"
MQTT_TOPIC_SUB = "v1/devices/me/rpc/request/+"

# Function to insert JSON data into PostgreSQL database
def insert_data_into_postgres(json_data, host, database, user, password, port, table_name):
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

        # Create a cursor
        cursor = connection.cursor()

        # Define the SQL query to insert JSON data into the database
        insert_query = "INSERT INTO {} (time, tempmois) VALUES (%s, %s::jsonb)".format(table_name)

        # Get the current timestamp
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Execute the SQL query with the current time and JSON data
        cursor.execute(insert_query, (current_time, json_data))

        # Commit the transaction
        connection.commit()

        print("Data inserted successfully into PostgreSQL")

    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data into PostgreSQL:", error)

    finally:
        # Close database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# function on rs485
def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    #TODO: Update the cmd to control 2 devices
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setRelay1":
            temp_data['relay1'] = jsonobj['params']
            # client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            if temp_data['relay1']:
                setDevice1(True) 
            else:
                setDevice1(False) 
        if jsonobj['method'] == "setRelay2":
            temp_data['relay2'] = jsonobj['params']
            # client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
            # if temp_data['valueFAN']:
                # setDevice2(True) 
            # else:
                # setDevice2(False) 
    except:
        pass

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_ACCESS_TOKEN)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

portName = getPort()
print(portName)



try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

relay1_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
relay1_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setDevice1(state):
    if state == True:
        ser.write(relay1_ON)
    else:
        ser.write(relay1_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

def get_current_temperatureHCM(url):
    # Send a GET request to the URL
    response = requests.get(url)
    print("response: ", response)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    print("soup:", soup)
    

    # Find the element with class 'display-temp' and get its text
    temp_element = soup.find('div', class_='h2')
    print("temp_element:", temp_element)
    temperature_string = temp_element.text.strip()
    return temperature_string

# temp = 10
# mois = 10
while True:
    print("TEST SENSOR")
    # mqttClient.publish(MQTT_TOPIC_PUB_TEMP,readTemperature())
    time.sleep(30)
    
    temp = readTemperature()
    mois = readMoisture()
    collect_data = {'temperature': temp, 'humidity': mois}
    data_to_publish = json.dumps(collect_data)
    print("Data to publish:        ", data_to_publish)
    mqttClient.publish(MQTT_TOPIC_PUB, data_to_publish)

    # Insert the JSON data into PostgreSQL database with current timestamp
    insert_data_into_postgres(data_to_publish, host, database, user, password, port, table_name)

    # Get TempHCM
    temperatureHCM = get_current_temperatureHCM(url)
    print("HCM Temperature:", temperatureHCM)
    
