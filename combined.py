# Adafruit Libraries and constants
ADAFRUIT_IO_USERNAME = "Boltz"
ADAFRUIT_IO_KEY = "aio_FptZ83idYiNEfybcXPAtUzYQTpTD"

from Adafruit_IO import Client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


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

bottom_fan = 24
bottom_light = 25

GPIO.setup(top_fan, GPIO.OUT)
GPIO.setup(top_light, GPIO.OUT)

GPIO.setup(bottom_fan, GPIO.OUT)
GPIO.setup(bottom_light, GPIO.OUT)


GPIO.output(top_light, OFF)
GPIO.output(top_fan, OFF)

GPIO.output(bottom_light, OFF)
GPIO.output(bottom_fan, OFF)



# Feeds
topTempFeed = aio.feeds('incubator.top-temperature')
topHumFeed = aio.feeds('incubator.top-humidity')
bottomTempFeed = aio.feeds('incubator.bottom-temperature')
bottomHumFeed = aio.feeds('incubator.bottom-humidity')
outTempFeed = aio.feeds('incubator.outside-temperature')
outHumFeed = aio.feeds('incubator.outside-humidity')


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
		if temp >= 32: # 39
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
	else:
		if temp >= 32:
			print ("Turning off the bottom light...")
			GPIO.output(bottom_light, OFF)
			print ("Turning on top motor")
			GPIO.output(bottom_fan, ON)
		elif temp <= 27:
			print ("Turning on bottom light...")
			GPIO.output(bottom_light, ON) 
			print ("Turning off bottom motor...")
			GPIO.output(bottom_fan, OFF)
		else:
			GPIO.output(bottom_light, ON)
			GPIO.output(bottom_fan, OFF)







# Main loop of the code

try:
	data = readData()
	checkLimit(data["top_temperature"], data["top_humidity"], "top")
	checkLimit(data["bottom_temperature"], data["bottom_humidity"], "bottom")
	while True:

		
		""" 
		  If temperature goes above 39 degrees, put off light and put on the fan. 
		  Open the vent
		  If temperature is getting below 27 degrees, put off fan and put on light. 
		  Close the vent 
		"""
		#data = readData()
		#checkLimit(data["top_temperature"], data["top_humidity"], "top")


		# Top sensor readings
		mylcd.lcd_display_string("T-Hum:" + str(data["top_humidity"]) + "%", 1)
		mylcd.lcd_display_string("T-Temp:" + str(data["top_temperature"]) + "C", 2)
		
		# Sending the data to Adafruit.io
		aio.send_data(topTempFeed.key, str(data["top_temperature"]))
		aio.send_data(topHumFeed.key, str(data["top_humidity"]))
		aio.send_data(bottomTempFeed.key, str(data["bottom_temperature"]))
		aio.send_data(bottomHumFeed.key, str(data["bottom_humidity"]))
		aio.send_data(outTempFeed.key, str(data["outside_temperature"]))
		aio.send_data(outHumFeed.key, str(data["outside_humidity"]))
		
		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")
		checkLimit(data["bottom_temperature"], data["bottom_humidity"], "bottom")
		# Wait for some time
		sleep(3) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		sleep(1) # Wait for 1 second

		# Bottom sensor readings
		mylcd.lcd_display_string("B-Hum:" + str(data["bottom_humidity"]) + "%", 1)
		mylcd.lcd_display_string("B-Temp:" + str(data["bottom_temperature"]) + "C", 2)

		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")
		checkLimit(data["bottom_temperature"], data["bottom_humidity"], "bottom")
		sleep(3) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		sleep(1) # Wait for 1 second

		# Outside sensor readings
		mylcd.lcd_display_string("O-Hum:" + str(data["outside_humidity"]) + "%", 1)
		mylcd.lcd_display_string("O-Temp:" + str(data["outside_temperature"]) + "C", 2)

		data = readData()
		checkLimit(data["top_temperature"], data["top_humidity"], "top")
		checkLimit(data["bottom_temperature"], data["bottom_humidity"], "bottom")
		sleep(3) # Wait for 7 seconds

		mylcd.lcd_clear() # Clear screen
		sleep(1) # Wait for 1 second


except KeyboardInterrupt:
	mylcd.backlight(0)
	GPIO.cleanup()

