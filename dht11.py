
import sys
import Adafruit_DHT


top_pin = 17
bottom_pin = 27


top_humidity, top_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, top_pin)
bottom_humidity, bottom_temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bottom_pin)


if top_humidity is not None and top_temperature is not None:
    print('Top temp={0:0.1f}*  Top humidity={1:0.1f}%'.format(top_temperature, top_humidity))
    print('Bottom temp={0:0.1f}*  Bottom humidity={1:0.1f}%'.format(bottom_temperature, bottom_humidity))

else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
