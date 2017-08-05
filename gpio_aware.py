#!/usr/bin/python3
# control relay via gpio based on time of day
# 8/3/17
# updated 8/4/17

import time
import pigpio
from datetime import date, datetime, timedelta

life = True


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
    pi.write(switch, states[state][0])
    sleep_till = get_future_time(get_now(), states[state][1])
    sleep_interval = get_time_interval(get_now(), sleep_till)
    time.sleep(sleep_interval.total_seconds())

    return state


if __name__ == '__main__':
    switch = 7  # pin controlling relay
    pi = initialize(switch)
    state = 1

    while life:
        try:
            work_night_shift(pi, switch, state)
        except Exception:
            life = False
        except KeyboardInterrupt:
            print('...user exit received...')
