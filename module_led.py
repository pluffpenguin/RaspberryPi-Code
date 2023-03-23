
# Based on NeoPixel library and strandtest example by Tony DiCola (tony@tonydicola.com)
# To be used with a 12x1 NeoPixel LED stripe.
# Place the LEDs in a circle an watch the time go by ...
# red = hours
# blue = minutes 1-5
# green = seconds
# (To run the program permanently and with autostart use systemd.)

from array import array
from random import randint
import time
from time import sleep
import datetime

from rpi_ws281x_python import PixelStrip, Color

# LED strip configuration:
# 6.6 ft LED strip: 192
# rectangle LED strip: 256
# PC Case LED strip: 30cm, 43

# LED_COUNT = 43
# LED_COUNT = int( input("How many LED's?\n>") )        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

SHIFT_TIMER = 0.05
class ModuleLed:
    def __init__(self):
        self.LED_COUNT = 192
        # self.LED_COUNT = int( input("How many LED's?\n>") )
        self.strip = PixelStrip(
        self.LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.targetColor = [0, 0, 0]
        self.endColor = [0, 0, 0]
        self.fadeFunction = None
        self.settings = {
            "maxSteps": 50,
            "currentStep": 0
        }
        self.strip.begin()
        
    
    def turnoff(self):
        self.strip.setBrightness(0)
        self.strip.show()

    def fadeColor(self, color):
        if color == self.endColor:
            return False
        # add event call or something idk
        if self.fadeFunction == True: 
            self.fadeFunction = False
            time.sleep(1/10)
        self.fadeFunction = True
        # initialize color intervals
        previousColor = self.endColor
        self.endColor = color
        
        # get the rgb steps
        rstep = int(color[0] - previousColor[0])/self.settings["maxSteps"]
        gstep = int(color[1] - previousColor[1])/self.settings["maxSteps"]
        bstep = int(color[2] - previousColor[2])/self.settings["maxSteps"]
        
        # absolute value of steps
        allSteps = [rstep, gstep, bstep]
        # for i in range(len(allSteps)):
        #     if allSteps[i] < 0:
        #         allSteps[i] = -1*allSteps[i]
            
        # while loop to change the colors in the background
        self.settings["currentSteps"] = 0
        while self.fadeFunction == True and self.settings["currentSteps"] < self.settings["maxSteps"]:
            self.settings["currentSteps"] += 1
            # add to the target color
            for i in range(len(self.targetColor)):
                self.targetColor[i] = self.targetColor[i] + allSteps[i]
            
            # local variable, turn targetColor to ints
            stepColor = self.targetColor
            for i in range(len(stepColor)):
                stepColor[i] = int(stepColor[i])
            # set color to int converted stepColor
            try:
                print(f'[ MODULE ]: The stepColor: {stepColor}, {type(stepColor[0])}')
                self.setAllLeds(stepColor)
            except:
                print(f"INT32 ERROR: {stepColor}")
            time.sleep(SHIFT_TIMER)
        
        self.settings["currentSteps"] = 0    
    
    def setAllLeds(self, targetRGB: array):
        targetColor = Color(targetRGB[0], targetRGB[1], targetRGB[2])
        for i in range(self.LED_COUNT):
            self.strip.setPixelColor(i, targetColor)
        self.strip.show()
    
    
    
    def setBrightness(self, value):
        print(f'[CLIENT] Setting Brightness to: {value}')
        if value < 0: 
            value = value*-1
        self.strip.setBrightness(value)
        self.strip.show()
    
        

