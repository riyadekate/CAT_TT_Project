#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 06:48:49 2018

@author: pi
"""

#!/usr/bin/python3
#@author: CAT

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

log_file = list()


try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	exit()
	
print('Ready')

    
def plot_this():
    df = pd.read_csv(os.path.join(os.getcwd(), "data_log.csv"))
    x = df['timestamp']
    pitch = df['pitch']
    roll = df['roll']
    
    pitch_line, = plt.plot(x[-200:], pitch[-200:], 'b', label = "pitch")
#    roll_line, = plt.plot(x[-200:], roll[-200:], 'g', label = "roll")
    plt.ylim([-90, 90])
    plt.title('Pitch vs Time')
    plt.ylabel('pitch angle (degrees)')
    plt.xlabel('epoch time')
#    plt.legend([pitch_line, roll_line], ['pitch angle (deg)', 'roll angle (deg)'])
#    plt.legend(handles = [pitch_line])
    plt.draw()
    plt.pause(0.1)
    
def get_value_from_can():
    message = bus.recv()
    if message.arbitration_id == 217065857:
        byte1 = str(hex(message.data[0]))[2:]                  
        byte1 ='{:0<2}'.format(byte1)
        byte2 = str(hex(message.data[1]))[2:]                  
        byte2 ='{:0<2}'.format(byte2)
        byte3 = str(hex(message.data[2]))[2:]                  
        byte3 ='{:0<2}'.format(byte3)
        pitch = byte3 + byte2 + byte1
        pitch = int(pitch, 16)
        pitch = (pitch/32768) - 250
        
        byte3 = str(hex(message.data[3]))[2:]                  
        byte3 ='{:0<2}'.format(byte1)
        byte4 = str(hex(message.data[4]))[2:]                  
        byte4 ='{:0<2}'.format(byte2)
        byte5 = str(hex(message.data[5]))[2:]                  
        byte5 ='{:0<2}'.format(byte3)
        roll = byte5 + byte4 + byte3
        roll = int(roll, 16)
        roll = (roll/32768) - 250
        
        string_to_write = {'timestamp': message.timestamp,'pitch' : pitch, 'roll': roll}
        return string_to_write
    else:
        return 0



file_save_time = datetime.now()     
update_plot_time = datetime.now()
           
try:
    while True:
        val = get_value_from_can()
        if val !=0:
            log_file.append(val)
            
        cur_time = datetime.now()
        if((cur_time - file_save_time).total_seconds() >= 1 * 1):
            df = pd.DataFrame(log_file)
            #path = os.path.join(os.getcwd(), str(cur_time) + ".csv") 
            path = os.path.join(os.getcwd(), "data_log.csv") 
            df.to_csv(path, index = False)      
            file_save_time = cur_time
            plot_this()            
    
except KeyboardInterrupt:
    print("Keyboard interrupt")
    os.system("sudo /sbin/ip link set can0 down")
    print("\rBring can down")

