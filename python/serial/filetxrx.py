#!/usr/bin/python

#
# A simple utility which opens a tty device arg[0] and a file arg[1].
# It reads the file line by line and sends it at a regular (default 0.05s) intervals to serial port and reads from
# the same serial port and writes the data to stdout.
#

import serial
import sys
import time

DELAY = 0.05

def openSerial(tty):
    # Open serial device with timeout set to zero to enforce non blocking reads.
    ser = serial.Serial(tty, timeout=0)
    ser.baudrate = 115200 
    return ser

def write(ser, data):
     line = data
     ser.write(line)
     time.sleep(DELAY)

def read(ser):
    data = ser.read()
    sys.stdout.write(data)

def readandsend(tty, filename):
    ser = openSerial(tty)
    with open(filename) as f:
        for line in f:
            write(ser, line)
            read(ser)
    ser.close()

if __name__ == "__main__":
    # execute only if run as a script
    readandsend(sys.argv[1], sys.argv[2])
