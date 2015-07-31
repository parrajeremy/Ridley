import sqlite3
import pca9557 as pca
import briza_eeprom as be 
import hdc1000 as hdc
import LPS25H as lph
import data_calc as dc
import lmp91000 as lmp
import ads1220 as ads
import EEPROM as eeprom
import sensor_init as s
import time
import Board as board
import socket


sen1 = '1'
sen2 = '2'
s1 = ''
s2 = ''
board_addr = board.boards()#
addrs = []

##########################################################
##read calibration parameters from sensor module eeprom##
########################################################

def calibrate(board_addr):   
    print "calibrate"
    parameters = {}    
    #try:       
    for i in range(len(board_addr)):            
        parameters[board_addr[i]] = {"spec1": eeprom.realSensorData(board_addr[i],1), "spec2": eeprom.realSensorData(board_addr[i],2)}
    print parameters
    return parameters        
    
def dbcalibrate(addresses):
    be.ui2eepromTransfer()    
    parameters = {}
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    for i in range(len(addresses)): 

        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec1'" % addresses[i])
        spec1 = c.fetchone()        
        
        #print "SPEC1"
        print spec1        
        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec2'" % addresses[i])
        spec2 = c.fetchone()
        print spec2        
        parameters[addresses[i]] = {"spec1": [str(spec1[3]),str(spec1[6]), str(spec1[7]),str(spec1[4]), str(spec1[5]),str(spec1[8])],"spec2": [str(spec2[3]),str(spec2[6]), str(spec2[7]),str(spec2[4]), str(spec2[5]),str(spec2[8])]}
    print parameters
    conn.close()
        #parameters[addr] = {}
    print parameters            
    #conn.close()
    return parameters

############################################################################  
##configuring other sensors on the board like : humidity, temp, pressure###
##########################################################################
lph.configure()
def other_sensor():
    humidity = hdc.readHDC_humidity()
    temperature = hdc.readHDC_temp()
    pressure = lph.getPressure()
    return temperature, humidity, pressure
##############################
##sensor init/configuration##
############################

#configuring the on board sensor configuration
def sensor1(s1):
    pca.pca_config(1,0,0)
    s.init(s1)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1,1,1) 



def conf_sensor1():
#    print("sensor 1:")
    pca.pca_config(1,0,0)
    s1_avg = dc.s1_avg_data()
    sensor1Data = ads.get_readData()
    #dc.get_s1Avg()
    pca.pca_config(1,1,1)
    #print s1_avg
    val1 =  s1_avg   
    return val1
    
def sensor2(s2):
    s.init(s2)
    pca.pca_config(0,1,0)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1,1,1)

def conf_sensor2():
#    print("sensor 2:")
    pca.pca_config(0,1,0)
    s2_avg = dc.s2_avg_data()
    sensor2Data = ads.get_readData()
    #dc.get_s2Avg()
    pca.pca_config(1,1,1)
    #print s2_avg    
    val2 = s2_avg
    return val2
    
###################################################
##Calibrate and temperature adjust sensor values##
#################################################
def transform(temperature, nA, sensitivity, baseline, zero, span, type1):
    #print "transforming"
    #print temperature, nA, sensitivity, baseline, zero, span, type1   
    #nA = float(rawvalue/1425.40783) 
    print type1, nA
    nazt = baseline+zero*temperature-20
    nact = nA - nazt
    print str("1/float*"+str(sensitivity)+"*"+str(nact)+"*"+str("(1-float("+str(span)+"*"+str(temperature)+"-20"))    
    concentration=(1/sensitivity)*nact*(1-span*(temperature-20))
    #concentration=abs(concentration)
    return concentration
#################################################
##Read sensor values and construct data object##
###############################################
def readSensors(boardAdr, s1, s2, cvals):
               
       # parameters = {}           
       # parameters[boardAdr] = {"spec1": eeprom.realSensorData(boardAdr,1), "spec2": eeprom.realSensorData(boardAdr,2)}
       # print parameters        
       # cvals = parameters#calibrate(boardAdr)        
        #print boardAdr, s1, s2, cvals
        temperature, humidity, pressure = other_sensor()
        board.call_pca(boardAdr)
        time.sleep(0.4)

        time.sleep(0.4)

        time.sleep(0.4)
        ads.get_ads_config0(0x70)
        time.sleep(0.4)
        #print "sensor 1"
        val1 = float(conf_sensor1())
        time.sleep(0.4)
        ads.get_ads_config0(0x60)
        time.sleep(0.4)
        #print "sensor2"
        val2 = float(conf_sensor2())
        
        time.sleep(0.4)
        time.sleep(0.39)   
        print cvals
        type1 = str(cvals[boardAdr]['spec1'][0])
        type2 = str(cvals[boardAdr]['spec2'][0])
        sensitivity1 = float(cvals[boardAdr]['spec1'][1])
        sensitivity2 = float(cvals[boardAdr]['spec2'][1])
        baseline1 = float(cvals[boardAdr]['spec1'][2])
        baseline2 = float(cvals[boardAdr]['spec2'][2])
        zero1 = float(cvals[boardAdr]['spec1'][3])
        zero2 = float(cvals[boardAdr]['spec2'][3])
        span1 = float(cvals[boardAdr]['spec1'][4])
        span2 = float(cvals[boardAdr]['spec2'][4])
        unit1 = cvals[boardAdr]['spec1'][5]
        unit2 = cvals[boardAdr]['spec2'][5]
        #print val1, val2        
        con1 = abs(transform(temperature, val1, sensitivity1, baseline1, zero1, span1, type1))
        con2 = abs(transform(temperature, val2, sensitivity2, baseline2, zero2, span2, type2))
        print str("Concentration " + str(type1)+ ":" + str(con1)+", " + "Concentration " + str(type2)+ ":" + str(con2))
        dataline = {"temperature": temperature, "humidity": humidity, "pressure": pressure, "address": boardAdr, "typeSensor1": str(str(type1)+"("+str(boardAdr)+")"), "valueSensor1": val1, "concentrationSensor1": str(con1),  "unit1": str(unit1), "typeSensor2":str(str(type2)+"("+str(boardAdr)+")"), "valueSensor2": val2, "unit2": str(unit2), "concentrationSensor2": str(con2)}
        
        return dataline
        
################################
##write data object to socket##
##############################
def writeSocket(dataline):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((HOST,PORT))
        sock.send(str(dataline))
        sock.close()         
    except Exception, ex:
        sock.close()
        print ex
        pass

    
def main():
    types = {}
    board_addr = board.boards()
    print board_addr
    for i in range(len(board_addr)): 
        s1, s2 = board.board_init(board_addr[i])
        addr = board_addr[i]       
        print s1, s2
        types[addr] = str(s1), str(s2)
        #print types[addr]
    #init()
    #be.eeprom2uiTransfer()
    #be.ui2eepromTransfer()
 
    #be.ui2eepromTransfer()
    
    cvals = calibrate(board_addr)
    iteration = 0
    
    while True:
        #if iteration < 5:
        cvals = dbcalibrate(board_addr)
        #subprocess
        iteration = iteration + 1
        #print iteration
        try:
            #cvals = calibrate(board_addr)
            dataline = [] 
            #print board_addr              
            for i in range(len(board_addr)):
                #print types[board_addr[i]][0], types[board_addr[i]][1]                
                data = readSensors(board_addr[i], types[board_addr[i]][0], types[board_addr[i]][1], cvals)
                dataline.append(data)         
            writeSocket(dataline)
        except Exception as ex:
            print ex
            raise
        #else:
        #    print "Updating calibration parameters"
        #    cvals = calibrate(board_addr)
        #    iteration = 0
    
if __name__ =="__main__":

    HOST = 'localhost' 
    PORT = 50007 
    PORT2 = 50008
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    #global cvals
    global c
    global conn
    #conn = sqlite3.connect("./unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    #c = conn.cursor()   
    main()