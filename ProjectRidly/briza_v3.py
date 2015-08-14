import sqlite3
import pca9557 as pca
#import briza_eeprom_v3 as be 
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
import os.path
import sys
import briza_eeprom_v3 as be

global boards
def init(boards):
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    
    #with dbopen("/usr/lib/edison_config_tools/public/unified.db") as c:
    #c = conn.cursor()
    print "initing"
    #c.execute('''DROP TABLE IF EXISTS eeprom''')
    c.execute('''CREATE TABLE eeprom (serial,addr,socket,type,sensitivity, baseline, span, offset,unit)''')
    sensors = [('n/a',0x53, 'spec1', 'TOX',1,1,0,0,'ppb'),
               ('n/a',0x53, 'spec2', 'TOR',1,1,0,0,'ppb'),
                ('n/a',0x55, 'spec1', 'SO2',1,1,0,0,'ppb'),
                ('n/a',0x55, 'spec2', 'H2S',1,1,0,0,'ppb'),
                ('n/a',0x56, 'spec1', 'NO2',1,1,0,0,'ppb'),
                ('n/a',0x56, 'spec2', 'O3-',1,1,0,0,'ppb'),
                ('n/a',0x57, 'spec1', 'CO-',1,1,0,0,'ppb'),
                ('n/a',0x57, 'spec2', 'TOX',1,1,0,0,'ppb')
              ]
    c.executemany('INSERT INTO eeprom VALUES (?,?,?,?,?,?,?,?,?)', sensors)       
    c.execute('''DROP TABLE IF EXISTS calibrate''')
    c.execute('''CREATE TABLE calibrate (id INTEGER PRIMARY KEY AUTOINCREMENT,'AAunit' TEXT DEFAULT 'ppb','ABunit' TEXT DEFAULT 'ppb','BAunit' TEXT DEFAULT 'ppb','BBunit' TEXT DEFAULT 'ppb','CAunit' TEXT DEFAULT 'ppb','CBunit' TEXT DEFAULT 'ppb','DAunit' TEXT DEFAULT 'ppb','DBunit' TEXT DEFAULT 'ppb','AAaddr' TEXT DEFAULT '87','AAsel' TEXT DEFAULT 'CO-', 'AA_sen' TEXT DEFAULT '10.02', 'AA_base' TEXT DEFAULT '16.76', 'AA_zero' TEXT DEFAULT '0', 'AA_span' TEXT DEFAULT '0.6', 'ABaddr' TEXT DEFAULT '87','ABsel' TEXT DEFAULT 'TOX', 'AB_sen' TEXT DEFAULT '-39.91', 'AB_base' TEXT DEFAULT '-0.18', 'AB_zero' TEXT DEFAULT '0', 'AB_span' TEXT DEFAULT '0', 'BAaddr' TEXT DEFAULT '86','BAsel' TEXT DEFAULT 'O3-', 'BA_sen' TEXT DEFAULT '-14.05', 'BA_base' TEXT DEFAULT '3.90', 'BA_zero' TEXT DEFAULT '0', 'BA_span' TEXT DEFAULT '0', 'BBaddr' TEXT DEFAULT '86','BBsel' TEXT DEFAULT 'NO2', 'BB_sen' TEXT DEFAULT '34.04', 'BB_base' TEXT DEFAULT '44.01', 'BB_zero' TEXT DEFAULT '0', 'BB_span' TEXT DEFAULT '1.2', 'CAaddr' TEXT DEFAULT '85','CAsel' TEXT DEFAULT 'SO2', 'CA_sen' TEXT DEFAULT '189.49', 'CA_base' TEXT DEFAULT '87.24', 'CA_zero' TEXT DEFAULT '0', 'CA_span' TEXT DEFAULT '0.3', 'CBaddr' TEXT DEFAULT '85', 'CBsel' TEXT DEFAULT 'H2S', 'CB_sen' TEXT DEFAULT '-49.51', 'CB_base' TEXT DEFAULT '3.33', 'CB_zero' TEXT DEFAULT '0', 'CB_span' TEXT DEFAULT '0', 'DAaddr' TEXT DEFAULT '83', 'DAsel' TEXT DEFAULT 'TOX', 'DA_sen' TEXT DEFAULT '15.37', 'DA_base' TEXT DEFAULT '161.41', 'DA_zero' TEXT DEFAULT '0', 'DA_span' TEXT DEFAULT '0', 'DBaddr' TEXT DEFAULT '83',  'DBsel' TEXT DEFAULT 'TOR', 'DB_sen' TEXT DEFAULT '15.37', 'DB_base' TEXT DEFAULT '161.41', 'DB_zero' TEXT DEFAULT '0', 'DB_span' TEXT DEFAULT '0')''')  
    c.execute('INSERT INTO calibrate (id) VALUES (1)')
        
    conn.commit()        
    conn.close()  

    #be.commit2eeprom


##########################################################
##read calibration parameters from sensor module eeprom##
########################################################

def calibrate(boards):   
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    spec1 = {}    
    print "calibrate"
    parameters = {}    
    #try: 
    print boards      
    for b in boards:# in range(len(boards)):         
        if b==87:   
            parameters[b] = {"spec2": eeprom.realSensorData(b,1), "spec1": eeprom.realSensorData(b,2)}
        #eeprom.init_EEPROM(boards[i])          
        else:
            parameters[b] = {"spec2": eeprom.realSensorData(b,1), "spec1": eeprom.realSensorData(b,2)}
        print parameters
       
    #while len(parameters1) !=0:
    #    spec1[parameters1.pop()] = [parameters1.pop() for i in range(6)]
    #print spec1, spec2
    #for key in spec1.iterkeys():

        query1 = str('UPDATE eeprom SET type="%s",sensitivity="%s", baseline="%s", offset="%s", span="%s", unit="%s" WHERE addr=%s and socket="spec1"') % ((str(parameters[b]["spec1"][0]), str(parameters[b]["spec1"][1]),  str(parameters[b]["spec1"][2]), str(parameters[b]["spec1"][3]),str(parameters[b]["spec1"][4]), str(parameters[b]["spec1"][5]), str(b)))       
        query2 = str('UPDATE eeprom SET type="%s",sensitivity="%s", baseline="%s", offset="%s", span="%s", unit="%s" WHERE addr=%s and socket="spec2"') % ((str(parameters[b]["spec2"][0]), str(parameters[b]["spec2"][1]),  str(parameters[b]["spec2"][2]), str(parameters[b]["spec2"][3]),str(parameters[b]["spec2"][4]), str(parameters[b]["spec2"][5]), str(b)))       

        print query1  
        
        c.execute(query1)
        c.execute(query2)
        #conn.commit()  
    
    print "DONE"
    conn.commit()
    conn.close()        
    print "PARAMETERS",
    print parameters
    time.sleep(5)
    #be.eeprom2uiTransfer(boards)
    return parameters        
    
def dbcalibrate(addresses):
    #import briza_eeprom_v3 as be 
    spec1 = []
    spec2 = []    
    #be.ui2eepromTransfer()    
    parameters = {}
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    for i in range(len(addresses)): 

        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec1'" % addresses[i])
        spec1 = c.fetchone()        
        
        #print "SPEC1"
        #print spec1        
        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec2'" % addresses[i])
        spec2 = c.fetchone()
        #print spec2        
        parameters[addresses[i]] = {"spec1": [str(spec1[3]),str(spec1[4]), str(spec1[5]),str(spec1[6]), str(spec1[7]),str(spec1[8])],"spec2": [str(spec2[3]),str(spec2[4]), str(spec2[5]),str(spec2[6]), str(spec2[7]),str(spec2[8])]}
   # print parameters
    conn.close()
        #parameters[addr] = {}
   # print parameters            
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
    #print type1, nA
    nazt = baseline+zero*temperature-20
    nact = nA - nazt
    #print str("NA: " + str(nA) + "Baseline: " +  str(baseline) + "Sensitivity: " + str(sensitivity)+" NACT: "+str(nact)+"*"+str("Span: "+str(span)+" Temperature: "+str(temperature)+"-20"))    
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
        val2 = float(conf_sensor1())
        time.sleep(0.4)
        ads.get_ads_config0(0x60)
        time.sleep(0.4)
        #print "sensor2"
        val1 = float(conf_sensor2())
        
        time.sleep(0.4)
        time.sleep(0.39)   
        #print cvals
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
        con1 = transform(temperature, val1, sensitivity1, baseline1, zero1, span1, type1)
        con2 = transform(temperature, val2, sensitivity2, baseline2, zero2, span2, type2)
        print str("Concentration " + str(type1)+ ":" + str(con1)+", " + "Concentration " + str(type2)+ ":" + str(con2))
        #if boardAdr=='87':
        dataline = {"temperature": temperature, "humidity": humidity, "pressure": pressure, "address": boardAdr, "typeSensor1": str(str(type1)+"("+str(boardAdr)+")"), "valueSensor1": val1, "concentrationSensor1": str(con1),  "unit1": str(unit1), "typeSensor2":str(str(type2)+"("+str(boardAdr)+")"), "valueSensor2": val2, "unit2": str(unit2), "concentrationSensor2": str(con2)}
        
        print dataline
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

def convert_hex(boardNo):
	board = int(boardNo, 16)
	return board

def boardId():

    sys.argv.pop(0)
    print sys.argv
    for i in range(len(sys.argv)):
        hexboards.append(sys.argv[i])        
        boards.append(convert_hex(sys.argv[i]))
        #board1 = convert_hex(b1)
    return boards

def main(boards):
    types = {}
    cvals = calibrate(boards)
    for i in range(len(boards)): 
#        s1, s2 = 
        board.board_init(boards[i])
        addr = boards[i]       
        #print s1, s2
        types[addr] = str(s1), str(s2)
        print types[addr]  
 
    #be.com
    iteration = 0
    
    while True:
        #if iteration < 5:
        #cvals = dbcalibrate(boards)
        #subprocess
        iteration = iteration + 1
        #print iteration
        try:
            #cvals = calibrate(boards)
            dataline = [] 
            #print boards              
            for i in range(len(boards)):
                #print types[boards[i]][0], types[boards[i]][1]                
                data = readSensors(boards[i], types[boards[i]][0], types[boards[i]][1], cvals)
                dataline.append(data)         
            writeSocket(dataline)
        except Exception as ex:
            print ex
            raise
        #else:
        #    print "Updating calibration parameters"
        #    cvals = calibrate(boards)
        #    iteration = 0
    
if __name__ =="__main__":
    global boards
    boards = []
    hexboards = []
    boards = boardId()   
    if os.path.isfile("/home/root/Ridley/ProjectRidly/unified.db") == True:
        print "DB FOUND"        
        pass
    else:
        init()
    #import Board as board
    sen1 = '1'
    sen2 = '2'
    s1 = ''
    s2 = ''

    #

    addrs = []
    HOST = 'localhost' 
    PORT = 50007 
    PORT2 = 50008
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    #global cvals
    global c
    global conn
    #conn = sqlite3.connect("./unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    #c = conn.cursor()   
    main(boards)