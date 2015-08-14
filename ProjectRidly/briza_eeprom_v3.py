import mraa as m
import populate_sensor_data as sd
import sys
#mport Board as board
import sqlite3
import EEPROM as e
print 'Address of the boards :', len(sys.argv)-1, 'boards.'
print 'Address list:', str(sys.argv)
import time

def init(boards):
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    print "initing"
    c.execute('''DROP TABLE IF EXISTS eeprom''')
    c.execute('''CREATE TABLE eeprom (serial,addr,socket,type,sensitivity, baseline, span, offset,unit)''')
    #for board in boards:
    #    sensors.append('n/a',board, 'spec1', 'TOX',1,1,0,0,'ppb')
    sensors = [('n/a',0x53, 'spec1', 'TOX',1,1,0,0,'ppb'),
               ('n/a',0x53, 'spec2', 'TOR',1,1,0,0,'ppb'),
                ('n/a',0x55, 'spec1', 'SO2',1,1,0,0,'ppb'),
                ('n/a',0x55, 'spec2', 'H2S',1,1,0,0,'ppb'),
                ('n/a',0x56, 'spec1', 'NO2',1,1,0,0,'ppb'),
                ('n/a',0x56, 'spec2', 'O3-',1,1,0,0,'ppb'),
                ('n/a',0x57, 'spec2', 'CO-',1,1,0,0,'ppb'),
                ('n/a',0x57, 'spec1', 'TOX',1,1,0,0,'ppb')
              ]
    c.executemany('INSERT INTO eeprom VALUES (?,?,?,?,?,?,?,?,?)', sensors)       
    c.execute('''DROP TABLE IF EXISTS calibrate''')
    c.execute('''CREATE TABLE calibrate (id INTEGER PRIMARY KEY AUTOINCREMENT,'AAunit' TEXT DEFAULT 'ppb','ABunit' TEXT DEFAULT 'ppb','BAunit' TEXT DEFAULT 'ppb','BBunit' TEXT DEFAULT 'ppb','CAunit' TEXT DEFAULT 'ppb','CBunit' TEXT DEFAULT 'ppb','DAunit' TEXT DEFAULT 'ppb','DBunit' TEXT DEFAULT 'ppb','AAaddr' TEXT DEFAULT '87','AAsel' TEXT DEFAULT 'CO-', 'AA_sen' TEXT DEFAULT '10.02', 'AA_base' TEXT DEFAULT '16.76', 'AA_zero' TEXT DEFAULT '0', 'AA_span' TEXT DEFAULT '0.6', 'ABaddr' TEXT DEFAULT '87','ABsel' TEXT DEFAULT 'TOX', 'AB_sen' TEXT DEFAULT '-39.91', 'AB_base' TEXT DEFAULT '-0.18', 'AB_zero' TEXT DEFAULT '0', 'AB_span' TEXT DEFAULT '0', 'BAaddr' TEXT DEFAULT '86','BAsel' TEXT DEFAULT 'NO2', 'BA_sen' TEXT DEFAULT '-14.05', 'BA_base' TEXT DEFAULT '3.90', 'BA_zero' TEXT DEFAULT '0', 'BA_span' TEXT DEFAULT '0', 'BBaddr' TEXT DEFAULT '86','BBsel' TEXT DEFAULT 'O3', 'BB_sen' TEXT DEFAULT '34.04', 'BB_base' TEXT DEFAULT '44.01', 'BB_zero' TEXT DEFAULT '0', 'BB_span' TEXT DEFAULT '1.2', 'CAaddr' TEXT DEFAULT '85','CAsel' TEXT DEFAULT 'SO2', 'CA_sen' TEXT DEFAULT '189.49', 'CA_base' TEXT DEFAULT '87.24', 'CA_zero' TEXT DEFAULT '0', 'CA_span' TEXT DEFAULT '0.3', 'CBaddr' TEXT DEFAULT '85', 'CBsel' TEXT DEFAULT 'H2S', 'CB_sen' TEXT DEFAULT '-49.51', 'CB_base' TEXT DEFAULT '3.33', 'CB_zero' TEXT DEFAULT '0', 'CB_span' TEXT DEFAULT '0', 'DAaddr' TEXT DEFAULT '83', 'DAsel' TEXT DEFAULT 'TOX', 'DA_sen' TEXT DEFAULT '15.37', 'DA_base' TEXT DEFAULT '161.41', 'DA_zero' TEXT DEFAULT '0', 'DA_span' TEXT DEFAULT '0', 'DBaddr' TEXT DEFAULT '83',  'DBsel' TEXT DEFAULT 'TOR', 'DB_sen' TEXT DEFAULT '15.37', 'DB_base' TEXT DEFAULT '161.41', 'DB_zero' TEXT DEFAULT '0', 'DB_span' TEXT DEFAULT '0')''')  
    c.execute('INSERT INTO calibrate (id) VALUES (1)')
    #commit2eeprom(boards)   
    conn.commit()        
    conn.close()  
        
def ui2eepromTransfer():
    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()

    print "ui2eeprom"
    spec1 = {}   
    spec2 = {}
    query1 = str('SELECT AAaddr, AAsel, AA_sen, AA_base, AA_zero, AA_span, AAunit, BAaddr, BAsel,  BA_sen, BA_base, BA_zero, BA_span, BAunit, CAaddr, CAsel, CA_sen, CA_base, CA_zero, CA_span, CAunit,  DAaddr, DAsel, DA_sen, DA_base, DA_zero, DA_span, DAunit FROM calibrate ORDER BY id DESC')
    query2 = str('SELECT ABaddr,ABsel, AB_sen, AB_base, AB_zero, AB_span, ABunit,BBaddr, BBsel, BB_sen, BB_base, BB_zero, BB_span, BBunit, CBaddr, CBsel, CB_sen, CB_base, CB_zero, CB_span, CBunit, DBaddr, DBsel, DB_sen, DB_base, DB_zero, DB_span, DBunit FROM calibrate ORDER BY id DESC')    
    c.execute(query1)  
    params1 = c.fetchall()
    c.execute(query2)
    params2 = c.fetchall()
    
    parameters1 = ",".join(map(str,params1[0][0:])).split(',')
    parameters2 = ",".join(map(str,params2[0][0:])).split(',')

    while len(parameters1) !=0:
        spec1[parameters1.pop()] = [parameters1.pop() for i in range(6)]
    while len(parameters2) !=0:
        spec2[parameters2.pop()] = [parameters2.pop() for i in range(6)]
    #print spec1, spec2
    for key in spec1.iterkeys():
        #print spec1[key]
        query1 = str('UPDATE eeprom SET unit="%s",sensitivity="%s", baseline="%s", offset="%s", span="%s", type="%s" WHERE addr=%s and socket="spec1"') % ((str(spec1[key][0]), str(spec1[key][4]),  str(spec1[key][3]), str(spec1[key][2]),str(spec1[key][1]), str(spec1[key][5]), str(key)))       
        #print query1        
        c.execute(query1)
        #conn.commit()  
    for key in spec2.iterkeys():
        query2 = str('UPDATE eeprom SET unit="%s",sensitivity="%s", baseline="%s", offset="%s", span="%s", type="%s" WHERE addr=%s and socket="spec2"') % ((str(spec2[key][0]), str(spec2[key][4]), str(spec2[key][3]), str(spec2[key][2]),str(spec2[key][1]),  str(spec2[key][5]), str(key)))        
        #print query2
        c.execute(query2)
    print "DONE"
    conn.commit()
    conn.close()
        
def eeprom2uiTransfer(boards):

    conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
    c = conn.cursor()
    print "eeprom2ui"
    addresses = boards
    uidict1 = {}
    uidict2 = {}

    for addr in addresses: 
        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec1'" % addr)
        spec1 = c.fetchone()        
        #print "SPEC1"
        #print spec1        
        uidict1[addr] = [str(spec1[3]),str(spec1[4]), str(spec1[5]),str(spec1[6]), str(spec1[7]),str(spec1[8])]
        #print "UIDICT"
        #print uidict1            
        c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec2'" % addr)
        spec2 = c.fetchone()
        uidict2[addr] = [str(spec2[3]),str(spec2[4]), str(spec2[5]),str(spec2[6]), str(spec2[7]),str(spec2[8])]
        #print "UIDICT"            
        #print uidict2
   # query = str('UPDATE calibrate SET AAsel="%s", AA_sen=%s, AA_base=%s, AA_zero=%s, AA_span=%s, AAunit="%s", ABsel="%s", AB_sen=%s, AB_base=%s,AB_zero=%s, AB_span=%s,ABunit="%s", BAsel="%s", BA_sen=%s, BA_base=%s, BA_zero=%s, BA_span=%s,BAunit="%s", BBsel="%s", BB_sen=%s, BB_base=%s,BB_zero=%s, BB_span=%s,BBunit="%s", CAsel="%s", CA_sen=%s, CA_base=%s, CA_zero=%s, CA_span=%s,CAunit="%s", CBsel="%s", CB_sen=%s, CB_base=%s, CB_zero=%s, CB_span=%s,CBunit="%s", DAsel="%s", DA_sen=%s, DA_base=%s, DA_zero=%s,DA_span=%s,DAunit="%s", DBsel="%s", DB_sen=%s, DB_base=%s, DB_zero=%s,DB_span=%s,DBunit="%s" WHERE id=1') % (str(uidict1[87][0]),str(uidict1[87][1]),str(uidict1[87][2]),str(uidict1[87][3]),str(uidict1[87][4]),str(uidict1[87][5]),str(uidict2[87][0]),str(uidict2[87][1]),str(uidict2[87][2]),str(uidict2[87][3]),str(uidict2[87][4]),str(uidict2[87][5]),str(uidict1[86][0]),str(uidict1[86][1]),str(uidict1[86][2]),str(uidict1[86][3]),str(uidict1[86][4]),str(uidict1[86][5]),str(uidict2[86][0]),str(uidict2[86][1]),str(uidict2[86][2]),str(uidict2[86][3]),str(uidict2[86][4]),str(uidict2[86][5]),str(uidict1[85][0]),str(uidict1[85][1]),str(uidict1[85][2]),str(uidict1[85][3]),str(uidict1[85][4]),str(uidict1[85][5]),str(uidict2[85][0]),str(uidict2[85][1]),str(uidict2[85][2]),str(uidict2[85][3]),str(uidict2[85][4]),str(uidict2[85][5]),str(uidict1[83][0]),str(uidict1[83][1]),str(uidict1[83][2]),str(uidict1[83][3]),str(uidict1[83][4]),str(uidict1[83][5]),str(uidict2[83][0]),str(uidict2[83][1]),str(uidict2[83][2]),str(uidict2[83][3]),str(uidict2[83][4]),str(uidict2[83][5]))   
   # c.execute(query)
    conn.commit()
    conn.close()
    
def commit2eeprom(boards):
        conn = sqlite3.connect("/home/root/Ridley/ProjectRidly/unified.db")#/usr/lib/edison_config_tools/public/unified.db")
        c = conn.cursor()     
        for i in range(len(boards)): 
            
            c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec1'" % boards[i])
            spec1 = c.fetchone()                      
            c.execute("SELECT * FROM eeprom WHERE addr = %i AND socket = 'spec2'" % boards[i])
            spec2 = c.fetchone()       
            e.init_EEPROM(boards[i])
            time.sleep(0.4)
            e.writeSensorQRData(1,",".join(map(str,spec1[1:])),",".join(map(str,spec1[1:])))
            #print e.realSensorData(boards[i],1)
            e.writeSensorData(2,",".join(map(str,spec2[1:])),",".join(map(str,spec2[1:])))
            #print e.readSensorData(boards[i],2)
            
def convert_hex(boardNo):
	board = int(boardNo, 16)
	return board

def boardId():
    boards = []
    sys.argv.pop(0)
    print sys.argv
    for i in range(len(sys.argv)):
        boards.append(convert_hex(sys.argv[i]))

    return boards



if __name__ =="__main__":
    boards = boardId()
    init(boards)    
    for b in boards:
        
        pop1, pop2, pop3 = sd.boardDataInit(b)
        print pop1, pop2, pop3

        