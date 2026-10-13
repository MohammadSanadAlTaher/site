# main.py
"""
Browser GUI logic for Trace Similarity (PyScript port of gui_main.py).
The page layout lives in app.html; the comparison tools live in
analysis_tools.py. This file connects the two: it loads a report CSV,
lets you pick a reference and test traces, plots them, and runs every
tool in analysis_tools.TOOLS for each (reference, test) pair.

The desktop version reads traces from an AEDT report. A browser cannot
reach AEDT, so here the data comes from a CSV exported from that report.
"""

import csv
import html
import io
import math
import traceback

from pyscript import document, when, window
from pyscript.ffi import create_proxy

import analysis_tools

csv_input = document.querySelector("#csv-file")
csv_label = document.querySelector("#csv-label")
sample_btn = document.querySelector("#sample-btn")
data_status = document.querySelector("#data-status")
reference_select = document.querySelector("#reference")
test_list = document.querySelector("#test-list")
plot_btn = document.querySelector("#plot-btn")
compute_btn = document.querySelector("#compute-btn")
status_line = document.querySelector("#status")
plot_box = document.querySelector("#plot-box")
legend = document.querySelector("#legend")
results_empty = document.querySelector("#results-empty")
results_table = document.querySelector("#results-table")
results_head = document.querySelector("#results-head")
results_body = document.querySelector("#results-body")
log_box = document.querySelector("#log")

# The loaded report: shared x-axis plus {trace_name: [y_values]}, in the
# order the CSV lists them.
report_x_label = ""
report_x = []
report_traces = {}

# Results of the last Compute, kept so the table can be re-sorted.
result_tools = []      # column titles after "Trace"
result_rows = []       # [{"trace": name, "cells": [(text, sort_key), ...]}]
result_sort = (None, False)   # (column index, reversed)


# --------------------------------------------------------------------------
# Small UI helpers
# --------------------------------------------------------------------------

def write_log(msg, error=False):
    """Appends a line to the Log tab and mirrors it under the buttons."""
    log_box.textContent = log_box.textContent + ">> " + str(msg) + "\n"
    log_box.scrollTop = log_box.scrollHeight
    set_status(msg, error)


def set_status(msg, error=False):
    status_line.textContent = str(msg)
    if error:
        status_line.classList.add("is-error")
    else:
        status_line.classList.remove("is-error")


def show_tab(name):
    """name is 'plot', 'results' or 'log'."""
    document.querySelector(f"#tab-{name}").click()


def set_busy(busy):
    plot_btn.disabled = busy
    compute_btn.disabled = busy


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


# --------------------------------------------------------------------------
# Report data
# --------------------------------------------------------------------------

def parse_report_csv(text):
    """
    Parses a report CSV: the first column is the x-axis, every other column
    is a trace named by the header row. Returns (x_label, x_values,
    {trace_name: [y_values]}). Rows that are blank or not numeric are skipped.
    """
    text = text.lstrip("\ufeff")
    first_line = text.split("\n", 1)[0]
    delimiter = max([",", ";", "\t"], key=first_line.count)
    rows = [row for row in csv.reader(io.StringIO(text), delimiter=delimiter) if row]
    if len(rows) < 2:
        return "", [], {}

    header = [name.strip() for name in rows[0]]
    names = header[1:]
    x_values = []
    traces = {name: [] for name in names}
    for row in rows[1:]:
        if len(row) < len(header):
            continue
        try:
            numbers = [float(cell) for cell in row[:len(header)]]
        except ValueError:
            continue
        x_values.append(numbers[0])
        for name, value in zip(names, numbers[1:]):
            traces[name].append(value)
    return header[0], x_values, traces


def sample_report():
    """Made-up return-loss curves so the page can be tried without a file."""
    freqs = [2.0 + i * 0.005 for i in range(201)]

    def notch(f0, q, depth):
        values = []
        for f in freqs:
            detune = q * (f / f0 - f0 / f)
            values.append(20 * math.log10(abs(1 - depth / (1 + 1j * detune))))
        return values

    traces = {
        "dB(S(1,1)) - patch_l='38mm'": notch(2.45, 40, 0.95),
        "dB(S(1,1)) - patch_l='37.5mm'": notch(2.48, 40, 0.93),
        "dB(S(1,1)) - patch_l='37mm'": notch(2.52, 36, 0.90),
        "dB(S(1,1)) - patch_l='36mm'": notch(2.60, 30, 0.80),
    }
    return "Freq [GHz]", freqs, traces


def load_report(source, x_label, x_values, traces):
    """Makes a parsed report the current one and refreshes the pickers."""
    global report_x_label, report_x, report_traces, result_rows
    if not x_values or not traces:
        write_log(
            f"No numeric data found in {source}. The file needs a header row, "
            "then rows of numbers with the x-axis in the first column.",
            error=True,
        )
        return

    report_x_label, report_x, report_traces = x_label, x_values, traces
    names = list(traces)

    reference_select.innerHTML = "".join(
        f'<option value="{i}">{html.escape(name)}</option>' for i, name in enumerate(names)
    )
    reference_select.value = "0"
    reference_select.disabled = False
    test_list.innerHTML = "".join(
        f'<label class="test"><input type="checkbox" value="{i}" checked>'
        f"<span>{html.escape(name)}</span></label>"
        for i, name in enumerate(names)
    )
    mark_reference()

    result_rows = []
    results_table.hidden = True
    results_empty.hidden = False
    set_busy(False)

    summary = f"{source}: {plural(len(names), 'trace')}, {plural(len(x_values), 'point')}"
    data_status.textContent = summary
    write_log(f"Loaded {summary}.")
    plot_traces()


def reference_name():
    names = list(report_traces)
    return names[int(reference_select.value)] if names else ""


def mark_reference():
    """The reference cannot also be a test trace, so its checkbox is locked."""
    boxes = test_list.querySelectorAll("input")
    for i in range(boxes.length):
        box = boxes.item(i)
        is_reference = box.value == reference_select.value
        box.disabled = is_reference
        box.parentElement.classList.toggle("is-reference", is_reference)


def selected_tests():
    names = list(report_traces)
    boxes = test_list.querySelectorAll("input")
    chosen = []
    for i in range(boxes.length):
        box = boxes.item(i)
        if box.checked and not box.disabled:
            chosen.append(names[int(box.value)])
    return chosen


# --------------------------------------------------------------------------
# Line plot (plain SVG, styled by the .frame/.grid/.trace rules in app.html)
# --------------------------------------------------------------------------

# matplotlib's default colour cycle, minus its grey.
PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
           "#8c564b", "#e377c2", "#bcbd22", "#17becf"]

LEFT, RIGHT, TOP, BOTTOM = 60, 14, 12, 46


def _ticks(lo, hi, target=6):
    """Round tick values covering lo..hi, about `target` of them."""
    raw = (hi - lo) / target
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 5, 10) if raw <= m * mag * 1.0000001)
    first = math.ceil(lo / step - 1e-9)
    ticks = []
    i = first
    while i * step <= hi + step * 1e-9:
        ticks.append(i * step)
        i += 1
    return ticks


def _bounds(values, pad=0.0):
    finite = [v for v in values if math.isfinite(v)]
    if not finite:
        return 0.0, 1.0
    lo, hi = min(finite), max(finite)
    if lo == hi:
        return lo - 0.5, hi + 0.5
    margin = (hi - lo) * pad
    return lo - margin, hi + margin


def line_chart_svg(x_label, x_values, series, width=640, height=400):
    """series is a list of (values, colour or None); None marks the reference.
    width and height are in pixels, so text stays the same size on any screen."""
    x_lo, x_hi = _bounds(x_values)
    y_lo, y_hi = _bounds([v for values, _ in series for v in values], pad=0.06)
    plot_w, plot_h = width - LEFT - RIGHT, height - TOP - BOTTOM

    def sx(v):
        return LEFT + (v - x_lo) / (x_hi - x_lo) * plot_w

    def sy(v):
        return TOP + (y_hi - v) / (y_hi - y_lo) * plot_h

    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="Line plot of the selected traces">',
        f'<rect class="frame" x="{LEFT}" y="{TOP}" width="{plot_w}" height="{plot_h}"/>',
    ]
    for tick in _ticks(x_lo, x_hi, target=max(3, plot_w // 90)):
        x = sx(tick)
        parts.append(f'<line class="grid" x1="{x:.2f}" y1="{TOP}" x2="{x:.2f}" y2="{TOP + plot_h}"/>')
        parts.append(f'<text class="tick-x" x="{x:.2f}" y="{TOP + plot_h + 14}">{tick:g}</text>')
    for tick in _ticks(y_lo, y_hi, target=max(3, plot_h // 45)):
        y = sy(tick)
        parts.append(f'<line class="grid" x1="{LEFT}" y1="{y:.2f}" x2="{LEFT + plot_w}" y2="{y:.2f}"/>')
        parts.append(f'<text class="tick-y" x="{LEFT - 8}" y="{y:.2f}">{tick:g}</text>')
    parts.append(
        f'<text class="axis-title" x="{LEFT + plot_w / 2}" y="{height - 8}">{html.escape(x_label)}</text>'
    )

    for values, colour in series:
        d, pen_down = [], False
        for x, y in zip(x_values, values):
            if math.isfinite(x) and math.isfinite(y):
                d.append(f"{'L' if pen_down else 'M'}{sx(x):.2f},{sy(y):.2f}")
                pen_down = True
            else:
                pen_down = False   # leave a gap where data is missing
        if colour is None:
            parts.append(f'<path class="trace is-reference" d="{" ".join(d)}"/>')
        else:
            parts.append(f'<path class="trace" style="stroke:{colour}" d="{" ".join(d)}"/>')

    parts.append("</svg>")
    return "".join(parts)


def plot_traces():
    """Plots the reference and the ticked test traces."""
    if not report_traces:
        write_log("Load a report first.", error=True)
        return
    names = list(report_traces)
    reference = reference_name()
    tests = selected_tests()

    series, legend_items = [], []
    for name in tests:
        colour = PALETTE[names.index(name) % len(PALETTE)]
        series.append((report_traces[name], colour))
        legend_items.append(f'<li><i style="background:{colour}"></i>{html.escape(name)}</li>')
    series.append((report_traces[reference], None))   # drawn last, on top
    legend_items.insert(0, f'<li class="is-reference"><i></i>{html.escape(reference)} (reference)</li>')

    # Show the tab first so the chart can be drawn at the box's real width.
    show_tab("plot")
    width = max(320, int(plot_box.clientWidth or 640))
    height = round(min(400, max(240, width * 0.62)))
    plot_box.innerHTML = line_chart_svg(report_x_label, report_x, series, width, height)
    legend.innerHTML = "".join(legend_items)


# --------------------------------------------------------------------------
# Compute: every tool in analysis_tools.TOOLS, for every test trace
# --------------------------------------------------------------------------

def _cell(value):
    """Turns a tool's return value into (display text, sort key). A tool may
    return one number or several; several are shown comma-separated and
    sorted by the first value, then the second, and so on."""
    try:
        numbers = [float(value)]
    except (TypeError, ValueError):
        numbers = [float(v) for v in value]
    text = ", ".join(f"{v:.4f}" for v in numbers)
    key = None if any(math.isnan(v) for v in numbers) else tuple(numbers)
    return text, key


def run_analysis():
    if not report_traces:
        write_log("Load a report first.", error=True)
        return
    if not selected_tests():
        write_log("Tick at least one test trace other than the reference.", error=True)
        return
    # Let the browser paint the "Computing" state before the work starts.
    set_busy(True)
    set_status("Computing...")
    window.setTimeout(_compute_proxy, 30)


def _compute(*_):
    global result_tools, result_rows, result_sort
    try:
        reference = reference_name()
        tests = selected_tests()
        reference_values = report_traces[reference]
        result_tools = list(analysis_tools.TOOLS)
        result_rows = []
        failures = 0

        for test_name in tests:
            cells = []
            for tool_name, tool_fn in analysis_tools.TOOLS.items():
                try:
                    text, key = _cell(tool_fn(report_x, reference_values, report_traces[test_name]))
                    write_log(f"{tool_name} ({reference} vs {test_name}): {text}")
                except Exception as exc:
                    text, key = "error", None
                    failures += 1
                    write_log(f"{tool_name} failed for {test_name}: {exc}")
                cells.append((text, key))
            result_rows.append({"trace": test_name, "cells": cells})

        result_sort = (None, False)
        render_results()
        done = f"Computed {plural(len(result_tools), 'tool')} for {plural(len(tests), 'trace')}."
        if failures:
            write_log(f"{done} {plural(failures, 'result')} failed; see the Log tab.", error=True)
        else:
            write_log(done)
        show_tab("results")
    except Exception as exc:
        write_log(traceback.format_exc())
        write_log(f"Unexpected error: {exc}", error=True)
        show_tab("log")
    finally:
        set_busy(False)


_compute_proxy = create_proxy(_compute)


def render_results():
    """Draws the Results table from result_rows in the current sort order."""
    column, reverse = result_sort
    rows = list(result_rows)
    if column == 0:
        rows.sort(key=lambda row: row["trace"].lower(), reverse=reverse)
    elif column is not None:
        # Numeric sort; failed results stay at the bottom either way.
        good = [row for row in rows if row["cells"][column - 1][1] is not None]
        bad = [row for row in rows if row["cells"][column - 1][1] is None]
        good.sort(key=lambda row: row["cells"][column - 1][1], reverse=reverse)
        rows = good + bad

    headings = []
    for i, title in enumerate(["Trace"] + result_tools):
        state = "none" if i != column else ("descending" if reverse else "ascending")
        headings.append(
            f'<th scope="col" aria-sort="{state}">'
            f'<button type="button" data-col="{i}">{html.escape(title)}</button></th>'
        )
    results_head.innerHTML = "<tr>" + "".join(headings) + "</tr>"

    body = []
    for row in rows:
        cells = "".join(
            f'<td class="is-error">{text}</td>' if key is None else f"<td>{text}</td>"
            for text, key in row["cells"]
        )
        body.append(f'<tr><td>{html.escape(row["trace"])}</td>{cells}</tr>')
    results_body.innerHTML = "".join(body)

    results_empty.hidden = True
    results_table.hidden = False


# --------------------------------------------------------------------------
# Events
# --------------------------------------------------------------------------

@when("change", "#csv-file")
def on_file_chosen(event):
    files = csv_input.files
    if files.length == 0:
        return
    file = files.item(0)
    name = str(file.name)
    reader = window.FileReader.new()

    def on_loaded(_event):
        csv_input.value = ""   # so choosing the same file again reloads it
        try:
            load_report(name, *parse_report_csv(str(reader.result)))
        except Exception as exc:
            write_log(traceback.format_exc())
            write_log(f"Could not read {name}: {exc}", error=True)
            show_tab("log")

    reader.onload = create_proxy(on_loaded)
    reader.readAsText(file)


@when("click", "#sample-btn")
def on_sample_click(event):
    load_report("Sample data", *sample_report())


@when("change", "#reference")
def on_reference_changed(event):
    mark_reference()


@when("click", "#plot-btn")
def on_plot_click(event):
    plot_traces()


@when("click", "#compute-btn")
def on_compute_click(event):
    run_analysis()


@when("click", "#results-head")
def on_results_head_click(event):
    """Click a column heading to sort by it; click again to reverse."""
    global result_sort
    button = event.target.closest("button")
    if not button:
        return
    column = int(button.getAttribute("data-col"))
    previous_column, previous_reverse = result_sort
    result_sort = (column, not previous_reverse if column == previous_column else False)
    render_results()


# --------------------------------------------------------------------------
# Startup: this runs once Python and the packages have finished loading.
# --------------------------------------------------------------------------

csv_input.disabled = False
csv_label.classList.remove("is-disabled")
sample_btn.disabled = False
write_log(f"Python is ready. Tools: {', '.join(analysis_tools.TOOLS) or 'none registered'}.")
set_status("Choose a report CSV, or use the sample data.")