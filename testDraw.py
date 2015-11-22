# -*- coding: utf-8 -*-
"""
Created on Mon May 06 11:59:41 2013

@author: FoxR
"""

#def MVP_plots():
import matplotlib
import numpy as np  
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
import time
plt.ion()
  
print matplotlib.__version__
n=0
fig1 = plt.figure(1,(4,3.5))
  #plt.show()
while 1:
  print "MVP Plots"
  fig1.clf()
  plt.plot(np.arange(0,n,1))
  n=n+1       
  plt.draw()
  plt.pause(1.)
  print 'Redraw!'

    
    

    




