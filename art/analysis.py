# by Pavlo Bazilinskyy <p.bazilinskyy@tue.nl>
"""Analyse data of the eHMI-on-vehicles study exported from MongoDB.

Writes per-participant tables to _output/ (not in git: they hold personal data)
and aggregate figures to figures/ (used in README.md).
"""
import glob
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import art as ar  # noqa: E402

logger = ar.CustomLogger(__name__)  # use custom logger

ROOT = ar.settings.root_dir
MAPPING = os.path.join(ROOT, ar.common.get_configs('mapping_stimuli'))
OUT = ar.settings.output_dir
FIG = os.path.join(ROOT, 'figures')
W = ar.common.get_configs('stimulus_width')  # size of stimuli on screen
H = ar.common.get_configs('stimulus_height')
MIN_GAZE_DISTINCT = ar.common.get_configs('min_gaze_distinct')  # share of distinct points below which gaze is frozen

# questions after each image (slider-0..3), 0-100
QUESTIONS = {
    'cross': 'Would you cross?\n(0 definitely not, 100 definitely)',
    'safe': 'How safe do you feel crossing?\n(0 very unsafe, 100 very safe)',
    'clear': 'How clear is the message?\n(0 not clear, 100 very clear)',
    'quick': 'How quickly do you understand intent?\n(0 very slow, 100 very fast)',
}
# eHMI conditions in display order: (label, intended message)
EHMI = {
    'Base': ('No eHMI', 'none'),
    'Walk': ('Text English: WALK', 'go'),
    'Stop': ('Text English: STOP', 'stop'),
    'LocalGo': ('Text local: go (Chaliye / Lopen)', 'go'),
    'Rukiye': ('Text local: stop (Rukiye)', 'stop'),
    'SymbolGreen': ('Symbol green', 'go'),
    'SymbolRed': ('Symbol red', 'stop'),
    'GreenBar': ('Light bar green', 'go'),
    'RedBar': ('Light bar red', 'stop'),
}
# colours: reference palette (blue, orange, aqua), neutral gray, ink
GO, STOP, THIRD, NONE = '#2a78d6', '#eb6834', '#1baf7a', '#8a8984'
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': GRID, 'axes.labelcolor': INK2, 'xtick.color': INK2,
                     'ytick.color': INK2, 'text.color': INK, 'axes.titlecolor': INK, 'figure.facecolor': 'white',
                     'axes.spines.top': False, 'axes.spines.right': False, 'savefig.dpi': 150})


def load(folder, files):
    """Return dict worker_code -> list of trials, merging all saved chunks of a participant."""
    runs = {}
    for name in files:
        for line in open(os.path.join(folder, name)):
            if not line.strip():
                continue
            data = json.loads(line)['data']
            code = next((t['worker_code'] for t in data if t.get('worker_code')), None)
            runs.setdefault(code, []).extend(data)
    return {code: sorted(trials, key=lambda t: t['trial_index']) for code, trials in runs.items()}


def tidy(runs):
    """Build tables of participants, answers per image, post-questionnaire and gaze samples."""
    mapping = pd.read_csv(MAPPING)
    mapping['image_id'] = mapping['image_name'].str.replace('image_', '').astype(int)
    people, answers, post, gaze = [], [], [], []
    for code, trials in runs.items():
        responses = {}
        for t in trials:
            if t['trial_type'] in ('survey-text', 'survey-multi-choice', 'survey-html-form-slider'):
                responses.update(t.get('response') or {})
        images = [t for t in trials if t['trial_type'] == 'image-keyboard-response']
        attention = {k: v for k, v in responses.items() if k.startswith('attention_q')}
        check = next((t for t in trials if t['trial_type'] == 'browser-check'), {})
        planned = next((len(t['image_ids']) for t in trials if 'image_ids' in t), np.nan)
        points = [(p['x'], p['y']) for t in images for p in t.get('webgazer_data', [])]
        gaze_ok = len(points) > 0 and len(set(points)) / len(points) >= MIN_GAZE_DISTINCT
        people.append({
            'worker_code': code, 'browser': check.get('browser'), 'os': check.get('os'),
            'width': check.get('width'), 'height': check.get('height'),
            'images_planned': planned, 'images_seen': len(images),
            'completed': 'suggested_improvements' in responses,
            'minutes': round(trials[-1]['time_elapsed'] / 60000, 1),
            # the attention checks are asked in random order; count wrong answers by their text
            'attention_answered': len(attention),
            'attention_wrong': sum(v not in ('4', 'For me to observe images', 'Water is wet', 'Images with traffic',
                                             'Car') for v in attention.values()),
            'gaze_samples': len(points), 'gaze_distinct': len(set(points)), 'gaze_valid': gaze_ok,
            **{k: responses.get(k) for k in ('age', 'gender', 'education', 'occupation', 'nationality',
                                             'country_residence', 'walking_frequency', 'vehicle_yield',
                                             'smartphone_while_crossing', 'av_awareness',
                                             'av_passenger_experience', 'av_trust')}})
        post_items = {k: float(v) for k, v in responses.items()
                      if k.startswith(('trust_', 'ehmi_safe_', 'helpful_', 'combo_', 'safety_', 'location_'))}
        if post_items:
            post.append({'worker_code': code, **post_items})
        by_index = {t['trial_index']: t for t in trials}
        for t in trials:
            r = t.get('response') or {}
            if t['trial_type'] != 'survey-html-form-slider' or 'slider-0' not in r:
                continue
            # the image shown right before the answers; older data has no 'stimulus' on the answers
            stimulus = t.get('stimulus') or by_index.get(t['trial_index'] - 1, {}).get('stimulus')
            if not stimulus:
                continue
            answers.append({'worker_code': code, 'image_id': int(stimulus.split('_')[-1].split('.')[0]),
                            **{q: float(r['slider-%d' % i]) for i, q in enumerate(QUESTIONS)}})
        if gaze_ok:
            for t in images:
                rect = list(t['webgazer_targets'].values())[0]
                for p in t['webgazer_data']:
                    gaze.append((code, int(t['stimulus'].split('_')[-1].split('.')[0]),
                                 (p['x'] - rect['left']) * W / rect['width'],
                                 (p['y'] - rect['top']) * H / rect['height']))
    people = pd.DataFrame(people)
    answers = pd.DataFrame(answers).merge(mapping, on='image_id', how='left')
    # local-language "go" texts: Chaliye (Hindi), Lopen (Dutch)
    answers['ehmi_group'] = answers['ehmi'].replace({'Chaliye': 'LocalGo', 'Lopen': 'LocalGo'})
    answers = answers.merge(people[['worker_code', 'country_residence']], on='worker_code')
    answers['residence'] = answers['country_residence'].fillna('Unknown').str.strip().str.title()
    gaze = pd.DataFrame(gaze, columns=['worker_code', 'image_id', 'x', 'y'])
    return people, answers, pd.DataFrame(post), gaze


def mean_ci(per_participant):
    """Mean across participants and half-width of the 95% CI (normal approximation)."""
    v = per_participant.dropna()
    ci = 1.96 * v.std(ddof=1) / np.sqrt(len(v)) if len(v) > 1 else np.nan
    return v.mean(), ci, len(v)


def condition_means(answers, by):
    """Average within each participant first, then across participants (participant is the unit)."""
    per = answers.groupby(['worker_code'] + by)[list(QUESTIONS)].mean().reset_index()
    rows = []
    for key, g in per.groupby(by):
        key = key if isinstance(key, tuple) else (key,)
        for q in QUESTIONS:
            m, ci, n = mean_ci(g[q])
            rows.append({**dict(zip(by, key)), 'question': q, 'mean': m, 'ci': ci, 'n': n})
    return pd.DataFrame(rows)


def dots(ax, y, m, ci, color, label=None):
    ax.errorbar(m, y, xerr=ci, fmt='o', ms=6, color=color, ecolor=color, elinewidth=2, capsize=0,
                mec='white', mew=1, label=label)


def finish(fig, name, n_people, note=''):
    fig.text(0.01, -0.04, 'N = %d participant%s. Dots: mean, lines: 95%% CI across participants.%s'
             % (n_people, '' if n_people == 1 else 's', note), fontsize=8, color=INK2)
    fig.savefig(os.path.join(FIG, name), bbox_inches='tight')
    plt.close(fig)


def fig_ehmi(answers, n):
    s = condition_means(answers, ['ehmi_group'])
    keys = [k for k in EHMI if k in set(s['ehmi_group'])]
    fig, axes = plt.subplots(1, 4, figsize=(14, 4.2), sharey=True)
    for ax, q in zip(axes, QUESTIONS):
        for i, k in enumerate(keys):
            row = s[(s.ehmi_group == k) & (s.question == q)].iloc[0]
            color = {'go': GO, 'stop': STOP, 'none': NONE}[EHMI[k][1]]
            dots(ax, i, row['mean'], row['ci'], color)
        ax.set_title(QUESTIONS[q], fontsize=10, loc='left')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', color=GRID, lw=0.8)
    axes[0].set_yticks(range(len(keys)), [EHMI[k][0] for k in keys])
    axes[0].invert_yaxis()
    handles = [plt.Line2D([], [], marker='o', ls='', color=c, label=lab)
               for c, lab in ((GO, 'Message: go'), (STOP, 'Message: stop'), (NONE, 'No eHMI'))]
    fig.legend(handles=handles, loc='upper right', ncol=3, frameon=False, bbox_to_anchor=(1, 1.06))
    fig.suptitle('Ratings by eHMI', x=0.01, ha='left', fontsize=13, y=1.06)
    finish(fig, 'ratings_by_ehmi.png', n)


def fig_vehicle_distance(answers, n):
    s = condition_means(answers, ['vehicle', 'distance'])
    vehicles = ['Car', 'Bus', 'Truck', 'Tuk_Tuk']
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), sharey=True)
    for ax, q in zip(axes, QUESTIONS):
        for d, color, off in ((10, '#86b6ef', -0.12), (20, '#184f95', 0.12)):
            for i, v in enumerate(vehicles):
                row = s[(s.vehicle == v) & (s.distance == d) & (s.question == q)]
                if len(row):
                    dots(ax, i + off, row['mean'].iloc[0], row['ci'].iloc[0], color, '%d m' % d if i == 0 else None)
        ax.set_title(QUESTIONS[q], fontsize=10, loc='left')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', color=GRID, lw=0.8)
    axes[0].set_yticks(range(4), [v.replace('_', '-') for v in vehicles])
    axes[0].invert_yaxis()
    fig.legend(*axes[0].get_legend_handles_labels(), title='Distance to vehicle', loc='upper right', ncol=2,
               frameon=False, bbox_to_anchor=(1, 1.16))
    fig.suptitle('Ratings by vehicle and distance', x=0.01, ha='left', fontsize=13, y=1.12)
    finish(fig, 'ratings_by_vehicle_distance.png', n)


def fig_country(answers, n):
    s = condition_means(answers, ['country', 'residence'])
    groups = sorted(s['residence'].unique())[:3]  # three colours validate all-pairs; fold the rest if needed
    fig, axes = plt.subplots(1, 4, figsize=(14, 2.4), sharey=True)
    for ax, q in zip(axes, QUESTIONS):
        for j, (grp, color) in enumerate(zip(groups, (GO, STOP, THIRD))):
            off = (j - (len(groups) - 1) / 2) * 0.2
            for i, c in enumerate(['INDIA', 'Netherlands']):
                row = s[(s.country == c) & (s.residence == grp) & (s.question == q)]
                if len(row):
                    dots(ax, i + off, row['mean'].iloc[0], row['ci'].iloc[0], color, grp if i == 0 else None)
        ax.set_title(QUESTIONS[q], fontsize=10, loc='left')
        ax.set_xlim(0, 100)
        ax.set_ylim(1.5, -0.5)
        ax.grid(axis='x', color=GRID, lw=0.8)
    axes[0].set_yticks([0, 1], ['Indian footage', 'Dutch footage'])
    fig.legend(*axes[0].get_legend_handles_labels(), title='Participants living in', loc='upper right', ncol=3,
               frameon=False, bbox_to_anchor=(1, 1.3))
    fig.suptitle('Ratings by country of the footage and of participants', x=0.01, ha='left', fontsize=13, y=1.25)
    finish(fig, 'ratings_by_country.png', n)


def fig_post(post, n):
    labels = {
        'trust_vehicle_yield': 'Trust: vehicle stops or yields at crosswalk',
        'ehmi_safe_no_ehmi': 'Prefer for safe crossing: no eHMI',
        'ehmi_safe_text_en': 'Prefer for safe crossing: text (English)',
        'ehmi_safe_regional_text': 'Prefer for safe crossing: text (regional language)',
        'ehmi_safe_light': 'Prefer for safe crossing: light signal',
        'ehmi_safe_symbol': 'Prefer for safe crossing: symbol',
        'helpful_text': 'Helpful: text', 'helpful_symbols': 'Helpful: symbols', 'helpful_lights': 'Helpful: lights',
        'helpful_combination': 'Helpful: combination of two or more',
        'combo_pref_text_light': 'Prefer combination: text + light',
        'combo_pref_text_symbol': 'Prefer combination: text + symbol',
        'combo_pref_light_symbol': 'Prefer combination: light + symbol',
        'safety_vehicle_car': 'Safe crossing in front of: car', 'safety_vehicle_bus': 'Safe crossing in front of: bus',
        'safety_vehicle_truck': 'Safe crossing in front of: truck',
        'safety_vehicle_tuk-tuk': 'Safe crossing in front of: tuk-tuk',
        'location_windshield': 'Display location: windshield', 'location_hood': 'Display location: hood',
        'location_grille': 'Display location: grille', 'location_multiple': 'Display location: multiple',
    }
    items = [k for k in labels if k in post.columns]
    fig, ax = plt.subplots(figsize=(8, 0.32 * len(items) + 1))
    for i, k in enumerate(items):
        m, ci, _ = mean_ci(post[k])
        dots(ax, i, m, ci, GO)
    ax.set_yticks(range(len(items)), [labels[k] for k in items])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.grid(axis='x', color=GRID, lw=0.8)
    ax.set_xlabel('Rating (0-100)')
    ax.set_title('Post-experiment questionnaire', loc='left', fontsize=13, pad=12)
    finish(fig, 'post_questionnaire.png', n)


def density(points, sigma):
    """Gaze density on an 8 px grid over the stimulus, smoothed with a Gaussian of sigma bins, max 1."""
    inside = points[(points.x >= 0) & (points.x < W) & (points.y >= 0) & (points.y < H)]
    h, _, _ = np.histogram2d(inside.y, inside.x, bins=[H // 8, W // 8], range=[[0, H], [0, W]])
    k = np.exp(-0.5 * (np.arange(-3 * sigma, 3 * sigma + 1) / sigma) ** 2)
    k /= k.sum()
    h = np.apply_along_axis(lambda r: np.convolve(r, k, 'same'), 1, h)
    h = np.apply_along_axis(lambda c: np.convolve(c, k, 'same'), 0, h)
    return h / h.max() if h.max() > 0 else h


def gaze_per_stimulus(gaze):
    """Save gaze over each stimulus as figures/gaze/image_<id>.jpg; return rows for the README table."""
    from PIL import Image
    folder = os.path.join(FIG, 'gaze')
    os.makedirs(folder, exist_ok=True)
    for old in glob.glob(os.path.join(folder, 'image_*.jpg')):
        os.remove(old)
    mapping = pd.read_csv(MAPPING)
    stimuli = os.path.dirname(MAPPING)
    orange = np.array([235, 104, 52], dtype=float)  # categorical slot 2, stands out on the gray photo
    rows = []
    for image_id, g in sorted(gaze.groupby('image_id'), key=lambda kv: kv[0]):
        photo = Image.open(os.path.join(stimuli, 'image_%d.jpg' % image_id)).convert('L').resize((640, 360))
        base = 255 - 0.6 * (255 - np.asarray(photo, dtype=float))  # lighten so the gaze reads on top
        heat = Image.fromarray((density(g, 3) * 255).astype(np.uint8)).resize((640, 360), Image.BILINEAR)
        heat = np.asarray(heat) / 255
        alpha = (0.9 * heat ** 0.6)[..., None]  # lift low densities so sparse gaze stays visible
        out = (1 - alpha) * base[..., None] + alpha * orange
        Image.fromarray(out.astype(np.uint8)).save(os.path.join(folder, 'image_%d.jpg' % image_id), quality=80)
        m = mapping[mapping.image_name == 'image_%d' % image_id].iloc[0]
        ehmi = EHMI[m.ehmi][0] if m.ehmi in EHMI else 'Text local: ' + m.ehmi
        country = 'India' if m.country == 'INDIA' else 'NL'
        label = '%s, %s, %s, %d m' % (country, m.vehicle.replace('_', '-'), ehmi, m.distance)
        rows.append((image_id, label, g.worker_code.nunique()))
    return rows


def update_readme(rows, n_valid):
    """Replace the gaze section of README.md between its markers with a table of per-stimulus heatmaps."""
    path = os.path.join(ROOT, 'README.md')
    start, end = '<!-- gaze-per-stimulus:start -->', '<!-- gaze-per-stimulus:end -->'
    readme = open(path).read()
    if start not in readme:
        return
    cells = ['<td width="33%%"><img src="figures/gaze/image_%d.jpg" alt="Gaze on image %d"><br>'
             '<sub>Image %d: %s (n = %d)</sub></td>' % (i, i, i, label, n) for i, label, n in rows]
    table = '\n'.join('<tr>%s</tr>' % ''.join(cells[i:i + 3]) for i in range(0, len(cells), 3))
    body = ('Gaze (orange, stronger = more) over each stimulus, from the %d participant%s with valid gaze data. '
            '%d of 136 stimuli have gaze data so far; n is the number of participants per stimulus.\n\n'
            '<table>\n%s\n</table>' % (n_valid, '' if n_valid == 1 else 's', len(rows), table))
    if not rows:
        body = 'No valid gaze data yet.'
    before, rest = readme.split(start, 1)
    with open(path, 'w') as f:
        f.write(before + start + '\n' + body + '\n' + end + rest.split(end, 1)[1])


def fig_gaze(gaze, n_valid, n_all):
    fig, ax = plt.subplots(figsize=(8, 4.8))
    if len(gaze):
        h = density(gaze, 4)
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
            'seq', ['#ffffff', '#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b'])
        ax.imshow(h, extent=[0, W, H, 0], cmap=cmap, vmin=0, vmax=1, interpolation='bilinear')
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_xlabel('x (px)')
    ax.set_ylabel('y (px)')
    fig.suptitle('Gaze density over the stimulus, all images pooled (darker = more gaze)', x=0.01, ha='left',
                 fontsize=13)
    fig.text(0.01, -0.02, 'N = %d of %d participants with valid gaze data (frozen gaze excluded).'
             % (n_valid, n_all), fontsize=8, color=INK2)
    fig.savefig(os.path.join(FIG, 'gaze_heatmap.png'), bbox_inches='tight')
    plt.close(fig)


def main(folder, files):
    """Read the exported data, save per-participant tables and draw all figures."""
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    people, answers, post, gaze = tidy(load(folder, files))
    for name, df in (('participants', people), ('answers', answers), ('post_questionnaire', post)):
        df.to_csv(os.path.join(OUT, name + '.csv'), index=False)
    cols = ['worker_code', 'browser', 'images_seen', 'images_planned', 'completed', 'minutes',
            'attention_wrong', 'gaze_valid', 'country_residence']
    logger.info('Participants:\n{}', people[cols].to_string(index=False))
    n = answers['worker_code'].nunique()
    fig_ehmi(answers, n)
    fig_vehicle_distance(answers, n)
    fig_country(answers, n)
    if len(post):
        fig_post(post, len(post))
    n_valid = int(people['gaze_valid'].sum())
    fig_gaze(gaze, n_valid, len(people))
    rows = gaze_per_stimulus(gaze)
    if ar.common.get_configs('update_readme'):
        update_readme(rows, n_valid)
    logger.info('Saved tables to {} and figures to {}.', OUT, FIG)
