# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:28:19 2015

@author: isaaccla
"""

import briza_eeprom as be
import time
try:
    be.ui2eepromTransfer()    
    time.sleep(2)
    be.commit2eeprom()
    
    print "Calibrated"
except:
    print "Calibration error"
    raise