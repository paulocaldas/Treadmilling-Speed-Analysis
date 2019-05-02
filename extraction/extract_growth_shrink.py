#@ ScriptService scripts
#@ ImagePlus(label="Image to process (2D+time)") imp
from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"

import os
import sys

from ij import IJ 
from java.io import File
from ij.gui import GenericDialog

def get_script_patch():
    import inspect
    return os.path.dirname(os.path.abspath(inspect.getsourcefile(lambda:0)))

root_pkg_path = get_script_patch()
sys.path.append(root_pkg_path)



def pixel_resolution_dialog(pixel_width=None, frame_interval=None):
    if pixel_width is None:
        pixel_width = 1
    if frame_interval is None:
        frame_interval = 1
        
    gd = GenericDialog("Specify image resolution")
    gd.addNumericField("Pixel width (microns): ", pixel_width, 4)
    gd.addNumericField("Frame interval (seconds): ", frame_interval, 4)

    gd.showDialog() 
    if gd.wasCanceled():
        return 

    pixel_width = gd.getNextNumber()
    frame_interval = gd.getNextNumber()
    return pixel_width, frame_interval

if __name__ in ["__builtin__", "__main__"]:
    cali           = imp.getCalibration().copy()
    pixel_width    = cali.pixelWidth
    frame_interval = cali.frameInterval
    
    res = pixel_resolution_dialog(pixel_width=pixel_width, frame_interval=frame_interval)
    if res:
        pixel_width, frame_interval = res
        cali.pixelWidth    = pixel_width
        cali.pixelHeight   = pixel_width
        cali.frameInterval = frame_interval
        cali.setUnit("micron")
        cali.setTimeUnit("sec.")

        imp.setCalibration(cali)
        
        scripts.run(File(os.path.join(root_pkg_path, "src", "growth_shrink.py")), True)