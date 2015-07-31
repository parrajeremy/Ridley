import mraa as m
import math
import time

hdc = m.I2c(1)
hdc.address(0x40)


def readHDC_humidity():
    hdc.writeByte(0x01)
    time.sleep(0.008)
    val1,val2 = hdc.read(2)
    #val1 = hdc.readByte()
    #val2 = hdc.readByte()
    humidity = (val2 | (val1 << 8))
    h = humidity / math.pow(2,16)*100
    #print "HUMIDITY = %f" %(humidity / math.pow(2,16) * 100)
    return h

#def get_humidity():
	#return h

def readHDC_temp():
    hdc.writeByte(0x00)
    time.sleep(0.02)
    val1,val2 = hdc.read(2)
    #val1 = hdc.readByte()
    #val2 = hdc.readByte()
    val1 = val1 & 0xFC
    temperature = (val2 | (val1 << 8))
    t = (temperature / math.pow(2,16))*165 - 40
    #print "TEMPERATURE = %f" % ((temperature / math.pow(2,16)) * 165 - 40)
    return t

#def get_temp():
	#return temperature

if __name__ == '__main__':
    hdc = m.I2c(1)
    hdc.address(0x40)









