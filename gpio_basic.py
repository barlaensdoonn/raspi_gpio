#!/usr/bin/python3
# gpio basic with power switch tail (PWST)
# 8/3/17
# must start pigpio as daemon before running scripts: sudo pigpiod 
# succesful calls to pigpio methods seem to return 0
# this sketch has pi's gpio pin 7 connected to PWST's 1 [+in] and ground to PWST's 2 [-in]

import time
import pigpio

switch_pin = 7
pi = pigpio.pi()
pi.set_mode(7, pigpio.OUTPUT)

# write pin 7 high
pi.write(7, 1)
time.sleep(1)
pi.write(7, 0)
