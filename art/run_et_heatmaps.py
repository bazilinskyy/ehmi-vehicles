#!/usr/bin/env python3
"""
Standalone script — eye-tracking heatmaps from test_data.json.

For each stimulus, loads all participants' WebGazer gaze points, normalises
them to the stimulus display area, and renders a KDE heatmap overlaid on the
corresponding image from public/img/stimuli/.

Output PNGs are written to  <project_root>/output/figures/et_heatmaps/.

Usage:
    python art/analysis/run_et_heatmaps.py
"""

import json
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image

import art as ar

ar.logs(show_level='info', show_color=True)
logger = ar.CustomLogger(__name__)  # use custom logger

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------


def load_test_data(path, stimuli_dir=None):
    """Parse test_data.json (NDJSON) and return gaze data grouped by stimulus.
    Gaze coordinates are normalised to the stimulus display bounding box so
    that (0, 0) is the top-left corner of the image as shown on screen.
    Args:
        path (str or list): path to a single NDJSON file, or a list of paths.
        stimuli_dir (str, optional): directory containing the stimulus images.
            When given, 'image_path' is populated for each entry.
    Returns:
        dict: {stimulus_name: {
                 'gaze_points':       [[x, y], ...],   # display-relative px
                 'gaze_raw':          [{x, y, t}, ...], # original screen px
                 'bboxes':            [bbox_dict, ...],  # per-trial bbox
                 'participant_count': int,
                 'image_path':        str or None,
               }}
    """
    paths = [path] if isinstance(path, str) else list(path)

    records = []
    for p in paths:
        with open(p) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

    data = defaultdict(lambda: {
        'gaze_points': [],
        'gaze_raw': [],
        'bboxes': [],
        'participant_count': 0,
        'image_path': None,
    })
    for record in records:
        for trial in record.get('data', []):
            if trial.get('trial_type') != 'image-keyboard-response':
                continue
            gaze_raw = trial.get('webgazer_data')
            if not gaze_raw:
                continue
            targets = trial.get('webgazer_targets', {})
            bbox = targets.get('#jspsych-image-keyboard-response-stimulus')
            stim = trial.get('stimulus', '')
            if isinstance(stim, list):
                stim = stim[0]
            stim_name = os.path.splitext(os.path.basename(stim))[0]
            entry = data[stim_name]
            entry['participant_count'] += 1
            entry['gaze_raw'].extend(gaze_raw)
            if bbox:
                entry['bboxes'].append(bbox)
                left = bbox.get('left', 0)
                top = bbox.get('top',  0)
                for pt in gaze_raw:
                    entry['gaze_points'].append([pt['x'] - left, pt['y'] - top])
            else:
                for pt in gaze_raw:
                    entry['gaze_points'].append([pt['x'], pt['y']])
            if stimuli_dir and entry['image_path'] is None:
                img_name = os.path.basename(stim)
                candidate = os.path.join(stimuli_dir, img_name)
                if os.path.exists(candidate):
                    entry['image_path'] = candidate
    return dict(data)


def _display_size(entry):
    """Return the median (width, height) of the display bounding box."""
    bboxes = entry.get('bboxes', [])
    if not bboxes:
        return 800, 600
    return (
        int(np.median([b['width'] for b in bboxes])),
        int(np.median([b['height'] for b in bboxes])),
    )


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_heatmap(stimulus, entry, output_dir, dpi=120):
    """Render and save one heatmap PNG for a stimulus.

    The stimulus image is resized to the participant display dimensions
    (derived from the webgazer_targets bounding box) so that the gaze
    coordinates align directly with the image content.

    Args:
        stimulus (str): stimulus name (used for title and filename).
        entry (dict): data dict as returned by load_test_data.
        output_dir (str): directory to write the output PNG.
        dpi (int): figure DPI.
    """
    gaze_points = entry['gaze_points']
    n_pts = len(gaze_points)
    n_pp = entry['participant_count']

    if n_pts < 5:
        logger.info(f'  [skip] {stimulus}: too few gaze points ({n_pts})')
        return

    xy = np.array(gaze_points, dtype=float)
    x, y = xy[:, 0], xy[:, 1]

    disp_w, disp_h = _display_size(entry)

    fig, ax = plt.subplots(figsize=(disp_w / dpi, disp_h / dpi), dpi=dpi)

    # --- background image ---------------------------------------------------
    image_path = entry.get('image_path')
    if image_path and os.path.exists(image_path):
        img_pil = Image.open(image_path).resize((disp_w, disp_h), Image.LANCZOS)
        ax.imshow(np.asarray(img_pil), extent=[0, disp_w, disp_h, 0], aspect='auto')
    else:
        ax.set_facecolor('#222222')

    # --- KDE heatmap --------------------------------------------------------
    try:
        sns.kdeplot(
            x=x, y=y,
            ax=ax,
            fill=True,
            alpha=0.55,
            cmap='RdYlGn_r',
            bw_adjust=0.5,
            clip=((0, disp_w), (0, disp_h)),
        )
    except Exception as exc:
        logger.error(f'  [warn] KDE failed for {stimulus}: {exc}')

    # --- individual gaze dots -----------------------------------------------
    ax.scatter(x, y, s=6, c='white', alpha=0.20, linewidths=0, zorder=5)

    # --- axes ---------------------------------------------------------------
    ax.set_xlim(0, disp_w)
    ax.set_ylim(disp_h, 0)    # y-axis points downward (screen convention)
    ax.set_axis_off()

    fig.suptitle(
        f'{stimulus}  —  {n_pp} participant{"s" if n_pp != 1 else ""},  '
        f'{n_pts} gaze points',
        fontsize=9, y=0.995,
    )
    plt.subplots_adjust(top=0.96, bottom=0, left=0, right=1)

    # --- save ---------------------------------------------------------------
    out_path = os.path.join(output_dir, f'et_heatmap_{stimulus}.png')
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight')
    plt.close(fig)
    logger.info(f'  [saved] {out_path}')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    os.makedirs(os.path.join(ar.settings.output_dir, 'figures'), exist_ok=True)

    data = load_test_data(ar.common.get_configs('files_heroku'), stimuli_dir=ar.common.get_configs('path_stimuli'))

    logger.info(f'Loaded {len(data)} stimuli:\n')
    logger.info(f'  {"Stimulus":<20} {"Participants":>12} {"Gaze pts":>10} {"Image":>6}')
    logger.info(f'  {"-"*20} {"-"*12} {"-"*10} {"-"*6}')
    for name, entry in sorted(data.items()):
        img_ok = 'ok' if entry['image_path'] else 'miss'
        logger.info(f'  {name:<20} {entry["participant_count"]:>12} '
                    f'{len(entry["gaze_points"]):>10} {img_ok:>6}')

    logger.info('\nGenerating heatmaps ...\n')
    for stimulus, entry in sorted(data.items()):
        plot_heatmap(stimulus, entry, os.path.join(ar.settings.root_dir, 'figures'))

    logger.info('\nDone.')


if __name__ == '__main__':
    main()
