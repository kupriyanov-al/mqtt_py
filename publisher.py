

import random
import json
import time, datetime
from paho.mqtt import client as mqtt_client


broker = 'test.mosquitto.org'
port = 1883
topic = "topic_name"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_publish(client, userdata, mid):
         print("on pub")
  

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker, port)
    return client


def publish(client):
    
    temp = random.randint(20, 30)
    
    while True:
        time.sleep(10)
      
        msg = {"datastamp": datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S'),  "temperatura":temp,  "vent": "On"}

        
        msg = json.dumps(msg)
        # print("")
        result = client.publish(topic, msg, )

        print(
            f"Статус отправки сообщения rc: {result.rc} is_published: {result.is_published()}")
        
        if result.is_published():
            print("publish!!!!!")
        
        status = result[0]
        if status == 0:
            print(f"Отправлено сообщение `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
     
def run():
    client = connect_mqtt()
    publish(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
    
