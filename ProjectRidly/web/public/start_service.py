# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:10:32 2015

@author: isaaccla
"""
import os
import time
os.system('python /home/root/Ridley/ProjectRidly/briza_eeprom_v3.py 0x53 0x55 0x56 0x57 &')
time.sleep(2)
os.system('python /home/root/Ridley/ProjectRidly/sensesock.py &')
os.system('python /home/root/Ridley/ProjectRidly/briza_v3.py 0x53 0x55 0x56 0x57 &')