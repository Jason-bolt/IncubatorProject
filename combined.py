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
#top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
#bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)
#outside_humidity, outside_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, outside_pin)

# Defining relay constants
ON = GPIO.LOW
OFF = GPIO.HIGH

# Defining relay pins
GPIO.setmode(GPIO.BCM)

top_fan = 18
top_light = 23

GPIO.setup(top_fan, GPIO.OUT)
GPIO.setup(top_light, GPIO.OUT)

GPIO.output(top_light, OFF)
GPIO.output(top_fan, OFF)



# Read sensor values
def readData():
	# Getting the temperature and humidity for both DHTs
	top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
	bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)
	outside_humidity, outside_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, outside_pin)
	data = {
		"top_humidity" : top_humidity,
		"top_temperature" : top_temperature,
		"bottom_humidity" : bottom_humidity,
		"bottom_temperature" : bottom_temperature,
		"outside_humidity" : outside_humidity,
		"outside_temperature" : outside_temperature
		}
	return data


# Function to check temperature and humidity limits of the sensor
def checkLimit(temp, humid, position):
	if position == "top":
		if temp >= 39:
			print ("Turning off the top light...")
			GPIO.output(top_light, OFF)
			print ("Turning on top motor")
			GPIO.output(top_fan, ON)
		elif temp <= 27:
			print ("Turning on top light...")
			GPIO.output(top_light, ON) 
			print ("Turning off top motor...")
			GPIO.output(top_fan, OFF)
		else:
			GPIO.output(top_light, ON)
			GPIO.output(top_fan, OFF)
#	else:
#		if temp >= 39:
#			print ("Turning off the top light...")
#			GPIO.output(top_light, OFF)
#			print ("Turning on top motor")
#			GPIO.output(top_fan, ON)
#		elif temp <= 27:
#			print ("Turning on top light...")
#			GPIO.output(top_light, ON) 
#			print ("Turning off top motor...")
#			GPIO.output(top_fan, OFF)
#		else:
#			GPIO.output(top_light, ON)
#			GPIO.output(top_fan, OFF)







# Main loop of the code

try:
	
	while True:

		
		""" 
		  If temperature goes above 39 degrees, put off light and put on the fan. 
		  Open the vent
		  If temperature is getting below 27 degrees, put off fan and put on light. 
		  Close the vent 
		"""
		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")


		# Top sensor readings
		mylcd.lcd_display_string("T-Hum:" + str(data["top_humidity"]) + "%", 1)
		mylcd.lcd_display_string("T-Temp:" + str(data["top_temperature"]) + "C", 2)
		# Wait for some time
		sleep(7) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")
		#sleep(1) # Wait for 1 second

		# Bottom sensor readings
		mylcd.lcd_display_string("B-Hum:" + str(data["bottom_humidity"]) + "%", 1)
		mylcd.lcd_display_string("B-Temp:" + str(data["bottom_temperature"]) + "C", 2)

		sleep(7) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")
		#sleep(1) # Wait for 1 second

		# Outside sensor readings
		mylcd.lcd_display_string("O-Hum:" + str(data["outside_humidity"]) + "%", 1)
		mylcd.lcd_display_string("O-Temp:" + str(data["outside_temperature"]) + "C", 2)

		sleep(7) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		sleep(1) # Wait for1 second


except KeyboardInterrupt:
	mylcd.backlight(0)
	GPIO.cleanup()

