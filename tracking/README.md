# Tracking Fluorescent speckles with TrackMate (ImageJ)

Here we use TrackMate for particle detection and tracking (Tinevez et al. 2016). We decided to use this tool since it is an open-source toolbox available for ImageJ and provides a user-friendly graphical user interface (GUI) with several features for visualization and data export. On a first apporach we used TrackMate's GUI to identify the best parameters for detecting, tracking and linking the trajectories of fluorescent speckles on our data. After finding those optimal parameters, we can process TrackMate in batch to analyze multiple time-lapse movies without using the GUI. For this purpose we wrote a macro for imageJ that uses the Laplacian detector (LoG) and a set of different filters that we found handy for our analysis. They can of course be set to zero if unecessary.

## Usage

`track_growth_shrink_batch.py` <br>
*running the macro opens an interactive dialogue that allows to select the directory folder and introduce all the necessary parameters (is self-explanatory). TrackMate runs on the background and saves two xml files for each analyzed movie (same directory). The 'TM' file can be load back on imageJ (load TrackMate file option) and check the whole analysis. The xml file contains all the coordenates and temporal info for each particle and trajectory. This second file is then used as input for the last step of the analysis.*
