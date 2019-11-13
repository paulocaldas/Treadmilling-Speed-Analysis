# bkg_functions to analyze trajectories in batch 
# author = paulo.caldas@ist.ac.at // christoph.sommer@ist.ac.at

import os
import glob
import sys
from tqdm import tqdm_notebook as tqdm
from bkg_func import core

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
        
def run_batch_processing(files_dir,
                         track_displacement = True,
                         msd_weighted = False,
                         msd_single_track = False,
                         directionality = False,
                         plot_tracks = False,
                         clip = 0.5, plot_every = 10):

    data_path = os.path.join(files_dir,'*.xml')
    files = glob.glob(data_path)

    if len(files) == 0:
        print('File directory is empty!')
    
    else:
    	for n_file, xml_file in tqdm(enumerate(files), desc = 'progress ...', total=len(files)):
            
            print('processing ' + os.path.basename(xml_file))
			
            try:
                with HiddenPrints(): core.analyze_tracks(xml_file, #this blocks print statments while running the function
                                					track_displacement = track_displacement,
					                                msd_weighted = msd_weighted,
					                                msd_single_track = msd_single_track,
					                                directionality = directionality,
					                                plot_tracks = plot_tracks,
					                                clip = clip, plot_every = plot_every)
            except:
                print ("\t something went wrong: file could not be processed ... skipping")
                continue
    
    print('\ncomplete!')