# Generating fluorescent speckles by differential imaging

Intensity subtraction of two consecutive frames generates a new time-lapse movie where persistent pixels are removed and only short-term intensity oscilations are kept. Thus, motionless objects generate dark pixels after this process, while positive and negative intensity differences correspond to fluorescent material being added or removed at a given position, respectively. We use this strategy to produce time-lapse movies of directionally moving fluorescent speckles corresponding to growth and shrinkage of protofilaments within bundles of a cytoskeletal protein called FtsZ. <br>
To reduce noise and background contribution during the subtraction process and improve the subsquent tracking procedure, we include a spatiotemporal Gaussian filter prior to image subtraction. Our script applies a box filter defined by σ(xy), which should be adjusted according to the size of the object of interest, and σ(t), which should be adjusted according to the frame rate.

## Usage: ImageJ macro

Two ImageJ macros (Jython) are available:

**extract_growth_shrink.py**<br>
input: time-lapse movie open in imageJ. An interactive window allows to correct/modify physical units and set the box filter.
output: two new movies corresponding to growth (green) and shrinkage (red) overlapped with the raw data.
channels can be slipted and used for posterior analsysis

**extract_growth_shrink_batch.py**
input: an interactive window allows to select a folder containing several time-lapse movie, set correct/modify physical units and set the box filter.
output: runs the previous analysis to all files in a windowless process and saves all 'growth' and 'shrink' movies as tif files.

extract_growth_shrink.py	intial commit for growth/shrinkage extraction fiji scripts	13 days ago
extract_growth_shrink_batch.py	intial commit for growth/shrinkage extraction fiji scripts	13 days ago

growth_shrink.py
temporal_gradient.py	

You can run the tracking analysis using IPython notebook or from the command line interface
