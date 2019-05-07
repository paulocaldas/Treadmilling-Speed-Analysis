#@ File(label="Input folder with growth/shrinkage movies", style="directory") input_dir
#@ String(label="File extension", value="tiff") file_ext

#@ String (visibility=MESSAGE, value="Detector settings") msg1
#@ Float(label="Diameter of speckle (um)",  value=0.5, stepSize=0.02, min=0) diameter
#@ Float(label="Threshold", value=5, stepSize=0.1, min=0) threshold
#@ Boolean(label="Subpixel localization", value=true) do_subpixel_localization
#@ Boolean(label="Median filtering", value=False) do_median_filtering

#@ String (visibility=MESSAGE, value="Linker settings") msg2
#@ Float(label="Link maximum distance (um)",  value=0.5, stepSize=0.02, min=0) linking_max_distance
#@ Float(label="Gap closing maximum distance (um)",  value=0.5, stepSize=0.02, min=0) gap_closing_max_distance
#@ Integer(label="Maximum frame gap (frames)", value=0, min=0) max_frame_gap

#@ String (visibility=MESSAGE, value="Filter settings") msg3
#@ Float(label="Particles min SNR ratio",  value=0.5, stepSize=0.1, min=0) snr
#@ Float(label="Track min displacement (um)", value=0.2, min=0) track_displacement
#@ Integer(label="Track min duration (sec)", value=12, min=0) track_duration

from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"


import os
import sys
import math
import glob
from collections import namedtuple

from java.io import File
from loci.plugins import BF
from ij import IJ, ImagePlus, ImageStack, WindowManager

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))
# TODO: this will change one the scripts are nicely packaged
sys.path.append(get_script_patch())

from src.trackmate_utils import run_trackmate

UserParameters = namedtuple("UserParameters",  
							   ['do_subpixel_localization', 
                                'radius', 
                                'threshold', 
                                'do_median_filtering', 
                                'linking_max_distance', 
                                'gap_closing_max_distance', 
                                'max_frame_gap', 
                                'track_duration', 
                                'track_displacement',
                                'quality', 
                                'snr'
                               ])      
                                 
def main(input_dir, file_contains, params):
    file_list = glob.glob(os.path.join(str(input_dir), "*.{}".format(file_ext)))

    file_contains = file_contains.strip()
    if len(file_contains) > 0:
        file_list = filter(lambda x: file_contains in os.path.basename(x), file_list)

    if len(file_list) == 0:
        IJ.showMessage("No files found to process.")
        return
        

    for input_file in file_list:
        imp = BF.openImagePlus(input_file)[0]
        path = os.path.dirname(input_file)
        file_name = os.path.basename(input_file)
    
        run_trackmate(imp, path, file_name, params, batch_mode=True)

    IJ.showMessage("Processing of {} input files done.".format(len(file_list)))
        
if __name__ == "__builtin__":

    file_contains = ""
    params = UserParameters(do_subpixel_localization, 
                            diameter / 2., 
                            threshold, 
                            do_median_filtering, 
                            linking_max_distance, 
                            gap_closing_max_distance, 
                            max_frame_gap, 
                            track_duration, 
                            track_displacement,
                            0, 
                            snr)
                            
    main(input_dir, file_contains, params)
                     

    

