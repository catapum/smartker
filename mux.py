import smbus
import time
import sys

class multiplex:
    
    def __init__(self, bus):
        self.bus = smbus.SMBus(bus)

    def channel(self, address=0x70,channel=0):  # values 0-3 indictae the channel, anything else (eg -1) turns off all channels
        
        if   (channel==0): action = 0x04
        elif (channel==1): action = 0x05
        elif (channel==2): action = 0x06
        elif (channel==3): action = 0x07
        else : action = 0x00

        self.bus.write_byte_data(address,0x04,action)  #0x04 is the register for switching channels 


def initialise():
    bus=1       # 0 for rev1 boards etc.
    address=0x70
    plexer = multiplex(bus)
    plexer.channel(address,3)


I2C_address = 0x70
I2C_bus_number = 1
I2C_ch_0 = 0b00000001
I2C_ch_1 = 0b00000010
I2C_ch_2 = 0b00000100
I2C_ch_3 = 0b00001000
I2C_ch_4 = 0b00010000
I2C_ch_5 = 0b00100000
I2C_ch_6 = 0b01000000
I2C_ch_7 = 0b10000000

def I2C_setup(i2c_channel_setup):
    bus = smbus.SMBus(I2C_bus_number)
    bus.write_byte(I2C_address,i2c_channel_setup)
    time.sleep(0.1)
    print "TCA9548A I2C channel status:", bin(bus.read_byte(I2C_address))


def choose_relevant_sensor(channel):
    
    try:
        I2C_setup(channel)
    except:
        print "bookmarker not connected"
        try:
            I2C_setup(ch)
        except:
            print "no sensor found"


