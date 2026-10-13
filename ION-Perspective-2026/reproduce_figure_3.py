"""Figure 3: six separate numerical panels from processed TSV values."""
import sys
sys.dont_write_bytecode = True
from plot_common import *
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

PLOT_BOX = dict(left=0.11, right=0.99, bottom=0.23, top=0.80)


def exafs():
    rows = read('figure_3_exafs.tsv')
    specs = [('Cl-', 'K'), ('Br-', 'K'), ('I-', 'L1'), ('Na+', 'K'), ('K+', 'K'), ('Cs+', 'L1')]
    fig, axes = plt.subplots(1, 6, figsize=(10.8, 3.75))
    for ax, (ion, edge), limit in zip(axes, specs, (1, 0.6, 0.49, 1, 0.6, 0.6)):
        x, y = xy(select(rows, ion=ion, edge=edge, series='MB-nrg'), 'k_A_1', 'k2_chi_A_2')
        ax.plot(x, y, color=ION_COLORS[ion], linewidth=1.8)
        x, y = xy(select(rows, ion=ion, edge=edge, series='Experiment'), 'k_A_1', 'k2_chi_A_2')
        ax.scatter(x, y, facecolor='white', edgecolor='black', s=15, linewidth=0.6)
        ax.set_xlim(2, 8)
        ax.set_ylim(-limit, limit)
        ax.set_title(ion_label(ion) + ': ' + edge + '-edge', fontsize=9)
        ax.set_xlabel(r'$k$ (Å$^{-1}$)', fontsize=10)
        ax.tick_params(labelsize=8)
        box(ax)
    axes[0].set_ylabel(r'$k^2\chi(k)$')
    fig.legend(handles=[Line2D([], [], color='black', label='MB-nrg'),
                        Line2D([], [], color='black', marker='o', markerfacecolor='white',
                               linestyle='none', label='Experiment')],
               loc='lower center', ncol=2, fontsize=9)
    fig.subplots_adjust(left=0.07, right=0.995, bottom=0.22, top=0.82, wspace=0.5)
    save(fig, 'figure_3_a_exafs')


def rdf():
    rows = read('figure_3_rdf.tsv')
    for ions, name, label in ((HALIDES, 'halide', r'$g_{X^-O}$'), (ALKALI, 'alkali', r'$g_{M^+O}$')):
        fig, ax = plt.subplots(figsize=(4.5, 1.9))
        for ion in ions:
            x, y = xy(select(rows, ion=ion), 'r_A', 'g_ion_O')
            ax.plot(x, y, color=ION_COLORS[ion], label=ion_label(ion), linewidth=1.4)
        ax.set_xlim(1.5, 7)
        ax.set_ylim(0, 10)
        ax.axhline(1, color='gray', linestyle=':', linewidth=0.6)
        ax.set_xlabel(r'$r_{ion-O}$ (Å)')
        ax.set_ylabel(label)
        ax.legend(loc='upper right', ncol=2, fontsize=7)
        box(ax)
        fig.subplots_adjust(left=0.14, right=0.99, bottom=0.29, top=0.97)
        save(fig, 'figure_3_b_' + name + '_rdf')


def solvation():
    rows = read('figure_3_solvation.tsv')
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    for index, row in enumerate(rows):
        color = ION_COLORS[row['ion']]
        low, high = float(row['experiment_lower_kcal_mol']), float(row['experiment_upper_kcal_mol'])
        ax.fill_betweenx([index - 0.38, index + 0.38], low, high, color='#fee08b', edgecolor='#b8860b', alpha=0.65)
        for offset, key, alpha in ((-0.17, 'mb_nrg', 1), (0.17, 'mb_nrg_nqe', 0.55)):
            value = float(row[key + '_kcal_mol'])
            error = float(row[key + '_uncertainty_kcal_mol'])
            ax.barh(index + offset, value + 50, left=-50, height=0.34,
                    color=color, edgecolor='black', linewidth=0.45, alpha=alpha)
            ax.errorbar(value, index + offset, xerr=error, fmt='none', color='black', capsize=3, linewidth=0.8)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([ion_label(row['ion']) for row in rows])
    ax.set_xlim(-50, -132)
    ax.set_ylim(len(rows) - 0.4, -0.6)
    ax.set_xlabel(r'$\Delta G^{real}_{hyd}$ (kcal/mol)')
    ax.legend(handles=[Patch(facecolor='#fee08b', label='Experiment'),
                       Patch(facecolor='gray', label='MB-nrg'),
                       Patch(facecolor='gray', alpha=0.55, label='MB-nrg with NQE')],
              loc='lower right', fontsize=7)
    box(ax)
    fig.subplots_adjust(left=0.2, right=0.99, bottom=0.22, top=0.98)
    save(fig, 'figure_3_c_solvation')


def dipole():
    rows = read('figure_3_dipole.tsv')
    fig, axes = plt.subplots(2, 1, figsize=(4.5, 3.75), sharex=True, sharey=True)
    bulk_x, bulk_y = xy(select(rows, series='Bulk_water'), 'dipole_D', 'probability')
    for ax, ions in zip(axes, (HALIDES, ALKALI)):
        ax.fill_between(bulk_x, 0, bulk_y, color='#858585', alpha=0.30, linewidth=0, label='Bulk water')
        for ion in ions:
            x, y = xy(select(rows, series=ion), 'dipole_D', 'probability')
            ax.plot(x, y, color=ION_COLORS[ion], label=ion_label(ion), linewidth=1.6)
        ax.set_xlim(1.6, 4.35)
        ax.set_ylim(0, 2.2488237537596927)
        ax.tick_params(axis='y', labelleft=False)
        ax.legend(loc='upper right', ncol=2, fontsize=6.5)
        box(ax)
    axes[1].set_xlabel(r'$\mu$ (D)')
    fig.supylabel('Normalized Probability', x=0.045)
    fig.subplots_adjust(**PLOT_BOX, hspace=0.08)
    save(fig, 'figure_3_d_dipole')


def ir():
    rows = read('figure_3_ir.tsv')
    fig = plt.figure(figsize=(4.5, 3.75))
    grid = fig.add_gridspec(1, 3, width_ratios=(1.39, 0.63, 1.10), wspace=0.055, **PLOT_BOX)
    axes = [fig.add_subplot(grid[0, i]) for i in range(3)]
    for segment, ax, bounds, ticks in zip(('1', '2', '3'), axes,
                                         ((60, 1450), (1470, 2100), (2900, 4000)),
                                         ((500, 1000), (1600, 2000), (3100, 3600))):
        for ions, baseline in ((ALKALI, 0), (HALIDES, 1)):
            x, y = xy(select(rows, series='Bulk_water', segment=segment), 'frequency_cm_1', 'relative_absorption')
            ax.fill_between(x, baseline, baseline + 0.82 * y, color='#858585', alpha=0.27, linewidth=0)
            for ion in ions:
                x, y = xy(select(rows, series=ion, segment=segment), 'frequency_cm_1', 'relative_absorption')
                ax.plot(x, baseline + 0.82 * y, color=ION_COLORS[ion], linewidth=1.25)
        ax.set_xlim(*bounds)
        ax.set_ylim(0, 1.88)
        ax.set_xticks(ticks)
        ax.tick_params(axis='y', left=False, labelleft=False)
        box(ax)
    axes[0].set_ylabel('Infrared Absorption (Arb. unit)')
    axes[1].set_xlabel(r'Frequency (cm$^{-1}$)')
    for left, right in zip(axes[:-1], axes[1:]):
        left.spines['right'].set_visible(False)
        right.spines['left'].set_visible(False)
        for ax, x in ((left, 1), (right, 0)):
            for y in (0, 1):
                ax.plot((x - 0.018, x + 0.018), (y - 0.025, y + 0.025),
                        transform=ax.transAxes, color='black', clip_on=False, linewidth=0.7)
    fig.legend(handles=[Line2D([], [], color=ION_COLORS[ion], label=ion_label(ion)) for ion in HALIDES + ALKALI],
               loc='upper center', bbox_to_anchor=(0.55, 0.99), ncol=5, fontsize=6.5)
    save(fig, 'figure_3_e_ir')


def main():
    exafs()
    rdf()
    solvation()
    dipole()
    ir()


if __name__ == '__main__':
    main()
