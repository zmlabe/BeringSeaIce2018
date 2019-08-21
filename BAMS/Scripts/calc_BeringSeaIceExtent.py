"""
Script calculates sea ice extent in the Bering Sea from SIC fields

Notes
-----
    Author : Zachary Labe
    Date   : 24 March 2019
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import datetime

### Define directories
directorydata = '/surtsey/zlabe/seaice/SIC_Alaska/' 
directorydata2 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Data/'
directorydata3 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering SIE - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
yearsat = np.arange(1979,2018+1,1)

### Retrieve data from historical sea ice atlas
filename = directorydata + 'Alaska_SIC_Jan_1850-2018.nc'

data = Dataset(filename)
iceold = data.variables['sic'][:]
lat1 = data.variables['lat'][:]    
lon1 = data.variables['lon'][:]
data.close()

print('Completed: Data read!')

### Meshgrid
lon2,lat2 = np.meshgrid(lon1,lat1)

### Bering Sea Ice Mask
latq = lat2.copy()
latq[np.where(latq>67)] = 0.
latq[np.where(latq>0.)] = 1

### Mask values below 15%
ice = iceold * latq

### Extent is a binary 0 or 1 for 15% SIC threshold
thresh=85
ice[np.where(ice<thresh)]=np.nan
ice[np.where(ice>=thresh)]=1

### Calculate sea ice extent
ext = np.zeros((years.shape[0]))
valyr = np.zeros((ice.shape))
for yr in range(years.shape[0]):
    for i in range(lat2.shape[0]):
        for j in range(lon2.shape[1]):
            if ice[yr,i,j] == 1.0:
               ### Area of 0.25 grid cell [769.3 = (111.32/4) * (110.57/4)]
               valyr[yr,i,j] = 769.3 * np.cos(np.radians(lat2[i,j]))
    ext[yr] = np.nansum(valyr[yr,:,:])/1e6
    
### Save sea ice extent data (yearly) from sea ice atlas
np.savetxt(directorydata3 + 'Bering_SIE85_iceatlas_01_1850-2018.txt',ext,
       delimiter=',',header='File contains January SIE from historical' \
       '\n ice atlas (University of Alaska) for years' \
       '\n 1850-2018 \n')