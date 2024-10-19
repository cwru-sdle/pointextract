# pointextract
Polar to cartesian transforms using annular point sampling

Designed to unwrap 2D cross section images of 3D X-ray computed tomography scans.
The topological transformation enables the surface of a circular or elliptical object to be aligned for downsteam analysis.

<img src="./docs/workflow.png" width="700">

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

## Questions
This package is still in early development. Please feel free to post to the GitHub Issues page with questions.

## Acknowledgements
This material is based upon research in the Materials Data Science for Stockpile Stewardship Center of Excellence (MDS3-COE).

<cite> [Case Western Reserve University, SDLElab] [1]</cite>

[1]: http://sdle.case.edu
