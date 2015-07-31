import socket
import os
import time
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 5005             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
def localwrite(values, optstr=''):
    print values, optstr
    with open('/usr/lib/edison_config_tools/public/pmdata.csv', 'a') as f:
        t = time.asctime()
	tb = t[11:-5]
        writeline = ",".join(['%s' % num for num in values])        
        f.write(str(optstr) + writeline + "\n")
        f.flush()
        f.close()
        return        

headers = ["PM1 (ug/m3)","PM10 (ug/m3)","PM2.5 (ug/m3)"]
iteration = int(0)
localwrite(headers)
linetime = time.time()
#try:
#	os.system('mv /usr/lib/edison_config_tools/public/pmdata.csv /usr/lib/edison_config_tools/public/pmdata%s.bak' % linetime)
#except:
#	pass
while True:
    linetime = time.time()
    iteration = iteration + 1
    conn, addr = s.accept()
    print 'Connected by', addr
    data = str(conn.recv(1024))
    data = eval(data)
    datarow = [",".join(['%s' % data[i] for i in data])]
    localwrite(datarow)        
    if not data: pass
    else: print datarow, type(data) 
