"""
Plots Bering sea ice concentration anomalies (from PIOMAS) for Jan-Apr 2018

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

### Define directories
directorydata = '/surtsey/zlabe/seaice/SIC_Alaska/BAMS/Monthly_SIC/' 
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/BAMS/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print('\n' '----Plotting Bering SIC Anomalies - %s----' % titletime)

### Define years
years = np.arange(1979,2018+1,1)

def readPiomas(directory,years):
    """
    Function reads PIOMAS binary and converts to standard numpy array.

    Parameters
    ----------
    directory : string
        working directory for stored PIOMAS files
    years : integers
        years for data files
    threshold : float
        mask sea ice concentration amounts < to this value

    Returns
    -------
    lats : 2d array
        latitudes
    lons : 2d array
        longitudes
    var : 4d array [year,month,lat,lon]
        sea ice concentration (0-1) 

    Usage
    -----
    lats,lons,var = readPiomas(directory,years,threshold)
    """
    
    print('\n>>> Using readPiomas function!')
    
    ### Import modules
    import numpy as np
    import datetime
    
    ### Current times
    now = datetime.datetime.now()
    yr = now.year
    dy = now.day
    
    ### Retrieve Grid
    grid = np.genfromtxt(directory + 'grid.txt')
    grid = np.reshape(grid,(grid.size))  
    
    ### Define Lat/Lon
    lon = grid[:grid.size//2]   
    lons = np.reshape(lon,(120,360))
    lat = grid[grid.size//2:]
    lats = np.reshape(lat,(120,360))
    
    ### Call variables from PIOMAS
    files = 'area'
    
    ### Read data from binary into numpy arrays
    var = np.empty((len(years),12,120,360))
    
    print('Currently reading PIOMAS data!')
    for i in range(len(years)):
        data = np.fromfile(directory + files + '_%s.H' % (years[i]),
                           dtype = 'float32')

    ### Reshape into [year,month,lat,lon]
        months = data.shape[0]//(120*360)
        if months != 12:
            lastyearq = np.reshape(data,(months,120,360))
            emptymo = np.empty((12-months,120,360))
            emptymo[:,:,:] = np.nan
            lastyear = np.append(lastyearq,emptymo,axis=0)
            var[i,:,:,:] = lastyear
            
            month = datetime.date(yr, months, dy).strftime('%B')
            print('SIC data available through ---> "%s"' % month)
            print('SIC data available from ---> (%s - %s)' \
                    % (np.nanmin(years),np.nanmax(years)))
            
        elif months == 12:
            dataq = np.reshape(data,(12,120,360))        
            var[i,:,:,:] = dataq
        else:
            ValueError('Issue with reshaping SIC array from binary')

    print('Masking SIC data < %s fraction!')

    print('*Completed: Read SIC data!')   
    
    return lats,lons,var

### Read in sea ice concentration data
lats,lons,sic = readPiomas(directorydata,years)

### Calculate anomalies for 1981-2010 baseline
yearq = np.where((years >= 1981) & (years <= 2010))[0]
mean = np.nanmean(sic[yearq,:,:,:],axis=0)
anom = sic - mean

### Slice months for January-April
winterq = anom[:,:4,:,:]

### Calculate for 1-100%
winter = winterq*100

### Calculate for 2018
winter18q = winter[-1,:,:,:]

### Take mean for Jan-Apr
winter18 = np.nanmean(winter18q,axis=0)

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
circle = m.drawmapboundary(fill_color='white')
#m.drawlsmask(land_color='k',ocean_color='k')

cs = m.contourf(lons,lats,winter18,np.arange(-75,75.1,5),latlon=True,
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
plt.savefig(directoryfigure + 'Jan-Apr_2018_BeringSIC_Anomalies.png', dpi=900)

print('Completed: Script done!')