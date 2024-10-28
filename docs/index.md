# pointextract

Polar to cartesian transforms using annular point sampling.

Designed to unwrap 2D cross section images of 3D X-ray computed tomography scans.
The topological transformation enables the surface of a circular or elliptical object to be "unwrapped" for downsteam analysis.

<img src="workflow.png" width="700">

## Installation

You can install the package with:
```bash
pip install pointextract
```

## Example

Simple example:
```python
import pointextract
from skimage import io, filters

img_arr = io.imread('./data/sample.png')

img_thresh = img_arr > filters.threshold_otsu(img_arr)
ellipse = ellipse_detect(img_thresh)

img_unwrap = unwrap_image(img_arr, ellipse, radial_distance=20, num_points=800)
```

## Functions

::: pointextract.main
