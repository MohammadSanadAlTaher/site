# calculations.py
"""
Backend for the browser version of the Superformula Patch Creator.

PLACEHOLDER -- replace the body of compute_patch_shape() with the real
calculation. main.py only relies on the signature and the return value
described below, which match the desktop extension.

Anything that talks to AEDT (get_all_designs, create_shape) cannot run
here: this code executes inside the visitor's browser, which has no AEDT
session to connect to.
"""

import numpy as np

N_POINTS = 361


def compute_patch_shape(m, n_1, n_2, n_3, r_t):
    """
    Returns (phi_values, r_t_values, r_phi, sf_c):

        phi_values  angles in radians, one per point
        r_t_values  r_t at each angle (same length as phi_values)
        r_phi       outline radius at each angle (same length)
        sf_c        whatever extra result you want to carry along;
                    main.py receives it but does not display it

    Lists or numpy arrays are both fine.
    """
    # ---- placeholder: plain superformula with a = b = 1, scaled so the
    # ---- outline just touches the circle of radius r_t.
    phi_values = np.linspace(0.0, 2.0 * np.pi, N_POINTS)
    a = b = 1.0
    base = (
        np.abs(np.cos(m * phi_values / 4.0) / a) ** n_2
        + np.abs(np.sin(m * phi_values / 4.0) / b) ** n_3
    )
    shape = base ** (-1.0 / n_1)
    sf_c = r_t / shape.max()
    r_phi = sf_c * shape
    r_t_values = np.full_like(phi_values, r_t)
    return phi_values, r_t_values, r_phi, sf_c