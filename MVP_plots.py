# -*- coding: utf-8 -*-
"""
Created on Mon May 06 11:59:41 2013

@author: FoxR
"""

#def MVP_plots():
if 1:
  import cPickle as pickle
  import numpy as np
  import matplotlib
  import sys

  matplotlib.use('Qt4Agg')
  import matplotlib.pyplot as plt
  import matplotlib.dates  as mdates
  import matplotlib.gridspec as gridspec
  import matplotlib.cm as cm
  import time,datetime
  import seawater.eos80 as sw
  import scipy.io as sio
  
  import os.path
  
  surveygridname='/Users/jklymak/DC15b/mvp/pickleGrid/surveyJ.pickle'
  density_contours = np.arange(1022, 1029, 0.25)    
  density_contourslab = np.arange(1022, 1029, 0.5)    
  ncasts=60
      
  todo3=['temp','salinity','O2']
  clim3=[[7.0,12],[28,33.5],[0,135.]]
  title3=['Temp [C]','S [psu]','O2 [%sat]']
  ylims3=[220,0] 

  lonlim = [-129.2,-128.4]
  latlim=[52,53.7]   
  latlim=[52.65,53.99]   
  lonlim = [-130.,-128.4]
  plt.ion()

  topo=pickle.load(open('coarsebathy.pickle','rb'))

  wpslat = 48.+np.array([0.61, .387, .497, .286, .487, .283, .148])
  wpslon = -125-np.array([.910, 1.019, .705, .869, .481, .349, .680])   
  # get waypoints from Svein's file
  #dat = np.loadtxt('Sveinsroute.RTE',delimiter='|',skiprows=1  )  
  #wpslon = dat[:,6]
  #wpslat = dat[:,5]

  sp = pickle.load(open('SpiceDef.pickle','rb'))

  def pw13spice(sal,temp,pden):
    beta = 7.7e-4*1000
    alpha = 2.0e-4*1000
    mt=reshape(mt,shape(temp))
    tau=2*(temp-mt)*0.2
    Sline=np.array([33.2,33.8])
    Tline=np.array([7.75,6.6])
    Sarray = np.arange(30,35,0.01)
    m = (np.diff(Tline)/np.diff(Sline))
    Tarray = m*(Sarray-Sline[0])+Tline[0]
    Pdarray=sw.pden(Sarray,Tarray,100.+0.*Tarray,0.)

    T0 = np.interp(pden,sp['pdengrid'][:-1],sp['meanT'][0])
    tau = 2*alpha*(temp-T0)
    return tau

  def dc15bspice(sal,temp,pden):
    pd=pden.flatten()-1000.
    good = np.where(np.isfinite(pd))
    mt=0.*pd
    
    mt[good]=np.interp(pd[good],sp['pdengrid'][:-1]+0.5*np.diff(sp['pdengrid']),sp['meanT'][0])
    mt=np.reshape(mt,np.shape(temp))
    tau=2*(temp-mt)*0.2
    return tau

  def getO2(analog,temp,depths):
    DO_A = -4.262146e+01;
    DO_B = +1.426020e+02;
    DO_C = -3.346404e-01;
    DO_D = +1.110000e-02;
    DO_E = +4.500000e-03;
    DO_F = +0.000000e+00;
    DO_G = +0.000000e+00;
    DO_H = +1.000000e+00;
    
    M,N=np.shape(temp)
    Pprime = DO_A / (1 + DO_D *(temp - 25.))+DO_B / ((analog - DO_F) * (1. + DO_D *(temp - 25.)) + DO_C + DO_F);
    DO = (DO_G + DO_H * Pprime) * (1.+DO_E * np.tile(np.reshape(depths,(M,1)),(1,N)));
    return DO



  while 1:
    if 1:
   # try:
      while os.path.exists('.PickleLock'):
        print('.PickleLock Exists\n')
        time.sleep(2)

        trying=True
        while trying:
          try:
            pickf = open(surveygridname,"rb") 
            grid_full=pickle.load(pickf)
            pickf.close()
            trying=False
          except:
            try:
              pickf.close()
            except:
              pass
            #print("Error:", sys.exec_info()[0])
            time.sleep(2)
            #print sys.last_value
            print 'Trying'
            trying=True
        print np.shape(grid_full['depths'])
        print np.shape(grid_full['temp'])
        grid_full['O2']=getO2(grid_full['analog'],grid_full['temp'],grid_full['depths'])
        print grid_full.keys()
        #def MVP_plots(grid_full):
        
        
        print "MVP Plots"
        fig1 = plt.figure(1,(16,10.5))
        plt.show()
        fig1.clf()
    
        # grid layout:
        gs3b3 = gridspec.GridSpec(4,3)
        # MVP Plots
        
        #plt.ion()
        plt.ioff
        X = grid_full['cast_number']
        Y = grid_full['depths']
            
        def contourZ(X,Y,Z,D,depth,contours,contourslab,cl,tit,cmap=matplotlib.cm.jet):
          xx = np.arange(min(X)-0.5,max(X)+0.51,1.)
          pc = plt.pcolormesh(xx,Y,np.ma.masked_where(np.isnan(Z),Z), vmin = cl[0], vmax = cl[1],rasterized=True,cmap=cmap)
          cb = plt.colorbar(pc, format = '%2.2f', orientation = 'vertical', pad = 0.08)
          cb.set_label(tit, fontweight='bold')
          plt.contour(X, Y, D-1000.,contours-1000., colors = 'k')
          co=plt.contour(X, Y, D-1000.,contourslab-1000., colors = 'k')
          print co
          plt.plot(X,depth,'k',linewidth=2)
          plt.clabel(co, colors = 'k', fmt = '%1.1f', fontsize = 7, use_clabeltext = True)
          plt.ylim(ylims3)
          plt.xlim(X[-1]+np.array([-ncasts,0.5]))
          return pc
          
          
        ax=[]
        for num,ind,clim,tit in zip([1,2,3],todo3,clim3,title3):
          Z = grid_full[ind]  
          print clim
          print ind
          print tit
          ax.append(plt.subplot(gs3b3[num-1,0:2]))
          plt.gca().set_axis_bgcolor('0.6')

          contourZ(X,Y,Z,grid_full['pden'],grid_full['bottom'],
                   density_contours,density_contourslab,clim,tit)
        plt.xlabel('Cast #')
        plt.ylabel('DEPTH [m]')
        #contourZ(X,Y,Z,density_contours,(cmin,cmax))
        #cb.set_label('Temp (degC)', fontweight='bold')
        #cmin = np.nanmin(Z)
        #cmax = np.nanmax(Z)
        
        starttime = mdates.num2date(grid_full['mtime'][0]).strftime('%Y-%m-%d %H:%M:%S')
        endtime = mdates.num2date(grid_full['mtime'][-1]).strftime('%H:%M:%S')
        #endtime = (datetime.datetime.fromtimestamp(grid_full['unixtime'][0,-1])).strftime('%Y-%m-%d %H:%M:%S')
        startendstring = ('Cast '+ str(int(grid_full['cast_number'][0])) + 
           ' at ' + starttime +' \nCast '+ str(int(grid_full['cast_number'][-1])) + ' at ' + endtime) 
        ax[0].set_title(startendstring,fontsize = 12)

        
        ### TS plot    
        plt.subplot(gs3b3[0:2,2])
        plt.plot(grid_full['salinity'][:,-ncasts:],grid_full['temp'][:,-ncasts:],'k.',markersize=1)  
        plt.plot(grid_full['salinity'][:,-2],grid_full['temp'][:,-2],'m.')  
        plt.plot(grid_full['salinity'][:,-1],grid_full['temp'][:,-1],'r.') 
        ss=np.linspace(np.nanmin(grid_full['salinity']),np.nanmax(grid_full['salinity']),50 )
        tt=np.linspace(np.nanmin(grid_full['temp']),np.nanmax(grid_full['temp']),50 )
        SS,TT=np.meshgrid(ss,tt)
        PDen=sw.pden(SS,TT,0.*TT,0)       
        
        cs=plt.contour(ss,tt,PDen-1000.,density_contours-1000.,colors='k')  
        plt.clabel(cs,fmt='%1.1f')
        plt.xlabel('S [psu]')
        plt.ylabel('T [C]')
        plt.xlim(clim3[1])
        plt.ylim(clim3[0])
        #plt.draw()

        ### Spice plot
        grid_full['spice']=dc15bspice(grid_full['salinity'],grid_full['temp'],grid_full['pden'])
        aa=ax.append(plt.subplot(gs3b3[3,0:2]))
        plt.gca().set_axis_bgcolor('0.6')
        clim=[-.5,0.5]
        pc=contourZ(X,Y,np.ma.masked_where(np.isnan(grid_full['spice']),
                  grid_full['spice']),grid_full['pden'],
                  grid_full['bottom'],density_contours,density_contourslab,
                  clim,'Spice',cmap=matplotlib.cm.RdBu_r)
        
        
#     
        axgeo=plt.subplot(gs3b3[2:4,2])
        print grid_full['longitude']
        plt.plot(wpslon,wpslat,'m')
        plt.plot(wpslon,wpslat,'om',markersize=6)
        plt.plot(grid_full['longitude'][-ncasts:]-100,grid_full['latitude'][-ncasts:],'k.',markersize=3)  
        plt.plot(grid_full['longitude'][-1]-100,grid_full['latitude'][-1],'rd',markersize=8)
        print np.shape(np.squeeze(topo['lon']))
        print np.shape(topo['lat'])
        xx=topo['lon'][:-1];yy=topo['lat'][:-1]
        cs=plt.contour(np.squeeze(topo['lon'][:-1]),np.squeeze(topo['lat'][:-1]),topo['dep'],np.arange(0,600,200),linestyles='-',linewidth=1.5,colors='0.5')
#        plt.clabel(cs,fontsize=8)
        cs=plt.contour(np.squeeze(topo['lon'][:-1]),np.squeeze(topo['lat'][:-1]),topo['dep'],np.arange(0,600,50),linestyles='-',linewidth=0.2,colors='0.5')
#       
        plt.contour(np.squeeze(topo['lon'][:-1]),np.squeeze(topo['lat'][:-1]),topo['dep'],[0,0],linestyles='-',linewidth=1.5,colors='0.2')
        plt.pcolormesh(xx,yy,topo['dep'],cmap=cm.ocean_r)
        plt.clim([0,1200])         
        plt.ylim(latlim)
        plt.xlim(lonlim)
        plt.colorbar(shrink=0.4)

        plt.xlabel('Lon [o]')
        plt.ylabel('Lat [o]')
        axgeo.set_aspect(1./np.cos(np.mean(np.pi/180.*grid_full['latitude'])))
        plt.title(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        plt.draw()
        print 'Pause!'
        plt.pause(40.)
        print 'Process'
        #execfile(r'/Users/jklymak/pythonMvp/MVP_dataprocessJMK.py')
        print 'Redraw!'
        
    else:
#    except:
      print 'Something broke.  Trying again '
      plt.pause(6.)

#    plt.savefig('C:\\Rowan\\MVP\\dat\\testcopyfolder\\test')#, format = 'png')
    
    

    




