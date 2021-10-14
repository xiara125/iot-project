import RPi.GPIO as GPIO
import time
from gpiozero import LED

LED_PIN1 = LED(19)
LED_PIN2 = LED(20)
LED_PIN3 = LED(21)

LED_PIN2.on()
# GPIO.output(LED_PIN2, True)


try:
    while True:
        
        if LED_PIN1.value == 1 or LED_PIN2.value == 1 or LED_PIN3.value == 1:
            time.sleep(10)
            LED_PIN1.off()
            LED_PIN2.off()
            LED_PIN3.off()
            print("소등완료")
        else:
            print("이미 LED 모두 소등")
            time.sleep(1)

except KeyboardInterrupt:
    print("키보드로 종료")
    
finally:
    GPIO.cleanup()
    print("프로그램 끝")
