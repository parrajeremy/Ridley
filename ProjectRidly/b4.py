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

#board addresses initialize
board_addr = [b_eeprom.board1, b_eeprom.board2, b_eeprom.board3, b_eeprom.board4]
print board_addr


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

def board_init(boardAdr):
	global s1, s2
	reading_eeprom(boardAdr)
	s1 = str(sen1)
	s2 = str(sen2)
	call_pca(boardAdr)
	print "sensor 1 %s" %s1
	print "sensor 2 %s" %s2
        sensor1(s1)
	sensor2(s2)


def sensor1(s1):
    #s.init(s1)
    pca.pca_config(1,0,0)
    print "sensor in sensor1 func %s" %s1
    s.init(s1)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1, 1, 1)	

def sensor2(s2):
    #s.init(s2)
    pca.pca_config(0,1,0)
    print "sensor in sensor2 func %s" %s2
    s.init(s2)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1,1,1)

#board_init(board_addr[0])
#board_init(board_addr[1])
#board_init(board_addr[2])
board_init(board_addr[3])

def conf_sensor1():
#    print("sensor 1:")
    dc.s1_avg_data()
    sensor1Data = ads.get_readData()
    s1_avg = dc.get_s1Avg()

def conf_sensor2():
#    print("sensor 2:")
    dc.s2_avg_data()
    sensor2Data = ads.get_readData()
    s2_avg = dc.get_s2Avg()


while 1==1:
	ts = t.time()
	t.sleep(0.4)
	ads.get_ads_config0(0x70)
	t.sleep(0.4)
	conf_sensor1()
	t.sleep(0.4)
	ads.get_ads_config0(0x60)
	t.sleep(0.4)
	conf_sensor2()
	


