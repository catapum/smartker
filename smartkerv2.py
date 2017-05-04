import time
import sys
import os
import pdb

from collections import namedtuple

#GPIO button
import RPi.GPIO as GPIO


#COLOUR SENSOR import
#import Adafruit_TCS34725


#E-ink screen imports
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

from EPD import EPD

from menu import menu


GPIO.setmode(GPIO.BCM)
#RED BUTTON
GPIO.setup(21, GPIO.IN)
#GREEN BUTTON
GPIO.setup(20, GPIO.IN)
#BLACK BUTTON
GPIO.setup(26, GPIO.IN)
#YELLOW BUTTON
GPIO.setup(19, GPIO.IN)

epd = EPD()
epd.clear()
#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 1

menu_screen = menu.MainScreen()
menu_screen.display()

while True:
    if(GPIO.input(19) == GPIO.LOW):
        menu_screen = menu_screen.press_2()
        menu_screen.display()
        print ("button BLUE is pressed")
    
    elif(GPIO.input(26) == GPIO.LOW):
        menu_screen = menu_screen.press_1()
        menu_screen.display()
        print ("button YELLOW is pressed")
    
    elif(GPIO.input(21) == GPIO.LOW):
        menu_screen = menu_screen.press_3()
        menu_screen.display()
        print ("button GREEN is pressed")
        
    elif(GPIO.input(20) == GPIO.LOW):
        menu_screen = menu_screen.press_4()
        menu_screen.display()
        print ("button RED is pressed")

    time.sleep(0.05)
    
tcs.disable()

 