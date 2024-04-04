import paho.mqtt.client as mqtt
import time
import keyboard
MQTT_SERVER = "mqtt.ohstem.vn"
MQTT_PORT = 1883
MQTT_USERNAME = "testing12345"
MQTT_PASSWORD = ""
MQTT_TOPIC_PUB = MQTT_USERNAME + "/control"
MQTT_TOPIC_SUB = MQTT_USERNAME + "/feeds/V1"
MQTT_TOPIC_SUB_TEMP = MQTT_USERNAME + "/temp"
MQTT_TOPIC_SUB_MOIS = MQTT_USERNAME + "/mois"


def mqtt_connected(client, userdata, flags, rc):
    print("Connected succesfully!!")
    client.subscribe(MQTT_TOPIC_SUB_TEMP)
    client.subscribe(MQTT_TOPIC_SUB_MOIS)
    client.subscribe(MQTT_TOPIC_SUB)
    client.subscribe(MQTT_TOPIC_PUB)

def mqtt_subscribed(client, userdata, mid, granted_qos):
    print("Subscribed to Topic!!!")

def mqtt_recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))

mqttClient = mqtt.Client()
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.connect(MQTT_SERVER, int(MQTT_PORT), 60)

#Register mqtt events
mqttClient.on_connect = mqtt_connected
mqttClient.on_subscribe = mqtt_subscribed
mqttClient.on_message = mqtt_recv_message

mqttClient.loop_start()


def setOn():
    mqttClient.publish(MQTT_TOPIC_PUB,1)
def setOff():
    mqttClient.publish(MQTT_TOPIC_PUB,0)


turnON = True
def toggle():
    global turnON
    if(turnON):
        setOn()
        turnON = False
    else:
        setOff()
        turnON = True
    print(turnON)

while True:
    # time.sleep(5)
    # counter += 1
    # mqttClient.publish(MQTT_TOPIC_SUB_TEMP, counter)
    # mqttClient.publish(MQTT_TOPIC_SUB_MOIS, 2)
    print("Press 'A' to trigger the callback function.")

    # Registering the callback function for the 'A' key
    keyboard.on_press_key('a', lambda _: toggle())
    keyboard.wait('esc')
