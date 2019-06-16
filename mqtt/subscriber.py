import time
import config
import uniqid
import paho.mqtt.client as paho

class subscriber:
    
    def __init__(self):
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
        self.client = paho.Client(
            client_id=client_id,
            clean_session=True,
            userdata=None,
            protocol=paho.MQTTv311,
            transport="tcp"
        )
        self.client.on_message = on_message
        # client.on_log = on_log

        print("Connecting to broker... " + broker)
        self.client.connect(
            broker,
            port=1883,
            keepalive=60,
            bind_address=""
        )

        for topic in topics:
            self.client.subscribe(topic)
        print("Subscribed.")

    def start_listening(self):
        self.client.loop_start()
        print("Listening...")
           
    def stop_listening(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Stopped Listening")

new_sub = subscriber()
new_sub.start_listening()

while True:
    try:
        while True:
            pass
    except KeyboardInterrupt:
        new_sub.stop_listening()
        print("Exiting")
        break
    except Exception:
        new_sub.stop_listening()
        del(new_sub)
        time.sleep(10)
        new_sub = subscriber()
        new_sub.start_listening()
    
