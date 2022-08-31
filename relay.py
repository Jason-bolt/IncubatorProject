from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 23

ON = GPIO.LOW
OFF = GPIO.HIGH

GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, ON)
time.sleep(5)
GPIO.output(pin, OFF)
time.sleep(5)

GPIO.cleanup()

#GPIO.output(5, GPIO.LOW)
#time.sleep(2)
