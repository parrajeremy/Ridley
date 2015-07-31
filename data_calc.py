import math
import mraa as m
import ads1220 as ads

s1_AVG1_SAMPLES = 7
s1_AVG2_SAMPLES = 5
s1_AVG3_SAMPLES = 3

s2_AVG1_SAMPLES = 7
s2_AVG2_SAMPLES = 5
s2_AVG3_SAMPLES = 3

s1_avg1_sample = [0,0,0,0,0,0,0]
s1_avg2_sample = [0,0,0,0,0]
s1_avg3_sample = [0,0,0]

s2_avg1_sample = [0,0,0,0,0,0,0]
s2_avg2_sample = [0,0,0,0,0]
s2_avg3_sample = [0,0,0]

s1_avg1count = 0
s1_avg2count = 0
s1_avg3count = 0

s2_avg1count = 0
s2_avg2count = 0
s2_avg3count = 0


s1_avgData = [0,0,0]
s2_avgData = [0,0,0]



def s1_avg_data():
    global nA2,s1_avgData, s1_avg1count, s1_avg2count, s1_avg3count
    s1_avg1_sample[s1_avg1count] = ads.readADS_Data()
    Raw_data1 =s1_avg1_sample[s1_avg1count]
    
    s1_avg1count = s1_avg1count + 1
    if s1_avg1count > (s1_AVG1_SAMPLES - 1):
        s1_avg1count = 0
    temp1 = 0

    for j in range(len(s1_avg1_sample)):
        temp1 = temp1 + s1_avg1_sample[j]
    temp1 = 0

    for j in range(len(s1_avg1_sample)):
        temp1 = temp1 + s1_avg1_sample[j]
    temp1 = temp1 / len(s1_avg1_sample)
    s1_avgData[0] = temp1

    s1_avg2_sample[s1_avg2count] = temp1
    s1_avg2count = s1_avg2count + 1
    if (s1_avg2count > s1_AVG2_SAMPLES - 1):
        s1_avg2count = 0

    temp1 =0
    for j in range(len(s1_avg2_sample)):
        temp1 = temp1 + s1_avg2_sample[j]
    temp1 = temp1 / len(s1_avg2_sample)
    s1_avgData[1] = temp1

    s1_avg3_sample[s1_avg3count] = temp1
    s1_avg3count = s1_avg3count + 1
    if (s1_avg3count > s1_AVG3_SAMPLES - 1):
        s1_avg3count = 0

    temp1 =0
    for j in range(len(s1_avg3_sample)):
        temp1 = temp1 + s1_avg3_sample[j]
    temp1 = temp1 / len(s1_avg3_sample)
    s1_avgData[2] = temp1

#    nA1 = Raw_data1 * 2.048 / 8388607 / 348000 * 1000000000
    nA1 = Raw_data1 / 1425.40783

#    mV1 = Raw_data1 * 2.048 / 8388607
    mV1 = Raw_data1 / 4095.9995117
    
#    print "Raw Data = %ld  mV = %f nA = %f average Data = %ld, %f V." % (Raw_data1, mV1, nA1, s1_avgData[2], (2.048 / 8388607*ads.int32(s1_avgData[2])))
#    print "Raw Data = %ld  mV = %f nA = %f " % (Raw_data1, mV1, nA1),
    #print "nA = %f" % (nA1),
#    print "Raw Data = %ld" % (Raw_data1),
    return nA1    
def get_s1Avg():

    return s1_avgData[2]
 
def s2_avg_data():
    global nA2, s2_avgData, s2_avg1count, s2_avg2count, s2_avg3count
    s2_avg1_sample[s2_avg1count] = ads.readADS_Data()
    Raw_data =s2_avg1_sample[s2_avg1count]
    
    s2_avg1count = s2_avg1count + 1
    if s2_avg1count > (s2_AVG1_SAMPLES - 1):
        s2_avg1count = 0
    temp = 0

    for i in range(len(s2_avg1_sample)):
        temp = temp + s2_avg1_sample[i]
    temp = 0

    for i in range(len(s2_avg1_sample)):
        temp = temp + s2_avg1_sample[i]
    temp = temp / len(s2_avg1_sample)
    s2_avgData[0] = temp

    s2_avg2_sample[s2_avg2count] = temp
    s2_avg2count = s2_avg2count + 1
    if (s2_avg2count > s2_AVG2_SAMPLES - 1):
        s2_avg2count = 0

    temp =0
    for i in range(len(s2_avg2_sample)):
        temp = temp + s2_avg2_sample[i]
    temp = temp / len(s2_avg2_sample)
    s2_avgData[1] = temp

    s2_avg3_sample[s2_avg3count] = temp
    s2_avg3count = s2_avg3count + 1
    if (s2_avg3count > s2_AVG3_SAMPLES - 1):
        s2_avg3count = 0

    temp =0
    for i in range(len(s2_avg3_sample)):
        temp = temp + s2_avg3_sample[i]
    temp = temp / len(s2_avg3_sample)
    s2_avgData[2] = temp
    
    nA2 = Raw_data / 1425.40783
    mV2 = Raw_data / 4095.9995117

#    print "Raw Data = %ld" % (Raw_data),
#    print "Raw Data = %ld  mV = %f nA = %f " % (Raw_data, mV2, nA2),
    #print "nA = %f" % (nA2),
#    print "Raw Data = %ld  average Data = %ld, %f V." % (Raw_data, s2_avgData[2], (2.048 / 8388607*ads.int32(s2_avgData[2])))
    return nA2
    
def get_s2Avg():   
    return s2_avgData[2]
