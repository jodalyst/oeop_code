from receiver_support import *



start_code = '001111'

sample_rate = 100     #sampling rate of receiver (samples per second)
measurement_duration = 5  #duration of listening (in seconds)




##########
##########
#YOUR CODE HERE:

# cleanOutput should return a string of 1s and 0s  from these measurements
#def cleanOutput(x):
#    xmax = max(x) #maximum measured value from data stream
#    xmin = min(x) ##minimum measured value from data stream
#    pass #your code here



def cleanOutput(x):
    xmax = max(x) #maximum measured value from data stream
    xmin = min(x) ##minimum measured value from data stream
    offsetAdjustedStream = [] #make an empty list
    for q in x:
        offsetAdjustedStream.append(q-xmin) #brings signal baseline down to 0V
    outputStream = '' #make an empty list to dump True/False values into
    trueThreshold = 2.0/3.0*(xmax - xmin) # 66.67% of maximum (True Threshold)
    falseThreshold = 1.0/3.0*(xmax - xmin) # 33.3% of maximum (False Threshold)
    for r in offsetAdjustedStream:
        if r > trueThreshold:
            outputStream.append('1')
        elif r < falseThreshold:
            outputStream.append('0')
        else:
            if len(outputStream)==0:
                outputStream.append('0')
            else:
                outputStream.append(outputStream[-1])
    return outputStream 

##############
##############
##############

output = record(sample_rate, duration,1)
cleaned_output = cleanOutput(output)

#Identify Start Code Locations:
#This part of the code will scan through your entire data string (held in the cleaned_output string right now) and find all 
#locations of the start_code.  In your case, the start code is most likely '001111'
#If no start code is found the code tells you that
#If one start code is found, the code returns the bit string from right after the start code to the end
#If more than one start code is found, the code returns the bit string between the first two start codes

def extractor( ,start_code):

    indexes = [i for i,x in enumerate(cleaned_output) if x == start_code] #lets us know the index of the start code at all spots:
    if len(indexes) == 0:
        print 'Start Code not Identified. Consider changing sampling rate or doing other things'
    elif len(indexes) == 1:
        print cleaned_output[indexes[0]+6:]
    else:
        print cleaned_output[indexes[0]+6 : indexes[1]] 
