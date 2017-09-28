#!/usr/bin/python

import serial
import sys
import time

def write(tty, data, count):
    if (count is not None):
        count = int(count)
    else:
        count = 1
   
    ser = serial.Serial(tty)
    ser.baudrate = 115200 
    for i in range(count): 
        line = data + "\r"
        ser.write(line)
        time.sleep(1)

    ser.close()

if __name__ == "__main__":
    # execute only if run as a script
    write(sys.argv[1], sys.argv[2], sys.argv[3])
