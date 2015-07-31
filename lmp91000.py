import mraa as m
import sys
import sensor_init as s


lmp = m.I2c(1)
lmp.address(0x48)


#LMP parameters

LMP_STATUS 		    = 	0x00
LMP_LOCK		    =	0x01
LMP_TIACN	    	=	0x10
LMP_MODECN	    	=	0x12
LMP_UNLOCK          =   0x00
LMP_REFCN           =   0x11

OP_MODE 		    =   0x00
TIA_GAIN 		    =   0x00
R_LOAD 			    =   0x00
INT_Z_SEL 		    =   0x00
REF_VOLTAGE 	    =   0x00
BIAS 			    =   0x00
BIAS_SIGN 		    =   0x00
ADC_GAIN 		    =   0x00
FET_SHORT_DISABLED  =   0x00


def get_OPMODE(op_mode):
    global OP_MODE
    OP_MODE = op_mode

def get_TIAGAIN(tiagain):
    global TIA_GAIN
    TIA_GAIN = tiagain

def get_RLOAD(rload):
    global R_LOAD
    R_LOAD = rload

def get_INTZSEL(int_z_sel):
    global INT_Z_SEL
    INT_Z_SEL = int_z_sel

def get_REFVOLTAGE(ref_voltage):
    global REF_VOLTAGE
    REF_VOLTAGE = ref_voltage

def get_BIAS(bias):
    global BIAS
    BIAS = bias

def get_BIAS_SIGN(bias_sign):
    global BIAS_SIGN
    BIAS_SIGN = bias_sign

def get_ADC_GAIN(adc_gain):
    global ADC_GAIN
    ADC_GAIN = adc_gain

def get_FETSHORT(fet_short):
    global FET_SHORT_DISABLED
    FET_SHORT_DISABLED = fet_short


def lmp_init():
    status = lmp.readReg(LMP_STATUS)
    if status == 1:
    	#print("lmp is ready to write.....now reading the lock")
    	lock = lmp.readReg(LMP_LOCK)
    	if lock == 1:
    		#print("needs to unlock the")
    		lmp.writeReg(LMP_LOCK, LMP_UNLOCK)
    		lock = lmp.readReg(LMP_LOCK)
    		if lock == 0:
    			#print("unlocking successful")
    			lmp.writeReg(LMP_TIACN, TIA_GAIN | R_LOAD)
    			lmp.writeReg(LMP_REFCN, REF_VOLTAGE | INT_Z_SEL | BIAS | BIAS_SIGN)
    			lmp.writeReg(LMP_MODECN,FET_SHORT_DISABLED | OP_MODE)
    			#to debug use print func
#   			printLMP()
    	lmp.writeReg(LMP_LOCK, LMP_LOCK)
    	lock = lmp.readReg(LMP_LOCK)
    	if lock == 1:
    		a = 0
		#print("lock successful")

def printLMP():
     s = lmp.readReg(LMP_TIACN)
     s1 = lmp.readReg(LMP_REFCN)
     s2 = lmp.readReg(LMP_MODECN)
    
     print("PARAMETERS VALUE AFTER INITIALIZATION")
     print("TIA_GAIN")
     print hex(TIA_GAIN)
     print ("OP_MODE")
     print hex(OP_MODE)
     print ("R_LOAD")       
     print hex(R_LOAD)
     print("INT_Z_SEL")
     print hex(INT_Z_SEL)
     print("REF_VOLTAGE")
     print hex(REF_VOLTAGE)
     print("BIAS")      
     print hex(BIAS)      
     print("BIAS_SIGN")   
     print hex(BIAS_SIGN)   
     print("ADC_GAIN")
     print hex(ADC_GAIN)
#     print("ADS_CONFIG0")
#     print hex(ads_config0)
     print("TIACN VALUE, REFCN VALUE, MODECN VALUE")
     print str("WHAT IS THIS"+str(hex(s)))
     print str("WHAT IS THIS"+str(hex(s1)))
