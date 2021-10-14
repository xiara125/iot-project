from logging import exception
import sounddevice as sd
from gpiozero import Button
from signal import pause

button = Button(26)

duration = 5
state = True

def stop():
    global state
    state = False

def callback(indata,outdata,frames,time,status):
    # if status:
    #     print(status)
    outdata[:] = indata

def start():
    with sd.Stream(channels=1, callback=callback):  # 녹음데이터가 생길때마다 호출할 callback   
        print('녹음 시작')
        # while state:
        sd.sleep(int(duration*1000))
        print('녹음 끝')

# try:
#     with sd.Stream(channels=1, callback=callback):


    

button.when_pressed = start
# button.when_released = stop
pause()
print('test')