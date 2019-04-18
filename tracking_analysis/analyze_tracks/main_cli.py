import os
import argparse
from matplotlib import pyplot as plt
from . import process

description = \
"""
Mean-square-displacement and velocity auto-correlation analyzes of growth and shrinkage tracks 
"""

def get_args():
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('track_file', type=str, nargs="+", help="Trackmate xml-track file or folder containing several")
    parser.add_argument('--clip', type=float, default=0.5, help="Use only clip fraction for fitting (default 0.5)")
    parser.add_argument('--plot_every', type=int, default=20, help="Plot every p th single track in output plot (default: 20)")

    return parser.parse_args()

def run(track_file, clip, plot_every):
    if os.path.isdir(track_file):
        process.analyze_tracks_batch(track_file, clip=clip, plot_every=plot_every)

    elif os.path.isfile(track_file):
        process.analyze_tracks(track_file, clip=clip, plot_every=plot_every)

def main():
    args = get_args()

    for tm_xml_fn in args.track_file:
        # check if file exits
        assert os.path.exists(tm_xml_fn), "File / folder '{}' does not exists. Skipping...".format(tm_xml_fn)

        # process it
        run(tm_xml_fn, args.clip, args.plot_every)

    plt.show()


# if __name__ == "__main__":
#     main()
