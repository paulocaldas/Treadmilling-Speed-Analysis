# Analyze Trajectories from XML files

This folder contains a python notebook `analyze_tracks_v2.ipynb` that uses TrackMate's XML file as input and computes: <br>

 * velocity distribuition directly from spot displacement 
 * mean velocity retrieved from a quadratic fit to a weighted-MSD curve
 * mean velocities distribution from a quadratic fit to individual MSD curves
 * directional persistence based on directional auto-correlation analysis
 
<hr>
the script works for a single xml file or in batch for multiple files at once <br>
the output is a pdf containing all figs and an excel book containing all tables (to plot elsewhere) <br>
files are saved in the same directory of the filename or files_dir <br>
all the scripts are inside the bkg_func folder. <br>

## Automatically install/update necssary packages (if necessary)
0. Updated version of Anaconda
1. Clone the git repository 
2. Open a (Anaconda) prompt and change directory to the tracking_analysis folder:
    `cd path\tracking_analysis_v2`
3. run pip install to install necessary python modules:
    `pip install -r requirements.txt -e .`
4. All requirements to make the code work are automatically resolved

## Jupyther notebook // simple usage of our script
1. Open `analyze_tracks_v2.ipynb` in Jupyter or IPython notebook
2. Set variable `filename` with `path_to_file/my_xml_file.xml` (or use example file) to analyze a single file
3. Set variable `files_dir` with `path/folder_containing_xml_files` to analyze multiple files at once

**clip:** *sets the % of the track length to fit the model; float from 0.0 to 1.0 (0.5 by default)* <br>
**plot_every:** *sets how many individual MSD curves to plot (plots every nth curve, less curves saves computation time)* <br>
