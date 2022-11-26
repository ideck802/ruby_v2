import RPi.GPIO as GPIO
import os
from pixel_ring import pixel_ring
from time import sleep
import threading

color = [255, 0, 69]

    
def off():
    os.system("sudo python3 lights_sudo.py " + "off " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " 0")

def set_color(red = 0, green = 0, blue = 0):
    pass
    #pixel_ring.set_color(None, red, green, blue)

def pulse(times):
    os.system("sudo python3 lights_sudo.py " + "pulse " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(times))

def flash(times):
    os.system("sudo python3 lights_sudo.py " + "flash " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(times))


#set_color(color[0], color[1], color[2])
os.system("sudo python3 lights_sudo.py " + "off " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " 0")
os.system("sudo python3 lights_sudo.py " + "flash " + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(5))

loop_flash = True
loop_pulse = True

def flashing_loop():
    while loop_flash:
        flash(1)

def flashing_start():
    global loop_flash
    loop_flash = True
    threading.Thread(target=flashing_loop).start()

def flashing_stop():
    global loop_flash
    loop_flash = False
    off()

def pulsing_loop():
    while loop_pulse:
        pulse(1)

def pulsing_start():
    global loop_pulse
    loop_pulse = True
    threading.Thread(target=pulsing_loop).start()

def pulsing_stop():
    global loop_pulse
    loop_pulse = False
    off()
    
#led.set_pixel(0, 0, 0, 0, 50)
#led.set_pixel(1, 0, 0, 0, 50)
#led.set_pixel(2, 0, 0, 0, 50)
#led.show()