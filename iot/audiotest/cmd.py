from re import S
from gpiozero import AngularServo, LED
from gpiozero.pins.pigpio import PiGPIOFactory
from . import kakaoSound as ks
import paho.mqtt.client as mqtt
from time import sleep

factory = PiGPIOFactory(host='192.168.35.71')
client = mqtt.Client()

dic = {
    'led_on' : ['주방 불 켜','주방 전등 켜','거실 불 켜','거실 전등 켜','침실 불 켜','침실 전등 켜','전체 불 켜','전체 전등 켜'],
    'led_off' : ['주방 불 꺼','주방 전등 꺼','거실 불 꺼','거실 전등 꺼','침실 불 꺼','침실 전등 꺼','전체 불 꺼','전체 전등 꺼'],
    'open_door' : '문 열어',
    'close_door' : ['문 닫어','문 닫아'],
    'weather' : '날씨 알려줘',
    'elevator' : '엘리베이터 불러줘',
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
        self.servo.angle = 60
    
    def close_door(self):
        self.servo.angle = 0

    def led_on(self,place):
        if place == 'k':
            self.k_led.on()
        elif place == 'l':
            self.l_led.on()
        elif place == 'b':
            self.b_led.on()
        elif place == 'a':
            self.k_led.on()
            self.l_led.on()
            self.b_led.on()
        self.led_state()

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
        self.led_state()

    def led_state(self):
        client.connect("192.168.35.129")
        client.publish("iot/led/kitchen",self.k_led.value)
        client.publish("iot/led/livingRoom",self.l_led.value)
        client.publish("iot/led/bedRoom",self.b_led.value)

    def weather(self):
        ks.play_weather()

    def elevator(self):
        try:
            client.connect("192.168.35.129")

            client.publish("iot/hong/control/elevator",'5')
            print('엘리베이터')
                
                
        except Exception as err:
            print("에러 : %s" %err)

    
    def ctr(self,value):
        print('value :',value)
        if value == None:
            ks.play_default()
            return
        for key, v in dic.items():
            if value in v:
                method_name = str(key)
                method = getattr(self,method_name)
                if '전체' in value:
                    place = 'a'
                    method(place)
                elif '주방' in value:
                    place = 'k'
                    method(place)
                elif '거실' in value:
                    place = 'l'
                    method(place)
                elif '침실' in value:
                    place = 'b'
                    method(place)
                else:
                    method()
                return
        ks.play_default()
        return
            
