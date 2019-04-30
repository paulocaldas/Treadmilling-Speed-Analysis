# Generating fluorescent speckles by differential imaging

Intensity subtraction of two consecutive frames generates a new time-lapse movie where persistent pixels are removed and only short-term intensity oscilations are kept. Thus, motionless objects generate dark pixels after this process, while positive and negative intensity differences correspond to fluorescent material being added or removed at a given position, respectively. We use this strategy to produce time-lapse movies of directionally moving fluorescent speckles corresponding to growth and shrinkage of protofilaments within bundles of a cytoskeletal protein called FtsZ. <br>
To reduce noise and background contribution during the subtraction process and improve the subsquent tracking procedure, we include a spatiotemporal Gaussian filter prior to image subtraction. Our script applies a box filter defined by σ(xy), which should be adjusted according to the size of the object of interest, and σ(t), which should be adjusted according to the frame rate.

## Usage: ImageJ macro

Two ImageJ macros (Jython) are available:

**extract_growth_shrink.py** <br>
*takes a time-lapse movie open in imageJ as input. An interactive window allows to correct/modify physical units, select the number of frames to analyze and set the box filter. The output is a composite movie containing two new movies corresponding to growth (green) and shrinkage (red) overlapped with the raw data. These channels can be splited and used for post-analsysis.*

**extract_growth_shrink_batch.py** <br>
*running the macro opens an interactive window that allows to select a folder containing several time-lapse movies, set the same parameter as before. The previous process is applied to all files in the selected folder in a windowless process. All 'growth' and 'shrink' movies are saved as tif files in the same directory.*

**growth_shrink.py and temporal_gradient.py**<br>
*contain necessary modules to run the macros above. they should be kept inside the same folder*
