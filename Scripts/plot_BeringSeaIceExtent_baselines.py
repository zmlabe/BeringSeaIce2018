"""
Script calculates rankings of sea ice extent from the Historical Sea Ice
Atlas (University of Fairbanks) for the Bering Sea

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
import scipy.stats as sts

### Define directories
directorydata2 = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Data/'
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
yearsat = np.arange(1979,2018+1,1)

### Retrieve data from NSIDC regional extent in Bering Sea
ice = np.genfromtxt(directorydata2 + 'Bering_SIE_iceatlas_' \
                          '02_1850-2018.txt',skip_header=1)

### Rank data
rank = sts.rankdata(ice[:-1],method='min')
maxq = ice[np.where(rank==np.max(rank))[0]]
minq = ice[np.where(rank==np.min(rank))[0]]

yearq = np.where((years>=1979) & (years<=2017))[0]
icebase = np.nanmean(ice[yearq],axis=0)

ice18 = ice[-1]

allbar = [icebase,maxq,minq,ice18]

###############################################################################
###############################################################################
###############################################################################
### Plot figures
### Plot sea ice extent
fig = plt.figure()
ax = plt.subplot(111)

N = len(allbar)
ind = np.arange(N)
width = 0.9

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
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.tick_params('both',length=5.5,width=2,which='major',color='darkgrey')
ax.spines['left'].set_linewidth(2)
ax.tick_params(labelbottom='off')
ax.spines['left'].set_position(('outward',-3))
plt.setp(ax.get_xticklines()[0:-1],visible=False)

rects = ax.bar(ind,allbar,width,color='deepskyblue',alpha=1,zorder=1)

rects[0].set_color('darkgrey')
rects[-1].set_color('r')

labels = [r'1979-2017 Mean',r'Max (1976)',r'Min (2001)',r'2018']
for i, rect in enumerate(rects):
    if i == 0:
        cc = 'darkgrey'
    elif any([i == 1,i==2]):
        cc = 'deepskyblue'
    elif i == 3:
        cc = 'r'
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height+0.01,
             r'\textbf{%s}' % labels[i], ha='center', va='bottom',color=cc)


plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.arange(0,2.5,0.2))),
           color='darkgrey')
plt.ylim([0,1])

plt.xlabel(r'\textbf{Historical Sea Ice Atlas, University of Alaska}',
           fontsize=12,alpha=1,color='darkgrey',rotation=0) 
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=12,alpha=1,color='darkgrey',rotation=90) 

fig.suptitle(r'\textbf{FEBRUARY : BERING SEA ICE}',
                       fontsize=22,color='darkgrey') 

plt.savefig(directoryfigure + 'Bering_SIE_baselines.png',dpi=300)

print('Completed: Figure plotted!')
print('Completed: Script done!')