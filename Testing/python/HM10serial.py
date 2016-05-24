import serial
import time

def readlineCR(port): #read a line from the serial port up to CR
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

port = serial.Serial("/dev/ttyAMA0", 9600, timeout=1) #set the serial port address
btthree = 0 #control bit to ensure BT03 is read once only
btfour = 0  #control bit to ensure BT04 is read once only

while True:
	# define and clear various program control bit
	btthreeconn = 0
	btfourconn = 0
	rcv = "0"
	rcv0 = "0"
	rcv1 = "0"	
	rcv2 = "0"
	
	port.write("AT")  #reset HM10
	time.sleep(0.3)   
	port.flushInput() #clear buffer
	print "Discovering BLE iBeacons"
	port.write("AT+DISI?")
	time.sleep(4) #need some time to allow the discovery to complete when there are multiple devices
	rcv = port.read(16) #read these characters to check if iBeacon found
	if ':' in rcv:
		rcv = port.read(42) #read these characters to check if BT01 is found
		if '4C000215' in rcv:
			print "Found BT01"
			rcvMaj = port.read(4) #read the major
			rcvMin = port.read(4) #read the minor
			print "Major:",rcvMaj 
			print "Minor:",rcvMin
		rcv = port.read(78) #need to read again in case there are multiple iBeacons found
		if '4C000215' in rcv:
			print "Found BT01"
                        rcvMaj = port.read(4) #read the major
                        rcvMin = port.read(4) #read the minor
                        print "Major:",rcvMaj
                        print "Minor:",rcvMin
		rcv = port.read(78) #need to read again in case there are multiple iBeacons found
                if '4C000215' in rcv:
                        print "Found BT01"
                        rcvMaj = port.read(4) #read the major
                        rcvMin = port.read(4) #read the minor
                        print "Major:",rcvMaj
                        print "Minor:",rcvMin
		rcv = port.read(78) #need to read again in case there are multiple iBeacons found
                if '4C000215' in rcv:
                        print "Found BT01"
                        rcvMaj = port.read(4) #read the major
                        rcvMin = port.read(4) #read the minor
                        print "Major:",rcvMaj
                        print "Minor:",rcvMin
	port.write("AT") #reset HM10
	time.sleep(0.3)
	port.flushInput() #clear buffer
	port.write("AT+DISC?")
	print "Discovering BLE Devices"
	time.sleep(4) #Need some time to allow the discovery to complete when there are multiple devices
	rcv = port.read(8) #read to clear the discovery start
	rcv = port.read(28) #read up to the first device name
	rcv0 = port.read(4) #this code can allow for up to three BT devices to be found together
	if ('BT' in rcv0):
		rcv = port.read(30) #multiple reads for when there are multiple devices
		rcv1 = port.read(4)
		if ('BT' in rcv1):
			rcv = port.read(30)
			rcv2 = port.read(4)
	
	if (btthree == 0) and (('BT03' in rcv0) or ('BT03' in rcv1) or ('BT03' in rcv2)):
		print "Found BT03" #Found BT03 - connect and read the data
		if ('BT03' in rcv0):
			port.write("AT+CONN0")
		if ('BT03' in rcv1):
                	port.write("AT+CONN1")
		if ('BT03' in rcv2):
	                port.write("AT+CONN2")
                time.sleep(1)
                port.flushInput()
                port.write("x")
		time.sleep(1)
                rcv = readlineCR(port)
		btthreeconn = 1
                if 'T' in rcv:
                        print rcv
                        btthree = 1

	if (btfour == 0) and (btthreeconn == 0) and (('BT04' in rcv0) or ('BT04' in rcv1) or ('BT04' in rcv2)):
        	print "Found BT04" #Found BT04 - connect and read the data
		if ('BT04' in rcv0):
	                port.write("AT+CONN0")
                if ('BT04' in rcv1):
                	port.write("AT+CONN1")
                if ('BT04' in rcv2):
                	port.write("AT+CONN2")
                time.sleep(1)
                port.flushInput()
                port.write("x")
		time.sleep(1)
                rcv = readlineCR(port)
                btfourconn = 1
		if 'T' in rcv:
                        print rcv
			btfour = 1

	if (btthreeconn == 0) and (btfourconn == 0) and (('BT05' in rcv0) or ('BT05' in rcv1) or ('BT05' in rcv2)):
                print "Found BT05" #Found BT05 - connect and read the data
                if ('BT05' in rcv0):
                        port.write("AT+CONN0")
                if ('BT05' in rcv1):
                        port.write("AT+CONN1")
                if ('BT05' in rcv2):
                        port.write("AT+CONN2")
		time.sleep(1)
		port.flushInput()
		time.sleep(5)
                rcv = readlineCR(port)
		if 'T' in rcv:
                        print rcv
