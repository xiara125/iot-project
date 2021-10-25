import io
import time
import numpy as np
from picamera import PiCamera, frames
import cv2

face_image = np.empty((640*480*3), dtype=np.uint8)
face_image = face_image.reshape((480,640,3))

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
        # face_image = np.empty((640*480*3), dtype=np.uint8)
        # print('이미지',face_image)
        # print(face_image.shape)
        
        while True:
            self.camera.capture(frame, format="jpeg",use_video_port=True)
            # self.camera.capture(frame, format="bgr",use_video_port=True)
            # print(frame)
            
            self.camera.capture(face_image, format="bgr",use_video_port=True)
            
            # print('face_image',face_image)
            # face_image = face_image.reshape((480,640,3))
            image = frame.getvalue()

            # face_image = face_image.reshape((480,640,3))
            # print('얼굴이미지 배열',face_image)
            # cv2.imshow('frame',face_image)
            # if cv2.waitKey(1)==13:
            #     break

            # generator 생성
            yield(b'--myboundary\n' # 경계선
                    b'Content-Type:image/jpeg\n'
                    # f"{len(image)}" : 문자열, .encode() : 문자열 -> byte배열
                    b'Content-Length: '+ f"{len(image)}".encode() + b'\n'
                    b'\n'+image + b'\n')    #'\n' : 헤더 바디 구분 빈 줄
            frame.seek(0)
            frame.truncate()    # 현재위치 뒤 부분을 제거