import numpy; np=numpy
import pandas; pd=pandas

import warnings
from functools import partial
from collections import defaultdict
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt


def msd_per_track(trajectory, coords):
    """Compute MSD for one trajectory """
    
    msd_curve = []
    n_shifts = len(trajectory)
    
    for shift in range(1, n_shifts):
        diffs = trajectory[coords] - trajectory[coords].shift(-shift)
        msd = np.square(diffs.dropna()).sum(axis=1)
        msd_curve.append(msd.mean())  
    
    taus = np.array(range(1,n_shifts))
    return taus, msd_curve


def msd_all_tracks(trajectory, msds_values, coords, frame="FRAME"):
    """Computes MSD and integrate results into a msds_values 
    dictionary. Note, this function has no ouput, adds the 
    pairs key,values to an existent dictionary
    """
    
    n_shifts = len(trajectory)
    for shift in range(1, n_shifts):
        diffs = trajectory[coords].shift(-shift) - trajectory[coords]
        msd = np.square(diffs.dropna()).sum(axis=1)

        taus = (trajectory[frame].shift(-shift) - trajectory[frame]).dropna()

        for t, m in zip(taus, msd):
            msds_values[t].append(m)

def parabola(t, D, V):                        
    return D*t + V*(t**2)

def gaussian(x, a, mu, sigma):
    return a*np.exp(-(x-mu)**2/(2*sigma**2))

def single_track_analysis(table_tracks, frame_interval, plot_every=10, track_id="TRACK_ID", coords=['POSITION_X', 'POSITION_Y']):
    ''' fits quadratic velocity to each msd curve individually
        returns diffusion coefficient and velocity in nm 
        output: (1) velocity distribution array and (2) list containing all dt/msd '''
    
    print('Processing Single Track MSD Analysis ...')
          
    all_velocities = [] # will store velocities
    
    # computes msd for each track
    all_msd_curves = table_tracks.groupby(track_id).apply(msd_per_track, coords=coords)
      
    fig, ax = plt.subplots(1, 2, figsize=(11, 4),  dpi=100)
    
    # for each curve (taus, msd values) fits the velocity with a quadratic equation
    
    clip = 0.5
    
    for i, (taus, msd) in enumerate(all_msd_curves):                    
        
        np.insert(taus,0,0)
        np.insert(msd,0,0)
        
        taus = taus * frame_interval
        
        if len(taus) > 5:
            
            clip = int(len(msd) * clip)

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                (D, V), cov = curve_fit(parabola, taus[:clip], msd[:clip], p0=(1,1))
                if V < 0:
                    continue
                V = np.sqrt(V)

            t_values = np.linspace(0,taus[-1],100)

            # plot only every 10th curve to save memory and time
            if i % plot_every == 0:
                #plt.figure(figsize=(4, 3), dpi=100)
                ax[0].plot(taus,msd, '-', lw=0.8, color = plt.cm.Blues(int(i // plot_every)*plot_every + 5))
                #ax[0].plot(t_values, parabola(t_values, *parameters))
                ax[0].set_title("MSD Single Track Analysis")
                ax[0].set_xlabel('Delay (s)', fontsize = 12)
                ax[0].set_ylabel('MSD ($\mu$m$^2$)', fontsize = 12)

            all_velocities.append(V*1000) #save all velocities in nanometers

    # plot final histogram
    all_velocities = [vel for vel in all_velocities if vel >= 1]
    
    binning = [max(len(all_velocities)) - min(len(all_velocities))]/10
    
    counts, bins, patches = plt.hist(all_velocities, bins = binning, edgecolor = 'black')
    
    bins = (bins[:-1] + np.diff(bins) / 2)
    
    param, cov = curve_fit(gaussian, bins,counts, p0=(10,10,10))
    x_values_to_fit = np.linspace(bins[0], bins[-1], 100)
    
    ax[1].plot(x_values_to_fit, gaussian(x_values_to_fit, *param),'r-', label = "GausFit \nmean = {:4.2f} nm/s".format(param[1]))
    ax[1].set_xlabel('Velocitities (nm/s)', fontsize=12)
    ax[1].set_ylabel('Counts', fontsize=12)
    ax[1].legend(loc=0, fontsize = 10, frameon = False)
    ax[1].set_title(" MSD Velocities Distribution")
    plt.subplots_adjust(wspace = 0.2)
    plt.tight_layout()
    
    #to generate a nice formated table
    all_msd_curves_table = [msds for i,(tau,msds) in enumerate(all_msd_curves)]
    time = np.arange(2, np.max([(len(i)) for i in all_msd_curves_table]) * frame_interval, frame_interval) # generate delays vector
    all_msd_curves_table.insert(0,time)
    all_msd_curves_table = pd.DataFrame(all_msd_curves_table).T
    
    return all_velocities, all_msd_curves_table


def msd_velocity_analysis(table_tracks, frame_interval, clip = 0.5, track_id="TRACK_ID", coords=['POSITION_X', 'POSITION_Y']):
    ''' takes the weighted average of all the msd curves estimated previously
    and fits a quadratic velocity to estimate velocity and/or diffusion coefficient
    output: velocity (V) and diffusion coeefient (D) from equation '''
    
    print('Processing Averaged MSD Analysis ...')
          
    msds_values = defaultdict(list)
    msds_values[0].append(0) # delay 0 has msd of 0

    table_tracks.groupby(track_id).apply(msd_all_tracks, msds_values = msds_values, coords=coords)

    # get mean msd and respective std
    ntracks    = np.array(list(map(len, msds_values.values())))
    msds_means = np.array(list(map(np.mean, msds_values.values())))
    msds_std   = np.array(list(map(np.std, msds_values.values())))
    
    msds_std[0] = msds_std[1] # avoid infinity weight
    #sems   = msds_stds/(np.sqrt(ntracks))

    t_axis = np.arange(len(msds_means)) * frame_interval 
        
    fig, ax = plt.subplots(1, figsize=(5, 4), dpi=100)
    
    ax.plot(t_axis, msds_means, '--sb', markersize = 5, label= "Mean MSD")
    ax.fill_between(t_axis, msds_means - msds_std, msds_means + msds_std, color='blue',  alpha=0.1, label="Std")
    
    # clip data to first half (or less!) to avoid statistically irrelevant data
    clip = int(len(msds_means) * clip)-1
    
    T = t_axis[:clip]
    Y = msds_means[:clip]
    W = msds_std[:clip]
    
    parameters, cov = curve_fit(parabola, T, Y, sigma = W, p0=(1,1))
    (D,V) = parameters
    V = numpy.sqrt(V)

    #Estimate standard deviation of the calculated parameters
    param_stdev = np.sqrt(np.diag(cov))
    V_std = param_stdev[1]
    D_std = param_stdev[0]
    
    t_values = np.linspace(0,t_axis[-1],100)
    ax.plot(t_values, parabola(t_values, *parameters), color = 'red', 
             label = " V = {:4.2f} nm/s".format(V*1000))
    ax.set_xlabel('Delays (s)', fontsize=12)
    ax.set_ylabel('MSD ($\mu$m$^2$)', fontsize=12)
    plt.title("MSD All Tracks Analysis")
    #plt.xlim([0,(()])
    #plt.ylim([0,2.5])
    plt.legend(frameon = False)
    plt.tight_layout()
    
    fit_data = pd.DataFrame([t_axis, msds_means, msds_std, t_values, parabola(t_values, *parameters)]).T
    fit_data.columns = ['time','msd_mean','msd_std','x_fit','y_fit']
    
    return V, D, fit_data
