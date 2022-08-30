# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

# DHT11 libraries
import sys
import Adafruit_DHT

# Rotary libraries
from RPi import GPIO


# DTH pins
top_pin = 17
bottom_pin = 27
outside_pin = 22


# Rotary pins
clk = 23
dt = 24


# Getting the temperature and humidity for both DHTs
top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)
outside_humidity, outside_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, outside_pin)


# Setting up rotary pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Rotary variables
counter = 0
previousValue = True


# Reading rotary data
clkState = GPIO.input(clk)
dtState = GPIO.input(dt)


# Initializing the lcd
mylcd = RPi_I2C_driver.lcd()




# Main loop of the code
while True:

	while True:	
		# Rotary section
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
		# stopping the loop
		count = 0
		if ((GPIO.input(clk), GPIO.input(dt)) == (1, 1)):
			for _ in range(5000):
				if clkState == 0:
					break
				else:
					count += 1
					sleep(0.1)
					continue
		if count == 5000:
			break




	sleep(2)

	# Top sensor readings
	mylcd.lcd_display_string("T-Hum:" + str(top_humidity) + "%", 1)
	mylcd.lcd_display_string("T-Temp:" + str(top_temperature) + "C", 2)

	for _ in range(7000):
		sleep (0.1) # Wait for 7 seconds
		if GPIO.input(clk):
			break
	#sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for1 second

	# Bottom sensor readings
	mylcd.lcd_display_string("B-Hum:" + str(bottom_humidity) + "%", 1)
	mylcd.lcd_display_string("B-Temp:" + str(bottom_temperature) + "C", 2)

	sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for1 second

	# Outside sensor readings
	mylcd.lcd_display_string("O-Hum:" + str(outside_humidity) + "%", 1)
	mylcd.lcd_display_string("O-Temp:" + str(outside_temperature) + "C", 2)

	sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for1 second





mylcd.backlight(0)
