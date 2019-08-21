"""
Script plots average January-April sea ice in the Bering Sea for the BAMS
manuscript

Notes
-----
    Author : Zachary Labe
    Date   : 24 March 2019
"""

### Import modules
import numpy as np
import matplotlib.pyplot as plt
import datetime
import cmocean

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
print('\n' '----Plotting Bering SIE - %s----' % titletime)

### Define years
years = np.arange(1850,2018+1,1)
yearsat = np.arange(1979,2018+1,1)

### Retrieve data from NSIDC regional extent in Bering Sea
extsat = np.genfromtxt(directorydata + 'Bering_SIE_NSIDC_Jan-Apr' \
                       '_1979-2018.txt',skip_header=1)

### Retrieve data from sea ice atlas
ext = np.genfromtxt(directorydata + 'Bering_SIE85_iceatlas_Jan-Apr' \
                       '_1850-2018.txt',skip_header=1)

###############################################################################
###############################################################################
###############################################################################
### Plot figures
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

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
        
ax.tick_params('both',length=5.5,width=2,which='major',color='dimgrey')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_color('dimgrey') 

plt.plot(years,ext,linewidth=2,color=cmocean.cm.balance(0.15),
         label=r'\textbf{Alaskan Ice (Bering Sea)}',
         zorder=2,clip_on=False)
plt.scatter(years[-1],ext[-1],s=30,color=cmocean.cm.balance(0.81),
            zorder=3,clip_on=False)
#plt.text(2022,0.237,r'\textbf{2019}',color='r',fontsize=17)

xlabels = list(map(str,np.arange(1850,2021,25)))
plt.xticks(np.arange(1850,2021,25),xlabels,rotation=0,color='k',size=8)
plt.xlim([1850,2018])

plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.round(np.arange(0,2.5,0.2),2))),
           color='k',size=8)
plt.ylim([0,1])

plt.ylabel(r'\textbf{Sea Ice Extent [$\bf{\times}$10$\bf{^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=12,alpha=1,color='k',rotation=90) 

le = plt.legend(shadow=False,fontsize=7.5,loc='lower left',
           bbox_to_anchor=(-0.016,-0.03),fancybox=True,frameon=False,ncol=1)
for text in le.get_texts():
    text.set_color('dimgrey') 
    
ax.yaxis.grid(zorder=1,color='darkgrey',alpha=1,linewidth=0.5)
plt.subplots_adjust(bottom=0.14)

plt.savefig(directoryfigure + 'BeringSIE85_Jan-Apr_1850-2018_iceatlas.png',
            dpi=600)
print('Completed: Figure plotted!')

###############################################################################
###############################################################################
###############################################################################
### Plot ice atlas with nsidc data
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
        
ax.tick_params('both',length=5.5,width=2,which='major',color='dimgrey')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 
ax.spines['bottom'].set_color('dimgrey')
ax.spines['left'].set_color('dimgrey') 

plt.plot(years,ext,linewidth=2,color=cmocean.cm.balance(0.15),
         label=r'\textbf{Historical Sea Ice Atlas}',
         zorder=2,clip_on=False)
plt.plot(yearsat,extsat,linewidth=1,color='r',
         label=r'\textbf{Sea Ice Index v3 (Bering Sea)}',
         zorder=3,clip_on=False)

xlabels = list(map(str,np.arange(1850,2021,25)))
plt.xticks(np.arange(1850,2021,25),xlabels,rotation=0,color='k',size=8)
plt.xlim([1850,2018])

plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.round(np.arange(0,2.5,0.2),2))),
           color='k',size=8)
plt.ylim([0,1])

plt.ylabel(r'\textbf{Sea Ice Extent [$\bf{\times}$10$\bf{^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=12,alpha=1,color='k',rotation=90) 

le = plt.legend(shadow=False,fontsize=7.5,loc='lower left',
           bbox_to_anchor=(-0.016,-0.03),fancybox=True,frameon=False,ncol=1)
for text in le.get_texts():
    text.set_color('dimgrey') 
    
ax.yaxis.grid(zorder=1,color='darkgrey',alpha=1,linewidth=0.5)
plt.subplots_adjust(bottom=0.14)

plt.savefig(directoryfigure + 'BeringSIE85_Jan-Apr_1850-2018_iceatlas+nsidc.png',
            dpi=600)

print('Completed: Figure plotted!')
print('Completed: Script done!')