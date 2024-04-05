print("Sensors and Actuators")

import time
import paho.mqtt.client as mqtt

# MQTT Broker configuration
MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "testing12345"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB_TEMP = MQTT_USERNAME + "/feeds/V1/temp/"
MQTT_TOPIC_PUB_MOIS = MQTT_USERNAME + "/feeds/V1/mois/"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V1/control"

# Function to handle MQTT connection
def mqtt_connected(client, userdata, flags, rc):
    print("Connected successfully!!")
    client.subscribe(MQTT_TOPIC_SUB)
    client.subscribe(MQTT_TOPIC_PUB_TEMP)  # Subscribe to temperature topic
    client.subscribe(MQTT_TOPIC_PUB_MOIS)  # Subscribe to moisture topic

# Function to handle incoming MQTT messages
def mqtt_recv_message(client, userdata, message):
    print("Received message on topic:", message.topic)
    print("Payload:", message.payload.decode("utf-8"))

# Create an MQTT client instance
mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, MQTT_PORT, 60)

# Register MQTT event handlers
mqttClient.on_connect = mqtt_connected
mqttClient.on_message = mqtt_recv_message

# Start the MQTT client's network loop
mqttClient.loop_forever()
