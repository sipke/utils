# Modified example from https://www.eclipse.org/paho/clients/python/
import time
import sys
import random
import string
import paho.mqtt.client as mqtt
from datetime import datetime

I_am_a_client = False 
I_am_a_server = False 
topic = "basic/test"
TOPICARG = "topic="
MQTTARG = "mqtt="

if len(sys.argv) > 1:
    for arg in sys.argv:
        if MQTTARG in arg:
            server = arg[len(MQTTARG):len(arg)]
        if arg == "server":
            I_am_a_server = True
        if arg == "client":
            I_am_a_client = True 
        if TOPICARG in arg:
            topic = arg[len(TOPICARG):len(arg)]
            print("Using topic: ", topic)



def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, user_data, flags, rc):
    print("Connected with result code ", str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    if rc == 0:
        client.connected = True


def on_disconnect(client, userdata, rc):
    print("on_disconnect, reason:", str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'), "on_message: ", msg.topic, " ", str(msg.payload))


def on_publish(client, user_data, mid):
    print("on_publish, ", "user data:", user_data, ", mid:", mid)


def subscribe_for_echo(topic):
    print("Subscribing to topic:", topic)
    client.subscribe(topic)

#mqtt ="test.mosquitto.org"
#mqtt="broker.hivemq.com"
if server is None:
    print("Please specify mqtt server address, e.g. mqtt=<myserver>")
    exit(1)

client = mqtt.Client(client_id=randomString(), clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set("anon", "")
client.connected = False
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Attempting to connect to server: ", server)
client.connect(server, 1883, 60)

"""
Start the client, and as the 'server' regularly post a topic, and if we are a client also we will receive it on
the subscribed topic, via on_message.
"""
count = 10
data = "Hello world"
client.loop_start()
while not client.connected and count > 0:
    count = count - 1
    time.sleep(1)
if client.connected:
    count = 20
    if I_am_a_client:
        subscribe_for_echo(topic)
    while client.connected:
        if I_am_a_server and count > 0:
            count = count - 1
            print("Publish: ", topic, ",", data)
            client.publish(topic, data, 2)
            time.sleep(1)
else:
    print("Could not connect")
client.loop_stop()
