"""
Script calculates the mean January-April sea ice extent for the Bering Sea
over the 1850 to 2018 period and 1979-2018 period

Notes
-----
    Author : Zachary Labe
    Date   : 24 March 2019
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy.stats as sts

### Define directories
directorydata = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Data/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Calculating Bering SIE - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
yearsat = np.arange(1979,2018+1,1)

###############################################################################
###############################################################################
###############################################################################
#### Retrieve data from NSIDC regional extent in Bering Sea

### Retrieve data from NSIDC regional extent in Bering Sea
beringjan = np.genfromtxt(directorydata + \
                           'Bering_SIE_NSIDC_01_1979-2018.txt')/1e6
beringfeb = np.genfromtxt(directorydata + \
                           'Bering_SIE_NSIDC_02_1979-2018.txt')/1e6
beringmar = np.genfromtxt(directorydata + \
                           'Bering_SIE_NSIDC_03_1979-2018.txt')/1e6
beringapr = np.genfromtxt(directorydata + \
                           'Bering_SIE_NSIDC_04_1979-2018.txt')/1e6       
                          
meansat = (beringjan + beringfeb + beringmar + beringapr)/4.                          

### Save sea ice extent data from NSIDC 
np.savetxt(directorydata + 'Bering_SIE_NSIDC_Jan-Apr_1979-2018.txt',meansat,
       delimiter=',',header='File contains mean Jan-Apr SIE from NSIDC' \
       '\n Sea Ice Index v3 for years 1979-2018 \n')

###############################################################################
###############################################################################
###############################################################################
#### Retrieve data from Sea Ice Atlas
atlasjan = np.genfromtxt(directorydata + 'Bering_SIE85_iceatlas_' \
                          '01_1850-2018.txt',skip_header=1)
atlasfeb = np.genfromtxt(directorydata + 'Bering_SIE85_iceatlas_' \
                          '02_1850-2018.txt',skip_header=1)
atlasmar = np.genfromtxt(directorydata + 'Bering_SIE85_iceatlas_' \
                          '03_1850-2018.txt',skip_header=1)
atlasapr = np.genfromtxt(directorydata + 'Bering_SIE85_iceatlas_' \
                          '04_1850-2018.txt',skip_header=1)

meanatlas = (atlasjan + atlasfeb + atlasmar + atlasapr)/4.                          

### Save sea ice extent data from NSIDC 
np.savetxt(directorydata + 'Bering_SIE85_iceatlas_Jan-Apr_1850-2018.txt',meanatlas,
       delimiter=',',header='File contains mean Jan-Apr SIE from historical' \
       '\n ice atlas (University of Alaska) for years' \
       '\n 1850-2018 \n')

###############################################################################
###############################################################################
###############################################################################
#### Compute Correlations
satperiod = meanatlas[-40:]

### Mask any nans before correlation
mask = ~np.logical_or(np.isnan(satperiod),np.isnan(meansat))
corr,p = sts.pearsonr(satperiod[mask],meansat[mask])
print('\n>>> Correlation between ice atlas and NSIDC is --> %s' % np.round(corr,3))
print('\n>>> P-value between ice atlas and NSIDC is --> %s' % p)