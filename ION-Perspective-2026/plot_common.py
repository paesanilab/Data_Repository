"""Small TSV reader and shared display settings; all paths stay in this folder."""
import csv
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / 'tmp'
CACHE.mkdir(exist_ok=True)
(CACHE / 'README.md').write_text('# Plotting cache\n\nTemporary Matplotlib cache for these independent reproducer scripts.\n')
os.environ.setdefault('MPLCONFIGDIR', str(CACHE))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HALIDES = ('F-', 'Cl-', 'Br-', 'I-')
ALKALI = ('Li+', 'Na+', 'K+', 'Rb+', 'Cs+')
ION_COLORS = dict(zip(HALIDES, ('#66c2a5', '#fc8d62', '#8da0cb', '#a6d854')))
ION_COLORS.update(zip(ALKALI, ('#66c2a5', '#fc8d62', '#8da0cb', '#a6d854', '#e78ac3')))
METHODS = ('PBE', 'B3LYP', 'PBE0-D3', 'ωB97X-D', 'MB-nrg')
METHOD_MARKERS = ('o', 's', '^', 'D', 'P')
METHOD_LINES = ('-', '--', '-.', ':', '-')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.linewidth': 1.3,
                     'axes.labelsize': 12, 'xtick.labelsize': 10, 'ytick.labelsize': 10,
                     'xtick.direction': 'in', 'ytick.direction': 'in',
                     'legend.frameon': False, 'figure.facecolor': 'white'})


def read(name):
    with (ROOT / name).open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def select(rows, **keys):
    return [row for row in rows if all(row[key] == value for key, value in keys.items())]


def xy(rows, x, y):
    return np.array([float(row[x]) for row in rows]), np.array([float(row[y]) for row in rows])


def ion_label(ion):
    return ion[:-1] + '$^{' + ion[-1] + '}$'


def ion_ticks(ax, positions, ions):
    ax.set_xticks(positions)
    ax.set_xticklabels([ion_label(ion) for ion in ions])
    for tick, ion in zip(ax.get_xticklabels(), ions):
        tick.set_color(ION_COLORS[ion])
        tick.set_fontweight('bold')


def box(ax):
    ax.tick_params(which='both', top=True, right=True)


def save(fig, name):
    directory = ROOT / 'panels'
    directory.mkdir(exist_ok=True)
    (directory / 'README.md').write_text(
        '# Numerical reproducer panels\n\nThese 19 separate PNGs are generated solely from the parent TSV files. '
        'Run `python3 reproduce_all.py` from output_data to regenerate them. '
        'Figure 2(c) and Figure 4(a) have no numerical sources here and are omitted.\n')
    path = directory / (name + '.png')
    fig.savefig(path, dpi=300, facecolor='white')
    plt.close(fig)
    print(path.name)
