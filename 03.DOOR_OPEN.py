import time
import RPi.GPIO as GPIO
import time
SERVO_PIN = 26
BTN_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down  = GPIO.PUD_UP)
frequency=GPIO.PWM(SERVO_PIN, 50)
frequency.start(0)
try:
    a=True
    while True:
        button_state = GPIO.input(BTN_PIN)
        if button_state==False:
            a=False if a else True
            print ("출력")
        if a:
            frequency.ChangeDutyCycle(9.5)
            # print("180")
        else:
            frequency.ChangeDutyCycle(2.5)
            # print("0")
        time.sleep(0.15)
except KeyboardInterrupt:
    frequency.stop()
finally:
    GPIO.cleanup()

    