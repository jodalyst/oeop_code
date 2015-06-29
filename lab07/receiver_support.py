#this file will 
import sys
import time
import spidev

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)


#set up spi communcation to MCP3008
spi = spidev.SpiDev()
spi.open(0,0)


#reads in MCP3008 in single-ended form.  
def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data



def record(sample_rate,duration, channel):
    if duration > 10:
        print 'Duration too long'
        return False
    if sample_rate > 600:
        print 'Sample Rate too high'
        return False
    
    total_samples = sample_rate*duration
    data = [0.0 for x in xrange(total_samples)]
    start = time.time()
    for x in range(total_samples):
        while time.time-start < x*1.0/sample_rate:
            pass
        data[x] = readChannel(channel)
    return data
        
