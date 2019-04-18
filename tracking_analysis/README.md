# Tracking post-analysis
Analyze growth and shrinkage tracks by means of
* MSD
* Velocity auto-correlation
and export results as Excel sheets and plots as pdf

## Input
TrackMate track xml file

## Output
* MSD analysis
* Velocity auto-correlation

## Installation
1. Clone the git repository 
2. Open (Anaconda prompt) and change directory to tracking_analysis

    `cd tracking_analysis`
3. pip install

    `pip install -e .`

4. All requirements are automatically resolved

## Usage
You can run the tracking analysis using IPython notebook or from the command line interface

#### Command line interace (CLI)
1. Open (Anaconda prompt) and change directory to tracking_analysis
2. Run the python command line interface on the bundled example file with clip of 0.25

    `analyze_tracks_cli analyze_tracks_cli example\example_growth_Tracks.xml --clip 0.25`


#### IPython notebook
1. Open `analyze_tracks.ipynb` in Jupyter or IPython notebook
2. Set variable `filename` or use example file
3. Use single or batch processing of entire folder


