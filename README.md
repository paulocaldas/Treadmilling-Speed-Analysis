# Treadmilling-Speed-Analysis
**Automated image analysis protocol to quantify the velocities of dynamic protein filaments**

This approach allows to quantify the velocities of thousands of dynamic treadmilling filaments simultaneously using simple open-source tools, namely ImageJ plugins and home-built pythn scripts. The approach is divided in three distinct steps:

**(A) Extraction** <br>
**Construction of differential image stacks to create fluorescent speckles (ImageJ macro)** <br>
`extract_growth_shrink.py` computes growth and shrinkage speckles of a single time-lapse movie <br>
`extract_growth_shrink_batch.py` applies the same computation to a folder containing multiple files <br>

**(B) Tracking** <br>
**Tracking the motion of the fluorescent speckles using TrackMate in Batch (ImageJ macro)** <br>
`track_growth_shrink_batch.py` opens an interactive window to run TracMate for several files at once <br>
 
**(C) Tracking_Analysis** <br>
**Analyze trajectories to quantify velocity and directionality of filaments (Python notebook)** <br>
`analyze_tracks.ipynb` computes velocity and directionality measurements for a single file or folder (batch) <br>

for more details on this approach and reference to our work check ***(future paper link)*** <br>
and some other examples of implementing this approach: ***(ZapA and FtsN paper)***
