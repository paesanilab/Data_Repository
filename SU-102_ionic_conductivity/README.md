# SU-102 Li+/PC Simulations

This folder contains the data for the paper *Molecular Origins of Lithium-Ion Transport in the Anionic Metal–Organic Framework SU-102*.

Paper link: [Will be updated later](#)

LAMMPS inputs and equilibrated structures for two Li+/propylene carbonate (PC) workflows in SU-102:

- color-charge nonequilibrium molecular dynamics (CCD-NEMD) for ionic conductivity;
- finite-difference thermodynamic integration (FDTI) for Li+ solvation free energy.

The inputs are templates. Adjust the executable, scheduler configuration, run length, and sampling settings for the target system.

## Contents

```text
initial_structure/                         120 equilibrated LAMMPS data files
NEMD_simulation/
├── start.lmps                             CCD-NEMD input
└── parameter/                             framework, PC, and Li+ parameters
solvation_free_energy_calculation/
├── initial_structure.data                 sample structure with one type-17 Li+
├── vdw_step/blnk_files/                   vdW-coupling window template
└── charge_step/blnk_files/                charge-coupling window template
```

`initial_001.data`–`initial_100.data` were used for NEMD, and `initial_001.data`–`initial_060.data` were used for FDTI.

## Requirements

- LAMMPS with the styles used by the supplied force fields.
- For FDTI, a LAMMPS build with the FEP package (`adapt/fep` and `compute fep`).

## CCD-NEMD

`NEMD_simulation/start.lmps` applies a color field along Cartesian `z` (the crystallographic `c` direction). Li+ has color charge `+1`, the framework carries the balancing color charge, and PC does not couple directly to the field. Only the transverse `x` and `y` kinetic degrees of freedom are thermostatted.

To prepare a run directory:

1. Copy `start.lmps` and all files from `NEMD_simulation/parameter/` into it.
2. Copy the chosen equilibrated structure into it as `initial_structure.data`.
3. Set `Efield` and `seed` near the start of `start.lmps`, then run LAMMPS from that directory.

The main outputs are `trajectory.lammpstrj`, `thermo.dat`, `final_structure.restart`, and `final_structure.data`.

## Solvation Free Energy

FDTI uses two stages for one selected Li+:

1. `vdw_step`: couple its soft-core Lennard-Jones interaction while its charge is zero.
2. `charge_step`: restore its charge while its Lennard-Jones interaction remains fully coupled.

The selected ion must be atom type 17 so it can be modified independently. The supplied `solvation_free_energy_calculation/initial_structure.data` is a ready-to-use example in which lithium atom 3189 is type 17.

To prepare another structure:

1. Change `16 atom types` to `17 atom types`.
2. Change exactly one Li+ from type 8 to type 17; leave the other 71 Li+ ions as type 8.
3. Add type 17 to `Masses` and `PairIJ Coeffs`, following the supplied example.

For each stage and lambda value:

1. Copy the corresponding `blnk_files/` template to a run directory.
2. Add the prepared structure as `initial_structure.data`.
3. Replace `_REPLACE_LAMBDA_` in `start.lmp` with the desired value.
4. Create a sibling `data/` directory for `fdti<lambda>.dat`, then run LAMMPS from the window directory.

The project used lambda values from 0.0 to 1.0 in increments of 0.1 for vdW coupling and 0.2 for charge coupling. Integrate the two sets of `fdti<lambda>.dat` results separately and sum their contributions.

Each window also writes energy, thermodynamic, trajectory, restart, and final-structure files.

## Atom Labels

Force-field labels do not exactly match the oxygen-site notation used in the associated text.

| System | Force-field label | Text notation |
| --- | --- | --- |
| SU-102 | `O_2` | $O_2$ |
| SU-102 | `O_3`, `O_3H` | $O_1$ |
| PC | `O_2` | $O_1^{\mathrm{PC}}$ |
| PC | `OS` | $O_2^{\mathrm{PC}}$ |

`O_3H` is the protonated framework oxygen.
