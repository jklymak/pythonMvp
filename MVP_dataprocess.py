# -*- coding: utf-8 -*-

"""
Created on Mon Mar 25 10:50:04 2013

@author: FoxR
"""
#def MVP_dataprocess():
import numpy as np
import glob
from loadMVP_raw import loadMVP_raw
import time
import cPickle as pickle

#datafolder = 'C:\\Rowan\\MVP\\dat\data'
datafolder = 'C:\\Rowan\\MVP\\dat\\testcopyfolder'
filenames_raw1 = glob.glob(datafolder + '\*.raw')

str1 = filenames_raw1[0].find('mvplm12_')
str2 = filenames_raw1[0].find('.raw')
filenumber_str = (filenames_raw1[0][str1+8:str2])
filenumber_int = int(filenames_raw1[0][str1+8:str2])

files_start = 0
files_todo = 50
files_num_success = 0
files_num_failed = 0
files_num_done = 0

files_name_failed = []# create a list of files that didn't load
files_name_success = []
files_name_done = []
# This says if the files_todo encompasses the final data file in the folder, then
# it will monitor for new data files. If the final data file is not in the range,
# then the program will not begin monitoring for enw data files
if files_todo + files_start > int(filenames_raw1[-1][str1+8:str2]):  
    files_todo =  int(filenames_raw1[-1][str1+8:str2]) - files_start
    monitor_newfiles = True
else:
    monitor_newfiles = False
#
grid_depth = np.arange(0,250,1)

max_abs_pressure = 0 # this variable is used in plotting later
gridfields = ['temp','salinity','density','analog', 'pressure']
gridxytfields = ['latitude','longitude','mtime','cast_number','unixtime']

grid_full = {}
for i in gridfields:
    grid_full[i] = np.empty([len(grid_depth),files_todo])
    grid_full[i][:] = np.NaN
  
gridxyt_full = {}  
for k in gridxytfields:
    #gridxyt_full[k] = np.zeros([1,files_todo])
    gridxyt_full[k] = np.empty((1,files_todo))
    gridxyt_full[k][:] = np.NaN

files_todo_names = filenames_raw1[files_start:(files_todo+files_start)]
for file in enumerate(files_todo_names):
    try:    
        grid_profile, grid_profilexyt, data = loadMVP_raw(file[1])
        for i in gridfields:
           try:
               grid_full[i][:,file[0]] = grid_profile[i][:,0]
           except:
               grid_full[i][:,file[0]] = np.NaN
        for k in gridxytfields:
            try:
                gridxyt_full[k][0,file[0]] = grid_profilexyt[k]
            except:
                gridxyt_full[k][0,file[0]] = np.NaN
        files_name_success.append(str(file[1]))
        files_num_success += 1
        
    except:
        print('WTF')
        files_name_failed.append(str(file[1]))
        files_num_failed += 1
    files_name_done.append(str(file[1]))
    files_num_done += 1

pickle.dump( grid_full, open("C:\\Rowan\\Python scripts\\save.p", "wb"))


print ('Gridded Data loaded.')
while monitor_newfiles == True:
    print('Monitoring for new data files, press Ctrl-C to stop.')
    for t in np.arange(0,5,1): # wait for this long
        time.sleep(1)
    filenames_raw2 = glob.glob(datafolder + '\*.raw')  #
    if not files_name_done == filenames_raw2:

        files_todo_names = filenames_raw2[files_start+files_num_done:-1]
        for file in enumerate(files_todo_names):
            try:    
                grid_profile, grid_profilexyt, data = loadMVP_raw(file[1])
                for i in gridfields:
                    #try:
                    #grid_full[i][:,file[0]+files_num_success-1] = grid_profile[i][:,0]
                     grid_full[i] = np.concatenate((grid_full[i],grid_profile[i]),axis = 1)
                    #except:
                        #grid_full[i][:,files_num_success+file[0]] = np.NaN
                for k in gridxytfields:

                    
                    #gridxyt_full[k] = np.concatenate((gridxyt_full[k],grid_profilexyt[k]),axis = 1)
                    test = np.reshape(grid_profilexyt[k], [1,1])
                    gridxyt_full[k] = np.concatenate((gridxyt_full[k],test),axis = 1)
                   
                files_name_success.append(str(file[1]))
                files_num_success += 1
                
            except:
                print('WTF')
                files_name_failed.append(str(file[1]))
                files_num_failed += 1
            files_num_done +=1
            files_name_done.append(str(file[1]))
            
                
    else:
        print('No new data files.')
    
#      'C:\\MVP\\dat\\testcopyfolder\\mvplm12_0580.raw'  
        
        
        
            
            
            
        
    
    
    
    
#    return grid_full, gridxyt_full


#grid_full, gridxyt_full = MVP_dataprocess()