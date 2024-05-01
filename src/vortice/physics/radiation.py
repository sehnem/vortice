import numpy as np

# TODO: implement the solar time equation
def potential_radiation_spencer(lat, dt, solar_constant=1376.0):
    """
    Calculate potential radiation based on latitude on a 30-minute basis.
    Returns an array of 17,568 radiation values.
    """
    # Calculate day of year (DOY), theta, and other parameters
    doy = dt.timetuple().tm_yday
    theta = 2 * np.pi * (doy - 1) / 365

    delta = (0.006918 - 0.399912 * np.cos(theta) + 0.070257 * np.sin(theta) -
             0.006758 * np.cos(2 * theta) + 0.000907 * np.sin(2 * theta) -
             0.002697 * np.cos(3 * theta) + 0.00148 * np.sin(3 * theta))

    las = 12 - dt.timetuple().tm_hour + dt.timetuple().tm_min/60

    omega = -15 * las
    lat_rad = np.radians(lat)

    omega_rad = np.radians(omega)
    theta_rad = np.arccos(
        np.sin(delta) * np.sin(lat_rad) +
        np.cos(delta) * np.cos(lat_rad) * np.cos(omega_rad)
    )

    rpot = (solar_constant * (1.00011 + 0.034221 * np.cos(theta) +
                              0.00128 * np.sin(theta) + 0.000719 * np.cos(2 * theta) +
                              0.000077 * np.sin(2 * theta)))

    pot_rad = rpot * np.cos(theta_rad)
    pot_rad = np.maximum(pot_rad, 0)

    return pot_rad