

import random
import json
import time, datetime
from paho.mqtt import client as mqtt_client
import queue

q = queue.Queue()


broker = 'test.mosquitto.org'
port = 1883
topic = "topic_name"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    
    def on_connect(client, userdata, flags, rc):
        print(f"on_connect flags={flags} , rc={rc}")
        
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.connected_flag = True
        else:
            print("Failed to connect, return code ", rc)
            client.reconnect()

    def on_publish(client, userdata, mid):
        print(f"on_publish mid={mid}")
         
    def on_disconnect(client, userdata, rc):
        client.connected_flag = False
        if rc != 0:
            print("Unexpected disconnection. Reconnecting...")
            try:
                client.reconnect()
            except:
              print("Disconnected")
        else:
         print("Disconnected successfully")
        
            
  
    client = mqtt_client.Client(client_id, clean_session=False)

    client.connected_flag = True
    # client.reconnect_delay_set(min_delay=1, max_delay=120)
    # client.reconnect_max_delay_set(maximum_delay=300)
    
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.connect(broker, port)  # 
    
    return client



def publish(client):
    
    temp = random.randint(20, 30)
    
    while True:
        time.sleep(10)
        msg = {"datastamp": datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S'),  "temperatura":temp,  "vent": "On"}
        msg = json.dumps(msg)
        q.put(msg)
        
        
        print(f"connected_flag={client.connected_flag}")
       
        if client.connected_flag:
            while not q.empty():
                msg=q.get()
                result = client.publish(topic, msg, qos=1)
                status = result[0]
                if status == 0:
                    print(f"Отправлено сообщение `{msg}` to topic `{topic}`") 
                else:
                    print(f"Failed to send message to topic {topic}")
                time.sleep(0.5)
        else:
            try:
                client.reconnect()
            except:
                print("reconnect error...")
            
def run():
    client = connect_mqtt()
    try:
        client.loop_start()
        # client.loop_forever()
        publish(client)
    except:
        print("ОШИБКА loop_start")
    


if __name__ == '__main__':
    run()
    
