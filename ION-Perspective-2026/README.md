This data was organized using AI tools.

# Source data for figure plots

This flat folder contains 12 numerical TSV tables. These tables contain the data necessary to plot the curves used in the manuscript figures. This repo also contains python scripts to regenerate the figure panels as PNG files.

## Reproduce the numerical panels using only this folder

Dependencies: Python 3, NumPy, and Matplotlib. Copy this folder anywhere, then run:

```sh
cd ION-Perspective-2026
python3 reproduce_all.py
```

Alternatively run `python3 reproduce_figure_1.py`, `python3 reproduce_figure_2.py`, `python3 reproduce_figure_3.py`, or `python3 reproduce_figure_4.py` individually. `plot_common.py` supplies the local TSV reader and shared display settings.

The scripts produce 19 separate PNGs in `panels/`: six for Figure 1, three for Figure 2, six for Figure 3, and four for Figure 4. They recreate the numerical curves, bars, and uncertainty bounds with similar styling and panel arrangement, but it does not automatically assemble the panels into a combined figure. The image-only Figure 2(c) and Figure 4(a) remain excluded.

## Tables and panel mapping

| Table | Current manuscript panel | Rows | Columns |
|---|---|---:|---|
| `figure_1_almo_eda.tsv` | 1(c): F⁻, I⁻, Li⁺, Cs⁺ | 160 | `ion`, `method`, `component`, `energy_kcal_mol` |
| `figure_1_energy_rmse.tsv` | 1(a): halides; 1(b): alkali metals | 45 | `ion`, `method`, `rmse_kcal_mol` |
| `figure_2_frequency_errors.tsv` | 2(a): halides above, alkali metals below | 115 | `ion`, `mode`, `method`, `delta_frequency_cm_1` |
| `figure_2_halide_experiment_errors.tsv` | 2(b): halide dihydrates | 12 | `ion`, `mode`, `delta_frequency_cm_1` |
| `figure_3_dipole.tsv` | 3(d) | 9599 | `series`, `dipole_D`, `probability` |
| `figure_3_exafs.tsv` | 3(a) | 1427 | `ion`, `edge`, `series`, `k_A_1`, `k2_chi_A_2` |
| `figure_3_ir.tsv` | 3(e) | 17773 | `series`, `segment`, `frequency_cm_1`, `relative_absorption` |
| `figure_3_rdf.tsv` | 3(b) | 959 | `ion`, `r_A`, `g_ion_O` |
| `figure_3_solvation.tsv` | 3(c) | 9 | `ion`, `mb_nrg_kcal_mol`, `mb_nrg_uncertainty_kcal_mol`, `mb_nrg_nqe_kcal_mol`, `mb_nrg_nqe_uncertainty_kcal_mol`, `experiment_lower_kcal_mol`, `experiment_upper_kcal_mol` |
| `figure_4_energy_components.tsv` | 4(d): F⁻; 4(e): I⁻ | 150 | `ion`, `component`, `z_A`, `energy_kcal_mol`, `lower_kcal_mol`, `upper_kcal_mol` |
| `figure_4_pmf.tsv` | 4(b): MB-nrg; 4(c): TTM-nrg | 464 | `ion`, `method`, `z_A`, `energy_kcal_mol`, `lower_kcal_mol`, `upper_kcal_mol` |
| `figure_4_water_density.tsv` | Shared background in 4(b–e) | 100 | `z_A`, `relative_density` |
