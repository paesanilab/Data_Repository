"""Figure 2: separate halide/alkali CCSD(T) errors and halide experiment errors."""
import sys
sys.dont_write_bytecode = True
from plot_common import *


def comparison(rows, ions, modes, labels, filename, methods=METHODS):
    fig, ax = plt.subplots(figsize=(12, 5))
    group_width = len(ions) + 0.25
    all_x, all_ions = [], []
    for group, (mode, label) in enumerate(zip(modes, labels)):
        positions = np.arange(len(ions)) + group * group_width
        all_x.extend(positions)
        all_ions.extend(ions)
        for method in methods:
            chosen = [select(rows, ion=ion, mode=mode, **({'method': method} if 'method' in rows[0] else {}))[0]
                      for ion in ions]
            y = [float(row['delta_frequency_cm_1']) for row in chosen]
            index = METHODS.index(method)
            ax.plot(positions, y, color='black', marker=METHOD_MARKERS[index],
                    linestyle=METHOD_LINES[index], markersize=9, markerfacecolor='white',
                    label=method if group == 0 else '_nolegend_')
            ax.scatter(positions, y, c=[ION_COLORS[ion] for ion in ions],
                       marker=METHOD_MARKERS[index], s=81, edgecolor='#222222', zorder=3)
        ax.text(float(positions.mean()), 0.25, label, transform=ax.get_xaxis_transform(),
                ha='center', va='center', fontsize=13,
                bbox={'facecolor': ('#4d9221', '#c51b7d', '#2166ac', '#b2182b')[group],
                      'edgecolor': 'none', 'alpha': 0.85, 'boxstyle': 'round,pad=0.4'}, color='white')
    ion_ticks(ax, all_x, all_ions)
    minimum = min(float(row['delta_frequency_cm_1']) for row in rows if row['ion'] in ions)
    ax.set_ylim(minimum - 0.05 * abs(minimum), 100 if len(methods) > 1 else 35)
    ax.set_xlim(-0.6, all_x[-1] + 0.6)
    ax.set_ylabel(r'$\Delta\omega$ (cm$^{-1}$)')
    ax.axhline(0, color='gray', linewidth=0.7)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=len(methods), fontsize=12)
    box(ax)
    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.12, top=0.87)
    save(fig, filename)


def main():
    rows = read('figure_2_frequency_errors.tsv')
    comparison(rows, HALIDES, ('Hydrogen-bonded O-H stretch', 'Free O-H stretch'),
               ('H-bonded OH Stretch', 'Free OH Stretch'), 'figure_2_a_halide_frequency')
    comparison(rows, ALKALI, ('Bend', 'Symmetric stretch', 'Asymmetric stretch'),
               ('Bend', 'Sym. Stretch', 'Asym. Stretch'), 'figure_2_a_alkali_frequency')
    comparison(read('figure_2_halide_experiment_errors.tsv'), ('Cl-', 'Br-', 'I-'),
               ('IHB_AD', 'IHB_DD', 'IH', 'F_OH'),
               (r'IHB$_{AD}$', r'IHB$_{DD}$', 'IH', r'F$_{OH}$'),
               'figure_2_b_halide_delta', methods=('MB-nrg',))


if __name__ == '__main__':
    main()
