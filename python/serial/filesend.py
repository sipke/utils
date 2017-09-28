#!/usr/bin/python

import serial
import sys
import time

DELAY = 0.05

def openSerial(tty):
    ser = serial.Serial(tty)
    ser.baudrate = 115200 
    return ser

def write(ser, data):
     line = data
     #data = raw_input(".")
     ser.write(line)
     time.sleep(DELAY)

def readandsend(tty, filename):
    ser = openSerial(tty)
    with open(filename) as f:
        for line in f:
            write(ser, line)
    ser.close()

if __name__ == "__main__":
    # execute only if run as a script
    readandsend(sys.argv[1], sys.argv[2])
