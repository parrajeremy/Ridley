import mraa as m
import time as t
import Board as board
import briza_eeprom as b_eeprom
import EEPROM as eeprom
import LPS25H as lph
import hdc1000 as hdc
import pca9557 as pca
import data_calc as dc
import ads1220 as ads
import sensor_init as s
logfile = open('sensor_data.txt','w')



board_addr = [b_eeprom.board1, b_eeprom.board2, b_eeprom.board3, b_eeprom.board4]


#board.board_init(board_addr[0])
#board.board_init(board_addr[1])
#board.board_init(board_addr[2])
board.board_init(board_addr[3])



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

def sensor1_conf():
    
    pca.pca_config(1,1,0)
    dc.s1_avg_data()
    rawData = ads.get_readData()
#    print"rawData sensor1 = %ld" %rawData
    logfile.write("\n\tSensor1  = ")
    logfile.write(str(rawData))


def sensor2_conf():
    pca.pca_config(1,1,0)
    dc.s2_avg_data()
    rawData = ads.get_readData()
#    print "rawData sensor 2 = %ld" %rawData
    logfile.write("\n\tSensor2  = ")
    logfile.write(str(rawData))

def load_board():
#    for i in range (0,1):
#        addr = board_addr[i]
        board.call_pca(0x57)
        t.sleep(1)
#        print "\n Board %ld  %ld" %(i, board_addr[i])
        logfile.write("\n Board  ")
#        logfile.write(str(board_addr[i]))
        ts = t.time()
        print "\n time %ld" %ts
        logfile.write("\nTimestamp  = ")
        logfile.write(str(ts))

        print("\n SENSOR 1 ")
        ads.get_ads_config0(0x7C)
        sensor1_conf()
        t.sleep(0.1)
        print("\n SENSOR 2 ")
        ads.get_ads_config0(0x64)
        sensor2_conf()

while 1==1:
#    other_sensor()
    t.sleep(0.1)
    load_board()

logfile.close()