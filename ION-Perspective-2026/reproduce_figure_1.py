"""Figure 1: two RMSE panels and four separate ALMO–EDA panels from TSVs."""
import sys
sys.dont_write_bytecode = True
from plot_common import *


def main():
    rows = read('figure_1_energy_rmse.tsv')
    for panel, ions in (('a_halide_energy', HALIDES), ('b_alkali_energy', ALKALI)):
        fig, ax = plt.subplots(figsize=(6, 5))
        for method, marker, style in zip(METHODS, METHOD_MARKERS, METHOD_LINES):
            values = [float(select(rows, ion=ion, method=method)[0]['rmse_kcal_mol']) for ion in ions]
            ax.plot(range(len(ions)), values, color='black', marker=marker,
                    linestyle=style, markersize=8, markerfacecolor='white', label=method)
            ax.scatter(range(len(ions)), values, c=[ION_COLORS[ion] for ion in ions],
                       marker=marker, s=64, edgecolor='#222222', zorder=3)
        ion_ticks(ax, range(len(ions)), ions)
        ax.set_xlim(-0.35, len(ions) - 0.65)
        ax.set_ylim(0, 0.7 if ions == HALIDES else 0.95)
        ax.set_ylabel(r'RMSE $V^{2B}$ (kcal/mol)')
        ax.legend(loc='upper right', ncol=2, fontsize=9)
        box(ax)
        fig.tight_layout()
        save(fig, 'figure_1_' + panel)

    rows = read('figure_1_almo_eda.tsv')
    methods = ('PBE-D3', 'B3LYP-D3', 'PBE0-D3', 'ωB97X-D3', 'MB-nrg')
    # The buffers remain distinct terms even though their legend colors match.
    components = [
        ('pauli_dispersion_buffer', 'Pauli + Disp.', '#f0027f', None),
        ('qc_buffer', 'Q.C.', '#f0027f', '////'),
        ('pauli_dispersion', 'Pauli + Disp.', '#f0027f', None),
        ('qc', 'Q.C.', '#f0027f', '////'),
        ('born_mayer', 'B-M', '#56b4e9', None),
        ('repulsive_vdw', 'Rep. vdW', '#cc79a7', None),
        ('dispersion', 'Disp.', '#fdc086', None), ('d3', 'D3', '#ffff99', None),
        ('polarization', 'Pol.', '#7fc97f', None),
        ('charge_transfer', 'CT', '#beaed4', None),
        ('electrostatics', 'Elec.', '#386cb0', None)]
    for ion, name in (('F-', 'fluoride'), ('I-', 'iodide'), ('Li+', 'lithium'), ('Cs+', 'cesium')):
        fig, ax = plt.subplots(figsize=(3.5, 7))
        bottom = np.zeros(len(methods))
        used = set()
        for key, label, color, hatch in components:
            selected = select(rows, ion=ion, component=key)
            if not selected:
                continue
            values = np.array([float(select(selected, method=method)[0]['energy_kcal_mol']) for method in methods])
            ax.bar(range(5), values, bottom=bottom, width=0.72, color=color, hatch=hatch,
                   edgecolor='#222222', linewidth=0.35, label=label if label not in used else '_nolegend_')
            used.add(label)
            bottom += values if ion in HALIDES else np.where(values < 0, values, 0)
        ax.set_xticks(range(5))
        ax.set_xticklabels(methods, rotation=90)
        ax.set_ylim(-85, 60)
        ax.set_yticks((-75, -50, -25, 0, 25, 50))
        ax.set_ylabel(r'$E_{model}$ (kcal/mol)')
        ax.axhline(0, color='gray', linewidth=0.7)
        ax.set_axisbelow(True)
        ax.grid(axis='y', linewidth=0.5, color='#dddddd')
        ax.set_title(ion_label(ion), bbox={'facecolor': ION_COLORS[ion], 'edgecolor': 'black', 'boxstyle': 'round'})
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.06), ncol=2, fontsize=7)
        box(ax)
        fig.subplots_adjust(left=0.25, right=0.98, bottom=0.17, top=0.76)
        save(fig, 'figure_1_c_' + name + '_almo')


if __name__ == '__main__':
    main()
