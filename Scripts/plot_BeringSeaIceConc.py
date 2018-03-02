"""
Plot reads in Bering Sea Ice Concentration data for February 1850-2018 and
also creates a netcdf file of the data!

Notes
-----
    Author : Zachary Labe
    Date   : 2 March 2018
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean
import datetime

### Define directories
directorydata = '/surtsey/zlabe/seaice_obs/SIC_Alaska/' 
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering SIC - %s----' % titletime)

### Define years
years = np.arange(1850,2017+1,1)

### Retrieve data from historical sea ice atlas
filename = directorydata + 'SNAP_SEA_ICE_ATLAS.nc'

data = Dataset(filename)
ice = data.variables['sic_con_pct'][:]
lat1 = data.variables['lat'][:]    
lon1 = data.variables['lon'][:]
time = data.variables['time'][:]
data.close()

print('Completed: Data read!')

### Retrieve February data
feb = ice[::12,:,:] # starts on 2/15/1850 to 2/15/2017

### Meshgrid
lon2,lat2 = np.meshgrid(lon1,lat1)

### Read data for 2018
filename2 = 'Alaska_SIC_Feb_2018.nc'
data = Dataset(directorydata + filename2)
ice18 = data.variables['sic'][:]

###############################################################################
###############################################################################
###############################################################################
### Plot figures
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='white')
plt.rc('axes',facecolor='black')

#def setcolor(x, color):
#     for m in x:
#         for t in x[m][1]:
#             t.set_color(color)
#
#fig = plt.figure()
#ax = fig.add_subplot(111)
#m = Basemap(projection='npstere',boundinglat=57,lon_0=270,resolution='l',
#            round =True,area_thresh=10000)
#m.drawcoastlines(color = 'tomato',linewidth=0.4)
#m.drawmapboundary(color='k')
##m.drawlsmask(land_color='k',ocean_color='k')
#
##parallels = np.arange(50,86,5)
##meridians = np.arange(-180,180,30)
##m.drawparallels(parallels,labels=[False,False,False,False],linewidth=0.0,color='w')
##par=m.drawmeridians(meridians,labels=[True,True,False,False],linewidth=0.0,fontsize=6,color='w')
##setcolor(par,'white')
#
#cs = m.contourf(lon,lat,ice[:,:]*100.,np.arange(20,101,2),extend='min',latlon=True)
#   
#cmap = cmocean.cm.ice     
#cs.set_cmap(cmap)
#
#m.fillcontinents(color='k')
#
#cbar = m.colorbar(cs,location='right',pad = 0.55)
#ticks = np.arange(20,101,10)
#labels = map(str,np.arange(20,101,10))
#cbar.set_ticklabels(ticks,labels)
#cbar.set_label(r'\textbf{ CONCENTRATION [\%]}',fontsize=13,color='darkgrey')
#cbar.ax.tick_params(axis='y', size=.001)
#                         
#            
#fig.subplots_adjust(top=0.905)
#
#print('Completed: Figure plotted!')
#
#plt.savefig(directorys + 'seaiceconc.png', dpi=300)
#
#print('Completed: Script done!')