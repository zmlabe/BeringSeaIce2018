"""
Calculates sea ice concentration from NOAA/NSIDC CDRv3 record for Jan-Apr 2018

Notes
-----
    Author : Zachary Labe
    Date   : 13 August 2019
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
directorydata = '/surtsey/zlabe/seaice/CDRv3/monthly/' 
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Calculating Bering SIC Anomalies - %s----' % titletime)

### Define attributes
years = np.arange(1979,2018+1,1)
yearq = np.where((years >= 1981) & (years <= 2010))[0]
months = np.arange(1,12+1,1)
monthq = [str(item).zfill(2) for item in months]
satellite1 = np.repeat(['n07'],103)
satellite2 = np.repeat(['f08'],53)
satellite3 = np.repeat(['f11'],45)
satellite4 = np.repeat(['f13'],147)
satellite5 = np.repeat(['f17'],132)
satall = (satellite1,satellite2,satellite3,satellite4,satellite5)
sat = np.concatenate(satall)

### Read in all data into [years,months,lat,lon]
count = 0
sic = np.empty((years.shape[0],months.shape[0],448,304))
for i in range(sic.shape[0]):
    for j in range(sic.shape[1]):
        count += 1
        time = '%s%s' % (years[i],monthq[j])
        if time == '198801':
            none = np.empty((448,304))
            none.fill(np.nan)
            sic[i,j,:,:] = none
        else:
            filename = 'seaice_conc_monthly_nh_%s_%s_v03r01.nc' % (sat[count-1],
                                                                     time)
            data = Dataset(directorydata + filename)
            sic[i,j,:,:] = data.variables['seaice_conc_monthly_cdr'][:]
            lat = data.variables['latitude'][:]
            lon = data.variables['longitude'][:]
            data.close()
        
### Mask missing data
sic[np.where(sic > 1)] = np.nan
sicq = sic*100.
        
### Compute 1981-2010 climatology
yearclimo = np.nanmean(sicq[yearq,:,:,:],axis=0)

### Compute anomalies 
anom = sicq - yearclimo

### Calculate mean Jan-Apr 2018
winter18 = np.nanmean(anom[-1,:4,:,:],axis=0)
winter18[np.isnan(winter18)] = 0.

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
             
### Alaska Region
latmin = 52
latmax = 73
lonmin = 167
lonmax = 218

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
circle = m.drawmapboundary(fill_color=cmocean.cm.balance(0.517))

cs = m.contourf(lon,lat,winter18,np.arange(-75,75.1,5),latlon=True,
                extend='both')

cmap = cmocean.cm.balance_r
cs.set_cmap(cmap)

m.fillcontinents(color='dimgrey')

cbar_ax = fig.add_axes([0.302,0.09,0.4,0.02])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
barlim = np.arange(-75,76,25)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.ax.tick_params(labelsize=6) 
cbar.set_label(r'\textbf{Sea Ice Concentration Anomalies [\%]}',fontsize=10,
                         color='k',labelpad=-26)
cbar.ax.tick_params(axis='x', size=.0001)
cbar.outline.set_edgecolor('dimgrey')
cbar.outline.set_linewidth(0.5)

plt.tight_layout()

fig.subplots_adjust(bottom=0.17)

print('Completed: Figure plotted!')
plt.savefig(directoryfigure + 'Jan-Apr_2018_BeringSIC_Anomalies_CDRv3.png', dpi=900)

print('Completed: Script done!')