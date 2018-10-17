import numpy
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv(r'CATdata.txt', '\t', skip_blank_lines = True)
df.columns = ['Date', 'Time','Data']
df = df.dropna(how = 'any')
df['new_time'] = pd.to_datetime(df['Time'], format='%H:%M:%S.%f')

df['PGNValue'] = df['Data'].str[2:6]
df['SPNLength'] = df['Data'].str[8:]

enginespeed_df = df[df['PGNValue'] == 'F004']

enginespeed_df['Enginespeed'] = enginespeed_df['SPNLength'].str[8:10] + enginespeed_df['SPNLength'].str[6:8]

enginespeed_df['Enginespeed'] = enginespeed_df.dropna(enginespeed_df['Enginespeed'] <= 'FF', inplace = True)
enginespeed_df['Enginespeed'] = enginespeed_df.dropna(enginespeed_df['Enginespeed'] <= '', inplace = True)






dataFile = open('CATdata.txt', 'r')
dataList = dataFile.readlines()
dataList = [x.strip() for x in dataList]
dataFile.close()

splitList = []
j = 0
dataList = [x.split('\t') for x in dataList]
for item in dataList:

    if item == ['']:
        continue
    splitList.append(item)


enginespeed = []
i = 0
for data in splitList:
    i=i+1
    

