import mraa as m
import time as t

LPS25H_SLAVE_ADDRESS = 0x5C
LPS25H_DEVICE_ID     = 0xBD

LPS25H_MAX_SPEED 	= 400 
AUTO_INCREMENT   	=(1 << 7)

#  Register Map 
REF_P_XL        	= 0x08
REF_P_L      		=  0x09 
REF_P_H   			= 0x0A 
WHO_AM_I        	= 0x0F

# Resolution - internal Avg setting 
RES_CONF        	= 0x10            
# pwr dwn, data rate, int en, BDU, AZ, SPI
CTRL_REG1       	= 0x20
# boot-refresh reg, fifo_en,wtm_en, mean,swreset, I2C, AZ, one-shot
CTRL_REG2       	= 0x21     
CTRL_REG3       	= 0x22            
CTRL_REG4 		= 0x23            
INT_CFG         	= 0x24                    
INT_SOURCE      	= 0x25              
STATUS_REG      	= 0x27            

# Pressure = (Pout H | Pout L | Pout XL)/4096 
PRESS_POUT_XL   	= 0x28            
PRESS_OUT_L     	= 0x29            
PRESS_OUT_H     	= 0x2A            

# T(degree C) = 42.5 + (TEMP_OUT / 480) -> TEMP_OUT  = ToutH | ToutL 
TEMP_OUT_L      	= 0x2B  
TEMP_OUT_H      	= 0x2C            

#disabled as of now
FIFO_CTRL       	= 0x2E 
FIFO_STATUS     	= 0x2F            
  
# Threshold value for pressure interrupt generation
THS_P_L         	= 0x30              
THS_P_H         	= 0x31              
  
#pressure offset value after soldering
RPDS_L          	= 0x39              
RPDS_H          	= 0x3A        

lps25h = m.I2c(1)
lps25h.frequency(267000)
lps25h.address(LPS25H_SLAVE_ADDRESS)

def configure():
	#lps25h = m.I2c(1)
	#lps25h.frequency(267000)
	#lps25h.address(LPS25H_SLAVE_ADDRESS)

	whoami = lps25h.readReg(WHO_AM_I)
	if (whoami != LPS25H_DEVICE_ID):
		print "LPS25H Device ID Error."

	# Configure the control registers & FIFO
	# AVGT=16, AVGP=32
	lps25h.writeReg(RES_CONF, 0x05)
	lps25h.writeReg(FIFO_CTRL, 0xC1)
	lps25h.writeReg(CTRL_REG2, 0x40)
	lps25h.writeReg(CTRL_REG1, 0x90)
	lps25h.writeReg(CTRL_REG3, 0x00)
	lps25h.writeReg(CTRL_REG4, 0x04)
	
def getPressure():
	#lps25h = m.I2c(1)
	#lps25h.frequency(267000)
	#lps25h.address(LPS25H_SLAVE_ADDRESS)

	data_ready = 0
	while(data_ready == 0):
		status = lps25h.readReg(STATUS_REG)
		#Check for Pressure & Temperature data availability	
		data_ready = status & 0x03
	if (data_ready):
		lps25h.writeByte(PRESS_POUT_XL | AUTO_INCREMENT)
		pressureBytes = lps25h.read(3)
		lPressure = 0
		lPressure = (pressureBytes[2] << 8)
		lPressure <<= 8
		lPressure |= (pressureBytes[1] << 8)
		lPressure |= pressureBytes[0]
		
		pressureData = lPressure / 4096		
		t.sleep(1)
		#print("PRESSURE")
		#print hex(pressureData)
		return pressureData

#configure()
#while True:
	#getPressure()
	#t.sleep(1)
