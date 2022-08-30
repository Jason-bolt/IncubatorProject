from RPi import GPIO
from time import sleep

clk = 23
dt = 24


GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0

previousValue = True

while True:
	if previousValue != GPIO.input(clk):
		if GPIO.input(clk) == False:
			if GPIO.input(dt) == False:
				counter += 1
				print (counter)
			else:
				counter -= 1
				if counter < 0:
					counter = 0
				print (counter)


	previousValue = GPIO.input(clk)

