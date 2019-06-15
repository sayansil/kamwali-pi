import time
import paho.mqtt.client as mqtt
import config
import uniqid

def on_message(client, userdata, message):
    topic       = message.topic[65:]
    payload     = message.payload.decode('utf-8')
    room        = topic[0:topic.find('/')]
    appliance   = topic[topic.find('/') + 1:]
    sender      = payload[0:payload.find('-')]
    action      = payload[payload.find('-') + 1:]

    with open("trusted") as f:
        trusted_ids = f.readlines()
    trusted_ids = [id.strip() for id in trusted_ids]

    if sender in trusted_ids:
        print("Room: " + room)
        print("Appliance: " + appliance)
        print("Action: " + action)
    else:
        print("Unidentified Sender: " + sender)


def on_log(mosq, obj, level, string):
    print(string)



def init():
    global client
    
    broker = config.broker
    uid = uniqid.uid

    client_id = "subscriber-" + uid

    topics = list()
    for room, appliances in config.appliances.items():
        for appliance in appliances:
            topics.append(
                config.base_topic + "/" +
                room + "/" +
                appliance
            )
    client = mqtt.Client(
        client_id=client_id,
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport="tcp"
    )
    client.on_message = on_message
    # client.on_log = on_log

    print("Connecting to broker... " + broker)
    client.connect(
        broker,
        port=1883,
        keepalive=60,
        bind_address=""
    )

    for topic in topics:
        client.subscribe(topic)
    print("Subscribed.")

def start_listening():
    print("Listening...")
    try:
        client.loop_start()
        while True:
            pass
    except KeyboardInterrupt:
        stop_listening()
       
def stop_listening():
    client.loop_stop()
    client.disconnect()
    print("Stopped Listening")
   
init() 
start_listening()

