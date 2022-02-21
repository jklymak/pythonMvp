# -*- coding: utf-8 -*-
"""
Created on Tue May 07 12:48:32 2013

@author: FoxR
"""
import numpy as np
from matplotlib.dates import date2num
import datetime
import seawater.eos80 as sw
import numpy.lib.recfunctions as rec
#import time
import scipy.signal as signal
import binMVPdata
import calendar
import xarray as xr

def loadMVP_raw(file,depthbins):
       # try:
    with open(file, 'r') as f:
        header = f.read(7000) #read in 7000 bytes to get the header

        profile_xyt = {}
        i = header.find('LAT ( ddmm.mmmmmmm,N):')
        profile_xyt['lat_DDMMmm'] = header[i+23:i+36]
        profile_xyt['lat_hemisphere'] = header[i+37:i+38]
        profile_xyt['latitude'] = (float(profile_xyt['lat_DDMMmm'][1:3])) +(np.divide((float(profile_xyt['lat_DDMMmm'][3:])),60))
        if (profile_xyt['lat_hemisphere']=='S'):
          profile_xyt['latitude']=-profile_xyt['latitude']

        i = header.find('LON (dddmm.mmmmmmm,E):')
        profile_xyt['lon_DDMMmm'] = header[i+23:i+36]
        profile_xyt['lon_hemisphere'] = header[i+37:i+38]
        profile_xyt['longitude'] =  (float(profile_xyt['lon_DDMMmm'][1:3])) +(np.divide((float(profile_xyt['lon_DDMMmm'][3:])),60))
        if profile_xyt['lon_hemisphere']=='W':
          profile_xyt['longitude'] =-profile_xyt['longitude']

        i = header.find('Time (hh|mm|ss.s):')
        profile_xyt['time'] = header[i+19:i+29]
        i = header.find('Date (dd/mm/yyyy):')
        profile_xyt['date'] = header[i+19:i+29]
        datetimestring = profile_xyt['date']+' '+profile_xyt['time']
        datetimefmt = ('%d/%m/%Y %H:%M:%S.%f')
        #print datetimestring[:-5]
        try:
            profile_xyt['datetime'] = datetime.datetime.strptime(datetimestring, datetimefmt)
        except:
            datetimefmt = ('%d/%m/%Y %H:%M')
            profile_xyt['datetime'] = datetime.datetime.strptime(datetimestring[:-5], datetimefmt)
        profile_xyt['datetime'] = np.datetime64(profile_xyt['datetime'])
        profile_xyt['tzone'] = 'Z'
        i = header.find('Index: ')
        profile_xyt['cast_number'] = int(header[i+7:i+11])
 #       profile_xyt['datetime']=date2num(profile_xyt['datetime'])
        #
        i = header.find('Bottom Depth (m):')
        profile_xyt['bottom']=float(header[i+17:i+22])
        # print profile_xyt['bottom']
        newline1 = header.find('\n',6000,len(header))
        newline2 = header.find('\n',newline1+1,len(header))
        rawfields = ["pressure","cond","temp","analog"]

        if newline2 - newline1 > 26:
            data0 = np.genfromtxt(file, usecols = (0,1,2,3), skip_header = 61,
                                 names = ["pressure","cond","temp","analog"])
        else:

            data0 = np.genfromtxt(file, usecols = (0,1,2), skip_header = 61,
                                 names = ["pressure","cond","temp"] )
            temparray = np.empty((data0['pressure'].shape))
            temparray.fill(np.NaN)
            data0 = rec.append_fields(data0,'analog', temparray, dtypes = float)
        # convert from data0 to data
        data = xr.Dataset(data_vars=dict(
                temperature=(['index'], data0['temp']),
                conductivity0=(['index'], data0['cond']),
                pressure=(['index'], data0['pressure']),
                longitude=(['profile'], [profile_xyt['longitude']]),
                latitude=(['profile'], [profile_xyt['latitude']]),
                datetime=(['profile'], [profile_xyt['datetime']]),
                cast_number=(['profile'], [profile_xyt['cast_number']]),
                bottom=(['profile'], [profile_xyt['bottom']]),
            ),
        )
        N = len(data['index'])
        tt=np.arange(0,N,1.)
        data['condutivity']=np.interp(tt-2.25,tt,data['conductivity0'])

        return data


def binMVPdata(binx,x,X):

    import numpy as np

    N = np.size(binx,0) #


    meanX = np.zeros((N,1))  #placeholder for the mean value in the bin
    sumX = np.zeros((N,1))  #placeholder for the sum in the bin
    varX = np.zeros((N,1))  #placeholder for variance in the bin
    nX = np.zeros((N,1))    #placeholder for the number of samples in the bin


    indx = np.floor(np.interp(x,binx,np.arange(0,N,1.0)))

    for ind in range(len(x)): #increments on the number of lines in X
        sumX[indx[ind],0]+=X[ind]
        nX[indx[ind],0]+=1
        varX[indx[ind],0]+=(meanX[indx[ind],0]-X[ind])**2

    nX[nX==0.0]=np.NaN
    meanX = sumX/nX

    varX = varX/nX


    return meanX


#file = 'C:\\Rowan\\MVP\\dat\\data\\mvplm12_0650.raw'
#profile_grid, profile_xyt, data = loadMVP_raw(file)

