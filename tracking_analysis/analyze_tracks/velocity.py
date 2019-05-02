import numpy; np=numpy
import pandas; pd=pandas

from functools import partial
from collections import defaultdict
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

def compute_velocities(trajectory, coords, frame="FRAME"):
    """computes velocity of tracks"""
    velo = (trajectory[coords] - trajectory[coords].shift(1)).dropna()
    velo[frame] = trajectory[frame].shift(1).dropna()

    return velo

def velocity_autocorr_all_tracks(trajectory, auto_corr_values, coords, frame="FRAME"):
    """Compute autocorrelation velocity for each trajectory
    and integrate results into a auto_corr_values dictionary.
    Note, this function has no ouput, adds key,values
    to an existent dictionary
    """
    n_shifts = len(trajectory)  
    corr_0 = np.square(trajectory[coords]).sum(axis=1).mean()
    
    for shift in range(n_shifts):
        corr = trajectory[coords] * trajectory[coords].shift(shift)
        corr = corr.dropna().sum(axis=1) / corr_0

        taus = (trajectory[frame].shift(-shift) - trajectory[frame]).dropna()

        for t, m in zip(taus, corr):
            auto_corr_values[shift].append(m)

def gaussian(x, a, mu, sigma):
    return a*np.exp(-(x-mu)**2/(2*sigma**2))


def velocities_distribution(table_tracks, frame_interval):
    '''plots distribuition of velocities directly from the track displacement'''
    
    print('Processing Velocities Distribution ...')
    
    velocities = table_tracks.groupby("TRACK_ID").apply(compute_velocities, coords=['POSITION_X', 'POSITION_Y']);
    velocities_dist = np.sqrt((velocities[['POSITION_X', 'POSITION_Y']] ** 2).sum(1)) / frame_interval * 1000 # in nm/s
    
    binning = int(np.sqrt(len(velocities_dist)))
    
    plt.figure(figsize=(5,4), dpi=100)
    counts, bins, patches = plt.hist(velocities_dist, bins = binning, color = 'blue', edgecolor = 'black')
       
    plt.xlabel('Velocitities (nm/s)', fontsize=12)
    plt.ylabel('Counts', fontsize=12)
    #plt.legend(loc=0, fontsize = 10, frameon = False)
    plt.title(" Velocities Distribution")
    
    return velocities_dist

def compute_directionality(table_tracks, frame_interval):
    'there is no output, just a visualization tool'
    
    print('Processing Velocity Autocorrelation ...')
          
    auto_corr_values = defaultdict(list)
    
    velocities = table_tracks.groupby("TRACK_ID").apply(compute_velocities, coords=['POSITION_X', 'POSITION_Y'])
    velocities.groupby("TRACK_ID").apply(partial(velocity_autocorr_all_tracks, auto_corr_values = auto_corr_values, coords=['POSITION_X', 'POSITION_Y']));

    ntracks     = np.array(list(map(len, auto_corr_values.values())))
    corr_means  = np.array(list(map(np.mean, auto_corr_values.values())))
    corr_stds   = np.array(list(map(np.std, auto_corr_values.values())))
    corr_t_axis = np.arange(len(corr_means)) * frame_interval
    corr_sems  = corr_stds/(np.sqrt(ntracks))

    plt.figure(figsize=(5,4), dpi=100)
    plt.plot(corr_t_axis, corr_means, '-b', label="<V_Corr>")
    plt.fill_between(corr_t_axis, corr_means - corr_sems, corr_means + corr_sems, color='blue',  alpha=0.1, label="error")

    plt.hlines(0, xmin=0, xmax=corr_t_axis.max(), linestyles = '--', lw = 0.5)
    plt.legend(loc=0, frameon = False)
    plt.xlabel("Delays (s)" , fontsize=12)
    plt.ylabel("Velocity Autocorrelation", fontsize=12)
    plt.ylim([-1, 1.1])
    plt.title('Directionality Analysis')
    plt.tight_layout()
    
    vcorr_data = pd.DataFrame([corr_t_axis,corr_means,corr_sems]).T
    vcorr_data.columns = ['time_axis','corr_mean','corr_sem']
    
    return vcorr_data
