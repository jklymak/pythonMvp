# -*- coding: utf-8 -*-
"""
Created on Mon May 06 15:25:29 2013

@author: FoxR
"""
import time

while True:
    
    
    print('1')
    #n = None
    #n = raw_input(('Monitoring for new data files, press q to quit. '))   
    #if n == "q":
    #    break
    #else:
    #    print ('2')
    rawfiles2 = glob.glob(datafolder + '\*.raw')
    if rawfiles1 == rawfiles2:
        break
    else:
        print('2')
    
    time.sleep(3)
print ('3')    
