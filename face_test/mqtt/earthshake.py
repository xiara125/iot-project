import threading
from time import sleep
import RPi.GPIO as GPIO
from audiotest import kakaoSound as ks
import paho.mqtt.client as mqtt
import spidev

SW420 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(SW420, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

es = mqtt.Client()
# es.connect("192.168.35.129")
def earthshake():
    while True:
        pre_data = GPIO.input(SW420)
        sleep(0.2)
        now_data = GPIO.input(SW420)

        if pre_data == 0 and now_data == 1:
            print('지진 발생')
            es.connect("192.168.35.129")
            es.publish('iot/earthshake',1)
            ks.tts('지진 발생!!')

            

earthshake_thread = threading.Thread(target=earthshake)
earthshake_thread.start()

LED_PIN = 19
GPIO.setmode(GPIO.BCM)
# GPIO.setup(CDS_PIN, GPIO.IN, pull_up_down  = GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000


illu = mqtt.Client()

def analog_read(channer):
    # if channer < 0 or channer >7:
    #     return -1
        
    r = spi.xfer2([1, (8+channer) << 4, 0])
    adc_out = ((r[1]&3)<<8)+r[2]
    return adc_out

def light():
    while True:
        reading = analog_read(1)
        voltage = reading * 3.3/1024
        # print("Reading=%d\tVotage=%f"%(reading, voltage))
        
        illu.connect("192.168.35.129")
        illu.publish('iot/sensors/Room/illu',reading)
        if reading < 100:
            GPIO.output(LED_PIN, GPIO.HIGH)
            # print("LED ON")
            # print("===============================")

        else :
            GPIO.output(LED_PIN, GPIO.LOW)
            # print("LED OFF")
            # print("===============================")
        sleep(1)

def mqtt_illu():
    
    reading = analog_read(1)    
    illu.connect("192.168.35.129")
    illu.publish('iot/sensors/Room/illu',reading)
    
    

my_thread2 = threading.Thread(target=light)
my_thread2.start()

# mqtt_illu_thread = threading.Thread(target=mqtt_illu)
# mqtt_illu_thread.start()