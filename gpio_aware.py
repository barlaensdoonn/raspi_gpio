#!/usr/bin/python3
# control relay via gpio based on time of day
# 8/3/17
# updated 8/4/17

import time
import pigpio
import logging
from datetime import date, datetime, timedelta


def initialize(pin):
    pi = pigpio.pi()
    pi.set_mode(pin, pigpio.OUTPUT)
    pi.write(pin, 0)

    return pi


def get_now():
    return datetime.now()


def get_tmrw(day):
    return date(day.year, day.month, day.day) + timedelta(days=1)


def get_future_time(ref_day, hour):
    '''return datetime object representing following day at hour [must be 0-23]'''

    tmrw = get_tmrw(ref_day)
    return datetime(tmrw.year, tmrw.month, tmrw.day, hour, 0, 0)


def get_time_interval(ref_day, time):
    return time - ref_day


def work_night_shift(pi, switch, state):
    '''
    -1 represents off, calculates time to next on; 1 is inverse
    currently wakeup is @ 21:00, bedtime is @ 10:00 (hour is held in states[key][1])
    '''
    states = {
        -1: (0, 21),
        1: (1, 10)
    }

    state *= -1
    logging.debug('changed state to {}'.format(state))

    pi.write(switch, states[state][0])
    logging.debug('wrote {} to gpio pin {}'.format(states[state][0], switch))

    sleep_until = get_future_time(get_now(), states[state][1])
    logging.debug('sleep_until calculated as {}'.format(sleep_until))

    sleep_interval = get_time_interval(get_now(), sleep_until)
    logging.debug('sleep_interval calculated as {}'.format(sleep_interval))

    logging.debug('sleeping for {} seconds...'.format(sleep_interval.total_seconds()))
    time.sleep(sleep_interval.total_seconds())

    logging.debug('yawn')
    logging.debug('<> <> <> <> <> <> <> <> <> <> <> <>')

    return state


if __name__ == '__main__':
    log_path = '/home/pi/gitbucket/raspi_gpio/logs/gpio_aware.log'
    logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.DEBUG)

    switch = 7  # gpio pin controlling relay
    pi = initialize(switch)
    state = 1
    life = True

    while life:
        try:
            work_night_shift(pi, switch, state)
        except Exception as e:
            logging.error('{}'.format(e))
            life = False
        except KeyboardInterrupt:
            logging.debug('...user exit received...')
