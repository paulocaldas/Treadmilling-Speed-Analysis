# Treadmilling-Speed-Analysis
**Automated image analysis protocol to quantify the velocities of dynamic protein filaments**

This approach allows to quantify the velocities of thousands of dynamic treadmilling filaments simultaneously using simple open-source tools, namely ImageJ plugins and home-built pythn scripts. The approach is divided in three distinct steps:

**(A) Construction of differential image stacks to create fluorescent speckles (ImageJ macro)** <br>

**extract_growth_shrink.py**: computes growth and shrinkage speckles for a time-lapse movie <br>
**extract_growth_shrink.py**: applies the same computation to folder containing multile files <br>

**(B) Tracking the motion of the fluorescent speckles using TrackMate in Batch (ImageJ macro)** <br>

**track_growth_shrink_batch.py**: opens an interactive window that allow to run TracMate for several files at once <br>
 
**(C) Analyze trajectories to quantify velocity and directionality of filaments (Python notebook)** <br>

**analyze_tracks.ipynb**: computes several measurements of velocity and directionaly for a single file or in batch <br>

for more details on this approach and reference to our work check ***(future paper link)*** <br>
and some other examples of implementing this approach: ***(ZapA and FtsN paper)***
