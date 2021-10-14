import RPi.GPIO as GPIO
import time
from gpiozero import LED

LED_PIN1 = LED(19)
LED_PIN2 = LED(20)
LED_PIN3 = LED(21)

LED_PIN2.on()
GPIO.output(LED_PIN2, True)


try:
    while True:
        
        if LED_PIN1 == True or LED_PIN2 == True or LED_PIN3 == True:
            time.sleep(10)
            GPIO.output(LED_PIN1, False)
            GPIO.output(LED_PIN2, False)
            GPIO.output(LED_PIN3, False)
            print("소등완료")
        else:
            print("이미 LED 모두 소등")
            time.sleep(1)

except KeyboardInterrupt:
    print("키보드로 종료")
    
finally:
    GPIO.cleanup()
    print("프로그램 끝")
