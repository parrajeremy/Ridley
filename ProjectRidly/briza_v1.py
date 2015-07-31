import mraa as m
import pca9557 as pca
import briza_eeprom as b_eeprom 
import hdc1000 as hdc
import LPS25H as lph
import data_calc as dc
import lmp91000 as lmp
import ads1220 as ads
import populate_sensor_data as sd
import EEPROM as eeprom
import sensor_init as s
import time as t


sen1 = '1'
sen2 = '2'
s1 = ''
s2 = ''
logfile = open('sensor_data.txt','w')

#board addresses initialize
board_addr = [b_eeprom.board1, b_eeprom.board2, b_eeprom.board3, b_eeprom.board4]
print board_addr

#other sensor configuration
lph.configure()

def other_sensor():
    humidity = hdc.readHDC_humidity()
    logfile.write("\nHumidity  = ")
    logfile.write(str(humidity))

    temperature = hdc.readHDC_temp()
    logfile.write("\nTemperature  = ")
    logfile.write(str(temperature))

    pressure = lph.getPressure()
    logfile.write("\nPressure  = ")
    logfile.write(str(pressure))

def reading_eeprom(boardAddr):
    eeprom.init_EEPROM(boardAddr)
    
    global sen1, sen2
    
    #reading from sensor 1
    se1 = eeprom.readSensorQRData(1)
    sen1 = eeprom.data[7:10]

    #reading from sensor2
    se2 = eeprom.readSensorQRData(2)
    sen2 = eeprom.data[7:10]

def call_pca(boardAddr):
    if boardAddr == board_addr[0]:
        pca.pca_init(0x1B)
        print "ON PCA : 0x1B"
    elif boardAddr == board_addr[1]:
        pca.pca_init(0x1D)
        print "ON PCA : 0x1D"
    elif boardAddr == board_addr[2]:
        pca.pca_init(0x1E)
        print "ON PCA : 0x1E"
    elif boardAddr == board_addr[3]:
        pca.pca_init(0x1F)
        print "ON PCA : 0x1F"
    else:
        print("please initialize the board in populate_sensor_board.py")

def sensor1():
    s.init(s1)
    pca.pca_config(1,0,0)
    lmp.lmp_init()
    ads.spi_init()   

def sensor1_conf():
    pca.pca_config(1,0,0)
    
    dc.s1_avg_data()
    rawData = ads.get_readData()
#    print"rawData sensor1 = %ld" %rawData
    logfile.write("\n\tSensor1  = ")
    logfile.write(str(rawData))


#    s1_avg = dc.get_s1Avg()

def sensor2():
    s.init(s2)
    pca.pca_config(0,1,0)
    #print("SENSOR2  : %s", s2)
    lmp.lmp_init()
    ads.spi_init()   


def sensor2_conf():
    pca.pca_config(0,1,0)
    dc.s2_avg_data()
    rawData = ads.get_readData()
#    print "rawData sensor 2 = %ld" %rawData
    logfile.write("\n\tSensor2  = ")
    logfile.write(str(rawData))


#    s2_avg = dc.get_s2Avg()


def board_init(boardAddr):
    global s1,s2
    addr = boardAddr
    reading_eeprom(addr)
    s1 = str(sen1)
    s2 = str(sen2)
    call_pca(addr)
    sensor1()
    sensor2()



#debug
b1 = board_addr[0]
b2 = board_addr[1]
b3 = board_addr[2]
b4 = board_addr[3]
print b2
#initializing the board with all the sensors
board_init(b1)
#board_init(b2)
board_init(board_addr[2])
board_init(board_addr[3])

def load_board():
    for i in range (0,4):
        addr = board_addr[i]
        t.sleep(1)
        print "\n Board %ld  %ld" %(i, board_addr[i])
        logfile.write("\n Board  ")
        logfile.write(str(board_addr[i]))
        ts = t.time()
        print "\n time %ld" %ts
        logfile.write("\nTimestamp  = ")
        logfile.write(str(ts))

        print("\n SENSOR 1 ")
        sensor1_conf()
        t.sleep(1)
        print("\n SENSOR 2 ")
        sensor2_conf()

while 1==1:
    other_sensor()
    t.sleep(0.1)
    load_board()

logfile.close()