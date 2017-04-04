import smbus
from time import sleep
import time
import os
import sys


def delay(time):
    sleep(time / 1000.0)


def delayMicroseconds(time):
    sleep(time / 1000000.0)


class Screen():

    enable_mask = 1 << 2
    rw_mask = 1 << 1
    rs_mask = 1 << 0
    backlight_mask = 1 << 3

    data_mask = 0x00

    def __init__(self, cols=16, rows=2, addr=0x27, bus=1):
        self.cols = cols
        self.rows = rows
        self.bus_num = bus
        self.bus = smbus.SMBus(self.bus_num)
        self.addr = addr
        self.display_init()

    def enable_backlight(self):
        self.data_mask = self.data_mask | self.backlight_mask

    def disable_backlight(self):
        self.data_mask = self.data_mask & ~self.backlight_mask

    def display_data(self, *args):
        self.clear()
        for line, arg in enumerate(args):
            self.cursorTo(line, 0)
            self.println(arg[:self.cols].ljust(self.cols))

    def cursorTo(self, row, col):
        offsets = [0x00, 0x40, 0x14, 0x54]
        self.command(0x80 | (offsets[row] + col))

    def clear(self):
        self.command(0x10)

    def println(self, line):
        for char in line:
            self.print_char(char)

    def print_char(self, char):
        char_code = ord(char)
        self.send(char_code, self.rs_mask)

    def display_init(self):
        delay(1.0)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(4.5)
        self.write4bits(0x30)
        delay(0.15)
        self.write4bits(0x20)
        self.command(0x20 | 0x08)
        self.command(0x04 | 0x08, delay=80.0)
        self.clear()
        self.command(0x04 | 0x02)
        delay(3)

    def command(self, value, delay=50.0):
        self.send(value, 0)
        delayMicroseconds(delay)

    def send(self, data, mode):
        self.write4bits((data & 0xF0) | mode)
        self.write4bits((data << 4) | mode)

    def write4bits(self, value):
        value = value & ~self.enable_mask
        self.expanderWrite(value)
        self.expanderWrite(value | self.enable_mask)
        self.expanderWrite(value)

    def expanderWrite(self, data):
        self.bus.write_byte_data(self.addr, 0, data | self.data_mask)


if __name__ == "__main__":
    screen = Screen(bus=1, addr=0x3f, cols=16, rows=2)
    screen.clear()
    screen.enable_backlight()

    l1_path = '/dev/shm/lcd_1'
    l2_path = '/dev/shm/lcd_2'
    if not os.path.isfile(l1_path):
        fp = open(l1_path, 'w')
        fp.write(time.strftime('%m-%d', time.localtime(time.time())))
        fp.close()
    if not os.path.isfile(l2_path):
        fp = open(l2_path, 'w')
        fp.write(time.strftime('%H:%M:%S', time.localtime(time.time())))
        fp.close()

    t_start = time.time()
    while True:
        t_cur = time.time()
        if t_cur - t_start > 57:
            break

        if t_cur - os.path.getmtime(l1_path) > 10:
            line1 = time.strftime(
                '%H:%M:%S', time.localtime(time.time())) + "  None"
        else:
            line1 = open(l1_path).read(16).strip()
        if t_cur - os.path.getmtime(l2_path) > 10:
            line2 = "No data"
        else:
            line2 = open(l2_path).read(16).strip()
        screen.display_data(line1, line2)
        sleep(1)
