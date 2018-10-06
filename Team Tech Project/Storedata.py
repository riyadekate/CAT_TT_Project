#!/usr/bin/python3
#
# simple_rx_test.py
# 
# This is simple CAN receive python program. All messages received are printed out on screen.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#

import can
import time
import os
import pandas as pd
import matplotlib.pyplot as plt


print('\n\rCAN Rx test')
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
time.sleep(0.1)	
x = []
try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')

try:
	while True:
		message = bus.recv()	# Wait until a message is received.
		
		c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
		s=''
		#pitchangle = message.data[3]+ message.data[2] + message.data[1]
		d = ' {}'.format(c+s)
		
		
		if message.arbitration_id == 217065857:
                    #pitchangle = hex(message.data[3])+ hex(message.data[2]) + hex(message.data[1])
                    #hex, string, concatonate, convert that string into a decimal
                    #x.append(d)
                    #print(x)
                    byte1 = str(hex(message.data[0]))[2:]                  
                    byte1 ='{:0<2}'.format(byte1)
                    byte2 = str(hex(message.data[1]))[2:]                  
                    byte2 ='{:0<2}'.format(byte2)
                    byte3 = str(hex(message.data[2]))[2:]                  
                    byte3 ='{:0<2}'.format(byte3)
                    val = byte3 + byte2 + byte1
                    #print ('hex: ', val)
                    val = int(val, 16)
                    #print('int: ', val)
                    val = (val/32768) - 250
                    
                    print(val)
                    
                    #pitchangle = int(hex9val, 16)
                    #pitchangle = pitchangle*(1/32768)
                    #pitchangle = pitchangle - 250
	                     
                    
		for i in range(message.dlc):
			s +=  '{0:x} '.format(message.data[i])
			
		#print(' {}'.format(c+s))
		
		
#scrolling plot		
                

except KeyboardInterrupt:
	#Catch keyboard interrupt
	os.system("sudo /sbin/ip link set can0 down")
	print('\n\rKeyboard interrtupt')