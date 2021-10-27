from gpiozero import MotionSensor, LED, Button
from signal import pause
import requests
import json
import sounddevice as sd
import soundfile as sf
from .cmd import Cmd
import io
from time import sleep
import threading

cmd = Cmd()
button = Button(26)
btn = Button(6)
door_btn = Button(18)

door_state = False
duration = 5


kakao_speech_url= "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = "c7ad259e95ebd7a313853e56601b000c"

headers = {
    "content-Type" : "application/octet-stream",
    "X-DSS-Service" : "DICTATION",
    "Authorization" : "KakaoAK " + rest_api_key,
}


def recognize(audio):
    res = requests.post(kakao_speech_url, headers=headers,data=audio)
    try:    # 인식 성공
        result_json_string = res.text[
            res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1
        ]
        result = json.loads(result_json_string)
        value = result['value']
    except: # 인식 실패
        value = None
    print('인식 결과 :',value)
    cmd.ctr(value)
    return


def record(seconds=10, fs=16000, channels=1):
    print('음성인식 시작')
    global data
    data = sd.rec(int(seconds*fs), samplerate=fs, channels=channels)


def end_record():
    sd.stop()
    audio = io.BytesIO()
    sf.write(audio,data,16000,format="wav")
    audio.seek(0)
    recognize(audio)


def callback(indata,outdata,frames,time,status):
    # if status:
    #     print(status)
    outdata[:] = indata

def start():
    with sd.Stream(channels=1, callback=callback):  # 녹음데이터가 생길때마다 호출할 callback   
        print('인터폰 시작')
        # while state:
        # sd.sleep(int(duration*1000))
        sd.sleep(1000)
        for i in range(5,0,-1):
            print(i)
            sd.sleep(1000)
        print('인터폰 끝')

def mqttSTT(seconds=5, fs=16000, channels=1):
    print('음성인식 시작')
    data = sd.rec(int(seconds*fs), samplerate=fs, channels=channels)
    sd.wait()
    audio = io.BytesIO()
    sf.write(audio,data,16000,format="wav")
    audio.seek(0)
    recognize(audio)


def door():
    global door_state
    if door_state:
        cmd.open_door()
        door_state = False
    else:
        cmd.close_door()
        door_state = True


button.when_pressed = record
button.when_released = end_record
btn.when_pressed = start
door_btn.when_pressed = door





# def test():
#     while True:
#         print('쓰레드 함수1')
#         sleep(1)

# def test2():
#     while True:
#         print('쓰레드 함수2')
#         sleep(1)

# def test3():
#     while True:
#         print('쓰레드 함수3')
#         sleep(1)

# my_thread = threading.Thread(target=test)
# my_thread.start()

# my_thread2 = threading.Thread(target=test2)
# my_thread2.start()

# my_thread3 = threading.Thread(target=test3)
# my_thread3.start()


# import RPi.GPIO as GPIO
# import spidev, time

# BUZZER = 18
# LED_PIN = 19
# SW420 = 23

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.setup(BUZZER, GPIO.OUT)
# GPIO.setup(SW420, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setwarnings(False)
# spi = spidev.SpiDev()
# spi.open(0,0)
# spi.max_speed_hz = 1350000
# time.sleep(1)

# pwm = GPIO.PWM(BUZZER, 1.0)
# pwm.start(50.0)
# def sw420():
#     try:
#         while True:
#             result = GPIO.input(SW420)
#             if result == 1:
#                 print("진동 감지")
#                 GPIO.output(LED_PIN, GPIO.HIGH)
#                 for count in range(0,3):
#                     pwm.ChangeFrequency(349)
#                     time.sleep(0.5)
#                     pwm.ChangeFrequency(262)
#                     time.sleep(0.5)
#                 time.sleep(0.05)
#                 pwm.ChangeDutyCycle(0,0)
#                 pwm.stop()
#             else:
#                 print("진동 미감지")
#                 time.sleep(0.05)

#     except KeyboardInterrupt:
#         print("키보드로 종료")
#     finally:
#         GPIO.cleanup()
#         print("프로그램 끝")

# my_thread4 = threading.Thread(target=sw420)
# my_thread4.start()