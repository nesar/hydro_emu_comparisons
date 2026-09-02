# Setup and inventory

## Environment

A dedicated venv (Python 3.10, at `./.venv`) holds all four emulator backends —
the numpy pin (`<1.24`, required by SEPIA) constrains everything else:

```bash
/usr/bin/python3.10 -m venv .venv
.venv/bin/pip install "numpy>=1.22,<1.24" "scipy<1.11" "matplotlib<3.9" "pandas<2.0"
.venv/bin/pip install "sepia @ git+https://github.com/lanl/SEPIA.git"
.venv/bin/pip install -e ../cosmohydro_emu -e ../subgrid_emu
.venv/bin/pip install pyccl baccoemu "numpy<1.24"   # MiraTitan-IV + bacco linear
.venv/bin/pip install jupyter nbconvert nbformat ipykernel
```

Exact versions: `requirements_frozen.txt`. Run notebooks with
`.venv/bin/jupyter` (or select the venv kernel).

The venv is registered as a Jupyter kernel named `hydro-emu-venv` (display name
"Python (.venv hydro_emu_comparisons)"); all notebooks' metadata point at it, so
VS Code / JupyterLab select it automatically. On a fresh machine re-register it:

```bash
.venv/bin/python -m ipykernel install --user --name hydro-emu-venv \
    --display-name "Python (.venv hydro_emu_comparisons)"
```

`.vscode/settings.json` also sets `python.defaultInterpreterPath` to `.venv`.
If VS Code still doesn't list the venv, open this folder as the workspace root
(not a parent directory) and run "Python: Select Interpreter" once.

## Notebooks (one per README.txt query)

| # | Notebook | Compares |
|---|----------|----------|
| 1 | `notebooks/nb1_cosmohydro_vs_subgrid.ipynb` | CosmoHydro_emu (cosmology fixed to the shared fiducial) vs Subgrid_emu: GSMF, fGas, CGD, CSFR, Pk-ratio (+2p variants), plus subgrid-parameter sweeps |
| 2 | `notebooks/nb2_pk_vs_miratitan.ipynb` | CosmoHydro `Pk_GO` and `Pk_hydro` vs MiraTitan-IV (pyccl `CosmicemuMTIVPk`), fiducial + (ωₘ, σ₈) grid, z = 0–2 |
| 3 | `notebooks/nb3_linear_vs_nonlinear_vs_data.ipynb` | bacco linear vs MT-IV / CosmoHydro non-linear P(k), against eBOSS DR14 Lyα points (+ drop-in user data) |
| 4 | `notebooks/nb4_frontier_e_comparison.ipynb` | All 3 emulators vs Frontier-E-Small extracts and (when portal is up) survey-scale Frontier-E catalogs |

## Fixed parameters

`fixed_parameters.txt` — Frontier-E cosmology and calibrated subgrid parameters,
with paper sources cited inline. All notebooks parse this file; edit it there, not
in the notebooks.

## Data

All loaders live in `data_observational/load_obs_data.py` (the one permitted `.py`).

- `data_observational/RealData/` — user-provided linear P(k) datasets (2026-08-31):
  `reid_DR7.txt` (SDSS DR7 LRG, Reid+10), `wmap_act.txt` (WMAP+ACT, Hlozek+12),
  `DR14_pm3d_19kbins.txt` (eBOSS DR14 Lyα, Chabanier+19; k in Mpc⁻¹, P in (Mpc/h)³),
  and the mpk_compilation repo. All conventions verified numerically against linear
  theory. `PowerSpectraObservationData.{csv,xlsx}` are NOT used — plot-digitizer
  exports with uncalibrated axes; the calibrated files cover the same surveys.
- `data_observational/kids_legacy/` — KiDS-Legacy deprojected Pm(k, z)
  (Broxterman+25, A&A 703 L3), copied from
  `CosmoHydro/data/Power_spec_targets/nonlinear_pk_targets/kids_legacy/`.
- `data_observational/gsmf/`, `cgd/`, `fgas/` — calibration targets as used by the
  Inference pipeline: Driver+22 GSMF (from the HAvoCC GSMF module data),
  McDonald+17 / Ghirardini+19 / Lehle+23 / Braspenning+23 gas-density profiles
  (HAvoCC CGD module data), Kugel+23 Table 5 gas fractions (transcribed from
  `load_hacc.load_fgas_obs`).
- `data_observational/user_pk/` — drop `[k, P, err]` text files here (k in h/Mpc,
  P in (Mpc/h)³, z = 0); `*_nl.txt` marks nonlinear-scale measurements.
  Notebook 3 picks them up automatically.
- `data_sims/frontier_e/pk_hydro/`, `pk_gravonly/` — survey-scale Frontier-E
  (3150 Mpc/h) total-matter power spectra, steps 624/498/415/310/247/205
  (z ≈ 0, 0.25, 0.5, 1, 1.5, 2), HACC format (k [h/Mpc], P [(Mpc/h)³]);
  moved out of the transferred "Docs & Files/powerspectra_hacc/" tree.
- `data_sims/frontier_e/catalogs/` — destination for survey-scale halo/galaxy
  catalog queries (OpenCosmo portal). Empty as of 2026-08-31: the portal's compute
  endpoint (`hacc-compute-portal-polaris-1-node`) was offline. Re-run the queries
  when it is back; the last section of notebook 4 will then run.
- Frontier-E-Small extracts are read in place from
  `../Data/ProfileData/SCIDAC_RUNS/SMALL_FRONTIERE[_GO]/`.
