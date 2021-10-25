from re import S
from gpiozero import AngularServo, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from . import kakaoSound as ks
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
        self.k_led = LED(17)
        self.l_led = LED(27)
        self.b_led = LED(13)
        

    def open_door(self):
        self.servo.angle = 45
    
    def close_door(self):
        self.servo.angle = -45

    def led_on(self,place):
        if place == 'k':
            self.k_led.on()
        elif place == 'l':
            self.l_led.on()
        elif place == 'b':
            self.b_led.on()

    def led_off(self,place):
        if place == 'k':
            self.k_led.off()
        elif place == 'l':
            self.l_led.off()
        elif place == 'b':
            self.b_led.off()
        elif place == 'a':
            self.k_led.off()
            self.l_led.off()
            self.b_led.off()

    def led_state(self):
        print(self.k_led.value)
        print(self.l_led.value)
        print(self.b_led.value)
        client.connect("192.168.35.129")
        client.publish("iot/led/kitchen",self.k_led.value)
        client.publish("iot/led/livingRoom",self.l_led.value)
        client.publish("iot/led/bedRoom",self.b_led.value)

    def weather(self):
        ks.play_weather()

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
            ks.play_default()
            
