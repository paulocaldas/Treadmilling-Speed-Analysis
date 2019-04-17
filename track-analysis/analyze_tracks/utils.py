from matplotlib import pyplot as plt

def plot_trajectories(table_tracks):
    """ Shows all the tracks """
    
    fig, ax = plt.subplots(figsize=(5,4), dpi = 100)
    plt.xlabel('x (microns)', fontsize=12)
    plt.ylabel('y (microns)', fontsize=12)
    plt.xlim([0,55])
    plt.ylim([0,55])
    
    for groups, columns in table_tracks.groupby('TRACK_ID'):
        plt.plot(columns['POSITION_X'],columns['POSITION_Y'], lw = 1)
    plt.title(['Number of Tracks =', groups])