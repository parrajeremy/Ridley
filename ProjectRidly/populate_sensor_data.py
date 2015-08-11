import EEPROM as e
#import pca9557 as pca

sensor1board1 = "TR,2,-37.38"
sensor1board1raw = "83,spec2,TOR,-48.13,0.75,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor2board1 = "TX,95,11.93"
sensor2board1raw ="83,spec1,TOX,9.74,110.08,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor1board2 = "H2S,425,162.58"
sensor1board2raw = "85,spec1,H2S,186.8,109.14,0,0.3,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor2board2 = "SO2,99,32.9"
sensor2board2raw = "85,spec2,SO2,27.84,43.78,1.5,0.5,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor1board3 = "O3,111,-20.74"
sensor1board3raw = "86,spec1,O3-,-14.05,1.16,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor2board3 = "NO2,26,-49.04"
sensor2board3raw = "86,spec2,NO2,-34.96,-0.02,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor1board4 = "CO,33,9.89"
sensor1board4raw = "87,spec1,CO-,9.93,14.84,2.375,0.4,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

sensor2board4 = "TX,120,13.13"
sensor2board4raw = "87,spec2,TOX,9.74,110.08,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

def board1DataInit(board1):
	e.init_EEPROM(board1)
	e.writeSensorQRData(1,sensor1board1,sensor1board1raw)
	e.writeSensorQRData(2,sensor2board1,sensor2board1raw)
#    pca.pca_init(board1 <<3)

def board2DataInit(board2):
	e.init_EEPROM(board2)
	e.writeSensorQRData(1,sensor1board2,sensor1board2raw)
	e.writeSensorQRData(2,sensor2board2,sensor2board2raw)
#   pca.pca_init(board2<<3)

def board3DataInit(board3):
	e.init_EEPROM(board3)
	e.writeSensorQRData(1,sensor1board3,sensor1board3raw)
	e.writeSensorQRData(2,sensor2board3,sensor2board3raw)
#    pca.pca_init(board3<<3)


def board4DataInit(board4):
	e.init_EEPROM(board4)
	e.writeSensorQRData(1,sensor1board4,sensor1board4raw)
	e.writeSensorQRData(2,sensor2board4,sensor2board4raw)
#    pca.pca_init(board4<<3)
