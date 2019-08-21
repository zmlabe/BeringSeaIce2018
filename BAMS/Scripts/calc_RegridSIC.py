"""
Regrid SIC data from 10 km to 0.25 grid

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
from scipy.interpolate import griddata as g

### Define directories
directorydata = '/surtsey/zlabe/seaice/SIC_Alaska/' 
directorydata2 = '/surtsey/zlabe/seaice/SIC_Alaska/sic2018/'
directorydata3 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering SIC - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
days = np.arange(1,28+1,1)

### Retrieve data from historical sea ice atlas (0.25)
filename = directorydata + 'SNAP_SEA_ICE_ATLAS_JAN.nc'

data = Dataset(filename)
ice = data.variables['sic_con_pct'][0,:,:]
lat1 = data.variables['lat'][:]    
lon1 = data.variables['lon'][:]
time = data.variables['time'][:]
data.close()

print('Completed: Data read!')

### Meshgrid
lon2,lat2 = np.meshgrid(lon1,lat1)

### Read in yearly data
sic19 = np.empty((31,849,849))
for i in range(days.shape[0]):
    filename = directorydata2 + 'jan_2018_%s.nc' % days[i]
    data = Dataset(filename,'r')
    sic19[i,:,:] = data.variables['ice_conc'][:]
    latold2 = data.variables['lat'][:]
    lonold2 = data.variables['lon'][:]
    data.close()
    
sic19[np.where(sic19 == -999)] = np.nan

### Calculate monthly average
sicmean = np.nanmean(sic19,axis=0)

#### Regrid data
ak = g((np.ravel(latold2),np.ravel(lonold2)),sicmean.ravel(),(lat2,lon2),
       method='linear')

def netcdfAlaska(lats,lons,var,directory):
    print('\n>>> Using netcdfAlaska function!')
    
    name = 'Alaska_SIC_Jan_2018.nc'
    filename = directory + name
    ncfile = Dataset(filename,'w',format='NETCDF4')
    ncfile.description = 'January 2018 SIC from OSISAF ' \
                        'interpolated on grid from' \
                        'Alaska Sea Ice Atlas'
    
    ### Dimensions
    ncfile.createDimension('lat',var.shape[0])
    ncfile.createDimension('lon',var.shape[1])
    
    ### Variables
    latitude = ncfile.createVariable('lat','f4',('lat','lon'))
    longitude = ncfile.createVariable('lon','f4',('lat','lon'))
    varns = ncfile.createVariable('sic','f4',('lat','lon'))
    
    ### Units
    varns.units = '%'
    ncfile.title = 'OSISAF SIC on AK Sea Ice Atlas Grid'
    ncfile.instituion = 'Dept. ESS at University of California, Irvine'
    ncfile.source = 'http://osisaf.met.no/p/ice/'
    ncfile.references = 'SSMIS (DMSP F18)]'
    
    ### Data
    latitude[:] = lats
    longitude[:] = lons
    varns[:] = var
    
    ncfile.close()
    print('*Completed: Created netCDF4 File!')
    
netcdfAlaska(lat2,lon2,ak,directorydata)