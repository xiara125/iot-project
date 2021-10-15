from gpiozero.output_devices import Servo
from mqtt import add_topic_handler
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from .car import Car
from audiotest.main import start,mqttSTT
from audiotest.kakaoSound import play_elevator
import threading

import paho.mqtt.client as mqtt
interphone = mqtt.Client()


factory = PiGPIOFactory(host='192.168.35.71') # 지터링 방지

servo = AngularServo(16,pin_factory=factory,
    min_angle=-90, max_angle=90,
    min_pulse_width=0.00045, max_pulse_width=0.0023)

def move_angle(topic, value):
    # print(topic,value)
    angle = int(value)
    servo.angle= -angle

add_topic_handler('control/camera',move_angle)


car = Car()

def move_car(topic, value):
    print(topic, value)
    car.move(value)

add_topic_handler('control/car',move_car)


def call_interphone(topic, value):
    print(topic,value)
    if value == '1':
        start()
        interphone.connect("192.168.35.129")
        interphone.publish("iot/hong/interphone",'0')

add_topic_handler('interphone',call_interphone)


def call_elevator(topic, value):
    if value == '1':
        play_elevator()

add_topic_handler('arrive/elevator',call_elevator)


def call_STT(topic, value):
    if value == 'call':
        my_thread = threading.Thread(target=mqttSTT)
        my_thread.start()
        

add_topic_handler('STT',call_STT)
