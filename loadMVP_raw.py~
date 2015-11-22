# -*- coding: utf-8 -*-
"""
Created on Tue May 07 12:48:32 2013

@author: FoxR
"""
def loadMVP_raw(file,depthbins):
    
    import numpy as np
    from matplotlib.dates import date2num
    import datetime
    import seawater.eos80 as sw
    import numpy.lib.recfunctions as rec
    #import time
    import scipy.signal as signal
    #import bindata
    #from binMVPdata import binMVPdata
    import binMVPdata
    import calendar
   # try:
    if 1:
        
        f = open(file, 'r')
#        print ("Processing " + file)
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
        profile_xyt['unixtime'] = calendar.timegm(profile_xyt['datetime'].utctimetuple())
        profile_xyt['mtime'] = date2num(profile_xyt['datetime'])
        profile_xyt['matlabtime'] = date2num(profile_xyt['datetime'])+366.
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
            data = np.genfromtxt(file, usecols = (0,1,2,3), skip_header = 61,
                                 names = ["pressure","cond","temp","analog"])
        else:
            
            data = np.genfromtxt(file, usecols = (0,1,2), skip_header = 61,
                                 names = ["pressure","cond","temp"] )
            temparray = np.empty((data['pressure'].shape))
            temparray.fill(np.NaN)
            data = rec.append_fields(data,'analog',temparray,dtypes = float)
        # lag conductivity to match w. temp cell
        N = np.shape(data['cond'])[0]
        #print N
        data = rec.append_fields(data,'cond0',data['cond'],dtypes = float)
        
        tt=np.arange(0,N,1.)
        data['cond']=np.interp(tt-2.25,tt,data['cond0'])
        

        #this loop here will find the indices for when the fish is going down
        pressurederivative = np.diff(data['pressure']) # take the derivative of the pressure profile
        B, A = signal.butter(2, 0.01, output='ba') # constants for the filter
        smooth_pressurederivative = signal.filtfilt(B,A, pressurederivative) #filter the pressure derivative, to smooth out the curve
        smooth_pressurederivative = np.append(smooth_pressurederivative,[0]) # make the arrays the same size
        down_inds = np.where(smooth_pressurederivative>0.05) # find the indices where the descent rate is more than 0.1

        #depth_bins = np.arange(0,300,1)
        profile_grid = {}        
        for k in rawfields:
            profile_grid[k] = binMVPdata.binMVPdata(depthbins,
            data['pressure'][down_inds],data[k][down_inds])
        
        profile_grid['salinity'] = sw.salt(profile_grid['cond']/42.9140, 
            profile_grid['temp'], profile_grid['pressure'])
        profile_grid['density'] = sw.dens(profile_grid['salinity'],  
            profile_grid['temp'],profile_grid['pressure'])          
        profile_grid['pden'] = sw.pden(profile_grid['salinity'],  
            profile_grid['temp'],profile_grid['pressure'],0)          
        
        
        f.close()

        return profile_grid, profile_xyt, data
    
    #except:
        
     #   print ("Could not process " + file)

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

