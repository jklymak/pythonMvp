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
# 
#import os.path, time
#print "last modified: %s" % time.ctime(os.path.getmtime(file))
sleeptime = 20

filestodo=[]
gridname=[] # name of grid that we want to save
# do these files for this 
filestodo.append(np.arange(10,15,1))
gridname.append('testA') # testing
filestodo.append(np.arange(15,94,1))
gridname.append('SurveyA') # Caamano to 3/4 up Douglas
filestodo.append(np.arange(94,190,1))
gridname.append('SurveyB') # Doug 4 down east side.
filestodo.append(np.arange(190,354,1))
gridname.append('SurveyC') # Wright SOund spatial survey
filestodo.append(np.arange(354,438,1))
gridname.append('SurveyD') # Gardner Canal
filestodo.append(np.arange(438,519,1))
gridname.append('SurveyE') # Douglas Channel
filestodo.append(np.arange(438,566,1))
gridname.append('SurveyELong') # Douglas Channel + Caamano
filestodo.append(np.arange(520,631,1))
gridname.append('SurveyF') # Caamano to Hecate
filestodo.append(np.arange(631,729,1))
gridname.append('SurveyG') # Caamano Sound
filestodo.append(np.arange(729,1085,1))
gridname.append('SurveyH') # Fishtrap survey
filestodo.append(np.arange(1085,1117,1))
gridname.append('SurveyI') # Fishtrap to Wright
filestodo.append(np.arange(1117,1159,1))
gridname.append('SurveyJ') # Lewis Channel to Douglas Channel
filestodo.append(np.arange(1159,1250,1))
gridname.append('SurveyK') # Lewis Channel to Douglas Channel


print filestodo

depth_bins = np.arange(0.,320+0.1,1.)
depths = depth_bins

max_abs_pressure = 0 # this variable is used in plotting later
gridfields = ['temp','salinity','density','analog', 'pressure','pden']
gridxytfields = ['latitude','longitude','mtime','cast_number','unixtime','bottom']

badfiles=[]

try:
  os.remove('.PickleLock')
except:
  pass

while 1:
  for gridind in [11,12]: 
    # now make the grid.  This is just concatenating the gridded profiles stored
    # in the pickle
    n=0
    print ""
    print "Griding: ##################################"
    print ""
    cgrid=dict()
    cgrid['depths']=depths
    cgrid['cast_number']=[]
    print np.shape(cgrid['cast_number'])[0]>0
    gname=pickleGridfolder+gridname[gridind] + '.pickle'      
    gridexists=os.path.isfile(gname)
    print gridexists
    num=0
    for inds in filestodo[gridind]:
      picklename=pickleCastfolder+prefix+'%04d'%inds + '.pickle'
      if os.path.isfile(picklename):
        if (num==0):
          with  open(picklename,"rb") as pickf:
            a=pickle.load(pickf)
            pgrid = a['pgrid']
            header=a['header']
            for key in pgrid.keys():
              cgrid[key]=pgrid[key]
            for key in ['cast_number','latitude','longitude','mtime','matlabtime','bottom']:
              cgrid[key]=header[key]
            num=1
        else: # grid exists
          if 1:
            print 'Adding %s to the cgrid' % (prefix+'%04d'%inds + '.pickle')
            try:
              with  open(picklename,"rb") as pickf:
                a=pickle.load(pickf)
        
                pgrid = a['pgrid']
                header=a['header']
                for key in pgrid.keys():
                  cgrid[key]=np.hstack((cgrid[key],pgrid[key]))
                for key in ['cast_number','latitude','longitude','mtime','matlabtime','bottom']:
                  cgrid[key]=np.hstack((cgrid[key],header[key]))
            except:
              print 'Error adding file %04d to the pickle' % inds  
        
    with open('.PickleLock','wb') as lock:
      lock.write('Boo')
    with  open(gname,"wb") as pickf:
      print 'Saving ' + gname
      pickle.dump(cgrid,pickf)
    lock.close()
    os.remove('.PickleLock')

    matname=matGridfolder+gridname[gridind] + '.mat'    
    saveMatGrid(matname,cgrid)
          
  print 'Waiting %1.0f s' % sleeptime 
  for ii in np.arange(0,sleeptime,1):
    time.sleep(1)
    print('.'),
  print 'Checking'
