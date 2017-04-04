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
    uri2 = "http://api.yeelink.net/v1.0/device/351785/sensor/395612/datapoints"
    uri10 = "http://api.yeelink.net/v1.0/device/351785/sensor/395762/datapoints"
    t = serial.Serial('/dev/ttyUSB0', 9600)
    s = struct.Struct('!16H')
    start_time = time.time()

    val_list2 = []
    val_list10 = []
    try:
        while True:
            n = t.inWaiting()
            if n > 0:
                buf = t.read(n)
                if n == 32:
                    tmp = s.unpack(buf)
                    if tmp[3] > 0:
                        val_list2.append(tmp[3])
                    if tmp[4] > 0:
                        val_list10.append(tmp[4])

            # 采集60s
            if time.time() - start_time > 30:
                break
    except Exception, e:
        print e

    c2 = len(val_list2)
    if c2 > 0:
        str_t = my_date(time.time(), "%Y-%m-%dT%H:%M:%S")
        buf = '{"timestamp":"%s","value":%s}' % (
            str_t, sum(val_list2) / c2)
        request = urllib2.Request(uri2)
        request.add_header(
            'U-ApiKey', '9e19146c5cc33233eb68fbe8c17ba559')
        req = urllib2.urlopen(request, buf)
        if req.code != 200:
            print req.code
        print buf
        print req.read()

    c10 = len(val_list10)
    if c10 > 0:
        str_t = my_date(time.time(), "%Y-%m-%dT%H:%M:%S")
        buf = '{"timestamp":"%s","value":%s}' % (
            str_t, sum(val_list10) / c10)
        request = urllib2.Request(uri10)
        request.add_header(
            'U-ApiKey', '9e19146c5cc33233eb68fbe8c17ba559')
        req = urllib2.urlopen(request, buf)
        if req.code != 200:
            print req.code
        print buf
        print req.read()
