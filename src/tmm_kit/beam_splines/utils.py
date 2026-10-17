import numpy as np


def adaptive_stiffness(
    element_length: float | np.ndarray,
    bandwidth: float,
):
    """Calculate adaptive beam support stiffness for better smoothing."""
    return element_length / bandwidth ** 4


def smoothing_spline_response(t_divider, bandwidth):
    """Calculate a theoretical smoothing spline response.

    It shows how much a smoothing spline of a given bandwidth
    attenuates a y(t) = cos(t / t_divider) signal.
    """
    return t_divider ** 4 / (bandwidth ** 4 + t_divider ** 4)
