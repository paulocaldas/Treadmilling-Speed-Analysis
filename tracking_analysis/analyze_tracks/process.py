import os
import glob
import sys

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from tqdm import tqdm_notebook as tqdm

from . import read, msd, velocity, utils

def analyze_tracks(filename, clip = 0.5, plot_every = 20):
    '''runs all type of analyses and saves all plots into a
    single pdf file and all data as sheets of one excel book'''
    
    plt.close("all")
    
    table_tracks, frame_interval, time_units, space_units = read.tm_xml_tracks(filename)

    print('\nPhysical units: {}, {}'.format(space_units, time_units))
    print('Number of tracks: {}'.format(len(table_tracks.TRACK_ID.unique())))
    print('Frame interval: {} \n'.format(frame_interval))

    # savename = filename.split(sep='/')[-1][:-4]
    with PdfPages(filename[:-4] + '_All_figs.pdf') as pdf:
        
        #table_tracks = table_tracks[:1000] # temporary hack to analyze only a few trajectories
        
        velo_dist = velocity.velocities_distribution(table_tracks, frame_interval);
        pdf.savefig(bbox_inches="tight")
            
        all_msds_vel, all_msd_curves = msd.single_track_analysis(table_tracks, frame_interval, plot_every);
        pdf.savefig(bbox_inches="tight")

        V, D, msd_fit = msd.msd_velocity_analysis(table_tracks, frame_interval, clip = 0.5)
        pdf.savefig(bbox_inches="tight")
        
        vcorr_data = velocity.compute_directionality(table_tracks, frame_interval)
        pdf.savefig(bbox_inches="tight")
                   
        with pd.ExcelWriter(filename[:-4] + '_Trackmate_Trajectory_Analysis.xlsx') as excel_sheet:
            
            pd.Series(velo_dist).to_excel(excel_sheet, sheet_name = 'vels_dist', index=False, header = False)
            pd.Series(all_msds_vel).to_excel(excel_sheet, sheet_name = 'msd_vels_hist', index=False, header = False)
            all_msd_curves.to_excel(excel_sheet, sheet_name = 'all_msd_curves', index=False, header = False)
            msd_fit.to_excel(excel_sheet, sheet_name = 'averaged_MSD ', index=False)
            vcorr_data.to_excel(excel_sheet, sheet_name = 'vcorr', index=False)
    
    print('Done!')


class HiddenPrints:
    """
    Small Helper class to prevent print statments during batch processing
    by redirecting stdout to devnull
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout

# running in batch
def analyze_tracks_batch(files_dir, clip = 0.5, plot_every = 20):
    
    data_path = os.path.join(files_dir,'*Tracks.xml')
    files = glob.glob(data_path)
    
    if len(files) == 0:
        print('File directory is empty!')
    else:
        for i, xml_file in tqdm(enumerate(files), desc='Progress ...', total=len(files)):
            print('Processing ' + os.path.basename(xml_file))
            try: 
                with HiddenPrints(): analyze_tracks(xml_file, clip=clip, plot_every=plot_every) #this blocks print statments while running the function
            except:
                print ("\t Error: File '{}' could not be processed... skipping")
                continue
    print('\nAll Done! Yay!')