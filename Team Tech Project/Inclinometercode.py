# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 13:11:55 2018

@author: c501
"""
#groupby
#Code for Actual Inclinometer Values 
import pandas as pd
import matplotlib.pyplot as plt


inc_df = pd.read_csv(r'Inclinometerdata.txt', '\t', skip_blank_lines = True)
inc_df.columns = ['Date', 'PGN','IDK', 'IDK','1', '2', '3', '4', '5', '6', '7', '8']
inc_df = inc_df.dropna(how = 'any')


inc_df['Date'] = pd.to_datetime(inc_df['Date'],unit='s')

inc_df['Pitchangle'] = inc_df['3'] + inc_df['2'] + inc_df['1']


inc1_df = inc_df[inc_df['PGN'].str[2:8] == 'f029e2']   #automate this
inc2_df = inc_df[inc_df['PGN'].str[2:8] == 'f02981']






inc1_df['Pitchangleconv'] = inc1_df['Pitchangle'].apply(lambda x:int(x, 16))
inc1_df['Pitchangleconv'] = inc1_df['Pitchangleconv'].apply(lambda x: x*(1/32768))
inc1_df['Pitchangleconv'] = inc1_df['Pitchangleconv'].apply(lambda x: x - 250 )

inc2_df['Pitchangleconv'] = inc2_df['Pitchangle'].apply(lambda x:int(x, 16))
inc2_df['Pitchangleconv'] = inc2_df['Pitchangleconv'].apply(lambda x: x*(1/32768))
inc2_df['Pitchangleconv'] = inc2_df['Pitchangleconv'].apply(lambda x: x - 250 )



input1 = input("Please chooose a channel: Inc1 or Inc 2   ")
x = str(input1)

if x == 'Inc1':
        plt.plot(inc1_df['Date'], inc1_df['Pitchangleconv'],'-ok')
        
if x == 'Inc2':
        plt.plot(inc2_df['Date'], inc2_df['Pitchangleconv'],'-ok')

else:
    print("This is not a valid channel")


