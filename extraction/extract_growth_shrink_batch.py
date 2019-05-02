#@ OpService ops
#@ File(label="Input directory containg (2D+time)", style="directory") input_dir
#@ String(label="File extensions", value='*.tif; *.tf8', persist=False) img_extensions

#@ String (visibility=MESSAGE, value="Image will be smoothed by a Gaussian filter") msg1
#@ Float(label="Sigma in time (frames)", value=1.5, stepSize=0.1, min=0) sigma_t
#@ Float(label="Sigma in space (pixel)", value=0.5, stepSize=0.1, min=0) sigma_xy

#@ Integer(label="Start Frame", value=0, min=0, persist=False) frame_start
#@ Integer(label="End Frame " , value=-1, persist=False) frame_end
#@ String (visibility=MESSAGE , value="(use -1 for last frame)") msg3

#@ Boolean(label="Normalize outputs", value=true) normalize_output

#@ Float(label="Pixel width in microns",  value=-1, stepSize=0.1, min=-1) pixel_width
#@ Float(label="Frame interval in seconds", value=-1, stepSize=0.1, min=0) frame_interval
#@ String (visibility=MESSAGE, value="To use pixel width and frame interval from meta-data use -1") msg4

#@Output comp
from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"

import os
import sys
import glob

from ij import IJ 
from loci.plugins import BF
from ij.plugin import ChannelSplitter
from net.imglib2.img.display.imagej import ImageJFunctions as IJF

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))

sys.path.append(get_script_patch())
from src.temporal_gradient import smooth_temporal_gradient

def main():
    files = []
    for filt in img_extensions.split(";"):
        if len(filt.strip()) > 0:
            files += glob.glob(os.path.join(str(input_dir), filt.strip()))
        else:
            files += glob.glob(os.path.join(str(input_dir), "*.*"))
            break


    if len(files) == 0:
        IJ.showMessage("No files found in '{}'\nfor extensions '{}'".format(str(input_dir), img_extensions))
    else:
        for fn in files:
            try:
                imp = BF.openImagePlus(fn)[0]
            except:
                IJ.showMessage("Could not open file '{}' (skipping).\nUse extension filter to filter non-image files...".format(str(fn)))
                continue

                
            img = IJF.wrap(imp)
            
            cali = imp.getCalibration().copy()
            if pixel_width > 0:
                cali.pixelWidth    = pixel_width
                cali.pixelHeight   = pixel_width
                cali.setUnit("micron")
            if frame_interval > 0:
                cali.frameInterval = frame_interval
                cali.setTimeUnit("sec.")
            
            imp_out = smooth_temporal_gradient(ops, img, sigma_xy, sigma_t, frame_start, frame_end, normalize_output)
            imp_out.setCalibration(cali)
        
            channels = ChannelSplitter.split(imp_out)            
            
            fn_basename = os.path.splitext(fn)[0]
            IJ.save(channels[0], "{}_shrinkage.tiff".format(fn_basename))
            IJ.save(channels[1], "{}_growth.tiff".format(fn_basename))
            
            print("{} processed".format(fn_basename))
             
        IJ.showMessage("Growth/shrinkage extraction of {} inputs finsihed.".format(len(files)))
       

if __name__ in ["__builtin__", "__main__"]:
    main()
