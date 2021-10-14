import RPi.GPIO as GPIO
import spidev, time

BUZZER = 18
LED_PIN = 19
SW420 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SW420, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000
time.sleep(1)

pwm = GPIO.PWM(BUZZER, 1.0)
pwm.start(50.0)

try:
    while True:
        result = GPIO.input(SW420)
        if result == 1:
            print("진동 감지")
            GPIO.output(LED_PIN, GPIO.HIGH)
            for count in range(0,3):
                pwm.ChangeFrequency(349)
                time.sleep(0.5)
                pwm.ChangeFrequency(262)
                time.sleep(0.5)
            time.sleep(0.05)
            pwm.ChangeDutyCycle(0,0)
            pwm.stop()
        else:
            print("진동 미감지")
            time.sleep(0.05)

except KeyboardInterrupt:
    print("키보드로 종료")
finally:
    GPIO.cleanup()
    print("프로그램 끝")