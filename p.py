import paho.mqtt.client as mqtt
import time

client = mqtt.Client('module_test_4')
client.connect('test.mosquitto.org', 1883, 10)

client.loop_start()


for i in range(50):
   print('dddddd') 
   client.publish('topic_2', "valeur %d" % i, qos=2)
   time.sleep(1)

client.loop_stop()
client.disconnect()