from typing import List, Tuple

import numpy as np
from skimage.feature import canny
from skimage.measure import EllipseModel

def ellipse_detect(img_arr: np.ndarray, sigma: float = 1.0) -> EllipseModel:
    """
    Detect an ellipse in a given image array using edge detection and ellipse fitting.

    Args:
        img_arr (np.ndarray): The input image array.
        sigma (float, optional): The standard deviation of the Gaussian filter used in edge detection. Defaults to 1.0.

    Returns:
        EllipseModel: Fitted ellipse object from scikit-image.

    Raises:
        ValueError: If the ellipse fitting fails.
    """
    edges = canny(img_arr, sigma=sigma)
    points = np.argwhere(edges != 0)
    ellipse = EllipseModel()
    if not ellipse.estimate(points):
        raise ValueError('Ellipse fitting failed. Try adjusting the sigma value or check the input image.')
    return ellipse

def unwrap_circle(img_arr: np.ndarray, radius: int, center: Tuple[int, int], points: int) -> np.ndarray:
    """
    Unwrap a circular region of an image into a linear array.

    Args:
        img_arr (np.ndarray): The input image array.
        radius (int): The radius of the circle to unwrap.
        center (Tuple[int, int]): The (y, x) coordinates of the circle's center.
        points (int): The number of points to sample along the circle.

    Returns:
        np.ndarray: A 1D numpy array containing the pixel values of the unwrapped circle.
    """
    def build_circle(r: int, num_points: int) -> Tuple[np.ndarray, np.ndarray]:
        """Generate x and y coordinates for a circle given a radius and number of points."""
        t = np.linspace(0, 2 * np.pi, num_points)
        x = r * np.cos(t)
        y = r * np.sin(t)
        return x.astype(int), y.astype(int)

    def center_circle(center: Tuple[int, int], x: np.ndarray, y: np.ndarray) -> List[Tuple[int, int]]:
        """Translate circle coordinates to be centered around a given point."""
        x = np.asarray(x) + int(center[1])  # x corresponds to columns (center[1])
        y = np.asarray(y) + int(center[0])  # y corresponds to rows (center[0])
        return list(zip(x, y))

    def extract_img_pix(points: List[Tuple[int, int]], img_arr: np.ndarray) -> np.ndarray:
        """Extract pixel values from the image at specified points."""
        return np.array([img_arr[y, x] for x, y in points])

    x, y = build_circle(radius, points)
    circle_points = center_circle(center, x, y)
    array_circle = extract_img_pix(circle_points, img_arr)
    return array_circle

def unwrap_image(img_arr: np.ndarray, ellipse: EllipseModel, radial_distance: int = 20, points: int = 600) -> np.ndarray:
    """
    Unwrap an annular region of an image centered around a specified ellipse into a 2D array.

    Args:
        img_arr (np.ndarray): The input image array.
        ellipse (EllipseModel): Ellipse object from scikit-image.
        radial_distance (int, optional): The radial distance from the base radius to start and end unwrapping. Defaults to 20.
        points (int, optional): The number of points to sample along each circle. Defaults to 400.

    Returns:
        np.ndarray: A 2D numpy array representing the unwrapped annular region.
    """
    xc, yc, a, b, theta = ellipse.params
    inner_radius = int(a) - radial_distance
    outer_radius = int(a) + radial_distance
    unwrapped_img = unwrap_circle(img_arr, outer_radius, (xc, yc), points)
    for i in reversed(range(inner_radius, outer_radius)):
        current_circle = unwrap_circle(img_arr, i, (xc, yc), points)
        unwrapped_img = np.vstack([unwrapped_img, current_circle])
    return unwrapped_img
