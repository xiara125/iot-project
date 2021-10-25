import cv2
import numpy as np
from os import makedirs
from os.path import isdir
from mysite.picam import face_image

face_state = 1


#얼굴 저장 함수
face_dirs = '/home/pi/workspace/iotWallpad/face/faces/'

face_classifier = cv2.CascadeClassifier('/home/pi/workspace/iotWallpad/face/haarcascade_frontalface_default.xml')

#얼굴 검출 함수
def face_extractor(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    #얼굴이 없으면 패스
    if faces is():
        return None
    #얼굴이 있으면 얼굴 부위만 이미지로 만들고
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    #리턴
    return cropped_face

# 얼굴만 저장하는 함수
def take_pictures(name):
    #해당 이름의 폴더가 없다면 생성
    if not isdir(face_dirs+name):
        makedirs(face_dirs+name)

    #카메라 on
    # cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://192.168.35.71:8000/mjpeg/stream/')
    count = 0
    global face_state
    

    while True:
        #카메라로 부터 사진 한장 읽어오기
        # ret, frame = cap.read()
        #사진에서 얼굴 검출, 얼굴이 검출되었다면

        face_img = face_extractor(face_image)

        if face_img is not None:
            count+=1
            #200x200 사이즈를 줄이거나 늘린다
            face = cv2.resize(face_img,(200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            #200X200 흑백 사진을 FACE/얼굴이름/USERXX.JPG로 저장
            file_name_path = face_dirs + name + '/user'+str(count)+'.jpg'            
            cv2.imwrite(file_name_path,face)

            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Cropper', face)
        else:
            print("Face not Found")
            # pass

        #얼굴 사진 100장을 다 얻엇거나 엔터키 누르면 종료
        if cv2.waitKey(1)==13 or count==100:
            # models = trains()
            face_state = 10
            break
    # print(face_state)
    # face_state = 1
    # cap.release()
    cv2.destroyAllWindows()
    print('Collecting Sample Complete')


def change_face_state():
    global face_state
    face_state = 1



# if __name__ == "__main__":
#     # 사진 저장할 이름을 넣어서 함수 호출
#     take_pictures('LeeDongHae')

def startFaceCap(name):
    take_pictures(name)
    

