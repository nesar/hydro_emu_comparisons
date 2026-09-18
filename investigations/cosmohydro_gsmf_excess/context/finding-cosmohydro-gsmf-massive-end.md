---
name: cosmohydro-gsmf-massive-end
description: "Open issue found 2026-09-17 — CosmoHydro_emu z=0 GSMF is 30-70% high above 1e11 Msun because the 400 Mpc/h training sims themselves are, not the emulator"
metadata: 
  node_type: memory
  type: project
  originSessionId: 288b244b-a542-4e5f-9cbf-53460e84a140
  modified: 2026-09-17T21:34:12.336Z
---

Found in nb6 (`notebooks/nb6_gsmf_z0_comparison.ipynb`, section F), 2026-09-17:

- CosmoHydro_emu over-predicts the z = 0 GSMF vs GAMA / UniverseMachine / Frontier-E-Small /
  survey-scale Frontier-E / Subgrid_emu by 1.3× at 1e11 Msun and 1.7× at 2.8e11 Msun.
- The GP emulator is faithful (hold-out RMS ≤ 0.06 dex). The raw 400 Mpc/h extracts
  themselves are +0.11 / +0.18 dex above the 128 Mpc/h suite at the same parameters;
  a quadratic fit to the raw 400 data reproduces the excess. Weak cosmology correlation.
- Halo level agrees: HMF_SOD/Tinker08 = 0.82 (400) vs 0.81 (128) vs 0.83 (FE-Small), so
  the difference is galaxy modelling / galaxy finding, not gravity or resolution.
- Discrepancy at 1e11 shrinks with z (0.12 dex at z=0 → 0.03 at z=1) but at 2.8e11 it
  stays ~0.2 dex up to z=1 and only vanishes at z=2.
- nb6 section G: not a mass-axis/h convention (h slip excluded; not a single shift).
  At MATCHED parameters (G3b) the 400-suite forms MORE stars at late times (CSFR 1.28x
  at z=0, 1.04x at z=1 vs the 128 suite; Frontier-E-Small matches the 128 suite) AND
  locks a larger fraction into galaxies (0.60 vs 0.54). Two components: weaker late-time
  quenching (HACC build/AGN params of the Frontier campaign) + galaxy-finder assignment
  (cosmotools aperture/dbscan/pmin; Frontier-E and 128-suite use 50/10/10). fGas agrees.
  Design-averaged CSFR medians are misleading (different M_seed range/cosmology).

**Why:** the user wants this investigated; it affects any calibration that uses the
CosmoHydro GSMF above ~4e10 Msun at z = 0.

**How to apply:** don't treat CosmoHydro_emu GSMF (z = 0, M* > 4e10) as a reference.
Next diagnostic: diff HACC `indat.params` of a 400 Mpc/h run vs Frontier-E
(`data_sims/frontier_e/pk_hydro/indat.params`) — the 128-suite / FE-Small param files are
not in the local Data copies. Analysis stays in nb6; the user asked not to modify the
emulator packages. See [[opencosmo-portal-conventions]] for the survey-scale reference.
