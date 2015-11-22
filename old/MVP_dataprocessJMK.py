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

filestodo=[]
gridname=[] # name of grid that we want to save
# do these files for this grid
filestodo.append(np.arange(2,15,1))
gridname.append('TestA')
filestodo.append(np.arange(15,615,1))
gridname.append('SurveyA')

depth_bins = np.arange(0.,320+0.1,1.)
depths = depth_bins

max_abs_pressure = 0 # this variable is used in plotting later
gridfields = ['temp','salinity','density','analog', 'pressure']
gridxytfields = ['latitude','longitude','mtime','cast_number','unixtime']

badfiles=[]



for gridind in [1]: 
  print "Translating: "+ datafolder+prefix+"*"

  for inds in filestodo[gridind]:
    dofile=1
    # check if we hwave already translated this file and that the translation 
    # is newer, in which case dont do this file
    rawname=datafolder+prefix+'%04d'%inds + '.raw'
    matname=matCastfolder+prefix+'%04d'%inds + '.mat'
    picklename=pickleCastfolder+prefix+'%04d'%inds + '.pickle'
    print 'Checking ' + prefix+'%04d'%inds + '.raw' 
    if os.path.isfile(matname):
      matfiletime=time.ctime(os.path.getmtime(matname))
      rawfiletime=time.ctime(os.path.getmtime(rawname))
      if (matfiletime>=rawfiletime):
        dofile=0
        
    if dofile:
      try:
        # translate:
        pgrid, header, data = loadMVP_raw(rawname,depth_bins)
        
        print pgrid.keys()
        # save!
        with  open(picklename,"wb") as pickf:
          print 'saving ' + prefix+'%04d'%inds + '.pickle' 
          print pgrid.keys()
          pickle.dump(dict(raw=data,header=header,pgrid=pgrid),pickf)
        saveMatMvp(matname,data,header)
      except:
        
        badfiles.append(inds)
        print 'Error with file %04d' % inds
  # done checking all the files that we wanted to check...
  # now make the grid.  This is just concatenating the gridded profiles stored
  # in the pickle
  n=0
  print ""
  print "Griding: ##################################"
  print ""
  cgrid=dict()
  cgrid['depths']=depths
  for inds in filestodo[gridind]:
    picklename=pickleCastfolder+prefix+'%04d'%inds + '.pickle'
    print 'Adding %s to the cgrid' % (prefix+'%04d'%inds + '.pickle')
    try:
      with  open(picklename,"rb") as pickf:
        a=pickle.load(pickf)
        print a['pgrid'].keys()
        pgrid = a['pgrid']
        header=a['header']
        if not(cgrid.has_key('temp')):
          for key in pgrid.keys():
            print key
            cgrid[key]=pgrid[key]
          for key in ['cast_number','latitude','longitude','mtime','matlabtime']:
            cgrid[key]=header[key]
        else:
          for key in pgrid.keys():
            cgrid[key]=np.hstack((cgrid[key],pgrid[key]))
          for key in ['cast_number','latitude','longitude','mtime']:
            cgrid[key]=np.hstack((cgrid[key],header[key]))
    except:
      print 'Error adding file %04d to the pickle' % inds  
  print cgrid.keys()
  picklename=pickleGridfolder+gridname[gridind] + '.pickle'
  with  open(picklename,"wb") as pickf:
    print 'Saving ' + picklename
    pickle.dump(cgrid,pickf)
  
  matname=matGridfolder+gridname[gridind] + '.mat'    
  saveMatGrid(matname,cgrid)
