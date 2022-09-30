# from gpiozero import Servo
from time import sleep
from RPi import GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

top_vent = GPIO.PWM(12, 50)
bottom_vent = GPIO.PWM(5, 50)

# servo = Servo(5)

try:
    while True:
        top_vent.start(4)
#         sleep(1)
#         bottom_vent.start(4)
        sleep(1)
        top_vent.ChangeDutyCycle(2.5)
        sleep(1)
#         bottom_vent.ChangeDutyCycle(2)
#         sleep(1)
#         top_vent.stop()
#         bottom_vent.stop()
except KeyboardInterrupt:
    print("Program stopped")
