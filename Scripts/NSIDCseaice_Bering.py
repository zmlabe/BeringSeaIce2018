"""
Reads in current year's Bering Arctic sea ice extent from 
Sea Ice Index 3 (NSIDC)

Website   : ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaice_analysis/
Author    : Zachary M. Labe
Date      : 2 March 2018
"""

### Import modules
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import cmocean

### Directory and time
directoryfigure = '/home/zlabe/Documents/Projects/BeringSeaIce2018/Figures/'
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
currentdoy = now.timetuple().tm_yday
doy = np.arange(0,365,1)
lastday = now.timetuple().tm_yday -2
years = np.arange(1979,2018+1,1)

### Load url
url = 'ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/seaice_analysis/' \
        'Sea_Ice_Index_Regional_Daily_Data_G02135_v3.0.xlsx'

## Read file
df_bering = pd.read_excel(url,sheet_name='Bering-Extent-km^2',header=1,
                            parse_cols=range(3,43,1))
bering = df_bering.as_matrix()

sie = bering/1e6
print('\nCompleted: Read sea ice data!')           

### Missing data in 2017
ice17q = sie[:,-2]
ice17q[np.where(np.isnan(ice17q))] = 5.66287231e-01

### Missing data in 2018 (leap year)
ice18q = sie[:,-1]
ice18q[58] = (0.26670926+0.28116941)/2

### Create running mean
N = 14

meanq = np.nanmean(sie[:,:],axis=1)
mean = np.convolve(np.append(meanq[-14:],meanq), np.ones((N,))/N, mode='valid') 
ice17 = np.convolve(np.append(sie[-14:,-3],ice17q),np.ones((N,))/N,mode='valid') 
ice18 = np.convolve(np.append(sie[-14:,-2],ice18q),np.ones((N,))/N,mode='valid')            

###########################################################################
###########################################################################
###########################################################################
### Create plot
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
plt.rc('savefig',facecolor='black')
plt.rc('axes',edgecolor='darkgrey')
plt.rc('xtick',color='white')
plt.rc('ytick',color='white')
plt.rc('axes',labelcolor='darkgrey')
plt.rc('axes',facecolor='black')

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
        
xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']

fig = plt.figure()
ax = plt.subplot(111)

ax.tick_params('both',length=5.5,width=2,which='major',color='darkgrey')             
adjust_spines(ax, ['left','bottom'])            
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none') 
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2) 

plt.axvline(30.4,color='darkgrey',linewidth=2,zorder=1,alpha=0.3)
plt.axvline(60.8,color='darkgrey',linewidth=2,zorder=1,alpha=0.3)

plt.plot(ice17,c='w',linewidth=1.3,zorder=3,alpha=1,label=r'\textbf{Year 2017}')
plt.plot(ice18,c='r',linewidth=3,zorder=4,alpha=1,label=r'\textbf{Year 2018}')
    
plt.plot(mean,c='deepskyblue',linewidth=4,zorder=2,linestyle='--',
         label=r'\textbf{1981-2010 Mean}',dashes=(1, 0.2))

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan']
plt.xticks(np.arange(0,361,30.4),xlabels,rotation=0,color='darkgrey')
plt.yticks(np.arange(0,2.5,0.2),list(map(str,np.arange(0,2.5,0.2))),
           color='darkgrey')
plt.ylim([0,0.8])
plt.xlim([0,361])

fig.suptitle(r'\textbf{BERING SEA ICE}',
                       fontsize=29,color='darkgrey')  

plt.ylabel(r'\textbf{Extent [$\bf{\times 10^{6}}$\ \textbf{km}$\bf{^2}$]}',
           fontsize=17,alpha=1,color='darkgrey',rotation=90) 

le = plt.legend(shadow=False,fontsize=10,loc='upper center',
           bbox_to_anchor=(0.51, -0.1),fancybox=True,frameon=False,ncol=3)
for text in le.get_texts():
    text.set_color('darkgrey') 
    
ax.annotate(r'\textbf{14-day running mean}',
            xy=(0, 0),xytext=(0.81,0.87),xycoords='figure fraction',
            fontsize=9,color='darkgrey',rotation=0,ha='center',va='center')
    
fig.subplots_adjust(bottom=0.15)
       
plt.savefig(directoryfigure + 'nsidc_sie_Bering.png',dpi=300)  

print('Completed: Script done!')                          