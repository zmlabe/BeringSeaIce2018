"""
Plots JAXA AMSR2 3.125 km (UHH-Processed) Sea Ice Concentration Data
 
Source : seaice.de
Author : Zachary Labe
Date : 13 March 2018
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import urllib.request as UL
import numpy as np
import datetime
import calendar as cal
import gzip
import math
import cmocean

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

now = datetime.datetime.now()
currentmn = str(now.month)
if now.day == 1:
    currentdy = str(cal.monthrange(now.year,now.month-1)[1])
    currentmn = str(now.month-1)
else:
    currentdy = str(now.day-1)
if int(currentdy) < 10:
    currentdy = '0' + currentdy
    
currentyr = str(now.year)

if int(currentmn) < 10:
    currentmn = '0' + currentmn

currenttime = currentmn + '_' + str(currentdy) + '_' + currentyr
titletime = currentmn + '/' + str(currentdy) + '/' + currentyr

print('\n' 'Current Time = %s' '\n' % titletime)

### Loop through time
for i in range(0,31,3):
    currentdy = str(i+1)
    currentmn = '02'
    if int(currentdy) < 10:
        currentdy = '0' + currentdy

    currentyr = '2018'
    currenttime = currentmn + '_' + str(currentdy) + '_' + currentyr
    titletime = currentmn + '/' + str(currentdy) + '/' + currentyr

    ### Pick data set
    icedataset = 'AMSR2'
        
    if icedataset == 'AMSR2':
        
        url = 'ftp://ftp-projects.cen.uni-hamburg.de/seaice/AMSR2/3.125km/'
        filename = 'Arc_%s%s%s_res3.125_pyres.nc.gz' % (currentyr,currentmn,currentdy)
        filenameout = 'Arc_AMSR2_SIC.nc'
        UL.urlretrieve(url+filename, filename)
        inF = gzip.open(filename, 'rb')
        outF = open(filenameout, 'wb')
        outF.write( inF.read() )
        inF.close()
        outF.close()
        
        data = Dataset(filenameout)
        ice = data.variables['sea_ice_concentration'][:]
        lat = data.variables['latitude'][:]    
        lon = data.variables['longitude'][:]
        data.close()
        
        ice = np.asarray(np.squeeze(ice/100.))
        
        print('Completed: Data read!')
        
    ice[np.where(ice <= 0.15)] = np.nan
    ice[np.where((ice >= 0.999) & (ice <= 1))] = 0.999
    ice[np.where(ice > 1)] = np.nan
    ice = ice*100.
    
    print('Completed: Ice masked!')
    
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
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ### Enter lat/lon
    region = 'bering'
    
    if region == 'kara':
        # Kara Sea
        latmin = 67
        latmax = 87
        lonmin = 20
        lonmax = 90
        
    elif region == 'beaufort':
        # Beaufort Sea
        latmin = 64
        latmax = 87
        lonmin = 180
        lonmax = 240
    
    elif region == 'bering':
        # Bering/Chukchi Sea/Okhotsk 
        latmin = 50
        latmax = 75
        lonmin = 166
        lonmax = 210
    
    elif region == 'greenland':
        # Greenland
        latmin = 55
        latmax = 89.5
        lonmin = 280
        lonmax = 395
        
    elif region == 'pacific':
        # Central Arctic
        latmin = 69
        latmax = 89.99
        lonmin = 160
        lonmax = 250    
    
    elif region == 'svalbard':
        latmin = 73
        latmax = 86
        lonmin = 340
        lonmax = 420
        
    elif region == 'GreenlandSea':
        latmin = 74
        latmax = 88
        lonmin = 330
        lonmax = 410
    
    else:
        ValueError('Wrong region listed!')
    
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
        lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
        lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
        x, y = prj(lons, lats)
        ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
        ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
        return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                           llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                           urcrnrlon=ur_lon, urcrnrlat=ur_lat, round=True,
                           resolution='l')
    
    m = polar_stere(lonmin,lonmax,latmin,latmax)
    m.drawcoastlines(color = 'dimgrey',linewidth=0.8)
    m.drawmapboundary(color='k')
    m.drawlsmask(land_color='k',ocean_color='k')
    
    cs = m.contourf(lon,lat,ice[:,:],np.arange(0,100.01,1),latlon=True)
         
    cmap = cmocean.cm.dense_r     
    cs.set_cmap(cmap)
    
    m.fillcontinents(color='k')
    
    cbar = m.colorbar(cs,location='right',pad = 0.2)
    cbar.outline.set_edgecolor('k')
    barlim = np.arange(0,101,50)
    cbar.set_ticks(barlim)
    cbar.set_ticklabels(list(map(str,barlim)))
    cbar.set_label(r'\textbf{SEA ICE CONCENTRATION (\%)}',fontsize=13,
                             alpha=1,color='darkgrey')
    cbar.ax.tick_params(axis='y', size=.001)
    cbar.outline.set_edgecolor('darkgrey')
    
    plt.title(r'\textbf{%s}' % titletime,
                 fontsize=29,color='white',alpha=0.6)
                             
                
    fig.subplots_adjust(top=0.89)

    print('Completed: Figure plotted!')
    plt.savefig(directoryfigure + 'seaiceconc_%s_%s.png' % (region,currenttime), dpi=250)
    
print('Completed: Script done!')