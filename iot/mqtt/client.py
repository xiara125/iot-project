import paho.mqtt.client as mqtt
from mqtt import topicHandler
from . import devices,earthshake
from gpiozero import MotionSensor, LED, Button
def on_connect(client, userdata, flags,rc):
    print("Connected with result code " + str(rc))
    if rc==0:
        # client.subscribe("iot/+/control/#")
        client.subscribe("iot/#")
    else:
        print('연결실패 :',rc)

def on_message(client,userdata,msg):
    topic = '/'.join(msg.topic.split('/')[2:])  # control/<device>
    handler = topicHandler.get(topic)
    # print(topic)
    if handler:
        value = msg.payload.decode()
        handler(msg.topic, value)
    else:
        print('unknon topic',msg.topic)


mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
try :
    mqttClient.connect("192.168.35.129")
    mqttClient.loop_start()     # 새로운 스레드로 이벤트 루프 실행, forever하면 웹서버 종료
except Exception as err:
    print('에러: %s'%err)    


