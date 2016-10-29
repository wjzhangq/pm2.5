# -*- coding:utf-8 -*-
import serial
import binascii
import struct
import urllib2
import datetime
import time


def my_date(unixtime, format='%m/%d/%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

if __name__ == '__main__':
    uri = "http://api.yeelink.net/v1.0/device/351785/sensor/395611/datapoints"
    t = serial.Serial('/dev/ttyUSB0', 9600)
    s = struct.Struct('!16H')
    pre_t = time.time()
    start_t = pre_t
    val = 0
    while True:
        n = t.inWaiting()
        if n > 0:
            buf = t.read(n)
            if n == 32:
                tmp = s.unpack(buf)
                val = tmp[3]

            cur_t = time.time()
            if cur_t - start_t > 40:
                break

            if val > 0 and cur_t - pre_t > 10:
                str_t = my_date(cur_t, "%Y-%m-%dT%H:%M:%S")
                buf = '{"timestamp":"%s","value":%s}' % (str_t, val)
                val = 0
                pre_t = cur_t
                request = urllib2.Request(uri)
                request.add_header(
                    'U-ApiKey', '9e19146c5cc33233eb68fbe8c17ba559')
                req = urllib2.urlopen(request, buf)
                if req.code != 200:
                    print req.code
                print buf
                print req.read()
