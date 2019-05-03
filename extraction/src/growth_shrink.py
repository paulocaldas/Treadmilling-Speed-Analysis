#@ OpService ops
#@ ImagePlus(label=" Time-Lapse to process") imp

#@ String (visibility=MESSAGE, value="Image will be smoothed by a Gaussian filter") msg1
#@ Float(label="Sigma in time (frames)",  value=1.5, stepSize=0.1, min=0) sigma_t
#@ Float(label="Sigma in space (pixel)", value=0.5, stepSize=0.1, min=0) sigma_xy
#@ String (visibility=MESSAGE, value="Select range") msg2
#@ Integer(label="Start Frame", value=0, min=0, persist=False) frame_start
#@ Integer(label="End Frame ", value=-1, persist=False) frame_end
#@ String (visibility=MESSAGE, value="(use -1 for last frame)") msg3
#@ Boolean(label="Normalize outputs", value=true) normalize_output

#@Output comp
from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"

import os
import sys

from ij import IJ 
from ij import CompositeImage
from net.imglib2.img.display.imagej import ImageJFunctions as IJF

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))

sys.path.append(get_script_patch())
from temporal_gradient import rescale_uint8, smooth_temporal_gradient

def main():
	img = IJF.wrap(imp)
	
	img_out = smooth_temporal_gradient(ops, img, sigma_xy, sigma_t, frame_start, frame_end, normalize_output )
	img_out.setCalibration(imp.getCalibration().copy()) 
	comp = CompositeImage(img_out, CompositeImage.COMPOSITE) 
	comp.show()

if __name__ in ["__builtin__", "__main__"]:
	main()
	