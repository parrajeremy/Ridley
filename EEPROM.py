import mraa as m
import time as t

PAGE_SIZE = 16
EEPROM_ADDR = 0

SENSOR1_SLOT_ADDR = 0
SENSOR2_SLOT_ADDR = 1
SENSOR1_RAW_ADDR  = 2
SENSOR2_RAW_ADDR  = 5

#eeprom = m.I2c(1)
#eeprom.frequency(350000)
#eeprom.address(EEPROM_ADDR)

data = None

def writePage(page):
	eeprom = m.I2c(1)
	eeprom.frequency(350000)
	eeprom.address(EEPROM_ADDR)
	
	dataPointer = (page - 1) * PAGE_SIZE
	data = bytearray([dataPointer])
	for i in range(0, 15):
        	data.insert(i+1, dataPointer + i)
	t.sleep(0.01)

def readPage(page):
        eeprom = m.I2c(1)
        eeprom.frequency(350000)
        eeprom.address(EEPROM_ADDR)

        data = bytearray([page])
        for i in range(0, 20):
                data.insert(i+1, i+1)

def strip_non_ascii(string):
	strippedData = ''
	for i in string:
        	if(i < '~'):
                	strippedData = strippedData + str(unichr(i))
		else:
			print i
	return strippedData

def writeSensorData(board, slot, sensorData):
	eeprom = m.I2c(1)
	eeprom.frequency(350000)
	eeprom.address(EEPROM_ADDR)

	sensorData.insert(0, 0x01)
	sensorData.insert(1, len(sensorData))
#	print "sensorData: %s" %sensorData

	dataPointer = (slot * PAGE_SIZE)
#	print "dataPointer for board: %d, slot %d = %d" %(board, slot, dataPointer)
	
	sensorData[0] = dataPointer 
	eeprom.write(sensorData)	
	t.sleep(0.01)

def writeSensorRawData(board, slot, sensorData):
	length = len(sensorData)
	if (length > 16):
		numPages = length / PAGE_SIZE

#	print "numPages = %d" %numPages

	indexPointer = 0
	for i in range(0, numPages + 1):
		indexPointer = i * (PAGE_SIZE - 1) 
		rawData = sensorData[indexPointer : indexPointer + PAGE_SIZE - 1]
#		print "rawData: %s" %rawData
		stringarray = bytearray(rawData)
		writeSensorData(0, (slot + i), stringarray)

######## Read real calibraation parameters
def realSensorData(board,slot):
        init_EEPROM(board)
        rawQR = strip_non_ascii(readSensorQRData(slot)[1]).strip(',').split(',')
        rawQR[7]=rawQR[7][0:3]
        rawQR=rawQR[2:8]
        #print rawQR        
        return rawQR

def readSensorData(board, slot):
        #print board, slot
        eeprom = m.I2c(1)
        eeprom.frequency(350000)
        eeprom.address(EEPROM_ADDR)
	
        dataPointer = (slot * PAGE_SIZE)
#        print "dataPointer for board: %d, slot %d = %d" %(board, slot, dataPointer)

	temp = bytearray([dataPointer])
	eeprom.write(temp)

	readData = eeprom.read(PAGE_SIZE)
#	readData = eeprom.read(dataLength)

#	strippedData = onlyAscii(strip_non_ascii(readData))
	
	strippedData = readData[1 : readData[0]]
	return strippedData

def chk(s):
	print "inside chk data1"
	#print data
	if (data.find(s)>= 0):
		print "DETECTED"
	else:
		print "Enter AGAIN !!"
	return s 

def readSensorRawData(board, slot):
	global data
	sensorRawData = ''
        for i in range(0, 3):
		sensorRawData = sensorRawData + readSensorData(0, (slot + i))
#		print "readData = %s" %sensorRawData
	data = str(sensorRawData)
	return sensorRawData

def convertToByteArray(string):
	length = len(string)
	bArray = bytearray([0x01, length])
	for i, c in enumerate(string):
        	bArray.insert(i + 2, c)
	
	#print bArray[0]
	#print bArray[1]
	#print "bArray = %s" %bArray

	return bArray

def onlyAscii(string):
        strippedData = ''
        for i in range (0, len(string)):
                if (ord(string[i]) < 175):
                        strippedData = strippedData + string[i]
        return strippedData

def findSensorCodes():
	sensors = [1, 2]
	
	sensors[0] = readSensorData(0, 0)
	sensors[1] = readSensorData(0, 1)

	return sensors
def findSensorRawCodes():
	sensorsRaw = [0, 1]
        sensorsRaw[0] = readSensorRawData(0, SENSOR1_RAW_ADDR)
        sensorsRaw[1] = readSensorRawData(0, SENSOR2_RAW_ADDR)

	return sensorsRaw

def writeDummySensorCodes():
	sensor1 = bytearray("TO,158,9.4")
	sensor2 = bytearray("TR,158,9.4")
	
#	sensor1.insert(0, 0x01)
#	sensor1.insert(1, len(sensor1))

#	sensor2.insert(0, 0x01)
#	sensor2.insert(1, len(sensor2))

#	sensor1Bytes = convertToByteArray(sensor1)	
#	sensor2Bytes = convertToByteArray(sensor2)

	writeSensorData(0, 0, sensor1) 
	writeSensorData(0, 1, sensor2)

def testProgram():
	writeDummySensorCodes()
	sensors = findSensorCodes()
	print "Sensors = %s" %sensors

	sensor1raw = bytearray("91814-B05 100106-CO-1410/ 158/9.4")
	sensor2raw = bytearray("91815-B06 100106-CO-1410/ 158/9.4")
	writeSensorRawData(0, SENSOR1_RAW_ADDR, sensor1raw)
	writeSensorRawData(0, SENSOR2_RAW_ADDR, sensor2raw)

	sensorsRaw = findSensorRawCodes()
	print "RawData: %s" %sensorsRaw

def init_EEPROM(addr):
	global EEPROM_ADDR
	EEPROM_ADDR = addr

def writeSensorQRData(sNo, data, raw):
    if(EEPROM_ADDR == 0):
                print "Please initialize the EEPROM ADDRESS. "
    else:
        if (sNo == 1):
            writeSensorData(0, SENSOR1_SLOT_ADDR, bytearray(data))
            writeSensorRawData(0, SENSOR1_RAW_ADDR, bytearray(raw))
        elif (sNo == 2):
            writeSensorData(0, SENSOR2_SLOT_ADDR, bytearray(data))
            writeSensorRawData(0, SENSOR2_RAW_ADDR, bytearray(raw))
        else:
            print "1. Wrong parameters passed."

def readSensorQRData(sNo):
	if(EEPROM_ADDR == 0):
		print "Please initialize the EEPROM ADDRESS. "
	else:
         try:
             sensorQR = [0, 1]
             if (sNo == 1):
                 sensorQR[0] = readSensorData(0, SENSOR1_SLOT_ADDR)
                 sensorQR[1] = readSensorRawData(0, SENSOR1_RAW_ADDR)
                 #print sensorQR
             elif (sNo == 2):
                 sensorQR[0] = readSensorData(0, SENSOR2_SLOT_ADDR)
                 sensorQR[1] = readSensorRawData(0, SENSOR2_RAW_ADDR)
                 #print sensorQR
             else:
                 print "2. Wrong parameters passed."
         except IndexError:
             pass
         
         return sensorQR
