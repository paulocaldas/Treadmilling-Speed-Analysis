# Treadmilling-Speed-Analysis
### Automated image analysis protocol to quantify the velocities of dynamic protein filaments

The workflow of this protocol to analyze filament polymerization dynamics starts from time lapse movies of evenly labeled treadmilling protein filament networks, followed by three computational steps:

(i)	**Extraction**: generation of dynamic fluorescent speckles by image subtraction; <br>
(ii)	**Tracking**: detection and tracking fluorescent speckles to build treadmilling trajectories <br>
(iii)	**Tracking Analysis**: analysis of trajectories to quantify velocity and directionality of filaments 

All these algorithms use simple open-source tools (ImageJ plugins and python scripts) and can be applied for a single time-lapse movie or for multiple files at once in batch processing mode. This creates a highly time-efficient routine to identify and track hundreds of speckles at once. 


**(A) Extraction** <br>
**Construction of differential image stacks to create fluorescent speckles (ImageJ macro)**

To extract dynamic information from filament networks, this protocol uses a background subtraction method based on image subtraction intensity. By subtracting the intensity of two consecutive frames, motionless objects produce dark pixels while positive and negative intensity differences correspond to fluorescent material being added or removed at a given position, respectively. When applying this procedure to an image sequence, we create a new time-lapse movie containing moving fluorescent speckles, corresponding to growing and shrinking filament ends within the bundles. Accordingly, this process allows to visualize and quantify polymerization as well as depolymerization rates.

Since simple image subtraction is susceptible to noise and can generate stretched speckles when sample acquirement rates are not ideal, we incorporated a pre-processing step where a spatiotemporal low-pass filter is applied prior to image subtraction (3D Gaussian filter). The extent of the spatiotemporal smoothing is defined by σ_xy and σ_t and should be tuned through trial and error until speckles with a good signal-to-noise ratio are created: σ_xy is relative to the size of the object of interest (in pixels) and σ_t to the frame rate. This step not only removes acquisition noise, but also increases the temporal coherence of speckle trajectories, improving the quality of the detection and tracking procedure in the next step.

`extract_growth_shrink.py` computes growth and shrinkage speckles of a single time-lapse movie <br>
`extract_growth_shrink_batch.py` computes growth and shrinkage speckles of mutiple files at once <br>

**(B) Tracking** <br>
**Tracking the motion of the fluorescent speckles using TrackMate in Batch (ImageJ macro)**

Here, we take advantage of TrackMate for particle detection and tracking of the fluorescent speckles. Reconstructed trajectories from the identified spatial positions in time can be further analyzed to retrieve quantitative information about the type of behavior (e.g. directed or diffusive motion), diffusion constant, velocity or lifetime of the particles, as well as the length of trajectories. On a first approach to this routine, TrackMate GUI should be used to identify the optimal parameters for detecting, tracking and linking the trajectories of the particles. Once the parameters for a given experimental setup are defined, the Trackmate protocol can be applied to multiple time-lapse movies simultaneously with our ImageJ macro.

`track_growth_shrink.py` opens an interactive window to run TracMate without GUI <br>
`track_growth_shrink_batch.py` opens an interactive window to run TracMate for several files at once <br>
 
**(C) Tracking_Analysis** <br>
**Analyze trajectories to quantify velocity and directionality of filaments (Python notebook)**

Here, we use the spatiotemporal information of the trajectories obtained from TrackMate to quantify speed and directionality. 
We compute the mean square displacement (MSD) of the particles and fit all the curves to a quadratic equation containing both a diffusion (D) and a constant squared velocity (𝜈) term. The positive curvature our MSD curves is characteristic of particles moving directionally. To further corroborate the information regarding directed motion, we also compute the velocity autocorrelation function (φ (δt)), where the angle of the normalized displacement vectors are compared pairwise as a function of an increasing time interval (δt). Random motion particles typically show velocity vectors completely uncorrelated with φ = 0 for all δt, while particles with a directed migration display highly correlated velocity vectors (φ > 0) even for larger δt. Our routine to analyze speckle trajectories is implemented in a simple IPython notebook. All imported modules located in the adjacent folder can be edited and adapted according to the each user needs

`analyze_tracks.ipynb` computes velocity and directionality measurements for a single file or folder (batch) <br>

### Illustration of the Differential Image Protocol

![alt text](https://github.com/paulocaldas/Treadmilling-Speed-Analysis/blob/master/fig_differential_image_protocol.png)

Overall, this approach allowed us to surpass the limitations of using kymographs and only requires widely-used open-source software packages with no need to change the standard time-lapse imaging. Moreover, even though we used this approach to quantitatively characterize growth and shrinkage of in vitro treadmilling FtsZ filaments, we believe this approach is applicable to study the polymerization dynamics of other cytoskeletal systems.

for more details on this approach and reference to our work: <br>
*(future chapter/paper link)*

Examples implementing this approach:<br>
*ZapA stabilizes FtsZ filament bundles without slowing down treadmilling dynamics* <br>
https://www.biorxiv.org/content/10.1101/580944v2 <br>
*FtsZ assembles the bacterial cell division machinery by a diffusion-and-capture mechanism* <br>
https://www.biorxiv.org/content/10.1101/485656v1
