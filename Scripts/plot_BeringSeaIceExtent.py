"""
Script calculates sea ice extent in the Bering Sea from SIC fields

Notes
-----
    Author : Zachary Labe
    Date   : 4 March 2018
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm

### Define directories
directorydata = '/surtsey/zlabe/seaice_obs/SIC_Alaska/' 
directorydata2 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Data/'
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

### Retrieve data from NSIDC regional extent in Bering Sea
beringold = np.genfromtxt(directorydata2 + 'BeringSeaIceExtent_NSIDC_' \
                       'regional_02_1979-2018.txt')
bering = beringold/1e6

### Retrieve data from historical sea ice atlas
filename = directorydata + 'Alaska_SIC_Feb_1850-2018.nc'

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

### Mask values below 20%
ice = iceold * latq

### Extent is a binary 0 or 1 for 15% SIC threshold
thresh=15
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
np.savetxt(directorydata2 + 'Bering_SIE_iceatlas_02_1850-2018.txt',ext,
       delimiter=',',header='File contains February SIE from historical' \
       '\n ice atlas (University of Alaska) for years' \
       '\n 1850-2018 \n')

### Calculate loess 
smoothed = sm.nonparametric.lowess(ext,np.arange(years.shape[0]))

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

fig = plt.figure()
ax = plt.subplot(111)

### Adjust axes in time series plots 
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 5))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([]) 
        
ax.tick_params('both',length=5.5,width=2,which='major',color='darkgrey')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 

plt.plot(years,ext,linewidth=2,color='deepskyblue',
         label=r'\textbf{Historical Sea Ice Atlas, University of Alaska}')
plt.plot(yearsat,bering,linewidth=0.9,color='r',
         label=r'\textbf{NSIDC Sea Ice Index, Version 3}')
plt.plot(years,smoothed[:,1],linewidth=0.9,linestyle='--',
         dashes=(1, 0.2),color='w',label=r'\textbf{Lowess Smoothing}')

xlabels = list(map(str,np.arange(1850,2021,25)))
plt.xticks(np.arange(1850,2021,25),xlabels,rotation=0,color='darkgrey')
plt.xlim([1850,2020])

plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.arange(0,2.5,0.2))),
           color='darkgrey')
plt.ylim([0.2,1])

fig.suptitle(r'\textbf{FEBRUARY : BERING SEA ICE}',
                       fontsize=22,color='darkgrey') 
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=17,alpha=1,color='darkgrey',rotation=90) 

le = plt.legend(shadow=False,fontsize=8,loc='upper center',
           bbox_to_anchor=(0.285, 0.17),fancybox=True,frameon=False,ncol=1)
for text in le.get_texts():
    text.set_color('darkgrey') 

plt.savefig(directoryfigure + 'Bering_SIE_Atlas.png',dpi=300)

print('Completed: Figure plotted!')
print('Completed: Script done!')