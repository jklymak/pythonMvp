import numpy as np
import time
import xarray as xr
import matplotlib.pyplot as plt


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

prefix = 'mvpla16_'
basedir='/Users/jklymak/DC15b/mvp/'
basedir='/Users/jklymak/Dropbox/pythonMvp/sampledata/'
datafolder = basedir+'raw/'
ncCastfolder = basedir+'nccasts/'
ncGridfolder = basedir+'ncgrid/'

sleeptime = 20
filestodo = dict()
filestodo['testA'] = np.arange(100, 107)

print(filestodo)

depth_bins = np.arange(0.,320+0.1,1.)
depths = (depth_bins[1:] + depth_bins[:-1]) / 2

max_abs_pressure = 0 # this variable is used in plotting later
gridfields = ['temperature','salinity','analog', 'pressure','pden']
gridxytfields = ['latitude','longitude','datetime','bottom']

badfiles=[]


analog = False
while 1:
  for gridind in ['testA']:
    # now make the grid.  This is just concatenating the gridded profiles stored
    # in the pickle
    n=0
    Ncasts = len(filestodo[gridind])
    Nbins = len(depths)
    print("Griding: ##################################")
    cgrid = xr.Dataset(coords={'depths': depths,
                               'cast_number': filestodo[gridind]},
                       data_vars={'temperature':(['depths', 'cast_number'],
                                  np.zeros((Nbins, Ncasts)))
                       })
    for td in gridxytfields:
      cgrid[td] = (['cast_number'], np.zeros(Ncasts))
    for td in gridfields:
      cgrid[td] = (['depths', 'cast_number'], np.zeros((Nbins, Ncasts)) * np.NaN)

    num = 0
    for inds in filestodo[gridind]:
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
    cgrid.to_netcdf(ncGridfolder+'/'+gridind+'.nc')

  print('Waiting %1.0f s' % sleeptime)
  for ii in np.arange(0,sleeptime,1):
    time.sleep(1)
    print('.'),
  print('Checking')


