"""
Plots composites of Bering Sea Ice Conc compared to various baselines

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
import math

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
years = np.arange(1850,2018+1,1)

### Retrieve data from historical sea ice atlas
filename = directorydata + 'Alaska_SIC_Feb_1850-2018.nc'

data = Dataset(filename)
ice = data.variables['sic'][:]
lat1 = data.variables['lat'][:]    
lon1 = data.variables['lon'][:]
data.close()

print('Completed: Data read!')

### Mask values below 20%
ice[np.where(ice<0.01)]=np.nan

### Meshgrid
lon2,lat2 = np.meshgrid(lon1,lat1)

### Analogs
analogs = np.array([1951,1959,1989,2003,2009,2010,2015,2017])
yearoldq = np.searchsorted(years,analogs)

### Baselines
yearnewq = np.where((years>=1979) & (years<=2017))[0]

iceold = np.nanmean(ice[yearoldq,:,:],axis=0)
icenew = np.nanmean(ice[yearnewq,:,:],axis=0)

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

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)
             
### Alaska Region
latmin = 50
latmax = 77
lonmin = 185
lonmax = 220

fig = plt.figure()

def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.
    
    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.
    
    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='l')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                       llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                       urcrnrlon=ur_lon, urcrnrlat=ur_lat, round=True,
                       resolution='l')

ax = fig.add_subplot(121)
m = polar_stere(lonmin,lonmax,latmin,latmax)
m.drawcoastlines(color = 'dimgrey',linewidth=0.8)
m.drawmapboundary(color='k')
m.drawlsmask(land_color='k',ocean_color='k')

cs = m.contourf(lon2,lat2,iceold,np.arange(0,101,2),latlon=True)
#cs1 = m.contour(lon2,lat2,iceold,np.arange(15,20,5),latlon=True,colors='m',
#               linewidths=1)
cs2 = m.contour(lon2,lat2,ice[-1,:,:],np.arange(15,20,5),latlon=True,colors='r',
                linewidths=2)

cmap = cmocean.cm.dense_r     
cs.set_cmap(cmap)

m.fillcontinents(color='k')

ax.annotate(r'\textbf{ANALOGS}',
            xy=(0, 0),xytext=(0.5,1.02),xycoords='axes fraction',
            fontsize=25,color='darkgrey',rotation=0,ha='center',va='center')
ax.annotate(r'\textbf{1951,1959,1989,2003,2009,2010,2015,2017}',
            xy=(0, 0),xytext=(0.5,0.1),xycoords='axes fraction',
            fontsize=7,color='darkgrey',rotation=0,ha='center',va='center')

###############################################################################
ax1 = fig.add_subplot(122)
m = polar_stere(lonmin,lonmax,latmin,latmax)
m.drawcoastlines(color ='dimgrey',linewidth=0.8)
m.drawmapboundary(color='k')
m.drawlsmask(land_color='k',ocean_color='k')

cs = m.contourf(lon2,lat2,icenew,np.arange(0,101,2),latlon=True)
#cs1 = m.contour(lon2,lat2,icenew,np.arange(15,20,5),latlon=True,colors='m',
#               linewidths=1)
cs2 = m.contour(lon2,lat2,ice[-1,:,:],np.arange(15,20,5),latlon=True,colors='r',
                linewidths=2)

cmap = cmocean.cm.dense_r     
cs.set_cmap(cmap)

m.fillcontinents(color='k')

cbar_ax = fig.add_axes([0.312,0.14,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='min',extendfrac=0.07,drawedges=False)
barlim = np.arange(0,101,50)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.set_label(r'\textbf{SEA ICE CONCENTRATION [\%]}',fontsize=13,
                         color='darkgrey',labelpad=-36)
cbar.ax.tick_params(axis='x', size=.001)

ax1.annotate(r'\textbf{1979--2017}',
            xy=(0, 0),xytext=(0.5,1.02),xycoords='axes fraction',
            fontsize=25,color='darkgrey',rotation=0,ha='center',va='center')
ax1.annotate(r'\textbf{2018 -- Red}',
            xy=(0, 0),xytext=(0.51,0.75),xycoords='figure fraction',
            fontsize=9,color='r',rotation=0,ha='center',va='center')
          
fig.subplots_adjust(hspace=-0.6)

print('Completed: Figure plotted!')

plt.savefig(directoryfigure + 'analogs_Bering.png', dpi=300)

print('Completed: Script done!')