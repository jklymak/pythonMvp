# -*- coding: utf-8 -*-
"""
Created on Wed May 01 11:20:18 2013

@author: FoxR
"""

#test program, to imitate tehe MVP writing new files to a folder.  I'll write 
#this program to periodically copy files from teh raw data folder into a test folder

import os
import glob
import shutil
import time

copy_sourcefolder = 'C:\\Rowan\\MVP\\dat\\data' #folder from which to draw files
copy_destfolder = 'C:\\Rowan\\MVP\\dat\\testcopyfolder' #folder to copy files to
os.chdir('C:\\Rowan\\MVP\\dat\\data') #Change working directory
rawfiles1 = glob.glob(copy_sourcefolder + '\*.raw')  #list of files in the original data folder


#copy_file_source = rawfiles1[-1]


for file in enumerate(rawfiles1):
    rawfiles2 = glob.glob(copy_destfolder + '\*.raw')  #list of files already copied in to test folder
    if len(rawfiles2) == 0:
        oldfilenumber = 0 
    else:
        oldfilenumber = int(rawfiles2[-1][40:44])
    newnumber = oldfilenumber + 1 
    copy_sourcefile = rawfiles1[-1][0:30] + str(newnumber).zfill(4) + rawfiles1[-1][34:]
    copy_destfile = copy_destfolder + copy_sourcefile[-17:]
    #copy_destfile = rawfiles2[-1][0:40] + str(newnumber).zfill(4) + rawfiles1[-1][34:]
    
    
    
    
    if not os.path.isfile(copy_destfile):
        
        shutil.copy(copy_sourcefile, copy_destfolder)
        print('Copying ' + copy_sourcefile)
        
    time.sleep(10)

print("done")    
        
        
        







