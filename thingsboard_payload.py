import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "demo.thingsboard.io"
MQTT_PORT = 1883
MQTT_ACCESS_TOKEN = "MNUrel9MvIV2iXce3LA1"
MQTT_TOPIC_SUB = "v1/devices/me/rpc/request/+"

def on_connect(client, userdata, flags, rc):
    print("Connected successfully!!")
    client.subscribe(MQTT_TOPIC_SUB)

def on_message(client, userdata, msg):
    print("Received message:", msg.payload.decode())

client = mqtt.Client()
client.username_pw_set(MQTT_ACCESS_TOKEN)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()
