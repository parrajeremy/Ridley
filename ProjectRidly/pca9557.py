import mraa as m
import time
import sys

Addr = 0x00
pca = m.I2c(1)
	
#PCA parameters
PCA_CONFIG_REG0	=	0x00
PCA_CONFIG_REG1	=	0x01
PCA_CONFIG_REG2	=	0x02
PCA_CONFIG_REG3	=	0x03
pca_config2		=	0x00
pca_config3		=	0x08

def pca_init(addr):
	global Addr
	Addr = addr
	pca.address(Addr)
#	print "PCA ADDRESS: %x" %Addr

def pca_config(afe1, afe2, adc):
    
    reg_value1 = ((adc << 2) | (afe2 << 1) | (afe1 << 0))
    pca.writeReg(PCA_CONFIG_REG1, reg_value1)
    value = pca.readReg(PCA_CONFIG_REG1)
    if value != reg_value1:
        print("Failed to configure PCA register 1.")
        print hex (value)

    pca.writeReg(PCA_CONFIG_REG2, pca_config2)
    value = pca.readReg(PCA_CONFIG_REG2)
    if value != pca_config2:
        print("Failed to configure PCA register 2.")
        print hex (value)

    pca.writeReg(PCA_CONFIG_REG3, pca_config3)
    value = pca.readReg(PCA_CONFIG_REG3)
    if value != pca_config3:
        print("Failed to configure PCA register 3.")
        print hex (value)


    #time.sleep(1)


	
	
	
	
def get_addr(addr):
	global Addr
	Addr = addr
	print Addr    	


		    

def printPCA():
    value = pca.readReg(PCA_CONFIG_REG1)
    value1 = pca.readReg(PCA_CONFIG_REG1)
    value2 = pca.readReg(PCA_CONFIG_REG1)
    print ("VALUES FOR PCA REG1, REG2, REG3")
    print (value)
    print (value1)
    print (value2)
    value3 = pca.readReg(PCA_CONFIG_REG0)
    print("VALUE IN REG0")
    print value3


        

