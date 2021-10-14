import io
import time
import numpy as np
from picamera import PiCamera, frames

class PiCam:
    def __init__(self, framerate=25, width=640, height=480):
        self.size = (width, height)
        self.framerate = framerate

        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = self.size
        self.camera.framerate = self.framerate

    # 사진 1장(jpeg) 리턴
    def snapshot(self):
        frame = io.BytesIO()
        self.camera.capture(frame,'jpeg',use_video_port=True)
        frame.seek(0)
        return frame.getvalue()     # frame.read()와 동일

class MJpegStreamCam(PiCam):
    def __init__(self, framerate=25, width=640, height=480):
        super().__init__(framerate=framerate, width=width, height=height)
    
    def __iter__(self):
        frame = io.BytesIO()
        while True:
            self.camera.capture(frame, format="jpeg",use_video_port=True)
            image = frame.getvalue()
            # generator 생성
            yield(b'--myboundary\n' # 경계선
                    b'Content-Type:image/jpeg\n'
                    # f"{len(image)}" : 문자열, .encode() : 문자열 -> byte배열
                    b'Content-Length: '+ f"{len(image)}".encode() + b'\n'
                    b'\n'+image + b'\n')    #'\n' : 헤더 바디 구분 빈 줄
            frame.seek(0)
            frame.truncate()    # 현재위치 뒤 부분을 제거