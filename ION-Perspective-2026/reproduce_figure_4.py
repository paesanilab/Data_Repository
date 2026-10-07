"""Figure 4: four PMF/energy panels with the exported density background."""
import sys
sys.dont_write_bytecode = True
from plot_common import *
from matplotlib.colors import LinearSegmentedColormap


def axes():
    fig, ax = plt.subplots(figsize=(5, 5))
    z, density = xy(read('figure_4_water_density.tsv'), 'z_A', 'relative_density')
    extent = (z[0] - (z[1] - z[0]) / 2, z[-1] + (z[-1] - z[-2]) / 2, -9.99, 20)
    cmap = LinearSegmentedColormap.from_list('density', [(158/255, 202/255, 225/255, 0), (158/255, 202/255, 225/255, 0.3)])
    ax.imshow(density[np.newaxis, :], origin='lower', aspect='auto', interpolation='bilinear',
              extent=extent, cmap=cmap, vmin=0, vmax=1, zorder=-10)
    ax.set_xlim(-10, 4)
    ax.set_ylim(-9.99, 20)
    ax.set_xticks(np.arange(-10, 5, 2))
    ax.axhline(0, color='black', linestyle='--', linewidth=0.7, zorder=0)
    ax.set_xlabel(r'$z$ (Å)')
    box(ax)
    return fig, ax


def profile(ax, rows, label, color, style='-'):
    x, y = xy(rows, 'z_A', 'energy_kcal_mol')
    lower = np.array([float(row['lower_kcal_mol']) for row in rows])
    upper = np.array([float(row['upper_kcal_mol']) for row in rows])
    ax.fill_between(x, lower, upper, color=color, alpha=0.3, linewidth=0)
    ax.plot(x, y, label=label, color=color, linestyle=style, linewidth=2)


def main():
    rows = read('figure_4_pmf.tsv')
    for model, panel, badge in (('MB-nrg', 'b', '#00d99a'), ('TTM-nrg', 'c', '#b36bff')):
        fig, ax = axes()
        for ion in HALIDES:
            profile(ax, select(rows, ion=ion, method=model), ion_label(ion), ION_COLORS[ion])
        ax.set_ylabel(r'$\Delta A$ (kcal/mol)')
        ax.text(0.06, 0.95, model, transform=ax.transAxes, va='top', fontsize=15,
                bbox={'boxstyle': 'round', 'facecolor': badge, 'edgecolor': 'black'})
        ax.legend(loc='lower left', fontsize=10)
        fig.tight_layout()
        save(fig, 'figure_4_' + panel + '_' + model.lower().replace('-', '_') + '_pmf')
    rows = read('figure_4_energy_components.tsv')
    components = [('free_energy', r'$\Delta A$', '#377eb8', '-'),
                  ('minus_T_entropy', r'$-T\Delta S$', '#e41a1c', '-'),
                  ('internal_energy', r'$\Delta U$', '#4daf4a', '-'),
                  ('ion_water_energy', r'$\Delta U_{iw}$', '#4daf4a', '--'),
                  ('water_water_energy', r'$\Delta U_{ww}$', '#4daf4a', ':')]
    for ion, panel, name in (('F-', 'd', 'fluoride'), ('I-', 'e', 'iodide')):
        fig, ax = axes()
        for key, label, color, style in components:
            profile(ax, select(rows, ion=ion, component=key), label, color, style)
        ax.set_ylabel('Energy (kcal/mol)')
        ax.text(0.06, 0.08, ion_label(ion), transform=ax.transAxes, fontsize=15,
                bbox={'boxstyle': 'round', 'facecolor': ION_COLORS[ion], 'edgecolor': 'black'})
        ax.legend(loc='upper left', fontsize=10)
        fig.tight_layout()
        save(fig, 'figure_4_' + panel + '_' + name + '_energy')


if __name__ == '__main__':
    main()
