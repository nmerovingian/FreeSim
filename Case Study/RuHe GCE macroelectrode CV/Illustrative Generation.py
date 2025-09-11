from matplotlib import pyplot as plt 
import pandas as pd 
import numpy as np 
import matplotlib.ticker as mtick
from matplotlib.cm import tab10,viridis,Blues



linewidth = 3
fontsize = 12
figsize = [8,4.5]

font = {'family' : 'monospace',
        'weight' : 'bold',
        'size'   : fontsize }
plt.rc('font', **font)  # pass in the font dict as kwarg

scan_rates = [0.005,0.01,0.025,0.05,0.1,0.2,0.4] # V/s 
peak_currents = [] #A, to be collected by iterating all voltammograms
forward_scan_peak_potentials = []
reverse_scan_peak_potentials = []
colors = viridis(np.linspace(0,1,len(scan_rates)))
df = pd.read_excel('RuHex CV.xlsx')


fig, ax = plt.subplots(figsize=(8,4.5))

for index, scan_rate in enumerate(scan_rates):
    #Iterate all voltammograms in this file corresponding to scans at different scan rates
    ax.plot(df.iloc[:,2*index],df.iloc[:,2*index+1],color=tuple(colors[index]),lw=10,alpha=0.8)
    peak_current = df.iloc[:,2*index+1].min()
    peak_currents.append(peak_current)
    forward_scan_peak_potential = df.iloc[df.iloc[:,2*index+1].idxmin(),2*index]
    forward_scan_peak_potentials.append(forward_scan_peak_potential)
    reverse_scan_peak_potential = df.iloc[df.iloc[:,2*index+1].idxmax(),2*index]
    reverse_scan_peak_potentials.append(reverse_scan_peak_potential)

    print((forward_scan_peak_potential+reverse_scan_peak_potential)/2)

    df_individual  = pd.DataFrame({'Potential, V':df.iloc[:,2*index],'Current, A':df.iloc[:,2*index+1]})
    
    df_individual.to_csv(f'./Individual Voltammograms/{scan_rate:.2E}.csv',index=False)
    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
#ax.set_xlabel('Potential, V vs. SCE',fontsize='large',fontweight='bold')
#ax.set_ylabel('Current, A',fontsize='large',fontweight='bold')
#ax.legend()

plt.minorticks_off()
#ax.axis('off')
plt.tight_layout()

fig.savefig('RuHexCV.svg')

