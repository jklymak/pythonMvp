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
import os.path
#import numpy
import scipy.io as sio
from saveMatMvp import saveMatMvp,saveMatGrid

#datafolder = 'C:/Rowan/MVP/dat\data'
prefix = 'mvpdc15b_'
#remotefolder = 'C:/cygwin/home/analysis/Test/mvp/data/'
basedir='/Users/jklymak/DC15b/mvp/'
datafolder = basedir+'data/'
matCastfolder = basedir+'matCast/'
matGridfolder = basedir+'matGrid/'
pickleCastfolder = basedir+'pickleCast/'
pickleGridfolder = basedir+'pickleGrid/'
first=1
last=4000

sleeptime=20

depth_bins = np.arange(0.,320+0.1,1.)

while 1:
  badfiles=[]
  goodfiles=[]
  fexists=[]
  print "Translating: "+ datafolder+prefix+"*"
  inds = first
  while (inds<=last):
    dofile=1
    # check if we hwave already translated this file and that the translation 
    # is newer, in which case dont do this file
    rawname=datafolder+prefix+'%04d'%inds + '.raw'
    matname=matCastfolder+prefix+'%04d'%inds + '.mat'
    picklename=pickleCastfolder+prefix+'%04d'%inds + '.pickle'
    #print 'Checking ' + prefix+'%04d'%inds + '.raw' 
    if os.path.isfile(matname):
      matfiletime=os.path.getmtime(matname)
      rawfiletime=os.path.getmtime(rawname)
      if (matfiletime>=rawfiletime+10*60):
        dofile=0
    if not(os.path.isfile(rawname)):
      #print prefix+'%04d'%inds + '.raw doesn''t exist' 
      dofile=0
    else:
      fexists.append(inds)
    if dofile:
#      if 1:
      try:
        # translate:
        pgrid, header, data = loadMVP_raw(rawname,depth_bins)        
        # save!
        with  open(picklename,"wb") as pickf:
          print 'saving ' + prefix+'%04d'%inds + '.pickle' 
          pickle.dump(dict(raw=data,header=header,pgrid=pgrid),pickf)
        saveMatMvp(matname,data,header)
        goodfiles.append(inds)
      #else:
      except:
        badfiles.append(inds)
        print 'Error with file %04d' % inds
    inds = inds+1 # check the next file
  # done checking all the files that we wanted to check...
  
  
  print 'Done checking files: '
  print 'Files %d to %d exist' % (fexists[0],fexists[-1])
  print 'Files done:'
  print goodfiles
  print 'Bad files:'
  print badfiles
  
  print 'Waiting %1.0f s' % sleeptime 
  for ii in np.arange(0,sleeptime,1):
    time.sleep(1)
    print('.'),
  print 'Checking'


