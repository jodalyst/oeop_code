#this file will 
import sys
import numpy as np
from scipy.io.wavfile import write
import time
import spidev
import wave

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



def musicMaker(data_set	, samp_rate, fname):
    bit_rate = 16
    average = np.mean(np.array(data_set))
    x = [y-average for y in data_set]
    maxval = 2**15 -1
    header = 0
    y = np.array(x)
    typ = np.int16
    adjusted = typ(y/np.max(np.abs(y)) * maxval)
    write(fname,samp_rate,adjusted)
    t = open(fname, 'rb').read()
    return fname





#record audio:

#set up a few things
num_samples = 10000
sample_rate = 1000
delay = 1.0/sample_rate

#premake the two lists to carve out location (not much faster, but more consistent so less jitter)
data = [0 for x in xrange(num_samples)]
tim = [0 for x in xrange(num_samples)]


#LED will go on for one second, then flash three times quickly and do a 10,000 sample burst collection

GPIO.output(4,1)
time.sleep(1)
for x in range(3):
    GPIO.output(4,0)
    time.sleep(0.1)
    GPIO.output(4,1)
    time.sleep(0.1)

start = time.time() #mark down start time
for x in xrange(num_samples):
    data[x]=(readChannel(1))
    tim[x] = time.time() 

GPIO.output(4,0) #turn off LED to tell user that recording is done!

timm = [x - tim[0] for x in tim] # normalize time.
timm = timm + range(15,50) #add on extra numbers to end to prevent overflow
total = time.time()-start #total duration of recording


sample_number = 0
downsample = []
data = data + data[-50:] #add on buffer at end for iteration protection
for x in range(int(total*sample_rate)):
    while x*1.0/sample_rate >= timm[sample_number]:
        sample_number +=1
    downsample.append(data[sample_number]) 

#fill in gaps to get number of points appropriately back up to ~16000/second
final_rate = 16000
ratio = int(final_rate/sample_rate)
audio_file = []
for datum in downsample:
    new = [datum for x in xrange(ratio)]
    audio_file = audio_file + new

#Write music file:
fname = '/home/pi/lab07_record' 
b =  musicMaker(fourk,1.0/final_rate,fname+'.wav')
os.system('aplay '+fname)
time.sleep(2*total)

#write csv file to save the recording
with open(fname+'.csv', 'wb') as csvout:
    csvout = csv.writer(csvout)
    
    for x in downsample:
        if x 
