"""
Calculate t test if sea ice extent means are different

Notes
-----
    Author : Zachary Labe
    Date   : 6 March 2018
"""

### Import modules
import numpy as np
import datetime
import scipy.stats as sts

### Define directories
directorydata2 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Calc SIE t test- %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
yearsat = np.arange(1979,2018+1,1)

### Retrieve data from NSIDC regional extent in Bering Sea
ice = np.genfromtxt(directorydata2 + 'Bering_SIE_iceatlas_' \
                          '02_1850-2018.txt',skip_header=1)

### Slice data based on time
yearq = np.where((years>=1979) & (years<=2017))[0]
icebase = ice[yearq]

yearqq = np.where((years>=1942) & (years<=1978))[0]
oldicebase = ice[yearqq]

### Calculate t test
t,pvalue = sts.ttest_ind(oldicebase,icebase)
