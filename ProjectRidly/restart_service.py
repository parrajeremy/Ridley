# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:02:39 2015

@author: isaaccla
"""
import os

try:
    os.system('python /home/root/ProjectRidly/stop_service.py')

except:
    print "Service not started"
    pass
try:
    os.system('python /home/root/ProjectRidly/start_service.py')
except:
    pass