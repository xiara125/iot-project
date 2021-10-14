import RPi.GPIO as GPIO
import spidev, time

# CDS_PIN = 18
LED_PIN = 19

GPIO.setmode(GPIO.BCM)
# GPIO.setup(CDS_PIN, GPIO.IN, pull_up_down  = GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1350000
# SPI 통신
def analog_read(channer):
    # if channer < 0 or channer >7:
    #     return -1
        
    r = spi.xfer2([1, (8+channer) << 4, 0])
    adc_out = ((r[1]&3)<<8)+r[2]
    return adc_out

while True:
    reading = analog_read(0)
    voltage = reading * 3.3/1024
    print("Reading=%d\tVotage=%f"%(reading, voltage))
    time.sleep(1)

    if reading < 100:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED ON")
        print("===============================")

    else :
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED OFF")
        print("===============================")


