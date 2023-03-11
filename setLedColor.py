
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
LED_COUNT = int( input("How many LED's?\n>") )        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False

SHIFT_TIMER = 0.05


# Main program logic follows:
# if __name__ == '__main__':
# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

def turnoff():
    strip.setBrightness(0)
    strip.show()

def shiftDown(strip: PixelStrip):
    for i in range(LED_COUNT, 0, -1):
        targetColor = strip.getPixelColorRGB(i-1)
        red = targetColor.__getattribute__('r')
        green = targetColor.__getattribute__('g')
        blue = targetColor.__getattribute__('b')
        targetColor = Color(red, green, blue)
        # print(targetColor)

        strip.setPixelColor(i, targetColor)
    
    strip.show()

def doThing():
    for i in range(0, strip.numPixels()):
        # targetColor = Color(0, 155, 255)
        
        # print(i, ":", targetColor)
        strip.setPixelColor(i, Color(255, 0, 0))
        # sleep(0.01)
    strip.show()

def setFirstLed(strip:PixelStrip, targetRGB: array):
    targetColor = Color(targetRGB[0], targetRGB[1], targetRGB[2])
    strip.setPixelColor(0, targetColor)

def incrementNextIndexMax2(value):
    return 0 if value+1 > 2 else value + 1

def rainbowCycle(strip: PixelStrip):
    targetRGB = [255, 0, 0]
    previous = 0
    current = 1
    

    increment = 5

    while True:
        # Change the RGB values
        print('checking cases: targetRGB = ', targetRGB)
        if targetRGB[previous] >= 255 and targetRGB[current] < 255:
            for i in range(0, 255 + 1, increment):
                # Least between the two values
                targetRGB[current] = (i>=255)*255 + (i<255)*i
                shiftDown(strip)
                setFirstLed(strip, targetRGB)
                strip.show()
                sleep(SHIFT_TIMER)
                
                # print('previous >= 255:', targetRGB)

        elif targetRGB[current] >= 244:
            for i in range(255, 0, -increment):
                # Greatest between 0 and possible negative number
                targetRGB[previous] = (i>=0)*i + (i<0)*0
                shiftDown(strip)
                setFirstLed(strip, targetRGB)
                strip.show()
                sleep(SHIFT_TIMER)
                # print('current >= 255:', targetRGB)

        # Shift the RGB
            current = incrementNextIndexMax2(current)
            previous = incrementNextIndexMax2(previous)
        

def setAllLeds(strip:PixelStrip, targetRGB: array):
    for i in range(LED_COUNT):
        targetColor = Color(targetRGB[0], targetRGB[1], targetRGB[2])
        strip.setPixelColor(i, targetColor)
    strip.show()

def getColorInput():
    r = int(input("Red:"))
    g = int(input("Green:"))
    b = int(input("Blue:"))
    
    return [r, g, b]
# turnoff()
# doThing()

print("the striP: ", strip)

setAllLeds(strip, getColorInput())


# shiftDown(strip)

# rainbowCycle(strip)
# print(strip.getBrightness())
# strip.show()


# for i in range(0, strip.numPixels(), 1):
#     strip.setPixelColor(i, Color(0, 0, 0))
# while True:
#     now = datetime.datetime.now()

#     # Low light during 19-8 o'clock
#     if(8 < now.hour < 19):
#         strip.setBrightness(200)
#     else:
#         strip.setBrightness(25)

#     hour = now.hour % 12
#     minute = now.minute / 5
#     second = now.second / 5
#     secondmodulo = now.second % 5
#     timeslot_in_microseconds = secondmodulo * 1000000 + now.microsecond

#     for i in range(0, strip.numPixels(), 1):
#         secondplusone = second + 1 if(second < 11) else 0
#         secondminusone = second - 1 if(second > 0) else 11
#         colorarray = [0, 0, 0]

#         if i == second:
#             if timeslot_in_microseconds < 2500000:
#                 colorarray[0] = int(
#                     0.0000508 * timeslot_in_microseconds) + 126
#             else:
#                 colorarray[0] = 382 - \
#                     int(0.0000508 * timeslot_in_microseconds)

#         if i == secondplusone:
#             colorarray[0] = int(0.0000256 * timeslot_in_microseconds)
#         if i == secondminusone:
#             colorarray[0] = int(
#                 0.0000256 * timeslot_in_microseconds) * -1 + 128
#         if i == minute:
#             colorarray[2] = 200
#         if i == hour:
#             colorarray[1] = 200

#         strip.setPixelColor(
#             i, Color(colorarray[0], colorarray[1], colorarray[2]))

#     strip.show()
#     time.sleep(0.1)

