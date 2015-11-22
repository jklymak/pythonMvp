# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 15:06:21 2013

@author: analysis
"""
import scipy.io as sio
def saveMatMvp(matname,data,header):
  """ 
  Need to save the MVP data in a matlab set of structures, so need to unpack
  """
  from matplotlib.dates import date2num
  import datetime
  str=""
  for fnames in data.dtype.names:
    str=str+ "'"+fnames +"'"+ ":data['"+fnames+"'],"
  header['datetime']=date2num(header['datetime'])
  
  for fnames in header.keys():
    str=str+ "'"+fnames +"'"+ ":header['"+fnames+"'],"
    
  str="sio.savemat('"+matname+"',{"+str+"})"
  
#  print 'Saving ' + matname
  
  exec(str)
  
def saveMatGrid(matname,cgrid):
  """ 
  Need to save the MVP data in a matlab set of structures, so need to unpack
  """
  from matplotlib.dates import date2num
  import datetime
  str=""    
  for fnames in cgrid.keys():
    str=str+ "'"+fnames +"'"+ ":cgrid['"+fnames+"'],"    
  str="sio.savemat('"+matname+"',{"+str+"})"
  
  #  print 'Saving ' + matname
  
  exec(str)
  