

import random
import json
import time
import datetime
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "topic_name"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'



def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.connected_flag = True
            
        else:
            print("Failed to connect, return code ", rc)
            client.recnnect()

def on_publish(client, userdata, mid):
        print(f"on pub {mid}" )

def on_disconnect(client, userdata, rc):
    client.connected_flag = False
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        client.reconnect()
    else :
        print ("Disconnected successfully")  
   


client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker, port)
client.loop_start()

temp = random.randint(20, 30)

while True:
    
    time.sleep(100)
    msg = {"datastamp": datetime.datetime.now().strftime(
            '%m.%d.%Y %H:%M:%S'),  "temperatura": temp,  "vent": "On"}

    msg = json.dumps(msg)
        # print("")
    result = client.publish(topic, msg, )

    status = result[0]
    if status == 0:
        print(f"Отправлено сообщение `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

        


    

def run():
   print('ddd') 
    
    


if __name__ == '__main__':
    run()
