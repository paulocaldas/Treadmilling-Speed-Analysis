import os
import argparse
from matplotlib import pyplot as plt
from analyze_tracks import read, msd, velocity, utils

description = \
"""
Mean-square-displacement and velocity auto-correlation analyzes of growth and shrinkage tracks 
"""

def get_args():
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('track_file', type=str, nargs='+', help="Trackmate xml-track file(s)")

    return parser.parse_args()

def process(tm_xml_fn):
    print("## Reading {}...".format(tm_xml_fn))

    # Read
    tracks, frame_interval, time_units, space_units = read.tm_xml_tracks(tm_xml_fn)

    print(' - Physical units: {}, {}'.format(space_units, time_units))
    print(' - Number of tracks: {}'.format(len(tracks.TRACK_ID.unique())))
    print(' - Frame interval: {}'.format(frame_interval))

    ## msd single
    vel_dist, all_msd_curves = msd.single_track_analysis(tracks, frame_interval)

    ## msd all
    msd.msd_velocity_analysis(tracks, frame_interval, clip = 0.5, units = 'µm/s')

    ## velcoity all
    velocity.compute_directionality(tracks, frame_interval)


def main():
    args = get_args()
    tm_xml_files = args.track_file

    for tm_xml_fn in tm_xml_files:
        # check if file exits
        assert os.path.exists(tm_xml_fn), "File '{}' does not exists. Skipping...".format(tm_xml_fn)

        # process it
        process(tm_xml_fn)

    plt.show()


if __name__ == "__main__":
    main()
