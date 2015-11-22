# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 10:50:04 2013

@author: FoxR
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib.dates import num2date
import os
import datetime
import time
import glob
import seawater.csiro as sw


#datafolder = 'C:\MVP\dat\data'
datafolder = 'C:\MVP\dat\\testcopyfolder'
rawfiles1 = glob.glob(datafolder + '\*.raw')
str1 = rawfiles1[0].find('mvplm12_')
str2 = rawfiles1[0].find('.raw')
int(rawfiles1[0][str1+8:str2])

files_start = 50
files_todo = 100


if files_todo + files_start > int(rawfiles1[-1][str1+8:str2]):
    files_todo =  int(rawfiles1[-1][str1+8:str2]) - files_start

#if files_todo > int(rawfiles1[-1][34:38]):
#    files_todo = int(rawfiles1[-1][34:38])
    
#os.chdir('C:\MVP\dat\data') #Change working directory





grid_depth = np.arange(0,250,1)
#grid_depth_midpoint = np.arange(0.5,250.5,1)
failedloadfiles = []# create a list of files that didn't load
max_abs_pressure = 0 # this variable is used in plotting later
grid_salinity = np.zeros([len(grid_depth),files_todo])
grid_temp = np.zeros([len(grid_depth),files_todo])
grid_density = np.zeros([len(grid_depth),files_todo])
grid_analog = np.zeros([len(grid_depth),files_todo])
grid_latitude = np.zeros([1,files_todo])
grid_longitude = np.zeros([1,files_todo])
grid_mtime = np.zeros([1,files_todo])

for file in enumerate(rawfiles1[files_start:(files_todo+files_start)]):
    try:
        
        f = open(file[1], 'r')
        print ("Processing " + file[1])
        header = f.read(7000) #read in 7000 bytes to get the header
        
        xyzt = {}
        i = header.find('LAT ( ddmm.mmmmmmm,N):')
        xyzt['lat_DDMM.mm'] = header[i+23:i+36]
        xyzt['lat_hemisphere'] = header[i+37:i+38]
        xyzt['lat_DD.dd'] =  (float(xyzt['lat_DDMM.mm'][1:3])) + (np.divide((float(xyzt['lat_DDMM.mm'][3:])),60))
        grid_latitude[:,file[0]] = xyzt['lat_DD.dd']
        i = header.find('LON (dddmm.mmmmmmm,E):')
        xyzt['lon_DDMM.mm'] = header[i+23:i+36]
        xyzt['lon_hemisphere'] = header[i+37:i+38]
        xyzt['lon_DD.dd'] =  (float(xyzt['lon_DDMM.mm'][1:3])) + (np.divide((float(xyzt['lon_DDMM.mm'][3:])),60))
        grid_longitude[:,file[0]] = xyzt['lon_DD.dd']
        i = header.find('Time (hh|mm|ss.s):')
        xyzt['time'] = header[i+19:i+29]
        i = header.find('Date (dd/mm/yyyy):')        
        xyzt['date'] = header[i+19:i+29]
        datetimestring = xyzt['date']+' '+xyzt['time']
        datetimefmt = ('%d/%m/%Y %H:%M:%S.%f')
        xyzt['datetime'] = datetime.datetime.strptime(datetimestring, datetimefmt)
        xyzt['mtime'] = date2num(xyzt['datetime'])
        grid_mtime[:,file[0]] = xyzt['mtime']
        #
        newline1 = header.find('\n',6000,len(header))
        newline2 = header.find('\n',newline1+1,len(header))
        #newline2-newline1
        if newline2 - newline1 ==33:
            cols = (0,1,2,3)
            names = ["pressure","cond","temp","analog"]
            names2 = ['temp','salinity','density','analog']
        
        else:
            cols = (0,1,2)
            names = ["pressure","cond","temp"]
            names2 = ['temp','salinity','density']
        
        data = np.genfromtxt(file[1], usecols = cols, skip_header = 61,names = names )
            #data = np.genfromtxt(file, delimiter =' ', skip_header = 61)
        
        
        m = max(data['pressure'])
        if m > max_abs_pressure:
            max_abs_pressure = m
        m_ind = [i for i, j in enumerate(data['pressure']) if j ==m] # this line finds the index of the max depth
        
        
        #this loop here will take the readings only when the fish is going down
        for j in names:
            vars()[j] = []
            for i in np.arange(1,float(m_ind[0])):
                if data['pressure'][i]-data['pressure'][i-1] >0:
                    vars()[j].append(data[str(j)][i])
                    
        depth = sw.depth(pressure, xyzt['lat_DD.dd'])        
        c3515 = 42.9140
        condr = [x/c3515 for x in cond]
        salinity = sw.salt(condr, temp, pressure)
        density = sw.dens(salinity, temp,pressure)  
        griddeddata=[]
    
        for k in names2:
            griddeddata = np.interp(grid_depth,depth,vars()[k],right=np.NaN)
            griddeddata = griddeddata[0:]
            vars()['grid_'+k][:,file[0]] = vars()['griddeddata']

        f.close()
    except:
        failedloadfiles.append(str(file))
        print ("Could not process " + file[1])
        for k in names2:
            vars()['grid_'+k][:,file[0]] = np.NaN


# Once loop is done, create a mesgrid 
grid_depth2 = grid_depth.reshape(-1,1)
grid_mtime2 = grid_mtime.reshape(-1,1)
X, Y = np.meshgrid(grid_mtime2, grid_depth2)

print('Gridded Data loaded.')

#Check to see if a new data file has been added to the directory, if so, append the data grids        
time_to_wait = 1

while True:
    print('Monitoring for new data files, press Ctrl-C to quit')
    rawfiles2 = glob.glob(datafolder + '\*.raw')
    
    if rawfiles1 != rawfiles2:
        print('1')
        
    
    else:
        print('No new data files, sleep for ' + str(time_to_wait) + ' seconds')
        
    time.sleep(time_to_wait)


            
        

    

    

#fig3 = plt.figure()
#X, Y = np.meshgrid(test3, grid_depth)
#ax1 = plt.contourf(X, Y, grid_temp)
#ax1.set_ylim(ax1.get_ylim()[::-1])

#draw()
