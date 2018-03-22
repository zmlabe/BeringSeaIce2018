"""
Script plots February sea ice extent in the Bering Sea from 1850-2018. Plot
is simplified for media release 

Notes
-----
    Author : Zachary Labe
    Date   : 22 March 2018
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import datetime

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

### Retrieve data from NSIDC regional extent in Bering Sea
ext = np.genfromtxt(directorydata2 + 'Bering_SIE_iceatlas_' \
                          '02_1850-2018.txt',skip_header=1)

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

plt.plot(years,ext,linewidth=3,color='deepskyblue',
         label=r'\textbf{Historical Sea Ice Atlas, University of Alaska}',
         zorder=2)
plt.scatter(years[-1],ext[-1],s=45,color='r',zorder=3)
plt.text(1997,0.237,r'\textbf{2018}',color='r',fontsize=15)

xlabels = list(map(str,np.arange(1850,2021,25)))
plt.xticks(np.arange(1850,2021,25),xlabels,rotation=0,color='darkgrey')
plt.xlim([1850,2020])

plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.arange(0,2.5,0.2))),
           color='darkgrey')
plt.ylim([0.2,1])

plt.title(r'\textbf{FEBRUARY : BERING SEA ICE}',
                       fontsize=26,color='darkgrey') 
plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=17,alpha=1,color='darkgrey',rotation=90) 

le = plt.legend(shadow=False,fontsize=8,loc='upper center',
           bbox_to_anchor=(0.2867, 0.07),fancybox=True,frameon=False,ncol=1)
for text in le.get_texts():
    text.set_color('darkgrey') 
    
ax.yaxis.grid(zorder=1,color='w',alpha=0.35,linewidth=0.5)

plt.savefig(directoryfigure + 'February_1850-2018_BeringSeaIceExtent.png',
            dpi=600)

print('Completed: Figure plotted!')
print('Completed: Script done!')