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
PARAMS = ["m", "n_1", "n_2", "n_3", "r_t"]

status_line = document.querySelector("#status")
plot_box = document.querySelector("#plot-box")
sf_c_box = document.querySelector("#p-sf_c")      # read-only: r_t / max(r(phi))
rot_slider = document.querySelector("#rot-slider")
rot_box = document.querySelector("#rot-box")

# The last successful calculation, (phi, r_t, r_phi), so that rotating only
# redraws the plot instead of recalculating the shape.
last_result = None
rotation_deg = 0.0


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
        value = field.valueAsNumber  # NaN when empty or not a number
        # data-min / data-max are optional; a field without them has no limit.
        lo = float(field.getAttribute("data-min")) if field.hasAttribute("data-min") else -math.inf
        hi = float(field.getAttribute("data-max")) if field.hasAttribute("data-max") else math.inf
        if math.isnan(value):
            problem = f"{name} must be a number."
        elif value < lo:
            problem = f"{name} must be at least {lo:g}."
        elif value > hi:
            problem = f"{name} must be at most {hi:g}."
        else:
            problem = None
        field.setAttribute("aria-invalid", "true" if problem else "false")
        if problem:
            problems.append(problem)
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

def draw():
    """Draws the last calculated shape, turned by the current rotation.
    Positive angles turn it counter-clockwise."""
    if last_result is None:
        return
    phi, r_t, r_phi = last_result
    turn = math.radians(rotation_deg)
    plot_box.innerHTML = polar_svg([p + turn for p in phi], r_t, r_phi)


def run_calculate():
    global last_result
    values, problems = read_params()
    if problems:
        sf_c_box.value = ""
        set_status(" ".join(problems), error=True)
        return
    m, n_1, n_2, n_3, r_t = values

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
        sf_c_box.value = ""
        set_status(f"Unexpected error: {exc}", error=True)
        return

    last_result = (phi, r_t_list, r_phi)
    sf_c_box.value = f"{float(sf_c):.4g}"
    draw()
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


# Rotation redraws straight away (no delay): it only turns the existing shape.
@when("input", "#rot-slider")
def on_rot_slider(event):
    global rotation_deg
    rotation_deg = rot_slider.valueAsNumber
    rot_box.value = f"{rotation_deg:g}"
    draw()


@when("input", "#rot-box")
def on_rot_box(event):
    global rotation_deg
    value = rot_box.valueAsNumber
    if math.isnan(value):        # mid-edit, e.g. only "-" typed so far
        return
    rotation_deg = max(-180.0, min(180.0, value))
    rot_slider.value = str(rotation_deg)
    draw()


@when("change", "#rot-box")
def on_rot_box_done(event):
    rot_box.value = f"{rotation_deg:g}"   # show the clamped value once editing ends


# --------------------------------------------------------------------------
# Startup: this runs once Python and the packages have finished loading.
# --------------------------------------------------------------------------

rotation_deg = rot_slider.valueAsNumber   # in case the slider moved while Python loaded
rot_box.value = f"{rotation_deg:g}"
run_calculate()