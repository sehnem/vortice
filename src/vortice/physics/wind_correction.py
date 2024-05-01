import numpy as np

def calculate_wind_direction(u, v, offset):
    """
    Calculate wind direction from u and v wind components.

    Args:
        u (np.ndarray): Array of u wind components.
        v (np.ndarray): Array of v wind components.
        offset (float): Offset to apply to the wind direction.

    Returns:
        np.ndarray: Array of wind directions in degrees.
    """
    # Calculate raw wind direction from wind vector

    return np.mod(180 - np.degrees(np.arctan2(v, u)) + offset, 360)


def angular_average(angles):
    """
    Calculate the angular average for a 1D array of angles in degrees.
    
    Args:
        angles (np.ndarray): 1D array of angular values in degrees.
    
    Returns:
        float: Angular average in degrees, normalized to the range 0-360.
    """
    # Convert angles to radians
    angles_rad = np.radians(angles)

    # Calculate the mean of cosines and sines
    cos_mean = np.mean(np.cos(angles_rad))
    sin_mean = np.mean(np.sin(angles_rad))

    return np.mod(np.degrees(np.arctan2(sin_mean, cos_mean)))