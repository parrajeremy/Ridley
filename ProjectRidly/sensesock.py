# -*- coding: utf-8 -*-
"""
Created on Mon Jun 08 09:42:25 2015

@author: isaaccla
"""

#!/usr/bin/env python
import os
import string
import time
import numpy as np
import socket
import sqlite3
import json
import ast
import urllib2
import EEPROM as ee
HOST = ''
PORT = 50007
PORT2 = 50008
wugID = 'KORTIGAR37'
addresses = []

def init():
    print "initing"
    try:
    
        stackconn = sqlite3.connect("/home/root/ProjectRidly/unified.db")
        sc = stackconn.cursor()
        #sc.execute('''DROP TABLE IF EXISTS stack''')
        query = str('''CREATE TABLE IF NOT EXISTS stack(id integer PRIMARY KEY AUTOINCREMENT, address integer, time timestamp, temp real, rh real, pressure real, type1 text, type2 text, adjusted1 real, adjusted2 real, raw1 real, raw2 real, unit1 text DEFAULT 'ppm', unit2 text DEFAULT'ppm' )''')                
        sc.execute(query)
        stackconn.commit() 
        stackconn.close()
    except Exception, e:
        stackconn.close()
        print e       
        
def calibrate(board_addr):   
    print "calibrate"
    parameters = {}    
    for i in range(len(board_addr)):
        if None in i:
            pass
        else:
            parameters[board_addr[i]] = {"spec1": ee.realSensorData(board_addr[i],1), "spec2": e.realSensorData(board_addr[i],2)}
    return parameters

def wug(wugvals, temp='', rh='', pressure='', ID=wugID):
    print "wugging"    
    tempf = float(temp*(9/5)+32)
    baroinch = pressure
    urll = str('http://rtupdate.wunderground.com/weatherstation/updateweatherstation.php?ID='+str(ID)+'&PASSWORD=silver21&dateutc=now&tempf='+str(tempf)+'&baromin='+str(round(baroinch,1))+'&humidity='+str(rh)+'&AqNO2='+str(wugvals['NO2'])+'AqSO2='+str(wugvals['SO2'])+'&AqCO='+str(wugvals['CO-'])+'&AqOZONE='+str(wugvals['O3-'])+'&action=updateraw&realtime=1&rtfreq=2.5')
    #print urll
    response=urllib2.urlopen(urll,timeout=1)
    return response
        
def readsock():
    print "reading Socket"    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
    
        conn, addr = s.accept()
        print 'Connected by', addr
        data = conn.recv(2048)
        #s.close()
        #print data
        if not data: 
            pass
        else: 
            data = ast.literal_eval(''.join(data))
            print str("DATA:" + str(data)) 
            s.close()
        return data

def readsockReg():
    print "reading Reg Socket"    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT2))
    s.listen(5)
    conn, addr = s.accept()
    print 'Connected by', addr
    data = conn.recv(2048)
    #print data
    while not data: 
        pass
    else: 
        data = ast.literal_eval(''.join(data))
        #print str("DATA:" + str(data)) 
        s.close()
    return data

#Optional writing to local file        
def localwrite1(values, optstr=''):
    print "writing 1"    
    #print values, optstr
    with open('data.csv', 'a') as f:
        writeline = ",".join(['%s' % num for num in values])        
        f.write(writeline + "\n")
        f.flush()
        f.close()
        
  
def flatten(lst):
    return sum( ([x] if not isinstance(x, list) else flatten(x)
             for x in lst), [] )
            
def wugdata(data):  
    print "datatoline"    
    types = []
    addresses = []
    values = []    
    adjusted = []    
    #print data    
    for i in data:
        temp = i['temperature']
        rh = float(float(i['humidity']))
        pressure = (100*int(i['pressure'])*2.96E-4)
        t = time.asctime()
        address = i['address']
        type1 = str(str(address) + ":" + i['typeSensor1'])
        type2 = str(str(address) + ":" + i['typeSensor2'])
        types.append(type1)
        types.append(type2)        
        unit1 =    str(i['unit1'])  
        unit2 =    str(i['unit2']) 
        units.append(unit1)
        units.append(unit2)
        value1 = float(i['valueSensor1'])
        value2 = float(i['valueSensor2'])
        adjusted1 = float(i['concentrationSensor1'])
        adjusted2 = float(i['concentrationSensor2'])       
        values.append(value1)
        values.append(value2)
        adjusted.append(adjusted1)
        adjusted.append(adjusted2)
        addresses.append(str(address))
    #print types, values, adjusted, temp, rh, pressure, address
    return types, values, adjusted, temp, rh, pressure, addresses, units

def dbinsert(data):
    print "table_create"    
    addresses = []
    types = [] 
    values = []
    adjusted = []    
    #data = readsock()
    print data    
    for i in data:
        addresses = []
        types = [] 
        values = []
        adjusted = []   
        temp = i['temperature']
        rh = float(float(i['humidity']))
        pressure = (100*int(i['pressure'])*2.96E-4)        
        linetime = time.time()
        address=str(i['address'])
        print address
        types.append(str(i['typeSensor1']))
        types.append(str(i['typeSensor2']))
        values.append(float(i['valueSensor1']))
        values.append(float(i['valueSensor2']))
        unit1 = str(i['unit1'])  
        unit2 = str(i['unit2'])  
        adjusted.append(float(i['concentrationSensor1']))
        adjusted.append(float(i['concentrationSensor2']))
        #Uncomment for raw only data
        #query2 =  '''INSERT INTO stack(address, time, rh, temp, pressure, type1, type2, adjusted1, adjusted2, raw1, raw2) VALUES ('%s', '%s', %s, %s, %s, '%s', '%s', %s, %s, %s, %s)'''  % (address, linetime, rh, temp, pressure, str(i['typeSensor1']), str(i['typeSensor2']), float(i['valueSensor1']), float(i['valueSensor2']),float(i['valueSensor1']),float(i['valueSensor2']))        
	  #Uncomment for transformed data 
        query2 =  '''INSERT INTO stack(address, time, rh, temp, pressure, type1, type2, adjusted1, adjusted2, raw1, raw2, unit1, unit2) VALUES ('%s', '%s', %s, %s, %s, '%s', '%s', %s, %s, %s, %s, '%s', '%s')'''  % (address, linetime, rh, temp, pressure, str(i['typeSensor1']), str(i['typeSensor2']), float(i['concentrationSensor1']), float(i['concentrationSensor2']),float(i['valueSensor1']),float(i['valueSensor2']), str(i['unit1']),str(i['unit2']))        
        try:
            stackconn = sqlite3.connect('/home/root/ProjectRidly/unified.db') 
            c = stackconn.cursor()
            #c.execute(query)               
            #conn.commit()        
            c.execute(query2)               
            stackconn.commit()   
            stackconn.close()
        except Exception, e:
            print "Error " + str(e)
            pass   

def main():
	init()
	while True:
		#linetime = float(time.time())
		data = readsock()              
		#types, values, adjusted, temp, rh, pressure, addresses, units = wugdata(data)
		dbinsert(data)		
		#print types
		#wugvals = {} 
		#for i in range(len(types)):
		#	print types[i][0:3], values[i]
		#	wugvals['%s' % types[i][0:3]] = values[i]
		#print wugvals

		#try:
			#Optionally define AQ values here(e.g. wugvals['NO2']= NO2)
			#resp = wug(wugvals, temp=temp, rh=rh, pressure=pressure)
			#print resp
		#except Exception, e:
		#	print e
		#	pass
main()
