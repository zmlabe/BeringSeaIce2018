"""
Plots Bering SST anomalies (from OISST) for Aug-Nov 2017

Notes
-----
    Author : Zachary Labe
    Date   : 6 May 2019
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean
import datetime
import math
import nclcmaps as ncm
from netCDF4 import Dataset

### Define directories
directorydata = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Data/' 
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering sST Anomalies - %s----' % titletime)

### Define years
years = np.arange(1979,2018+1,1)

### Read in SST anomaly data
data = Dataset(directorydata + 'OISST_2019_Aug_Nov.nc')
lats = data.variables['lat'][:]
lons = data.variables['lon'][:]
sst = data.variables['sst'][:].squeeze()
data.close()

lon2,lat2 = np.meshgrid(lons,lats)

###############################################################################
###############################################################################
###############################################################################
### Plot figures
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)
             
### Bering/Chukchi Seas Region
latmin = 50
latmax = 76
lonmin = 167
lonmax = 225

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

ax = fig.add_subplot(111)
m = polar_stere(lonmin,lonmax,latmin,latmax)
m.drawcoastlines(color = 'k',linewidth=0.8)
circle = m.drawmapboundary(fill_color='white')
m.drawlsmask(ocean_color='linen')

cs = m.contourf(lon2,lat2,sst,np.arange(-3,3.1,0.25),latlon=True,
                extend='both')

cmap = ncm.cmap('NCV_blu_red') 
cs.set_cmap(cmap)

m.fillcontinents(color='dimgrey',lake_color='dimgrey')

cbar_ax = fig.add_axes([0.302,0.09,0.4,0.02])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=True)
barlim = np.arange(-3,3.1,0.5)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.ax.tick_params(labelsize=6) 
cbar.set_label(r'\textbf{SST Anomalies [$^{\circ}$C]}',fontsize=10,
                         color='k',labelpad=-26)
cbar.ax.tick_params(axis='x', size=.0001)
cbar.outline.set_edgecolor('dimgrey')
cbar.outline.set_linewidth(0.5)

plt.tight_layout()

fig.subplots_adjust(bottom=0.17)

print('Completed: Figure plotted!')
plt.savefig(directoryfigure + 'Aug-Nov_2017_BeringSST_Anomalies.png', dpi=900)

print('Completed: Script done!')