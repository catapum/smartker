import sys

import Adafruit_TCS34725

from data import *

import mux




def choose_relevant_sensor():
    channels = [1, 2]
    mux.I2C_setup(1)
    try:
        tcs = Adafruit_TCS34725.TCS34725(integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_2_4MS,
                                 gain=Adafruit_TCS34725.TCS34725_GAIN_1X)
    except:
        mux.I2C_setup(2)
        tcs = Adafruit_TCS34725.TCS34725(integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_2_4MS,
                                 gain=Adafruit_TCS34725.TCS34725_GAIN_1X)
        tcs.set_interrupt(True)
    return tcs




def readColour():
    tcs = choose_relevant_sensor()
    tcs.set_interrupt(False)

    # Read the R, G, B, C color data.
    red_mean = []
    green_mean = []
    blue_mean = []
    for i in range(5):
        red, green, blue, colour_temp = tcs.get_raw_data()
        #RGB ratios
        total = red + green + blue
        #red_part = int(red*100.0/total)
        #green_part = int(green*100.0/total)
        #blue_part = int(blue*100.0/total)

        #RGB in 8 bits
        red, green, blue = (red*256/colour_temp, green*256/colour_temp, blue*256/colour_temp)
        red_mean.append(red)
        green_mean.append(green)
        blue_mean.append(blue)

        # Print out the values.
        #print 'COLOUR: R={0} G={1} B={2}'.format(red, green, blue)
        #print 'RATIOS: R={0} G={1} B={2}'.format(red_part, green_part, blue_part) 


    
    # Enable interrupts and put the chip back to low power sleep/disabled.
    tcs.set_interrupt(True)

    read = {"red": sum(red_mean)/len(red_mean),
            "green": sum(green_mean)/len(green_mean),
            "blue": sum(blue_mean)/len(blue_mean)}
    print 'COLOUR: R={0} G={1} B={2}'.format(read["red"], read["green"], read["blue"])

    return read

def closestEuclideanDistance(red, green, blue, red_part=None, green_part=None, blue_part=None, ratios=False):

    table, candidate = (rgb_ratios_table, RGBKey(red_part, green_part, blue_part)) if ratios else (rgb_table, RGBKey(red, green, blue))
    if candidate in table:
        return (candidate, table[candidate])

    distance = sys.maxint
    match = None
    for key in table.keys():
        calculated_distance = (candidate.red-key.red)**2 + (candidate.green-key.green)**2 + (candidate.blue-key.blue)**2
        distance, match = (calculated_distance, key) if ( calculated_distance < distance ) else (distance, match)

    #TODO: Check if minimum distance found is acceptable, if not return None
    print "Distance: ", distance
    if match:
        return (candidate, table[match])
    return {}

#choose_relevant_sensor()