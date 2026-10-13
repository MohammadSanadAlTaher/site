# main.py
"""
Browser GUI logic for the Superformula Patch Creator (PyScript port of
gui_main.py). The page layout lives in app.html; the math lives in
calculations.py. This file only connects the two: it reads the inputs,
calls sf_calc_code.compute_patch_shape(), then draws the plot.
"""

import math
import traceback

from pyscript import document, when, window
from pyscript.ffi import create_proxy

import sf_calc_code

# One name per input in app.html (the input ids are "p-" + name), in the
# order they are unpacked in run_calculate().
PARAMS = ["m", "n_1", "n_2", "n_3", "r_t", "p_th"]

status_line = document.querySelector("#status")
plot_box = document.querySelector("#plot-box")


# --------------------------------------------------------------------------
# Small UI helpers
# --------------------------------------------------------------------------

def set_status(msg, error=False):
    """Shows a message under the inputs; error=True turns it red."""
    status_line.textContent = str(msg)
    if error:
        status_line.classList.add("is-error")
    else:
        status_line.classList.remove("is-error")


def read_params():
    """Returns (values, problems). values follows the order of PARAMS;
    problems is a list of messages, empty when every input is valid."""
    values, problems = [], []
    for name in PARAMS:
        field = document.querySelector(f"#p-{name}")
        lo = float(field.getAttribute("data-min"))
        hi = float(field.getAttribute("data-max"))
        value = field.valueAsNumber  # NaN when empty or not a number
        ok = not math.isnan(value) and lo <= value <= hi
        field.setAttribute("aria-invalid", "false" if ok else "true")
        if not ok:
            problems.append(f"{name} must be a number between {lo:g} and {hi:g}.")
        values.append(value)
    return values, problems


# --------------------------------------------------------------------------
# Polar plot (plain SVG, styled by the .rim/.ring/.curve-* rules in app.html)
# --------------------------------------------------------------------------

SIZE = 240          # SVG viewBox is SIZE x SIZE
CENTRE = SIZE / 2
RADIUS = 90         # pixel radius of the outer rim


def _ring_step(r_max):
    """A round spacing for the grid rings that gives at most six of them."""
    mag = 10 ** math.floor(math.log10(r_max))
    for mult in (0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5):
        if r_max / (mult * mag) <= 6:
            return mult * mag
    return 10 * mag


def _path(phi, r, r_max, close=False):
    """SVG path data for one curve; skips points that are not finite."""
    points = []
    for angle, radius in zip(phi, r):
        if not (math.isfinite(angle) and math.isfinite(radius)):
            continue
        k = RADIUS * radius / r_max
        x = CENTRE + k * math.cos(angle)
        y = CENTRE - k * math.sin(angle)
        points.append(f"{x:.2f},{y:.2f}")
    if not points:
        return ""
    return "M" + " L".join(points) + (" Z" if close else "")


def polar_svg(phi, r_t, r_phi):
    """Builds the polar chart as an SVG string: 0 deg at the right, angles
    counter-clockwise, same convention as matplotlib's polar axes."""
    finite = [abs(v) for v in list(r_t) + list(r_phi) if math.isfinite(v)]
    r_max = 1.1 * max(finite) if finite and max(finite) > 0 else 1.0

    parts = [
        f'<svg viewBox="0 0 {SIZE} {SIZE}" role="img" '
        'aria-label="Polar plot of the outline r_phi and the radius r_t against phi">',
        f'<circle class="rim" cx="{CENTRE}" cy="{CENTRE}" r="{RADIUS}"/>',
    ]

    # Spokes and angle labels every 45 degrees.
    for deg in range(0, 360, 45):
        a = math.radians(deg)
        x, y = CENTRE + RADIUS * math.cos(a), CENTRE - RADIUS * math.sin(a)
        lx, ly = CENTRE + (RADIUS + 16) * math.cos(a), CENTRE - (RADIUS + 16) * math.sin(a)
        parts.append(f'<line class="spoke" x1="{CENTRE}" y1="{CENTRE}" x2="{x:.2f}" y2="{y:.2f}"/>')
        parts.append(f'<text class="angle-label" x="{lx:.2f}" y="{ly:.2f}">{deg}°</text>')

    # Grid rings. Each label sits just inside its ring, along 22.5 degrees,
    # so a curve that lies exactly on a ring does not run through the text.
    step = _ring_step(r_max)
    label_angle = math.radians(22.5)
    i = 1
    while step * i < r_max * 0.98:
        k = RADIUS * step * i / r_max
        parts.append(f'<circle class="ring" cx="{CENTRE}" cy="{CENTRE}" r="{k:.2f}"/>')
        if k > 20:
            lx = CENTRE + (k - 9) * math.cos(label_angle)
            ly = CENTRE - (k - 9) * math.sin(label_angle)
            parts.append(f'<text class="ring-label" x="{lx:.2f}" y="{ly:.2f}">{step * i:g}</text>')
        i += 1

    parts.append(f'<path class="curve-ref" d="{_path(phi, r_t, r_max)}"/>')
    parts.append(f'<path class="curve-shape" pathLength="1" d="{_path(phi, r_phi, r_max, close=True)}"/>')
    parts.append("</svg>")
    return "".join(parts)


# --------------------------------------------------------------------------
# Calculate and draw
# --------------------------------------------------------------------------

def run_calculate():
    values, problems = read_params()
    if problems:
        set_status(" ".join(problems), error=True)
        return
    m, n_1, n_2, n_3, r_t, p_th = values  # p_th is not used by the plot

    try:
        phi_values, r_t_values, r_phi_values, sf_c = sf_calc_code.compute_patch_shape(
            m, n_1, n_2, n_3, r_t
        )
        # Plain floats from here on, so lists and numpy arrays both work.
        phi = [float(v) for v in phi_values]
        r_t_list = [float(v) for v in r_t_values]
        r_phi = [float(v) for v in r_phi_values]
    except Exception as exc:
        traceback.print_exc()   # the full traceback goes to the browser console (F12)
        set_status(f"Unexpected error: {exc}", error=True)
        return

    plot_box.innerHTML = polar_svg(phi, r_t_list, r_phi)
    set_status(f"Plotted {len(phi)} points.")


DELAY_MS = 300
pending_timer = None

def _refresh(*_):
    global pending_timer
    pending_timer = None
    run_calculate()

_refresh_proxy = create_proxy(_refresh)

@when("input", ".param input")
def on_param_input(event):
    global pending_timer
    if pending_timer is not None:
        window.clearTimeout(pending_timer)   # inputs changed again: drop the pending redraw
    pending_timer = window.setTimeout(_refresh_proxy, DELAY_MS)


# --------------------------------------------------------------------------
# Startup: this runs once Python and the packages have finished loading.
# --------------------------------------------------------------------------

run_calculate()