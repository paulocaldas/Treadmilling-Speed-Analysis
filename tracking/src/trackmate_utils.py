"""
Christoph Sommer (IST Austria, 2019, christoph.sommer@ist.ac.at)
Paulo Caldas (IST Austria, 2019, pcaldas@ist.ac.at)


Uses the LoG detector and the Simple LAP Tracker
Accepts a SPT movie as input and saves the xml file as output (in the same dir)
a module at the bottom can be enable to save spots and tracks statistics
"""
from __future__ import print_function, division

__author__ = "christoph.sommer@ist.ac.at"


import os
import sys
import math
from collections import namedtuple
from java.io import File
from ij import IJ, ImagePlus, ImageStack, WindowManager

# Core TrackMate
from fiji.plugin.trackmate.io import TmXmlWriter
from fiji.plugin.trackmate.util import TMUtils
from fiji.plugin.trackmate import Settings, Model, SelectionModel, TrackMate
from fiji.plugin.trackmate.detection import DetectorKeys
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from fiji.plugin.trackmate.detection import DogDetectorFactory, LogDetectorFactory
from fiji.plugin.trackmate.features import FeatureFilter, \
                                           FeatureAnalyzer, \
                                           ModelFeatureUpdater
                                          
# Spot staticstics
from fiji.plugin.trackmate.features.spot import SpotContrastAndSNRAnalyzerFactory, \
                                                SpotIntensityMultiCAnalyzerFactory

# Track statistics
from fiji.plugin.trackmate.features.track import TrackBranchingAnalyzer, \
                                                 TrackDurationAnalyzer, \
                                                 TrackSpotQualityFeatureAnalyzer, \
                                                 TrackIndexAnalyzer, \
                                                 TrackLocationAnalyzer, \
                                                 TrackSpeedStatisticsAnalyzer
# Display results
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.visualization.hyperstack import  HyperStackDisplayer
# Export results
from fiji.plugin.trackmate.action import ExportTracksToXML
                                            

def run_trackmate(imp, path, filename, params, batch_mode=False):
    # initialize trackmate model
    model = Model()
    
    # Set logger - use to see outputs, not needed in batch mode
    model.setLogger(Logger.IJ_LOGGER)
    
    # Create setting object from image
    settings = Settings(imp)
    
    cal = imp.getCalibration()
    model.setPhysicalUnits("micron", "sec")
    
    # Configure detector
    settings.detectorFactory = LogDetectorFactory()
#    settings.detectorFactory = DogDetectorFactory()

    settings.detectorSettings = { 
      'DO_SUBPIXEL_LOCALIZATION' : params.do_subpixel_localization,
      'RADIUS' : params.radius, 
      'TARGET_CHANNEL' : 0,
      'THRESHOLD' : params.threshold,
      'DO_MEDIAN_FILTERING' : params.do_median_filtering,
    } 
    
#    print(params)
    
    # Add spot filters
    filter_quality = FeatureFilter('QUALITY', params.quality, True)
    settings.addSpotFilter(filter_quality)
    filter_snr = FeatureFilter('SNR', params.snr, True)
    settings.addSpotFilter(filter_snr)
    
    # Compute spot features
    settings.addSpotAnalyzerFactory(SpotIntensityMultiCAnalyzerFactory())
    settings.addSpotAnalyzerFactory(SpotContrastAndSNRAnalyzerFactory())
    
    # Compute track features
    settings.addTrackAnalyzer(TrackBranchingAnalyzer())
    settings.addTrackAnalyzer(TrackDurationAnalyzer())
    settings.addTrackAnalyzer(TrackIndexAnalyzer())
    settings.addTrackAnalyzer(TrackLocationAnalyzer())
    settings.addTrackAnalyzer(TrackSpeedStatisticsAnalyzer())
    settings.addTrackAnalyzer(TrackSpotQualityFeatureAnalyzer())
    
    # Update model
    ModelFeatureUpdater(model, settings )
    
    # Configure tracker
    settings.trackerFactory = SparseLAPTrackerFactory()
    settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
    settings.trackerSettings['LINKING_MAX_DISTANCE']     = params.linking_max_distance
    settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = params.gap_closing_max_distance
    settings.trackerSettings['MAX_FRAME_GAP']            = params.max_frame_gap
    
    # Add track filters
    filter_T1  = FeatureFilter('TRACK_DURATION'    , params.track_duration, True)
    filter_MTD = FeatureFilter('TRACK_DISPLACEMENT', params.track_displacement, True)

    settings.addTrackFilter(filter_T1)
    settings.addTrackFilter(filter_MTD)

    
    # Instantiate trackmate
    trackmate = TrackMate(model, settings)
     
    # Execute all
     
    ok = trackmate.checkInput()
    if not ok:
        IJ.showMessage("No spots found... Adjust detection parameter.\n" + str(trackmate.getErrorMessage()))
        sys.exit(str(trackmate.getErrorMessage()))
     
    ok = trackmate.process()
    if not ok:
        IJ.showMessage("No spots found... Adjust detection parameter.\n" + str(trackmate.getErrorMessage()))
        sys.exit(str(trackmate.getErrorMessage()))
    
    filename = os.path.splitext(filename)[0] #filename without extension
    outFile = File(os.path.join(path, filename + "_Tracks.xml"))
    ExportTracksToXML.export(model, settings, outFile)
    #imp.close()

    tm_writer = TmXmlWriter(File(os.path.join(path, filename + "_TM.xml")))
    tm_writer.appendModel(model)
    tm_writer.appendSettings(settings)
    tm_writer.writeToFile()
    

    if not batch_mode:
        selectionModel = SelectionModel(model)
        displayer = HyperStackDisplayer(model, selectionModel, imp)
        displayer.render()
        displayer.refresh()
        # Echo results with the logger we set at start:
        model.getLogger().log(str(model))
        
if __name__ == "__builtin__":
    pass

