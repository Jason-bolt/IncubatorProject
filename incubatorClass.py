""""

This python file is the software backend for controlling an automated incubator

The University of Cape Coast
Copyright (c) 2022 Jason Appiatu, All rights reserved


Author: Jason Kwame Appiatu
Date: 18th July, 2022

"""

# Libraries
from machine import Pin, PWM, I2C
import time
from sht30_library import SHT3X





class Incubator:
    
    # Constants to be used in the class
    UP_BULB = "up"
    DOWN_BULB = "down"
    
    
    
    def __init__(self, light_up_pin, light_down_pin):
        self.light_up = Pin(light_up_pin, Pin.OUT)
        self.light_down = Pin(light_down_pin, Pin.OUT)
        
    # Get state of light switches
    def bulbState(self, bulbSelect):
        if bulbSelect == self.UP_BULB:
            return "ON" if self.light_up.value() == 1 else "OFF"
        elif bulbSelect == self.DOWN_BULB:
            return "ON" if self.light_down.value() == 1 else "OFF"
        else:
            return -1 # If bublState is invalid
        
        
    # Turn on a light bulb. "bulbSelect" determines which bulb to switch
    # When "onOff" is True, switch on selected light bulb, else switch it off 
    def switchLight(self, bulbSelect, onOff):
        if bulbSelect == self.UP_BULB: # Upper light bulb selected
            self.light_up.value(1) if onOff == True else self.light_up.value(0)
            print("Turning on the top bulb")
        elif bulbSelect == self.DOWN_BULB: # Upper light bulb selected
            self.light_down.value(1) if onOff == True else self.light_down.value(0)
            print("Turning on the bottom bulb")
            
    # Function to control to servo motor, this is to control the tiny vent
    
    
    # Function to return the temperature and humidity
    def _readTempAndHumid(self):
        sensor = SHT3X()
        temp, humid = sensor.getTempAndHumi()
        return temp, humid
    
    # Function to display temperature and humidity
    def getTempAndHumidity(self):
        temp, humid = self._readTempAndHumid()
        print("Temporature:", temp, 'ºC, RH:', humid, '%')
    
    
    

