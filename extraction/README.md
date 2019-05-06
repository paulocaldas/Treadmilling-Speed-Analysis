# Generating fluorescent speckles by differential imaging

This folder contains two macros for imageJ: one to process a single movie (`extract_growth_shrink.py`) and a second one to process multiple files at once (`extract_growth_shrink_batch.py`). Both macros rely on modules contained inside the src folder and for that reason they should be kept together as they are here.

## Generate speckles from a single time-lapse movie

1. Open movie of interest in ImageJ (or Fiji).
2. Open macro `extract_growth_shrink.py` and run it.
3. A window pops up to correct/confirm the physical units.
4. A GUI is open to set the frame range (whole movie by default) and the box filter parameters σ_xy and σ_t. 
5. The output is a composite movie containing two new movies corresponding to growth (green) and shrinkage (red) overlapped with the raw data (blue). These channels can be splited and used for the following analysis step.

The extent of the spatial smoothing is defined by the standard deviation (σ) of two Gaussian functions (σ_x and σ_y). Our protocol applies an isotropic smoothing (σ_x = σ_y = σ_xy) and should be adjusted according to the size of the object of interest (in pixels). Likewise, the number of frames considered for the spatial filtering (σ_t) depends on the dynamics of the process studied and needs to be optimized for every given frame rate. This parameter is adjusted through trial and error until speckles with a good signal-to-noise ratio are created.

## Generate speckles in batch
Once the optimal box filter parameters are defined for a given experimental setup our protocol can be apply for several files at once:

1. Open macro `extract_growth_shrink_batch.py` in ImageJ (or Fiji) and run it.
2. A GUI is open to select a directory folder containing the files of interest and set the parameters for batch analysis. Note that only .tif and .tf8 files are processed by default, if no other file extension is provided. As before, set the frame range, calibrate the physical units, and provide the optimal box filter parameters (σ_xy and σ_t) ideally defined beforehand using the macro for a single movie.
3. Image subtraction is computed for every file in a windowless manner and two new-time lapse movies containing fluorescent speckles (growth and shrinkage) are saved in the same selected directory
