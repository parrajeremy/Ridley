import sys
import EEPROM as e
#import pca9557 as pca

 
def boardDataInit(board):
    
    if board==83:

        sensor1 = "TX,0,0"
        sensor1raw = "83,spec1,TOX,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

        sensor2 = "TR,0,0"
        sensor2raw ="83,spec2,TOR,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
        e.init_EEPROM(board)
        e.writeSensorQRData(2,sensor2,sensor1raw)
        e.writeSensorQRData(1,sensor2,sensor2raw)
        return board, sensor1, sensor2
    
    elif board==85:

        sensor1 = "SO2,0,0"
        sensor1raw = "85,spec1,SO2,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

        sensor2 = "H2S,0,0"
        sensor2raw = "85,spec2,H2S,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
        e.init_EEPROM(board)
        e.writeSensorQRData(2,sensor1,sensor1raw)
        e.writeSensorQRData(1,sensor2,sensor2raw)
        return board, sensor1, sensor2
    elif board==86:
        
        sensor1 = "NO2,0,0"
        sensor1raw = "86,spec1,NO2,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

        sensor2 = "O3,0,0"
        sensor2raw = "86,spec2,O3-,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
        e.init_EEPROM(board)
        e.writeSensorQRData(2,sensor1,sensor1raw)
        e.writeSensorQRData(1,sensor2,sensor2raw)
        return board, sensor1, sensor2

    elif board==87:
        sensor1 = "CO,0,0"
        sensor1raw = "87,spec1,CO-,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"

        sensor2 = "TX,0,0"
        sensor2raw = "87,spec2,TOX,1,0,0,0,raw\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff"
        e.init_EEPROM(board)
        e.writeSensorQRData(1,sensor2,sensor2raw)
        e.writeSensorQRData(2,sensor1,sensor1raw)
        return board, sensor1, sensor2    
    else: 
        pass
        print "Board addressing error"
    #print board, sensor1, sensor2
    #e.init_EEPROM(board)
    #e.writeSensorQRData(1,sensor1,sensor1raw)
    #e.writeSensorQRData(2,sensor2,sensor2raw)
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
    for board in boards:
        boardDataInit(boards)