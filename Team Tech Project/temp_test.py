#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 20:11:38 2018

@author: pi
"""

import os
import time
import datetime as dt
import pandas as pd
#download_dir = "test.csv"
log_file = list()

def measure_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))[:-3]
        
def read_time():
    date = dt.datetime.now()
    return date
    
string_to_write = "time, temperature"

while True:
    temp = measure_temp()
    cur_time = read_time()
    
    string_to_write = str(cur_time) + "," + temp + "\n"
    
    dict_val = {'time' : cur_time, 'temperature': temp}
    log_file.append(dict_val)        
    
    print(string_to_write)
    
    time.sleep(10)
    
    df = pd.DataFrame(log_file)
    df.to_csv("dataframe.csv", index = False)






