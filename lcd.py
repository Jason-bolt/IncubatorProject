# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

# DHT11 libraries
import sys
import Adafruit_DHT

# Rotary libraries
from RPi import GPIO

# Initializing the lcd
mylcd = RPi_I2C_driver.lcd()

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




# Main loop of the code
while True:
	print ("Begin")
	count = 0
	while True:
		# Rotary section
		if previousValue != GPIO.input(clk):
			count = 0
			if GPIO.input(clk) == False:
				if GPIO.input(dt) == False:
					counter += 1
					print (counter)
				else:
					counter -= 1
					if counter < 0:
						counter = 0
					print (counter)

		# stopping the loop

		else:
			count += 1
			print(count)
			sleep(0.5)
			if count == 50000:
				break

		previousValue = GPIO.input(clk)






	sleep(2)

	# Top sensor readings
	mylcd.lcd_display_string("T-Hum:" + str(top_humidity) + "%", 1)
	mylcd.lcd_display_string("T-Temp:" + str(top_temperature) + "C", 2)


	sleep(7) # Wait for 5 seconds

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
