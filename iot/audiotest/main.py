from gpiozero import MotionSensor, LED, Button
from signal import pause
import requests
import json
import sounddevice as sd
import soundfile as sf
from .cmd import Cmd
import io

button = Button(26)
btn = Button(6)
cmd = Cmd()

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

print('테스트')

button.when_pressed = record
button.when_released = end_record
btn.when_pressed = start