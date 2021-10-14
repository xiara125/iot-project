from re import S
from gpiozero import AngularServo, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from . import weather_info as wi
import paho.mqtt.client as mqtt
from time import sleep

factory = PiGPIOFactory(host='192.168.35.71')
client = mqtt.Client()

dic = {
    '문 열어' : 'open_door',
    '문 닫어' : 'close_door',
    '전등 켜' : 'led_on',
    '불 켜' : 'led_on',
    '전등 꺼' : 'led_off',
    '불 꺼' : 'led_off',
    '날씨 알려줘' : 'weather',
    'timeout' : 'timeout',
    '엘리베이터' : 'elevator'
}

class Cmd:
    def __init__(self):
        self.servo = AngularServo(16,pin_factory=factory,
                    min_angle=-90, max_angle=90,
                    min_pulse_width=0.00045, max_pulse_width=0.0023)
        self.led = LED(19)
        

    def open_door(self):
        self.servo.angle = 90
    
    def close_door(self):
        self.servo.angle = 0

    def led_on(self):
        self.led.on()

    def led_off(self):
        self.led.off()

    def weather(self):
        wi.play_weather()

    def elevator(self):
        try:
            # 2. 브로커 연결
            client.connect("192.168.35.129")

            client.publish("iot/hong/control/elevator",'5')
            print('엘리베이터')
                
                
        except Exception as err:
            print("에러 : %s" %err)

    
    def ctr(self,value):
        if value in dic.keys():
            method_name = f'{dic[value]}'
            # print(method_name)
            method = getattr(self,method_name)
            method()
        else:
            wi.play_default()
            
