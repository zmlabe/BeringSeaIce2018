"""
Script calculates sea ice extent in the Bering Sea from SIC fields
Notes
-----
    Author : Zachary Labe
    Date   : 12 March 2018
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm

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
print('\n' '----Plotting Bering SIE - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
yearsat = np.arange(1979,2018+1,1)

### Retrieve data from NSIDC regional extent in Bering Sea
beringoldf = np.genfromtxt(directorydata2 +'BeringSeaIce_NSIDC_Feb.txt')
beringf = beringoldf/1e6

beringoldd = np.genfromtxt(directorydata2 +'BeringSeaIce_NSIDC_Dec.txt')
beringd = beringoldd/1e6

beringoldj = np.genfromtxt(directorydata2 +'BeringSeaIce_NSIDC_Jan.txt')
beringj = beringoldj/1e6

#beringoldn = np.genfromtxt(directorydata2 +'BeringSeaIce_NSIDC_Nov.txt')
#beringn = beringoldn/1e6

bering = (beringd + beringj + beringf)/3.
#bering = (beringn + beringd + beringj + beringf)/4.
#bering = (beringj + beringf)/2.

print('Completed: Data read!')

### Calculate loess 
smoothed = sm.nonparametric.lowess(bering,np.arange(yearsat.shape[0]))

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

plt.plot(yearsat,bering,linewidth=3.5,color='orangered',
         marker='o',markersize=6,
         label=r'\textbf{NSIDC Sea Ice Index, Version 3}')
plt.scatter(yearsat[-1],bering[-1],s=45,color='r',zorder=3)
plt.text(2012.5,0.1823,r'\textbf{2018}',color='r',fontsize=15)

plt.plot(np.arange(1987,1990,2),np.array([bering[8],bering[10]]),linewidth=1.7,color='orangered',
         label=r'Missing Data',linestyle='--',
         dashes=(1, 0.4))
xlabels = list(map(str,np.arange(1979,2021,5)))
plt.xticks(np.arange(1979,2021,5),xlabels,rotation=0,color='darkgrey')
plt.xlim([1979,2019])

plt.yticks(np.arange(0,2.5,0.1),list(map(str,np.arange(0,2.5,0.1))),
           color='darkgrey')
plt.ylim([0.1,0.8])

ax.yaxis.grid(zorder=1,color='w',alpha=0.35,linewidth=0.5)

plt.title(r'\textbf{DEC-FEB : \underline{BERING} SEA ICE}',
                       fontsize=26,color='darkgrey') 
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=17,alpha=1,color='darkgrey',rotation=90) 

le = plt.legend(shadow=False,fontsize=8,loc='upper center',
           bbox_to_anchor=(0.212, 0.13),fancybox=True,frameon=False,ncol=1)
for text in le.get_texts():
    text.set_color('darkgrey') 

plt.savefig(directoryfigure + 'Bering_SeaIceExtent_DecJanFeb.png',dpi=600)

print('Completed: Figure plotted!')
print('Completed: Script done!')