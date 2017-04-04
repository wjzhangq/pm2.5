# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

PW_PIN = 12
ts = 0


def pw_callback(channel):
    global ts
    if GPIO.input(channel):
        ts = time.time()
    else:
        t = int((time.time() - ts) * 1000 - 2 + 0.5)
        if t >= 0 and t < 400:
            f = open('/dev/shm/lcd_1', 'w')
            f.write("PM2.5%4s%7s" % (t, time.strftime(
                '%M:%S', time.localtime(time.time()))))
            f.close()
            print t


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PW_PIN, GPIO.IN)
    GPIO.add_event_detect(PW_PIN, GPIO.BOTH, callback=pw_callback)

    try:
        time.sleep(55)         # wait 30 seconds
        print "Time's up. Finished!"
    finally:                   # this block will run no matter how the try block exits
        GPIO.cleanup()
