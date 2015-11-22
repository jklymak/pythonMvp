# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:09:36 2013

@author: FoxR
"""
#file = 'C:\\MVP\\dat\\testcopyfolder\\mvplm12_0150.raw'
#from loadMVP_raw import loadMVP_raw

#profile_grid, profile_xyt, data = loadMVP_raw(file)

def binMVPdata(binx,x,X):
    
    import numpy as np
    
    N = np.size(binx,0) # 
    
    
    meanX = np.zeros((N,1))  #placeholder for the mean value in the bin
    sumX = np.zeros((N,1))  #placeholder for the sum in the bin
    varX = np.zeros((N,1))  #placeholder for variance in the bin
    nX = np.zeros((N,1))    #placeholder for the number of samples in the bin
    
    #print ('Gridded data length: ' + str(len(binx)))
    #print ('Data length: ' + str(len(x)))
    
    indx = np.floor(np.interp(x,binx,np.arange(0,N,1.0)))
    #indx[indx<0]=0
    #indx[indx>N-1]=N-1
    
    #indy = np.floor(np.interp(y,biny,np.arange(0,M+1,1.0)))
    #indy[indy<0]=0
    #indy[indy>M-1]=M-1
    
    
    #for ind in range(len(x)):
    #    meanX[indy[ind],indx[ind]]+=X[ind]
    #    nX[indy[ind],indx[ind]]+=1
    for ind in range(len(x)): #increments on the number of lines in X
        sumX[indx[ind],0]+=X[ind]
        nX[indx[ind],0]+=1
        varX[indx[ind],0]+=(meanX[indx[ind],0]-X[ind])**2
    
    nX[nX==0.0]=np.NaN
    meanX = sumX/nX
    
    #for ind in range(len(x)):
        
    varX = varX/nX
    # mask
    #meanX = np.ma.masked_where(np.isnan(nX),meanX)
    #sumX = np.ma.masked_where(np.isnan(nX),sumX)
    #nX = np.ma.masked_where(np.isnan(nX),nX)
    #varX = np.ma.masked_where(np.isnan(nX),varX)
    
    return meanX
    

    
    

    
    