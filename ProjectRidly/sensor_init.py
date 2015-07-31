import sys
import mraa as m
import sys
import math
import pca9557 as pca
import lmp91000 as lmp
import ads1220 as ads

def init(sensor):
    if sensor == 'TOR':
       # print"TOR"
        Tor()
    elif sensor == 'TOX':
        #print"TOX"
        Tox()
    elif sensor == 'NO2':
        #print"NO2"
        NO2()
    elif sensor == 'O3-':
        #print"O3"
        O3()
    elif sensor == 'CO-':
        #print"CO"
        CO()
    elif sensor == 'SO2':
        #print "SO2"
        SO2()
    elif sensor == 'H2S':
        #print"H2S"
        H2S()

    #lmp.lmp_init()
    #ads.spi_init()


def Tox():
#    print("Configuring parameters for the Tox")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
   # print "AT TOX Bias"
    lmp.get_BIAS(0x05)
    lmp.get_BIAS_SIGN(0x10)
    lmp.get_ADC_GAIN(0x04)
    ads.get_ads_config0(0x50)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)


def Tor():
#    print("Configuring parameters for the Tor")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
    lmp.get_BIAS(0x06)
    lmp.get_BIAS_SIGN(0x00)
    lmp.get_ADC_GAIN(0x0C)
    ads.get_ads_config0(0x7C)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)


def CO():
#    print("Configuring parameters for the CO")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
    lmp.get_BIAS(0x01)
    lmp.get_BIAS_SIGN(0x10)
    lmp.get_ADC_GAIN(0x04)
    ads.get_ads_config0(0x00)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)

def O3():
#    print("Configuring parameters for the O3")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
    lmp.get_BIAS(0x01)
    lmp.get_BIAS_SIGN(0x00)
    lmp.get_ADC_GAIN(0x0C)
    ads.get_ads_config0(0x7C)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)

def NO2():
#    print("Configuring parameters for the NO2")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
   # print "AT NO2 Bias"
    lmp.get_BIAS(0x06)
    lmp.get_BIAS_SIGN(0x00)
    lmp.get_ADC_GAIN(0x0C)
    ads.get_ads_config0(0x64)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)

def H2S():
#    print("Configuring parameters for the H2S")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
    lmp.get_BIAS(0x08)
    lmp.get_BIAS_SIGN(0x10)
    lmp.get_ADC_GAIN(0x04)
    ads.get_ads_config0(0x7C)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)

def SO2():
#    print("Configuring parameters for the SO2")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
   # print "At SO2 Bias"
    lmp.get_BIAS(0x01)
    lmp.get_BIAS_SIGN(0x10)
    lmp.get_ADC_GAIN(0x0A)
    ads.get_ads_config0(0x64)
    ads.get_ads_config1(0x00)
    ads.get_ads_config2(0x40)
    ads.get_ads_config3(0x00)

def ETHL():
#    print("Configuring parameters for the Ethyl")
    lmp.get_OPMODE(0x03)
    lmp.get_TIAGAIN(0x00)
    lmp.get_RLOAD(0x00)
    lmp.get_INTZSEL(0x20)
    lmp.get_REFVOLTAGE(0x80)
    lmp.get_BIAS(0x04)
    lmp.get_BIAS_SIGN(0x10)
    lmp.get_ADC_GAIN(0x00)
#    ads.get_ads_config0()
#    ads.get_ads_config1()
#    ads.get_ads_config2()
#    ads.get_ads_config3()

