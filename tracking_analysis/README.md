# Analyze Trajectories from XML files

This folder contains a python notebook `analyze_tracks.ipynb` that uses TrackMate's XML file as input and computes: <br>

* Velocities distribution (histogram) directly from particle displacement
* Velocity distribution (histogram) from fitting MSD curves individually (assuming directed motion)
* Average velocity from fitting a weighted-mean MSD curve (assuming a directed motion)
* Velocity auto-correlation function

works for a single file or in batch. <br>
the output is a pdf containing all figs and an excel containing all data to plot elsewhere
All the necessary modules are inside the `analyze_tracks` folder.* <br>

## Usage Requirements
0. Updated version of Anaconda
1. Clone the git repository 
2. Open a (Anaconda) prompt and change directory to the tracking_analysis folder:
    `cd path\tracking_analysis`
3. run pip install to install necessary python modules:
    `pip install -r requirements.txt -e .`
4. All requirements to make the code work are automatically resolved

## IPython notebook
1. Open `analyze_tracks.ipynb` in Jupyter or IPython notebook
2. Set variable `filename` or use example file
3. Use single or batch processing of entire folder

**clip:** *defines the % of the track length to fit the model and is set to 0.5 by default* <br>
**plot_every:** *defines the interval for individual MSD curves and is set to 20 by default (less curves saves computation time)* <br>

## Command line Interface (optional feature)
1. Open a (Anaconda) prompt and change directory to tracking_analysis
2. Run the python command line interface. For the bundled example file with clip would be 0.25:

    `analyze_tracks_cli example\example_growth_Tracks.xml --clip 0.25`
