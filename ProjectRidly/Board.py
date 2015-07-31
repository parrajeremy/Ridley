import mraa as m
import pca9557 as pca
import briza_eeprom as b_eeprom 
import hdc1000 as hdc
import LPS25H as lph
import data_calc as dc
import lmp91000 as lmp
import ads1220 as ads
import populate_sensor_data as sd
import EEPROM as eeprom
import sensor_init as s
import time as t
import sqlite3
sen1 = '1'
sen2 = '2'
s1 = ''
s2 = ''

#[b_eeprom.board1, b_eeprom.board2, b_eeprom.board3, b_eeprom.board4]

#global board_addr

def reading_eeprom(boardAddr):
    global sen1, sen2
    eeprom.init_EEPROM(boardAddr)
    
    se1 = eeprom.readSensorQRData(1)
    sen1 = eeprom.data[9:12]

    se2 = eeprom.readSensorQRData(2)
    sen2 = eeprom.data[9:12]

def call_pca(boardAddr):    
    if boardAddr == board_addr[0]:
        pca.pca_init(0x1B)
#        print "ON PCA : 0x1B"
    elif boardAddr == board_addr[1]:
        pca.pca_init(0x1D)
 #       print "ON PCA : 0x1D"
    elif boardAddr == board_addr[2]:
        pca.pca_init(0x1E)
  #      print "ON PCA : 0x1E"
    elif boardAddr == board_addr[3]:
        pca.pca_init(0x1F)
   #     print "ON PCA : 0x1F"
    else:
        print("please initialize the board in populate_sensor_board.py")


def sensor1(s1):
    s.init(s1)
    pca.pca_config(1,0,0)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1,1,1)

def sensor2(s2):
    s.init(s2)
    pca.pca_config(0,1,0)
    lmp.lmp_init()
    ads.spi_init()
    pca.pca_config(1,1,1)

def board_init(boardAddr):
    global s1, s2
    reading_eeprom(boardAddr)
    call_pca(boardAddr)
    s1 = str(sen1)
    s2 = str(sen2)
#    print s1
#    print s2
    sensor1(s1)
    sensor2(s2)
    return s1, s2
#board_init(0x57)
            
def boards(): 
    conn = sqlite3.connect("/home/root/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    #with dbopen("/usr/lib/edison_config_tools/public/unified.db") as c:
    #c = conn.cursor()
    c.execute('SELECT DISTINCT addr FROM eeprom')
    addresses = c.fetchall() 
    conn.commit()
    conn.close()
    addrs = []
    for addr in addresses:            
        addr = int(addr[0])  
        addrs.append(addr)
    return addrs
    
board_addr = boards()

