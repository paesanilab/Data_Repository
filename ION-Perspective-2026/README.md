This data was organized using AI tools.

# Minimal numerical data for the paper figures

This flat folder contains 12 numerical TSV tables and one provenance TSV. It exports the final values used by the current packaged plotting scripts, using the revised Figure 2 supplied on 2026-10-06. The numerical tables exclude images, historical comparisons, unused methods, and raw intermediate measurements. Small independent Python scripts accompany them for reproduction checks. Re-export from the workspace root with `python3 export_output_data.py`. The exporter uses the existing system Python environment with NumPy, Matplotlib, Pandas, and SciPy; these dependencies are needed to reproduce and verify the existing numerical transformations, not to read the TSV files.

Every TSV is UTF-8, tab-separated, with exactly one header row. Floating-point values use 17 significant digits and round-trip without precision loss. Columns contain units: `A` = ångström, `D` = debye, `cm_1` = cm⁻¹, and `kcal_mol` = kcal/mol. Curve coordinates increase within each series. Data order preserves the selected ion/method/component order; it is deterministic rather than alphabetical. Dimensionless quantities are identified by name. No missing numeric cells or invented measurements are included.

`provenance.tsv` records the local source path and SHA-256 for every input and plotting script used by each table, plus the original source identity where recorded in the package manifest. These paths are provenance; interpreting the exported numerical tables does not require the original files. The exporter compares values with plotting artists in memory, reads every exported TSV back, and verifies that existing sources and figure files have not changed. It never saves a figure.

## Reproduce the numerical panels using only this folder

Dependencies: Python 3, NumPy, and Matplotlib. Copy this folder anywhere, then run:

```sh
cd output_data
python3 reproduce_all.py
```

Alternatively run `python3 reproduce_figure_1.py`, `python3 reproduce_figure_2.py`, `python3 reproduce_figure_3.py`, or `python3 reproduce_figure_4.py` individually. `plot_common.py` supplies the local TSV reader and shared display settings. Every input path is resolved relative to the script, so commands also work from another directory.

The scripts produce 19 separate PNGs in `panels/`: six for Figure 1, three for Figure 2, six for Figure 3, and four for Figure 4. They recreate the numerical curves, bars, and uncertainty bounds with similar styling and panel arrangement, without assembling manuscript composites. Values are read directly from the TSVs; smoothing, corrections, normalization, and PMF shifts are not repeated. Only documented visual offsets and stacking rules are applied. Shared bulk-water curves and the density background come from these tables too. The image-only Figure 2(c) and Figure 4(a) remain excluded.

No original figure scripts, raw measurements, images, or external provenance paths are read. `tmp/` holds a local Matplotlib cache. The generated PNGs are comparison artifacts; the flat TSV tables remain the numerical source of truth. Re-running a reproducer replaces its own PNGs, leaving the tables and original workspace figure outputs untouched.

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

## Selection and transformations

**Figure 1 energy RMSE.** 20 halide and 25 alkali values, using PBE, B3LYP, PBE0-D3, ωB97X-D, and MB-nrg. Alkali values use the source's 20 kcal/mol cutoff; halide values use the supplied common-test-set RMSEs. No sample counts or unused method rows are exported.

**Figure 1 ALMO–EDA.** Five selected methods for each of F⁻, I⁻, Li⁺, and Cs⁺. `method` uses the requested display labels PBE-D3, B3LYP-D3, PBE0-D3, ωB97X-D3, and MB-nrg. The halide source labels are PBE(-D3), B3LYP(-D3), PBE0(-D3), ωB97X-D, and MB-nrg; the alkali source instead spells the fourth method wB97X(-D3). This is documented display normalization, not interchangeability with wB97M-V or another functional.

`component` identifiers distinguish source terms that share a legend color. Halide order is `pauli_dispersion_buffer`, `qc_buffer`, `pauli_dispersion`, `qc`, `born_mayer`, `repulsive_vdw`, `dispersion`, `d3`, `polarization`, `charge_transfer`, `electrostatics`; alkali order omits the two buffer terms. Halide source terms are respectively Pauli + Dispersion Buffer, FF Buffer, Pauli + Dispersion, MB-nrg QC, TTM-nrg Buck, AMOEBA 14-7, Dispersion, D3 Correction, Polarization, Charge Transfer, Electrostatic. Alkali source columns are C_PRDI, QC, TTMREP, vdW_REP, DI, D3_CORR, POL, CT_noCP, C_EL. Halide bars stack by accumulating all preceding signed values. Alkali bars accumulate only preceding negative values; positive terms start at that baseline. Alkali DFT DI components are zeroed exactly as in the existing renderer; D3 corrections are retained. Components zero across all five selected methods for an ion are omitted. Zeros within retained components are explicit; absent components mean zero, not missing data. Plot limits are −85 to 60 kcal/mol; unmodified component values outside that display range are preserved.

**Figure 2 errors.** `delta_frequency_cm_1` is signed prediction minus reference, never an absolute error. The 115 CCSD(T) errors include 40 halide values (hydrogen-bonded/free OH) and 75 alkali values (bend/symmetric/asymmetric stretch). Displayed ωB97X-D refers to direct ωB97XD values in the halide AGR inputs and wb97xd-indexed alkali inputs. Axes have upper limit 100 cm⁻¹ and lower padding as in the current renderer. Panel (b) contains exactly 12 complete MB-nrg minus experiment pairs for Cl⁻, Br⁻, I⁻ and modes IHB_AD, IHB_DD, IH, F_OH; every retained pair is replicate 1. The mode identifiers are preserved from the reference table rather than reinterpreted. Missing pairs, the H–O–H bend, and the historical alkali experimental comparison are excluded. Theory and experiment precursor values are not duplicated because only their difference is displayed.

**Figure 3 EXAFS.** `series` is MB-nrg or Experiment; `edge` is K or L1. Values are the exact ordinates supplied to the renderer, restricted to 2 ≤ k ≤ 8 Å⁻¹. Where required, the source χ was multiplied by k²; already transformed experimental/theory inputs are kept as read, including the source-specific iodide convention. `k2_chi_A_2` names the plotted k²χ ordinate (Å⁻²), not a new harmonization of source conventions.

**Figure 3 RDFs.** The plotted ion–oxygen curves are kept over 1.5–7 Å, with adjacent boundary samples when needed to reproduce clipping. The g = 1 horizontal reference is a plotting convention. No secondary-shell columns are exported.

**Figure 3 dipoles.** Negative source probabilities are clipped to zero, followed by the existing Savitzky–Golay filter (21 points, degree 2), nonnegative clipping, and coordinate sorting. Nine first-shell ion distributions are exported. `Bulk_water` is the actual shared mean after interpolating the nine smoothed bulk profiles onto a 700-point grid from 1.6 to 4.35 D and averaging finite contributors; it is stored once and drawn in both ion-family boxes. No smoothing or further renormalization should be applied to these exported curves. The current display y range is (0.0, 2.2488237537596927) and the x range is 1.6–4.35 D; necessary boundary neighbors are retained.

**Figure 3 solvation.** MB-nrg and MB-nrg-with-NQE values already include charge-dependent surface-potential corrections. The correction uses Faraday's constant 96485.33212/4184 kcal mol⁻¹ V⁻¹, potentials −707.6 mV (classical) and −738.1 mV (NQE), and potential uncertainties 4.2 and 33.9 mV. Reported calculation and potential uncertainties are combined in quadrature. `uncertainty` columns are symmetric errors as used by the renderer, not lower/upper endpoints. Experimental lower/upper columns are the exact displayed range, not a statistical error estimate. Horizontal bars start at −50 kcal/mol and the reversed display spans −50 to −132 kcal/mol.

**Figure 3 IR.** Source intensities are nonnegative-clipped and sorted. The visible-range minimum is subtracted, then ion spectra are normalized by the maximum across the entire corresponding ion family (with a minimum divisor of 1). Bulk water is normalized by its own visible maximum and stored once. No additional normalization is needed. `segment` 1/2/3 corresponds to 60–1450, 1470–2100, and 2900–4000 cm⁻¹; draw each segment separately. The plot multiplies `relative_absorption` by 0.82, places alkali spectra at baseline 0 and halide spectra at baseline 1, and draws the shared bulk spectrum at both baselines. These visual offsets are not folded into the exported scientific amplitudes.

**Figure 4 PMFs.** Positions already subtract the positive-z water-density half-maximum position, 19.254590487634616 Å. Each mean PMF and its lower/upper bounds subtract the same baseline interpolated at shifted z = −10 Å. These bounds are the source-provided shaded envelopes; do not interpret them as a newly calculated confidence interval. Curves span the display interval −10 to 4 Å plus any needed boundary neighbors. Do not apply either shift again.

**Figure 4 energy components.** `free_energy`, `minus_T_entropy`, `internal_energy`, `ion_water_energy`, `water_water_energy` map to ΔA, −TΔS, ΔU, ΔU_ion–water, ΔU_water–water. Positions and mean/bounds are used directly as in the renderer; no additional PMF shift is applied. F⁻ and I⁻ only are exported over −10 to 4 Å, including boundary neighbors. The shared plotting y limits are −9.99 to 20 kcal/mol, but the exported energies and bounds are not clipped to those limits.

**Figure 4 water density.** Counts are transformed to (count − global minimum)/(global maximum − global minimum), with the same interface-position shift as the PMFs. Raw counts are excluded. The complete 100-sample normalized profile is retained because it is the actual raster used for the shared numerical background, and truncating it changes interpolation. Render as a one-row bilinearly interpolated raster over horizontal extent (-69.19758418763462, 30.55854036236538), with opacity varying from 0 to 0.30 in the source light-blue color #9ecae1. The z coordinates identify its sorted sample centers.

## Deliberate exclusions

Figure 2(c) (tunneling/pathway artwork) and Figure 4(a) (interface snapshot) are absent because their available sources are images. No numerical levels or molecular coordinates were inferred from those images. This numerical export therefore supports all other current panels but cannot alone reproduce those two image panels or the exact publication layout. Historical Figure 2 alkali comparison data, unused ions/methods/components, raw simulation distributions, original plotting style assets, and original figure PNG/PDF outputs are excluded. Locally generated reproducer PNGs are separate comparison artifacts.
