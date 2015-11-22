# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:09:36 2013

@author: FoxR
"""

def bindata(binx,biny,x,y,X):
    
    import numpy as np

    N = np.size(binx,0)-1
    M = np.size(biny,0)-1     
    
    
    meanX = np.zeros((M,N))
    varX = np.zeros((M,N))
    nX = np.zeros((M,N))
    
    print np.shape(binx)
    print np.shape(np.arange(0,N,1.0))
    
    indx = np.floor(np.interp(x,binx,np.arange(0,N+1,1.0)))
    indx[indx<0]=0
    indx[indx>N-1]=N-1

    indy = np.floor(np.interp(y,biny,np.arange(0,M+1,1.0)))
    indy[indy<0]=0
    indy[indx>M-1]=M-1
    
    
    for ind in range(len(x)):
        meanX[indy[ind],indx[ind]]+=X[ind]
        nX[indy[ind],indx[ind]]+=1
    nX[nX==0.0]=np.NaN;
    meanX = meanX/nX;

    for ind in range(len(x)):
        varX[indy[ind],indx[ind]]+=(meanX[indy[ind],indx[ind]]-X[ind])**2
    varX=varX/nX
    # mask
    meanX=np.ma.masked_where(np.isnan(nX),meanX)
    nX=np.ma.masked_where(np.isnan(nX),nX)
    varX=np.ma.masked_where(np.isnan(nX),varX)
    
    return meanX,varX,nX