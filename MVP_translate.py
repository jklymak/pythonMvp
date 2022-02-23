import numpy as np
import os.path
import seawater as sw
import xarray as xr
import logging
import datetime

def loadMVP_raw(file, condOffset=2.25):
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
      newline1 = header.find('\n',6000,len(header))
      newline2 = header.find('\n',newline1+1,len(header))
      rawfields = ["pressure","cond","temp","analog"]

      if newline2 - newline1 > 26:
          data0 = np.genfromtxt(file, usecols = (0,1,2,3), skip_header = 61,
                                names = ["pressure","cond","temp","analog"])
          analog = True
      else:
          analog = False
          data0 = np.genfromtxt(file, usecols = (0,1,2), skip_header = 61,
                                names = ["pressure","cond","temp"] )

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
      data['conductivity']=np.interp(tt-condOffset, tt, data['conductivity0'])
      data['salinity'] = sw.eos80.salt(data['conductivity']/ sw.constants.c3515, data['temperature'],
                                  data['pressure'])
      data['pden'] = sw.eos80.pden(data['salinity'], data['temperature'],
                                  data['pressure'], 0)

      if analog:
          data['analog'] = data0['analog']

      return data


logger = logging.getLogger(__name__)
def raw_to_netcdf(datafolder, ncCastfolder, prefix, first=1, last=5000):

  newFile = False
  badfiles=[]
  goodfiles=[]
  fexists=[]
  print ("Translating: "+ datafolder+prefix+"*")
  print ("  to: "+ ncCastfolder)
  inds = first
  while (inds<=last):
    dofile=True
    # check if we have already translated this file and that the translation
    # is newer, in which case dont do this file
    rawname=datafolder+prefix+'%04d'%inds + '.raw'
    logname=datafolder+prefix+'%04d'%inds + '.log'
    ncname= ncCastfolder+prefix+'%04d'%inds + '.nc'
    if os.path.isfile(ncname):
      ncfiletime=os.path.getmtime(ncname)
      rawfiletime=os.path.getmtime(rawname)
      if (ncfiletime>=rawfiletime+10*60):
        dofile=False
    if not(os.path.isfile(rawname)):
      #print prefix+'%04d'%inds + '.raw doesn''t exist'
      dofile=False
    else:
      # file exists, but is the cast done?
      done = False
      with open(logname, 'r') as flog:
        for l in flog:
          if 'SUMMARY' in l:
            done = True
            break
      if done:
        fexists.append(inds)
      else:
        dofile = False
    if dofile:
      try:
        # translate:
        newFile = True
        logger.info(f'opening {rawname}')
        data = loadMVP_raw(rawname, condOffset=2.25)
        logger.info(f'writing {ncname}')
        data.to_netcdf(ncname)
        goodfiles.append(inds)
      except:
        badfiles.append(inds)
        logger.info('Error with file %04d' % inds)
    inds = inds+1 # check the next file
  # done checking all the files that we wanted to check...

  logger.info('Done checking files: ')
  logger.info('Files %d to %d exist' % (fexists[0],fexists[-1]))
  logger.info('Files done:')
  logger.info(goodfiles)
  logger.info('Bad files:')
  logger.info(badfiles)

  return newFile



def mvpgridfield(depth_bins, cast, td):
  p = np.convolve(np.ones(10) / 10, cast['pressure'], mode='same')
  dp = np.diff(p)
  good = np.where(dp>0.05)
  dat = depth_bins[1:] * np.NaN
  if len(good) > 0:
    with np.errstate(invalid='ignore'):
      dat = (np.histogram(cast['pressure'][good], weights=cast[td][good],
                          bins=depth_bins)[0] /
            np.histogram(cast['pressure'][good],
                          bins=depth_bins)[0])
  return dat

def profiles_to_grid(depth_bins, filestodo, ncCastfolder, prefix, outFilen):

  depths = (depth_bins[1:] + depth_bins[:-1]) / 2

  gridfields = ['temperature','salinity','analog', 'pressure','pden']
  gridxytfields = ['latitude','longitude','datetime','bottom']

  analog = False
  # now make the grid.  This is just concatenating the gridded profiles stored
  # in the pickle
  Ncasts = len(filestodo)
  Nbins = len(depths)
  logger.info("Griding: ##################################")
  cgrid = xr.Dataset(coords={'depths': depths,
                            'cast_number': filestodo},
                    data_vars={'temperature':(['depths', 'cast_number'],
                                np.zeros((Nbins, Ncasts)))
                    })
  for td in gridxytfields:
    cgrid[td] = (['cast_number'], np.zeros(Ncasts))
  for td in gridfields:
    cgrid[td] = (['depths', 'cast_number'], np.zeros((Nbins, Ncasts)) * np.NaN)

  num = 0
  for inds in filestodo:
    with xr.open_dataset(f'{ncCastfolder}/{prefix}{inds:04d}.nc') as cast:
      if 'analog' in cast:
        analog = True
      for td in gridxytfields:
        cgrid[td][num] = cast[td].values[0]
      for td in gridfields:
        if td in cast:
          cgrid[td][:, num] = mvpgridfield(depth_bins, cast, td)
      num += 1
  if not analog:
    cgrid = cgrid.drop('analog')

  cgrid.to_netcdf(outFilen)


