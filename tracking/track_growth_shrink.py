#@ File(label="Input image containg growth or shrinkage (2D+time)", style="file") input_file

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
#@ Integer(label="Track duration (sec)", value=12, min=0) track_duration
#@ Float(label="Minimum track displacement (um)", value=0.2, min=0) track_displacement
#@ Float(label="Spot quality",  value=0, stepSize=0.1, min=0) quality
#@ Float(label="Spot signal-to-noise ratio",  value=0.5, stepSize=0.1, min=0) snr

from __future__ import print_function, division
import os
import sys
import math
from collections import namedtuple

from java.io import File
from loci.plugins import BF
from ij import IJ, ImagePlus, ImageStack, WindowManager

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))
# TODO: this will change one the scripts are nicely packaged
sys.path.append(get_script_patch())

from trackmate_utils import run_trackmate

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
                                            

def get_image(input_file):
    imp = BF.openImagePlus(input_file)[0]
    
    # Reorder stack to swap Z and T if needed
    nframes = imp.getDimensions()[4]
    nslices = imp.getDimensions()[3]
    if nframes == 1:
        IJ.run("Re-order Hyperstack ...", "channels=[Channels (c)] slices=[Frames (t)] frames=[Slices (z)]");
    
    return imp

        
if __name__ in ["__builtin__", "__main__"]:
    params = UserParameters(do_subpixel_localization, 
                            diameter / 2., 
                            threshold, 
                            do_median_filtering, 
                            linking_max_distance, 
                            gap_closing_max_distance, 
                            max_frame_gap, 
                            track_duration, 
                            track_displacement,
                            quality, 
                            snr)

    input_file = str(input_file)
                            
    path = os.path.dirname(input_file)
    file_name = os.path.basename(input_file)
    
    imp = get_image(input_file)
    run_trackmate(imp, path, file_name, params)

