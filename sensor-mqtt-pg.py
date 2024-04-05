pip install psycopg2
import psycopg2
from datetime import datetime
import paho.mqtt.client as mqtt

# PostgreSQL connection details
hostname = "bqnbcj8kxuogsigyhnzy-postgresql.services.clever-cloud.com"
database = "bqnbcj8kxuogsigyhnzy"
username = "ufjklpchveyybgraqhxu"
password = "AyR5dzFuySPaAcWd5po1AJMK063nkG"
port = "50013"

# Connect to PostgreSQL database
connection = psycopg2.connect(
    host=hostname,
    database=database,
    user=username,
    password=password,
    port=port
)
cursor = connection.cursor()
print("Connected to PostgreSQL database!")

# MQTT Broker configuration
MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "testing12345"
MQTT_PASSWORD = ""
MQTT_TOPIC_TEMP = MQTT_USERNAME + "/feeds/V1/temp"
MQTT_TOPIC_MOIS = MQTT_USERNAME + "/feeds/V1/mois"

# Function to handle MQTT connection
def mqtt_connected(client, userdata, flags, rc):
    print("Connected successfully!!")
    # Subscribe to the specified topics for temperature and moisture
    client.subscribe(MQTT_TOPIC_TEMP)
    client.subscribe(MQTT_TOPIC_MOIS)

# Function to handle incoming MQTT messages
def mqtt_recv_message(client, userdata, message):
    print("Received message on topic:", message.topic)
    print("Payload:", message.payload.decode("utf-8"))
    # Insert received data into PostgreSQL database along with current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if message.topic == MQTT_TOPIC_TEMP:
        insert_temperature_data(message.payload.decode("utf-8"), timestamp)
    elif message.topic == MQTT_TOPIC_MOIS:
        insert_moisture_data(message.payload.decode("utf-8"), timestamp)

# Function to insert temperature data into PostgreSQL database
def insert_temperature_data(data, timestamp):
    try:
        cursor.execute("INSERT INTO temperature (value, timestamp) VALUES (%s, %s)", (data, timestamp))
        connection.commit()
        print("Temperature data inserted into PostgreSQL database successfully!")
    except psycopg2.Error as e:
        print("Error inserting temperature data into PostgreSQL database:", e)

# Function to insert moisture data into PostgreSQL database
def insert_moisture_data(data, timestamp):
    try:
        cursor.execute("INSERT INTO moisture (value, timestamp) VALUES (%s, %s)", (data, timestamp))
        connection.commit()
        print("Moisture data inserted into PostgreSQL database successfully!")
    except psycopg2.Error as e:
        print("Error inserting moisture data into PostgreSQL database:", e)

# Create an MQTT client instance
mqttClient = mqtt.Client()
# Set username and password for authentication
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
# Register MQTT event handlers
mqttClient.on_connect = mqtt_connected
mqttClient.on_message = mqtt_recv_message
# Connect to the MQTT broker
mqttClient.connect(MQTT_SERVER, MQTT_PORT, 60)

# Start the MQTT client's network loop
mqttClient.loop_forever()
