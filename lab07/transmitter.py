#this code is run in lab07 remotely through the tutor only.  It takes in an input string (sys.argv[1]) and will transmit it on loop for sys.argv[2] number of times
#A third input (sys.argv[3]) is the data rate (in samples per second.  Must be at or below around 1000 per second
#If neither argv is provided they default to a quick '0000' message and a loop number of two.
#images are pretty small in this lab (so we can run the code on ~40 loops or so)
#audio files (2 bits, at 1000 samp/s for 1 second are about ten times as large...taking ~5 seconds for one transmission....
import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)

#Set up GPIO Outputs (LED) this will be for transmitting
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,0)

if len(sys.argv) ==4:
    data_set = sys.argv[1]
    loops = sys.argv[2]
    transmission_rate = sys.argv[3]
else:
    data_set = '0000'
    loops = 2 
    transmission_rate = 400 #Hertz

for loop in loops:
    start = time.time()
    for val in range(len(data_set)):
        while time.time()-start < val*1.0/transmission_rate:
            pass
        GPIO.output(17,int(data_set[v]) 

GPIO.cleanup()

