import pandas; pd = pandas
from xml.etree import cElementTree as ET

def tm_xml_tracks(fn):
    """Reads tracks from trackmate xml track file and returns a DataFrame 
    plus other additional data info (credits: Paulo Caldas) """
    
    tracks = ET.parse(fn)
    frame_interval = float(tracks.getroot().attrib["frameInterval"])
    time_units = str(tracks.getroot().attrib["timeUnits"])
    space_units = str(tracks.getroot().attrib["spaceUnits"])
    
    attributes = []
    for ti, track in enumerate(tracks.iterfind('particle')):
        for spots in track.iterfind('detection'):
            attributes.append([ti, int(spots.attrib.get('t')),
                                   float(spots.attrib.get('x')),
                                   float(spots.attrib.get('y'))])

    track_table = pd.DataFrame(attributes, columns=['TRACK_ID','FRAME','POSITION_X','POSITION_Y'])
    track_table['POSITION_T'] = track_table["FRAME"] * frame_interval
    
    return track_table, frame_interval, time_units, space_units