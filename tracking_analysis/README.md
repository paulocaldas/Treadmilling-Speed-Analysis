# Analyze Trajectories from XML files

This folder contains a python notebook `analyze_tracks.ipynb` that uses TrackMate's XML file as input. <br>
All the necessary modules are inside the `analyze_tracks` folder. <br>
This approach computes: <br>

* Velocities Distribuition Directly from Spot Displacement
* Velocitiy distribution from fitting MSD curves individually
* Average velocity from fitting a mean MSD curve
* Directionality from velocity auto-correlation analysis

*works for a single file or in batch. <br>
the output is a pdf containg all figs and an excel containing all data to plot elsewhere*

## Usage Requirements
0. Updated version of Anaconda
1. Clone the git repository 
2. Open a (Anaconda) prompt and change directory to the tracking_analysis folder:
    `cd path\tracking_analysis`
3. run pip install to install necessary python modules:
    `pip install -e .`
4. All requirements to make the code work are automatically resolved

## IPython notebook
1. Open `analyze_tracks.ipynb` in Jupyter or IPython notebook
2. Set variable `filename` or use example file
3. Use single or batch processing of entire folder

**clip:** *defines the % of the track lenght to fit the model* <br>
**plot_every:** *defines the interval for inidivual MSD curves (less curves saves computation time) <br>
*both parameters are optinal and set to 0.5 and 20, respecively

## Comand line Interface (optional feature)
1. Open a (Anaconda) prompt and change directory to tracking_analysis
2. Run the python command line interface. For the bundled example file with clip would be 0.25:

    " analyze_tracks_cli example\example_growth_Tracks.xml --clip 0.25 "
