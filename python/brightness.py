# importing the module
import time
import screen_brightness_control as sbc
import math 


# get current brightness  value
current_brightness = sbc.get_brightness()   
 
# get the brightness of the primary display
primary_brightness = sbc.get_brightness(display=0)


timer = 0
d = 0.2
period = 8


def getBrightness(time):
    # a function with a period of 8 seconds that returns a value between 25 and 100
    return 25 + 75 * (math.sin(2 * math.pi * time / period) + 1) / 2



oldTime = time.time()
while(True):
    if (time.time() - oldTime > d):
        timer += d
        oldTime = time.time()
        brightness = getBrightness(timer)
        sbc.set_brightness(brightness)