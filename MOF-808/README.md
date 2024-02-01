This folder contains input files for the molecular model of MOF-808 in the format of MBX interfaced with [LAMMPS](https://github.com/lammps/lammps)
File description:

empty_mof.system: the 1x1x1 MOF-808 framework.

5RH.system: the 1x1x1 framework with H2O loaded according to experimental isotherm at 5% RH.

5RH_data.system: LAMMPS data.system file of MOF-808 loaded according to experimental isotherm at 5% RH.

lmp_npt_mbpol: LAMMPS input file for running isothermal-isobaric ensemble MD with MB-pol.

lmp_nvt_mbpol: LAMMPS input file for running canonical ensemble MD with MB-pol.

lmp_nve_mbpol: LAMMPS input file for running micocanonical ensemble MD simulations with MB-pol.

lmp_umbrella_sample: LAMMPS input file for running umbrella sampling MD simulations with MB-pol.

plumed.dat: PLUMED input file for running umbrella sampling MD simulations.

CONFIG.01: the DL_POLY_2 input file for the initial configuration of MOF-808 at 5% RH.

FINAL_CONFIG.01: the DL_POLY_2 output file for the last configuration of the MOF-808 loaded at 5% RH after randomization and full 1 ns NPT run.


Remark:
For this study, most of the simulations in this work were executed using an in-house version of DL_POLY_2. However, we reccomend users instead utilize [LAMMPS](https://github.com/lammps/lammps) and have included LAMMPS input files that have been tested to perform identically to simulations done in DL_POLY_2. Umbrella sampling simulations were executed using LAMMPS integrated with [PLUMED v2.8](https://github.com/plumed/plumed2).
