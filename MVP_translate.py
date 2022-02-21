import numpy as np
from loadMVP_raw import loadMVP_raw
import time
import os.path


prefix = 'mvpla16_'
basedir='/Users/jklymak/Dropbox/pythonMvp/sampledata/'
datafolder = basedir+'raw/'
ncCastfolder = basedir+'nccasts/'
first=1
last=4000

sleeptime=20

depth_bins = np.arange(0.,320+0.1,1.)

while 1:
  badfiles=[]
  goodfiles=[]
  fexists=[]
  print ("Translating: "+ datafolder+prefix+"*")
  inds = first
  while (inds<=last):
    dofile=1
    # check if we have already translated this file and that the translation
    # is newer, in which case dont do this file
    rawname=datafolder+prefix+'%04d'%inds + '.raw'
    ncname= ncCastfolder+prefix+'%04d'%inds + '.nc'
    if os.path.isfile(ncname):
      ncfiletime=os.path.getmtime(ncname)
      rawfiletime=os.path.getmtime(rawname)
      if (ncfiletime>=rawfiletime+10*60):
        dofile=0
    if not(os.path.isfile(rawname)):
      #print prefix+'%04d'%inds + '.raw doesn''t exist'
      dofile=0
    else:
      fexists.append(inds)
    if dofile:
      try:
        # translate:
        data = loadMVP_raw(rawname, condOffset=2.25)
        data.to_netcdf(ncname)
        goodfiles.append(inds)
      except:
        badfiles.append(inds)
        print('Error with file %04d' % inds)
    inds = inds+1 # check the next file
  # done checking all the files that we wanted to check...


  print('Done checking files: ')
  print('Files %d to %d exist' % (fexists[0],fexists[-1]))
  print('Files done:')
  print(goodfiles)
  print('Bad files:')
  print(badfiles)

  print('Waiting %1.0f s' % sleeptime)
  for ii in np.arange(0,sleeptime,1):
    time.sleep(1)
    print('.'),
  print('Checking')


