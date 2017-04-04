#!/usr/bin/python

import time
import BMP180

# Initialise the BMP085 and use STANDARD mode (default value)
# bmp = BMP085(0x77, debug=True)
bmp = BMP180.BMP180()

# To specify a different operating mode, uncomment one of the following:
# bmp = BMP085(0x77, 0)  # ULTRALOWPOWER Mode
# bmp = BMP085(0x77, 1)  # STANDARD Mode
# bmp = BMP085(0x77, 2)  # HIRES Mode
# bmp = BMP085(0x77, 3)  # ULTRAHIRES Mode
t_start = time.time()
while True:
    temp = bmp.read_temperature()

# Read the current barometric pressure level
    pressure = bmp.read_pressure()

# To calculate altitude based on an estimated mean sea level pressure
# (1013.25 hPa) call the function as follows, but this won't be very accurate
    altitude = bmp.read_altitude()

# To specify a more accurate altitude, enter the correct mean sea level
# pressure level.  For example, if the current pressure level is 1023.50 hPa
# enter 102350 since we include two decimal places in the integer value
# altitude = bmp.readAltitude(102350)

    print "Temperature: %.2f C" % temp
    print "Pressure:    %.2f hPa" % (pressure / 100.0)
    print "Altitude:     %.2f\n" % altitude
    f = open('/dev/shm/lcd_2', 'w')
    f.write("%.2f C  %.2f hPa" % (temp, pressure / 100.0))
    f.close()
    t_cur = time.time()
    if t_cur - t_start > 50:
        break
    time.sleep(1)
