import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
pin = 20

try:
    while True:
        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if h is not None and t is not None:
            print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
        else:
            print('Read error')
        time.sleep(1)

except KeyboardInterrupt:
    print("키보드로 종료")
finally:
    print("프로그램 끝")