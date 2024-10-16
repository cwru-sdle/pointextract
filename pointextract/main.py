import numpy as np
from skimage.feature import canny
from skimage.measure import EllipseModel

def ellipse_detect(img_arr, sigma=1):
    """
    Detects an ellipse in a given image array using edge
    detection and ellipse fitting.

    Parameters:
    - img_arr: ndarray, the input image array.
    - sigma: float, the standard deviation of the Gaussian
    filter used in edge detection.

    Returns:
    - Ellipse object from sci-kit image
    """
    # Perform edge detection
    edges = canny(img_arr, sigma=sigma)

    # Find coordinates of all edge points
    points = np.argwhere(edges != 0)

    # Fit an ellipse model to the edge points
    ellipse = EllipseModel()
    ellipse.estimate(points)

    return ellipse

def unwrap_circle(img_arr, radius, center, points):
    """
    Unwraps a circular region of an image into a linear array.

    Parameters:
    - img_arr: ndarray, the input image array.
    - radius: int, the radius of the circle to unwrap.
    - center: tuple, the (x, y) coordinates of the circle's center.
    - points: int, the number of points to sample along the circle.

    Returns:
    - A 1D numpy array containing the pixel values of the unwrapped circle.
    """
    def build_circle(r, num_points):
        """Generates x and y coordinates for a circle given a
        radius and number of points."""
        t = np.linspace(0, 2 * np.pi, num_points)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return x.astype(int), y.astype(int)

    def center_circle(center, x, y):
        """Translates circle coordinates to be centered around a
        given point."""
        x = np.asarray(x) + int(center[0])
        y = np.asarray(y) + int(center[1])
        return list(zip(x, y))

    def extract_img_pix(points, img_arr):
        """Extracts pixel values from the image at specified points."""
        return np.asarray([img_arr[y, x] for x, y in points])

    x, y = build_circle(radius, points)
    circle_points = center_circle(center, x, y)
    array_circle = extract_img_pix(circle_points, img_arr)

    return array_circle

def unwrap_image(img_arr, ellipse,
                 radial_distance=20, points=400):
    """
    Unwraps an annular region of an image centered around
    a specified circle into a 2D array.

    Parameters:
    - img_arr: ndarray, the input image array.
    - ellipse: obj, ellipse object from sci-kit image
    - radial_distance: int, the radial distance from the base
        radius to the start and end unwrapping.
    - points: int, the number of points to sample along each circle.

    Returns:
    - A 2D numpy array representing the unwrapped annular region.
    """
    xc, yc, a, b, theta = ellipse.params

    inner_radius = int(a) - radial_distance
    outer_radius = int(a) + radial_distance

    unwrapped_img = unwrap_circle(img_arr, inner_radius, (yc, xc), points)

    for i in reversed(range(inner_radius + 1, outer_radius)):
        current_circle = unwrap_circle(img_arr, i, (yc, xc), points)
        unwrapped_img = np.vstack([unwrapped_img, current_circle])

    return unwrapped_img
