#!/usr/bin/python3
# pigpio util
# 8/5/17
# updated 8/5/17

import pigpio
import logging


def initialize_pigpiod(pin):
    logging.debug('initializing pigpiod.pi() class')
    pi = pigpio.pi()

    logging.debug('setting pin {} as output'.format(pin))
    pi.set_mode(pin, pigpio.OUTPUT)

    logging.debug('writing initial state 0 to pin {}'.format(pin))
    pi.write(pin, 0)

    return pi
