from MVP_translate import raw_to_netcdf, profiles_to_grid
from MVP_makeGridfile import profiles_to_grid
from tqdm import tqdm
import numpy as np
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
script to drive processing of sampledata.  Adapt on a per-mission basis:
"""

prefix = 'mvpla16_'
basedir='/Users/jklymak/Dropbox/pythonMvp/sampledata/'
datafolder = basedir+'raw/'
ncCastfolder = basedir+'nccasts/'
ncGridfolder = basedir+'ncgrid/'
remotedir = '/Volumes/booo/'

# define the grids by cast number:
filestodo = dict()
filestodo['testA'] = np.arange(100, 107)

depth_bins = np.arange(0.,320+0.1,1.)

ForceReplot = False
while True:
    # rsync any new files from MVP computer
    str= f"rsync -av {remotedir} {basedir}"
    logger.info("Running " + str)
    os.system(str)
    logger.info('done rsync')

    newFiles = raw_to_netcdf(datafolder, ncCastfolder, prefix)

    if newFiles or ForceReplot:
        for todo in ['testA']:
            logger.info(f'Gridding {todo}: {filestodo[todo][0]} to {filestodo[todo][-1]}')
            outFilen = ncGridfolder+todo+'.nc'
            profiles_to_grid(depth_bins, filestodo[todo], ncCastfolder,
                             prefix, outFilen)
    else:
        logger.info('No new files, so not changing grids or plotting')

    print('Pausing 30 s')
    for i in tqdm(range(30)):
        sleep(1)