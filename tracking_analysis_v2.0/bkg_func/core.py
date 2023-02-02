# bkg_functions to analyze trajectories 
# author = paulo.caldas@ist.ac.at // christoph.sommer@ist.ac.at

# import the basics
import pandas as pd
import numpy as np
import warnings
from functools import partial
from collections import defaultdict
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from xml.etree import cElementTree as ET
from matplotlib.backends.backend_pdf import PdfPages

# read and plot trajectories from xml files

def read_xml_tracks(fn):
    """Reads tracks from trackmate xml file and returns frame_interval, time_units,
	space_units and a table containg spot coordenates"""
    
    tracks = ET.parse(fn)
    frame_interval = float(tracks.getroot().attrib["frameInterval"])
    time_units = str(tracks.getroot().attrib["timeUnits"])
    space_units = str(tracks.getroot().attrib["spaceUnits"])
    
    attributes = []
    for ti, track in enumerate(tracks.iterfind('particle')):
        for spots in track.iterfind('detection'):
            attributes.append([ti, int(spots.attrib.get('t')),
                                   float(spots.attrib.get('x')),
                                   float(spots.attrib.get('y'))])

    track_table = pd.DataFrame(attributes, columns=['TRACK_ID','FRAME','POSITION_X','POSITION_Y'])
    track_table['POSITION_T'] = track_table["FRAME"] * frame_interval
    
    print('\nphysical units: {}, {}'.format(space_units, time_units))
    print('number of tracks: {}'.format(len(track_table.TRACK_ID.unique())))
    print('frame interval: {} \n'.format(frame_interval))

    return track_table, frame_interval, time_units, space_units

def plot_trajectories(table_tracks):
    """ Shows all the tracks """
    
    fig, ax = plt.subplots(figsize = (4,4), dpi = 120)
    plt.xlabel('x (microns)', fontsize=10)
    plt.ylabel('y (microns)', fontsize=10)
    #plt.xlim([0,55])
    #plt.ylim([0,55])
    
    for groups, columns in table_tracks.groupby('TRACK_ID'):
        plt.plot(columns['POSITION_X'],columns['POSITION_Y'], lw = 1)
    plt.title('Number of Tracks = ' + str(groups), fontsize = 9)
	
# all velocity functions

def compute_desloc_per_step(trajectory, frame_interval, coords = ['POSITION_X','POSITION_Y'], frame = 'FRAME'):
    """computes step displacement for a given track """
    desloc_per_step = (trajectory[coords] - trajectory[coords].shift(1)).dropna()
    desloc_per_step[frame] = trajectory[frame].shift(1).dropna()
    return desloc_per_step
	

def velocities_distribution(table_tracks, frame_interval, bins = 10):
    '''plots distribuition of velocities for all tracks directly from the track displacement'''
    
    print('... track displacement velocity analysis ... ')
    
    desloc_all_tracks = table_tracks.groupby("TRACK_ID").apply(compute_desloc_per_step, frame_interval = frame_interval);
    vel_dist = np.sqrt((desloc_all_tracks[['POSITION_X', 'POSITION_Y']] ** 2).sum(1)) / frame_interval * 1000 # in nm/s
    
    # plot histogram of velocitites in nanometers
    plt.figure(figsize = (4,3), dpi = 120)
    
    counts, bins, patches = plt.hist(vel_dist, bins = bins, 
                                     color = 'seagreen', alpha = 0.8, edgecolor = 'w',
                                     label = 'n_spots = ' + str(len(vel_dist)))
    
    plt.xlabel('velocitities (nm/s)', fontsize = 10)
    plt.ylabel('counts', fontsize = 10)
    plt.legend(loc = 0, fontsize = 8, frameon = True)
    plt.title("track displacement velocities", fontsize = 9)
    
    return vel_dist

# alternative version: compute the instant velocity of each track and averages everything for all tracks, smth like this:
# instant_velo = np.sqrt((desloc_per_step[coords[:-1]] ** 2).sum(1)) / (frame_interval * desloc_per_step[coords[-1]]) # gap corrects for jumps
# table_tracks.groupby("TRACK_ID").apply(instant_velo, frame_interval = frame_interval).mean()
# this creates a bias to a normal distribution as we compute a mean of means

def msd_per_track(trajectory, coords):
    """Compute MSD for one trajectory """
    
    msds = []
    n_shifts = len(trajectory)
    
    for shift in range(1, n_shifts):
        diffs = trajectory[coords] - trajectory[coords].shift(-shift)
        msd = np.square(diffs.dropna()).sum(axis=1)
        msds.append(msd.mean())  
    
    taus = np.array(range(1,n_shifts))
    return taus, msds

def parabola(t, D, V):                        
    return D*t + V*(t**2)
    
def single_track_analysis(table_tracks, frame_interval, clip = 0.5, plot_every = 10, bins = 10, coords = ['POSITION_X', 'POSITION_Y']):
    ''' fits quadratic velocity to each msd curve individually, with fitting parameters 
    diffusion coefficient (D) and velocity (V). the output is (i) velocity distribution
    array from all tracks and (ii) a list containing all the tau/msd curves'''
    
    print('... single track msd analysis ...')
          
    all_velocities = [] # will store velocities
    
    # computes curve (tau,msd pair) for each track
    all_msd_curves = table_tracks.groupby("TRACK_ID").apply(msd_per_track, coords=coords)
      
    # plot each curve and fit quadratic equation
    
    fig, ax = plt.subplots(1, 2, figsize=(8, 3),  dpi = 120)
    
    clip = clip             # defines the % of the length of the track to fit the equation below
    filtered_tracks = 0     # count number of final tracks analyzed
    
    for i, (taus, msd) in enumerate(all_msd_curves):                    
        
        np.insert(taus,0,0); np.insert(msd,0,0)
        
        taus = taus * frame_interval # convert number of frames in seconds
        
        # msds with at least 5 data points (frames) to make tHe fitting work
        
        if len(taus) > 2:
            
            filtered_tracks += 1
            
            #define the % of the length of the track to fit the equation
            clip = int(len(msd) * clip)
            
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                (D, V), cov = curve_fit(parabola, taus[:clip], msd[:clip], p0 = (1,1))

                if V < 0: 
                    continue
                    
                    print('negative velocity!')
				
                V = np.sqrt(V)
                                
            #t_values = np.linspace(0,taus[-1],300)
            
            if i % plot_every == 0: # plot only every nth curve to save ram memory and time
                
                ax[0].plot(taus, msd, '-o', markersize = 2, markeredgecolor = 'black', markeredgewidth = 0.2, 
										alpha = 0.4, lw = 1., color = plt.cm.Greens(i*0.1 + 100))
                
                
				# in case one wants to show the fits instead
				#ax[0].plot(t_values, parabola(t_values, D,V), '-', lw = 0.8, color = plt.cm.Greens(i*0.1))
                ax[0].set_title("single track MSD analysis", fontsize = 9)
                ax[0].set_xlabel('delay (s)', fontsize = 10)
                ax[0].set_ylabel('MSD ($\mu$m$^2$)', fontsize = 10)
            
            all_velocities.append(V * 1000) #save all velocities in nanometers
    
    if filtered_tracks < 10: 
        print('number of tracks with > 5 frames is too low or non-existent')
    
    # plot final histogram
    # all_velocities = [vel for vel in all_velocities if vel >= 1]

    counts, bins, patches = plt.hist(all_velocities, bins = bins, 
                                     color= 'seagreen', alpha = 0.8, edgecolor = 'w', 
                                     label = 'n_fits = ' + str(filtered_tracks))
    
    ax[1].set_xlabel('velocitities (nm/s)', fontsize=10)
    ax[1].set_ylabel('counts', fontsize = 10)
    ax[1].legend(loc = 0, fontsize = 8, frameon = True)
    ax[1].set_title("single track MSD velocities distribution", fontsize = 9)
    plt.subplots_adjust(wspace = 0.2)
    plt.tight_layout()
    
    #to generate a nice formated table
    all_msd_curves_table = [msds for i,(tau,msds) in enumerate(all_msd_curves)]
    time = np.arange(2, np.max([(len(i)) for i in all_msd_curves_table]) * frame_interval, frame_interval) # delay vector
    all_msd_curves_table.insert(0,time)
    all_msd_curves_table = pd.DataFrame(all_msd_curves_table).T
    
    return all_velocities, all_msd_curves_table

def msd_track_dictionary(trajectory, msds_values, coords = ['POSITION_X', 'POSITION_Y'], frame = "FRAME"):
    """Computes MSD and integrate results into a msds_values dictionary. Note,
	this function has no ouput, adds the pairs key,values to an existent dictionary """
    
    n_shifts = len(trajectory)
    for shift in range(1, n_shifts):
        diffs = trajectory[coords].shift(-shift) - trajectory[coords]
        msd = np.square(diffs.dropna()).sum(axis=1)
        
        taus = (trajectory[frame].shift(-shift) - trajectory[frame]).dropna()

        for t, m in zip(taus, msd):
            msds_values[t].append(m)
            
            
def msd_velocity_analysis(table_tracks, frame_interval, clip = 0.5, coords=['POSITION_X', 'POSITION_Y']):
    ''' takes the weighted average of all the msd curves for each tau and fits
    a quadratic velocity to estimate velocity (V) and/or diffusion coefficient (D)
    output: V,D and table containing fitting data'''
    
    print('... weighted msd analysis ...')
          
    msds_values = defaultdict(list)
    msds_values[0].append(0) # delay 0 has msd of 0

    table_tracks.groupby("TRACK_ID").apply(msd_track_dictionary, msds_values = msds_values, coords = coords)

    # get mean msd and respective std
    ntracks    = np.array(list(map(len, msds_values.values())))
    msds_means = np.array(list(map(np.mean, msds_values.values())))
    msds_std   = np.array(list(map(np.std, msds_values.values())))
    
    msds_std[0] = msds_std[1] # avoid infinity weight
    #sems   = msds_stds/(np.sqrt(ntracks))

    t_axis = np.arange(len(msds_means)) * frame_interval #frames to seconds
        
    fig, ax = plt.subplots(1, figsize=(4,3), dpi = 120)
    
    ax.plot(t_axis, msds_means, '--ob', markersize = 4, label= "mean MSD", 
            color = 'seagreen', markeredgecolor = 'black', markeredgewidth = 0.4)
    
    ax.fill_between(t_axis, msds_means - msds_std, msds_means + msds_std, color='seagreen',  alpha=0.1, label="std")
    
    # truncate data to avoid statistically irrelevant data
    clip = int(len(msds_means) * clip)-1
    
    T = t_axis[:clip]
    Y = msds_means[:clip]
    W = msds_std[:clip]
    
    parameters, cov = curve_fit(parabola, T, Y, sigma = W, p0=(1,1))
    (D,V) = parameters
    V = np.sqrt(V)

    # estimate standard deviation of the calculated parameters
    param_stdev = np.sqrt(np.diag(cov))
    V_std = param_stdev[1]
    D_std = param_stdev[0]
    
    t_values = np.linspace(0,t_axis[-1],100)
    ax.plot(t_values, parabola(t_values, *parameters), color = 'crimson', 
             label = " v_fit = {:4.2f} nm/s".format(V*1000)) # velocity converted in nm/s
    
    ax.set_xlabel('delays (s)', fontsize = 10)
    ax.set_ylabel('MSD ($\mu$m$^2$)', fontsize = 10)
    plt.title("weighted MSD analysis", fontsize = 9)
    #plt.xlim([0,(()])
    #plt.ylim([0,2.5])
    plt.legend(frameon = False, fontsize = 8)
    plt.tight_layout()
    
    fit_data = pd.DataFrame([t_axis, msds_means, msds_std, t_values, parabola(t_values, *parameters)]).T
    fit_data.columns = ['time','msd_mean','msd_std','x_fit','y_fit']
    
    return V, D, fit_data

# functions to compute directional persistence

def compute_dist_per_step(trajectory, coords = ['POSITION_X', 'POSITION_Y'] , frame = 'FRAME'):
    """computes step displacement of a given track"""
    dist_per_step = (trajectory[coords] - trajectory[coords].shift(1)).dropna()
    dist_per_step[frame] = trajectory[frame].shift(1).dropna()
    return dist_per_step

def track_autocorrelation(trajectory, dict_auto_corr_values, coords = ['POSITION_X', 'POSITION_Y'], frame = 'FRAME'):
    """ computes autocorrelation for a given 'dist_per_step' track table
    and integrates the result (tau,corr_values pair) into an existent dictionary.
    thus this function has no ouput, just adds key,values to dict """
    
    n_shifts = len(trajectory)  
    corr_0 = np.square(trajectory[coords]).sum(axis=1).mean()
    
    for shift in range(n_shifts):
        corr = trajectory[coords] * trajectory[coords].shift(shift)
        corr = corr.dropna().sum(axis=1) / corr_0

        taus = (trajectory[frame].shift(-shift) - trajectory[frame]).dropna()  # unit = frame number

        for t, m in zip(taus, corr):
            dict_auto_corr_values[shift].append(m)

def directional_persistence(track_table, frame_interval):
    ''' the directional autocorrelation function is applied to each track individual 
    and the correlation per step is saved as values of a dictionary with keys = taus.
    In the end, hundreds of correlation values are average for each delay time (tau)'''
    
    print('... directional persistence analysis ...')
    
    # compute step displacement for each trajectory
    distances_per_track = track_table.groupby("TRACK_ID").apply(compute_dist_per_step)

    # create an empty dictionary to add taus and correlation values
    auto_corr_values = defaultdict(list)

    # compute autocorrelation of each track (tau, corr pair) and add to the dictionary 
    distances_per_track.groupby("TRACK_ID").apply(partial(track_autocorrelation, dict_auto_corr_values = auto_corr_values))

    ntracks     = np.array(list(map(len, auto_corr_values.values())))      # number of tracks per tau
    corr_means  = np.array(list(map(np.mean, auto_corr_values.values())))  # mean corr_value per tau 
    corr_stds   = np.array(list(map(np.std, auto_corr_values.values())))   # stdev corr_value per tau
    corr_t_axis = np.arange(len(corr_means)) * frame_interval              # number of taus (frames) * time interval (in seconds)
    corr_sems   = corr_stds/(np.sqrt(ntracks))                             # stdev of the mean

    plt.figure(figsize=(4,3), dpi = 120)
    plt.plot(corr_t_axis, corr_means, '-g', label = " mean_correlation")
    plt.fill_between(corr_t_axis, corr_means - corr_sems, corr_means + corr_sems, color='seagreen',  alpha=0.1, label = "std_error")

    plt.hlines(0, xmin=0, xmax=corr_t_axis.max(), linestyles = '--', lw = 0.5)
    plt.legend(loc = 0, frameon = False, fontsize = 8)
    plt.xlabel("tau (s)" , fontsize=10)
    plt.ylabel("directional correlation", fontsize=10)
    plt.ylim([-1, 1.1])
    plt.title('directional persistence', fontsize = 9)
    plt.tight_layout()
    
    vcorr_data = pd.DataFrame([corr_t_axis,corr_means,corr_sems]).T
    vcorr_data.columns = ['time_axis','corr_mean','corr_sem']
    
    return vcorr_data

# main function	// concatenate all fcuntions

def analyze_tracks(filename, 
                   track_displacement = True,
                   msd_weighted = True,
                   msd_single_track = True,
                   directionality = True,
                   plot_tracks = True,
                   clip = 0.5, plot_every = 10):
    
    '''main function. computes all desire analyses written in the bkg_func folder.
	runs specific analysis if `True` and saves all the respective figs and tables
	as a single pdf file or excel book (respectively) using the same file directory'''
    
    #plt.close("all")
    
    track_table, frame_interval, time_units, space_units = read_xml_tracks(filename)

    # savename = filename.split(sep='/')[-1][:-4]
    with PdfPages(filename[:-4] + '_analyze_tracks_all_figs.pdf') as pdf:
        with pd.ExcelWriter(filename[:-4] + '_analyze_tracks_output.xlsx') as excel_sheet:        
            
            if track_displacement == True:
                vel_dist = velocities_distribution(track_table, frame_interval = frame_interval);
                
                pd.Series(vel_dist).to_excel(excel_sheet, sheet_name = 'vels_disp', index=False, header = False)
                pdf.savefig(bbox_inches="tight")

            if msd_weighted == True:

                V, D, table_msd_fit = msd_velocity_analysis(track_table, frame_interval = frame_interval, clip = clip)
                
                table_msd_fit.to_excel(excel_sheet, sheet_name = 'msd_weighted', index=False, header = True)
                pdf.savefig(bbox_inches="tight")

            if msd_single_track == True:
                all_single_msd_vel, all_curves = single_track_analysis(track_table, frame_interval = frame_interval, clip = clip, plot_every = plot_every)
                
                pd.Series(all_single_msd_vel).to_excel(excel_sheet, sheet_name = 'msd_single_vel_hist', index=False, header = False)
                all_curves.to_excel(excel_sheet, sheet_name = 'all_single_msd_curves', index=False, header = True)
                pdf.savefig(bbox_inches="tight")
            
            if directionality == True:
                vcorr_data = directional_persistence(track_table, frame_interval = frame_interval)
                
                vcorr_data.to_excel(excel_sheet, sheet_name = 'directionality', index=False)
                pdf.savefig(bbox_inches="tight")
                
            if plot_tracks == True:
                plot_trajectories(track_table)
                pdf.savefig(bbox_inches="tight")