# Requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *

# DHT11 libraries
import sys
import Adafruit_DHT

# Relay imports
from RPi import GPIO

# Initializing the lcd
mylcd = RPi_I2C_driver.lcd()


# DTH pins
top_pin = 17
bottom_pin = 27
outside_pin = 22

# Getting the temperature and humidity for both DHTs
top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)
outside_humidity, outside_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, outside_pin)

# Defining relay constants
ON = GPIO.LOW
OFF = GPIO.HIGH

# Defining relay pins
GPIO.setmode(GPIO.BCM)

top_fan = 18
GPIO.setup(top_fan, GPIO.OUT)


GPIO.cleanup()




# Main loop of the code
while True:


	# Getting the temperature and humidity for both DHTs
	top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
	bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)
	outside_humidity, outside_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, outside_pin)

	# Top sensor readings
	mylcd.lcd_display_string("T-Hum:" + str(top_humidity) + "%", 1)
	mylcd.lcd_display_string("T-Temp:" + str(top_temperature) + "C", 2)
	# Wait for some time
	sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for 1 second

	# Bottom sensor readings
	mylcd.lcd_display_string("B-Hum:" + str(bottom_humidity) + "%", 1)
	mylcd.lcd_display_string("B-Temp:" + str(bottom_temperature) + "C", 2)

	sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for 1 second

	# Outside sensor readings
	mylcd.lcd_display_string("O-Hum:" + str(outside_humidity) + "%", 1)
	mylcd.lcd_display_string("O-Temp:" + str(outside_temperature) + "C", 2)

	sleep(7) # Wait for 5 seconds

	mylcd.lcd_clear() # Clear screen
	sleep(1) # Wait for1 second




mylcd.backlight(0)
