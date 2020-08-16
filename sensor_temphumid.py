import Adafruit_DHT
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


def get_sensor_value():
    sensor = Adafruit_DHT.DHT11

    # GPIO23 (pin no: #16)
    pin = 23

    GPIO.setup(24, GPIO.OUT)
    GPIO.output(24, True)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    GPIO.output(24, False)

    if humidity is not None and temperature is not None:
#        print ("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
        return temperature, humidity
    else:
        print ("Failed to get reading.")
        return None, None


'''
def get_sensor_value():
    return 10.0, 30.0


'''

