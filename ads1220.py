import mraa as m
import time
import math
import sys

spi = m.Spi(0)
spi.mode(1)
spi.frequency(1000000)

#ADS Parameters
ADS_WREG		=	0x40
ADS_RREG		=	0x20
ADS_RESET		=	0x06
ADS_CONFIG_REG0 =   0x00
ADS_CONFIG_REG1 =   0x01
ADS_CONFIG_REG2 =   0x02
ADS_CONFIG_REG3 =   0x03
ADS_RDATA   	= 	0x10
ADS_DUMMY   	=  	0x00

ads_config0 	= 	0x00
ads_config1 	=	0x00
ads_config2		=	0x00
ads_config3		=	0x00

readData1 = 0

def get_ads_config0(config0):
    global ads_config0
    ads_config0 = config0
    
def get_ads_config1(config1):
    global ads_config1
    ads_config1 = config1

def get_ads_config2(config2):
    global ads_config2
    ads_config2 = config2

def get_ads_config3(config3):
    global ads_config3
    ads_config3 = config3

   
def spi_init():
#    data = spi.writeByte(ADS_RESET)
#    data = spi.writeByte(ADS_RREG)
#    time.sleep(1)
    spi.writeByte(0x43)
#    spi.writeByte((ADS_WREG) | (ADS_CONFIG_REG0 << 2))
#    spi.writeByte(0x50)
    spi.writeByte(ads_config0)
#    spi.writeByte(0x41)
#    spi.writeByte((ADS_WREG) | (ADS_CONFIG_REG1 << 2))
    spi.writeByte(0x00)
#    spi.writeByte(ads_config1)
#    spi.writeByte(0x42)
#    spi.writeByte((ADS_WREG) | (ADS_CONFIG_REG2 << 2))
    spi.writeByte(0x50)
#    spi.writeByte(ads_config2)
#    spi.writeByte(0x43)
#    spi.writeByte((ADS_WREG) | (ADS_CONFIG_REG3 << 3))
    spi.writeByte(0x00)
#    spi.writeByte(ads_config3)
#    time.sleep(1)
#    printADS()

def readADS_Data():


    spi.writeByte(0x40)
    spi.writeByte(ads_config0)
    time.sleep(0.1)

    spi.writeByte(0x08)
    time.sleep(0.1)
    
#    data = spi.writeByte(ADS_RREG | (ADS_RDATA << 2))
#    time.sleep(1)
    data1 = spi.writeByte(ADS_DUMMY)
    data2 = spi.writeByte(ADS_DUMMY)
    data3 = spi.writeByte(ADS_DUMMY)
#    data4 = spi.writeByte(ADS_DUMMY)
    readData = ((data1 << 16) | (data2 << 8) | (data3 >> 0))
#    readData = readData & 0b111111111111111111111111
    readData1 = readData
#    print printADS()
    if(readData >> 23):
        readData = -(16777215 - readData)
    
#    print("DATA AVAILABLE FROM THE SENSOR")
#    print(readData)
#    print (4.096 / (math.pow(2,24))*int32(readData))
    return readData

def get_readData():
	return readData1

def int32(x):
    if x > 0xFFFFFFFF:
        #raise overflow error
        print("Error Int32.................")
    if x > 0x7FFFFFFF:
        x = int(0x100000000 - x)
        if x < 2147483648:
            return -x
        else:
            return -2147483648
    return x

def  printADS():
    print "ADS"
    print ("printing configreg data config0, config1, config2, config3")
    ads_configreg0 = spi.writeByte(ADS_RREG | (ADS_CONFIG_REG0 << 2))
    ads_configreg0 = spi.writeByte(ADS_DUMMY)
    print str("WHAT IS THIS"+str(hex(ads_configreg0)))
    ads_configreg1 = spi.writeByte(ADS_RREG | (ADS_CONFIG_REG1 << 2))
    ads_configreg1 = spi.writeByte(ADS_DUMMY)
    print str("WHAT IS THIS"+str(hex(ads_configreg1)))
    ads_configreg2 = spi.writeByte(ADS_RREG | (ADS_CONFIG_REG2 << 2))
    ads_configreg2 = spi.writeByte(ADS_DUMMY)
    print str("WHAT IS THIS"+str(hex(ads_configreg2)))
    ads_configreg3 = spi.writeByte(ADS_RREG | (ADS_CONFIG_REG3 << 2))
    ads_configreg3 = spi.writeByte(ADS_DUMMY)
    print str("WHAT IS THIS"+str(hex(ads_configreg3)))



