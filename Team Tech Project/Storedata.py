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
import matplotlib.animation as animation
from datetime import datetime
import numpy as np

print('\n\rCAN Rx test')
print('Bring up CAN0....')
os.system("sudo /sbin/ip link set can0 up type can bitrate 250000")
time.sleep(0.1)

#Initialize variables
log_file = list()
xs = list()
ys = list()

fig = plt.figure()
ax = fig.add_subplot(1,1,1)



try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')

#function to plot livestream data from a canbus for a channel
def animate(i, xs, ys):
    global prev_time, log_file
    try:
        message = bus.recv()	# Wait until a message is received.
            
        if message.arbitration_id == 217065857:    #sorts the data based on it's PGN value and converts it to the appropriate value using the JSAE-1939 file
            byte1 = str(hex(message.data[0]))[2:]                  
            byte1 ='{:0<2}'.format(byte1)
            byte2 = str(hex(message.data[1]))[2:]                  
            byte2 ='{:0<2}'.format(byte2)
            byte3 = str(hex(message.data[2]))[2:]                  
            byte3 ='{:0<2}'.format(byte3)
            val = byte3 + byte2 + byte1
            val = int(val, 16)
            val = (val/32768) - 250
            
            string_to_write = {'timestamp': message.timestamp,'data' : val}
            log_file.append(string_to_write)
            
            
            cur_time = datetime.now()
            if((cur_time - prev_time).total_seconds() >= 1 * 60):    #Stores a datapoint every minute to Storedata.csv
                print("its been one minutes")
                df = pd.DataFrame(log_file)
                path = os.path.join(os.getcwd(), str(cur_time) + ".csv") 
                df.to_csv(path, index = False)      
                prev_time = cur_time
                log_file = list()
                print(log_file)
            msg_time = (time.strftime('%H:%M:%S.%f', time.localtime(message.timestamp)))   #converts timestamp from epoch time to standard time
           
            ys.append(val)
            xs = np.arange(len(ys))
            
            #Plots each datapoint in a continuously updating frame                
            ax.clear()
            ax.plot(xs,ys)
            plt.xticks(rotation = 45, ha = 'right')
            plt.subplots_adjust(bottom = 0.3)
            plt.title('pitch angle vs time')
            plt.ylabel('Pitch angle')
            plt.xlabel('Current time: ' + msg_time)

        
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        os.system("sudo /sbin/ip link set can0 down")
        print("Bring can down")


# This calls the animate function to create a running plot of the livestream data. When the code is interrupted, the canbus is set down ending the livestream plot.
try:
    prev_time = datetime.now()               
    ani= animation.FuncAnimation(fig, animate, fargs= (xs, ys), interval = 100)            
    plt.show()            
    
except KeyboardInterrupt:
    print("Keyboard inteedferrupt")
    os.system("sudo /sbin/ip link set can0 down")
    print("\n\rBring can down")
    
            
                


	
