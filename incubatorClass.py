"""

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
from d1motor import Motor
from rotary_irq_esp import RotaryIRQ





class Incubator:
    
    # CONSTANTS TO BE USED IN THE INCUBATOR CLASS
    # Bulb position
    UP_BULB = "up"
    DOWN_BULB = "down"
    
    # Light switch
    ON = True
    OFF = False
    
    # Rotary values
    MIN_ROTARY_VALUE = 180
    MAX_ROTARY_VALUE = 10000
    
    
#     clk_pin = 26
# dt_pin = 21
    
    # Initiating the class
    def __init__(self, light_up_pin, light_down_pin, rotary_clk_pin=None, rotary_dt_pin=None):
        self.light_up = Pin(light_up_pin, Pin.OUT)
        self.light_down = Pin(light_down_pin, Pin.OUT)
        self.rotary = RotaryIRQ(pin_num_clk=26, pin_num_dt=21, min_val=self.MIN_ROTARY_VALUE, max_val=self.MAX_ROTARY_VALUE, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)
        
        
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
            if onOff == self.ON:
                print("Turning on the top bulb")
                self.light_up.value(1)
            elif onOff == self.OFF:
                print("Turning off the top bulb")
                self.light_up.value(0)
            else:
                print("Wrong input for onOff value")
                return -1
        elif bulbSelect == self.DOWN_BULB: # Upper light bulb selected
            if onOff == self.ON:
                print("Turning on the bottom bulb")
                self.light_down.value(1)
            elif onOff == self.OFF:
                print("Turning off the bottom bulb")
                self.light_down.value(0)
            else:
                print("Wrong input for onOff value")
                return -1
        else:
            print("Wrong input")
            return -1
            
    # Function to control to servo motor, this is to control the tiny vent
    
    
    # Function to return the temperature and humidity
    def _readTempAndHumid(self):
        sensor = SHT3X()
        temp, humid = sensor.getTempAndHumi()
        return temp, humid
    
    # Function to display temperature and humidity
    def getTempAndHumid(self):
        temp, humid = self._readTempAndHumid()
        print("Temporature:", temp, 'ºC, RH:', humid, '%')
    
    
    
    
    
# Testing


incubator = Incubator(19, 22)
# print(incubator.bulbState(incubator.UP_BULB))
# incubator.switchLight(incubator.UP_BULB, incubator.ON)
incubator.getTempAndHumid()
# print(incubator._readTempAndHumid())

