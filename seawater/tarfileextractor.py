# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:20:32 2013

@author: FoxR
"""

import tarfile
tarfilename = ('C:\Python scripts\seawater\seawater-2.0.1.tar.gz')
extractTarPath = ('C:\Python scripts\seawater')
if tarfile.is_tarfile(tarfilename):
    tfile = tarfile.open(tarfilename,'r:gz')
    # list all contents
    print "tar file contents:"
    print tfile.list(verbose=False)
    # extract all contents
    tfile.extractall(extractTarPath)
else:
    print tarfilename + " is not a tarfile."
    
