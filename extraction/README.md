# Generating fluorescent speckles by differential imaging

Intensity subtraction of two consecutive frame generates a new time-lapse movie where persistent pixels are removed and only short-term intensity oscilations are kept. Thus, motionless objects generate dark pixels, while positive and negative intensity differences correspond to fluorescent material being added or removed at a given position, respectively.
To reduce noise and background contribution during the subtraction process, we include a spatiotemporal Gaussian filter prior to image subtraction. Our script applies a box filter defined by σ(xy), which should be adjusted according to the size of the object of interest, and σ(t), which should be adjusted according to the frame rate. Note that this procedure is similar to compute a moving-average process, but in combination with a Gaussian function, possible undesired blurring effects are reduced.

## Usage: ImageJ macro

Two ImageJ macros (Jython) are available:

**extract_growth_shrink.py**<br>
input: time-lapse movie open in imageJ. An interactive window allows to correct/modify physical units and the box filter.
output: two new movies corresponding to growth (green) and shrinkage (red) overlapped with the raw data.
channels can be slipted and used for posterior analsysis

**extract_growth_shrink_batch.py**
input: select a folder containing several time-lapse movie



extract_growth_shrink.py	intial commit for growth/shrinkage extraction fiji scripts	13 days ago
extract_growth_shrink_batch.py	intial commit for growth/shrinkage extraction fiji scripts	13 days ago

growth_shrink.py
temporal_gradient.py	

You can run the tracking analysis using IPython notebook or from the command line interface
