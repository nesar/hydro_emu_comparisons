# hydro_emu_comparisons — project instructions

Comparisons of three emulators (CosmoHydro_emu, Subgrid_emu, MiraTitan-IV via pyccl)
against each other, simulations (Frontier-E family) and observations. One notebook per
question; see `SETUP.md` for the notebook table, data inventory and environment.

## Conventions
- Analysis lives in `notebooks/nb*.ipynb`. Do not add `.py` files; the only helper module is
  `data_observational/load_obs_data.py` (data loading only). Never edit the emulator
  packages (`../cosmohydro_emu`, `../subgrid_emu`) or simulation outputs from here.
- Fixed cosmology / subgrid parameters come from `fixed_parameters.txt` (Frontier-E);
  every notebook parses that file rather than hard-coding values.
- Units: k in h Mpc⁻¹, P(k) in (h⁻¹Mpc)³; stellar masses in M☉ (HAVOCC divides HACC's
  M☉/h by h = 0.6766); GSMF / HMF in (h⁻¹Mpc)⁻³ dex⁻¹; halo masses in M☉/h.
- Notebooks are stored **executed** (figures embedded). Execute headlessly with
  `cd notebooks && ../.venv/bin/python -m nbconvert --to notebook --execute --inplace
  --ExecutePreprocessor.kernel_name=hydro-emu-venv <nb>.ipynb` (the `.venv/bin/jupyter`
  shim is broken). On another machine use whatever Python has the emulators installed and
  a matching kernel name.
- Percent signs inside matplotlib mathtext labels must be escaped (`\%`).

## CosmoHydro GSMF excess (resolved 2026-09-18, see REPORT.md)
`investigations/cosmohydro_gsmf_excess/REPORT.md` + `notebooks/nb7_*` — the 400 h⁻¹Mpc CosmoHydro training
runs were made with a newer CRK-HACC build (67cebcfb-type: `SF_FULL_SFR` on, `CHEM_USE_INIT_STAR_MASS`
off, weaker BH growth) than the 128 h⁻¹Mpc suite / Frontier-E(-Small). Parameters, finder, HAVOCC,
cosmology and box size are excluded. CosmoHydro_emu is therefore a different subgrid model: at the FE point
its GSMF is 1.3-1.7× high above 10¹¹ M☉ and P(k) is 1-5 % high at k = 2-10 h Mpc⁻¹. `BRIEF.md`/`PROMPT.md`
hold the original task. On Polaris, nb7 runs with the cluster `.venv` (see REPORT.md, "Environment note").

## Effective Frontier-E point for CosmoHydro_emu (nb8, 2026-09-19)
Because of the build difference, CosmoHydro_emu's subgrid parameters are re-interpreted rather than the suite re-run:
`notebooks/nb8_effective_frontier_e_parameters.ipynb` fits the five subgrid parameters (FE cosmology fixed) to the
Frontier-E family and stores the result in `data_sims/cosmohydro_400/effective_frontier_e_point.npz` (joint fit,
posterior median 16-84 %, samples). Winds unchanged; AGN sector shifts (M_seed ≈ 1.2×10⁶, ε_kin ≈ 0.25 posterior
median, with a strong M_seed–v_kin–ε_kin degeneracy). Use the posterior median as the interior effective point.
