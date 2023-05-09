# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:24:26 2023

@author: Dell
"""


# Initialising required libraries
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import plotly.express as px
from datetime import datetime
import datetime as dt

 
# Comment: this can be removed = CBR

# Loading the dataset

parse_dates = ['datetime']
df = pd.read_csv(r"C:\Users\Dell\Documents\PythonScripts\techbinder_export_data_20230502.csv", header=0 ,encoding = 'unicode_escape',sep=";", low_memory= False, parse_dates=parse_dates)

# df = pd.read_csv(r"C:\Users\Dell\Documents\PythonScripts\techbinder_export_data_20230502.csv", header=0 ,encoding = 'unicode_escape',sep=";", low_memory= False)

# Priting header names in console CBR
print (df.keys())


# Creating new filtered dataframe
newdf = df[(df.fqn == "MV_Bermuda_Islander.PharosOne/650/BWTS/Pumps/Ballast_pump_1_run") & (df.opcquality >= 192 )]  # Skipping values with opcquality less than 192 to remove potential duplicates & low quailty data

print (newdf.loc[:,:"datetime"]) #CBR

newdf.insert(2, 'time_diff', "")
newdf.insert(5, 'time_diff_float', "")


#print new instered col. CBR

print (newdf.iloc[:,2:3]) 

# subtracts value of time 2 from time 1 & adds value to col "time_diff" 
# converts te value of timedelate in time_diff_float to float to calcualte std dev. 

for i in range(0, len(newdf)):
    if i == int(len(newdf)-1):
        newdf.iloc[i, 2] = datetime.now()-datetime.now() #adding last value as 0 hhmmss
        newdf.iloc[i, 5] = (datetime.now()-datetime.now()).total_seconds()
        break
    else:
        newdf.iloc[i, 2] = newdf.iloc[i+1,1] - newdf.iloc[i,1] #adding values until cell before last
        newdf.iloc[i, 5] = (newdf.iloc[i+1,1] - newdf.iloc[i,1]).total_seconds()  #adding values until cell before last


# prints new df with the updates values in time_diff & time_diff_float  CBR

print (newdf.loc[:,"datetime":"time_diff"])
print (newdf.iloc[:,5:6])


#####################################

# calculating mean & std dev. Grouping by value in col FQN

mean = newdf.groupby('fqn')['time_diff'].mean(numeric_only=False)
std = newdf.groupby('fqn')['time_diff_float'].std(numeric_only=False)

#####################################

#convert seconds to HH:MM:SS to convert val of std dev back to raedable format

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)
     

# Driver program
std_hhmmss = convert(std)

#####################################
# Final result:

print("Mean time between starts: ",mean)
print("Standard devitatoin: " ,std_hhmmss)

# NEXT STEP tomorrow: read of tag in fqn from user input and assign to new variable to reuse the same file