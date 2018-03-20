"""
Script plots sea ice thickness (SIT) anomalies for the Bering Sea 
over DJF 2017-2018
 
Source : http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html
Author : Zachary Labe
Date   : 20 March 2018
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
import calc_SeaIceThick_PIOMAS as CP
import cmocean
import math
from matplotlib import cbook
from matplotlib.colors import Normalize
import numpy as ma

### Define directories
directorydata = '/surtsey/zlabe/seaice_obs/PIOMAS/'    
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'

yearmin = 1979
yearmax = 2018
years = np.arange(yearmin,yearmax+1,1)
       
### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr

print('\n' '----Plot Sea Ice Thickness - %s----' % titletime) 

### Use functions
lats,lons,sit = CP.readPiomas(directorydata,years,0.01)
meansit = CP.meanThick(1981,2010,years,sit)

meandjf = np.nanmean(meansit[np.array([0,1,-1]),:,:],axis=0)

print('Completed: Beginning plotting!')

###########################################################################
###########################################################################
### Calculate djf and anomaly

sitdec = sit[-2,-1,:,:]
sitjan = sit[-1,0,:,:]
sitfeb = sit[-1,1,:,:]

sitdjf = (sitdec+sitjan+sitfeb)/3.
anom = sitdjf - meandjf

anomf = sit[-1,1,:,:]-meansit[1,:,:]

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

### Functions to center colormap on 0 - white    
class MidPointNorm(Normalize):    
    def __init__(self, midpoint=0, vmin=None, vmax=None, clip=False):
        Normalize.__init__(self,vmin, vmax, clip)
        self.midpoint = midpoint

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if not (vmin < midpoint < vmax):
            raise ValueError("midpoint must be between maxvalue and minvalue.")       
        elif vmin == vmax:
            result.fill(0) # Or should it be all masked? Or 0.5?
        elif vmin > vmax:
            raise ValueError("maxvalue must be bigger than minvalue")
        else:
            vmin = float(vmin)
            vmax = float(vmax)
            if clip:
                mask = ma.getmask(result)
                result = ma.array(np.clip(ma.ma.filled(result,vmax), vmin, vmax),
                                  mask=mask)

            # ma division is very slow; we can take a shortcut
            resdat = result.data

            #First scale to -1 to 1 range, than to from 0 to 1.
            resdat -= midpoint            
            resdat[resdat>0] /= abs(vmax - midpoint)            
            resdat[resdat<0] /= abs(vmin - midpoint)

            resdat /= 2.
            resdat += 0.5
            result = ma.array(resdat, mask=result.mask, copy=False)                

        if is_scalar:
            result = result[0]            
        return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if cbook.iterable(value):
            val = ma.asarray(value)
            val = 2 * (val-0.5)  
            val[val>0]  *= abs(vmax - midpoint)
            val[val<0] *= abs(vmin - midpoint)
            val += midpoint
            return val
        else:
            val = 2 * (val - 0.5)
            if val < 0: 
                return  val*abs(vmin-midpoint) + midpoint
            else:
                return  val*abs(vmax-midpoint) + midpoint
norm = MidPointNorm(midpoint=0)

def setcolor(x, color):
     for m in x:
         for t in x[m][1]:
             t.set_color(color)
             
### Alaska Region
latmin = 55
latmax = 78
lonmin = 165
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

ax = fig.add_subplot(111)
m = polar_stere(lonmin,lonmax,latmin,latmax)
m.drawcoastlines(color = 'dimgrey',linewidth=1.4)
m.drawmapboundary(color='k')
m.drawlsmask(land_color='k',ocean_color='k')


cs = m.contourf(lons,lats,anomf,np.arange(-2,2.1,0.05),latlon=True,
                extend='both')

cmap = cmocean.cm.balance_r
cs.set_cmap(cmap)

m.fillcontinents(color='k')

cbar_ax = fig.add_axes([0.312,0.07,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal',
                    extend='both',extendfrac=0.07,drawedges=False)
barlim = np.arange(-2,3,1)
cbar.set_ticks(barlim)
cbar.set_ticklabels(list(map(str,barlim))) 
cbar.set_label(r'\textbf{SEA ICE THICKNESS ANOMALIES [m]}',fontsize=15,
                         color='darkgrey',labelpad=-38)
cbar.ax.tick_params(axis='x', size=.001)

ax.annotate(r'\textbf{FEBRUARY 2018}',
            xy=(0, 0),xytext=(0.5,1.06),xycoords='axes fraction',
            fontsize=25,color='darkgrey',rotation=0,ha='center',va='center')

fig.subplots_adjust(bottom=0.17)

print('Completed: Figure plotted!')

plt.savefig(directoryfigure + 'djf_sitanom_Bering.png', dpi=300)

print('Completed: Script done!')
