from gpiozero import Servo
from time import sleep

servo = Servo(12)

try:
#     while True:
    servo.value = 1
    sleep(0.5)
    servo.value = None
    sleep(1)
    servo.value = -1
    sleep(0.5)
    servo.value = None
#         servo.mid()
#         sleep(0.5)
#         servo.max()
#         sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")
