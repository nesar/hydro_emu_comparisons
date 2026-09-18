# Brief: why do the 400 h⁻¹Mpc CosmoHydro training runs have too many massive galaxies?

Self-contained handoff for an investigation on the cluster that holds the raw HACC /
cosmotools / HAVOCC outputs. Everything below was established locally in
`notebooks/nb6_gsmf_z0_comparison.ipynb` (executed, with figures; sections F and G and the
final summary cell are the relevant parts). Written 2026-09-17.

## 1. The finding

`cosmohydro_emu` (trained on the 400 h⁻¹Mpc "5SG+2COSMO" suite) predicts a z = 0 galaxy
stellar mass function (GSMF) that is **1.3× too high at M* = 10¹¹ M☉ and 1.7× too high at
2.8×10¹¹ M☉** relative to every other reference at the same parameters:

| reference | agreement with each other | CosmoHydro_emu relative to it |
|---|---|---|
| Subgrid_emu (64 × 128 h⁻¹Mpc suite, fixed cosmology) | ±6 % | +30-70 % above 10¹¹ M☉ |
| Frontier-E-Small (256 h⁻¹Mpc, same parameters) | 1-3 % above survey-scale | same excess |
| Frontier-E survey-scale (3150 h⁻¹Mpc, OpenCosmo galaxy catalog) | reference | same excess |
| GAMA DR4 (Driver+22) | ±5 % up to 2×10¹¹ M☉ | same excess |
| UniverseMachine DR1 | ±18 % | same excess |

Below ~3×10¹⁰ M☉ the CosmoHydro_emu GSMF is 2-5 % **low**. Frontier-E parameters:
κ_w = 3.0, e_w = 0.5, M_seed = 8×10⁵ M☉, v_kin = 5100 km/s, ε_kin = 1.3,
ωₘ = 0.14176, σ₈ = 0.8102 (`fixed_parameters.txt`).

## 2. What has been established (all in nb6)

1. **The GP emulator is faithful.** In-sample residual < 0.01 dex below 10¹¹ M☉; on the 10
   held-out runs (RUN100-109) the RMS is 0.03-0.06 dex in the top two bins. The bundled
   training arrays equal `10**GSMF_Aperture` of the raw extracts exactly.
2. **The raw 400 h⁻¹Mpc extracts themselves are high.** Evaluated at each other's design
   points: raw-400 / Subgrid_emu = +0.11 dex (10¹¹) and +0.18 dex (2.8×10¹¹);
   CosmoHydro_emu / raw-128 = +0.12 / +0.19 dex. A ridge-quadratic fit to the raw 400 data
   evaluated at the Frontier-E point reproduces the 1.29× / 1.68× excess; the same fit to
   the raw 128 data gives 1.00× / 1.13×.
3. **Not cosmology.** Residual at the top bin correlates weakly with ωₘ (r = 0.24) and σ₈
   (r = 0.35). ωₘ is varied at fixed h = 0.6766 in the 400 suite.
4. **Not haloes.** HMF_SOD / Tinker08 (each run's own cosmology, ≥ 20 haloes per bin) over
   10¹²-10¹⁴ M☉/h: 0.82 (400 suite), 0.81 (128 suite), 0.83 (Frontier-E-Small). The
   CosmoHydro HMF emulator matches Frontier-E-Small to ≤ 4 % up to 10¹³ M☉/h.
5. **Not the mass axis.** Both HAVOCC configs use h = 0.6766 and identical bins. Expressed
   as a horizontal shift the excess is Δ ≈ +0.08-0.11 dex above 4×10¹⁰ but −0.03 to −0.10
   dex below 2×10¹⁰ M☉; one shift (0.092 dex) leaves ±0.03 dex residuals of opposite sign;
   an h slip (0.17 dex) is far too large.
6. **Redshift dependence.** At 10¹¹ M☉ the excess is 0.12, 0.12, 0.08, 0.03, 0.03 dex at
   z = 0, 0.1, 0.5, 1, 2. At 2.8×10¹¹ M☉ it is 0.19-0.22 dex for all z ≤ 1 and 0.07 at z = 2.
7. **Star-formation budget at matched parameters** (raw 400 CSFR / Subgrid_emu CSFR at the
   same subgrid parameters): 1.28 (z = 0), 1.12 (z = 0.5), 1.04 (z = 1), 0.94 (z = 2).
   Frontier-E-Small / Subgrid_emu = 0.97-1.02 at all z. So the 400 h⁻¹Mpc runs form
   10-30 % more stars at z < 1 → weaker late-time quenching.
8. **More of the formed stars are counted in galaxies**: ∫M*φ dlogM* / ∫CSFR dt at the
   Frontier-E point = 0.60 (400 suite, regression) vs 0.54 (128 suite) vs 0.549
   (Frontier-E-Small). A bookkeeping / assignment component on top of (7).
9. **Cluster gas fractions agree**: raw-400 f_gas − Subgrid_emu = +0.01 at 10^13.5 M☉/h,
   ≈ 0 above 10¹⁴; Frontier-E-Small within 0.005 of both emulators. Kinetic AGN gas
   ejection behaves the same in both suites.
10. **Galaxy-finder settings known so far** (OpenCosmo catalog headers): 128 h⁻¹Mpc suite
    (Perlmutter, 2024-08) and Frontier-E both use `galaxy_aperture_radius` = 50,
    `galaxy_dbscan_neighbors` = 10, `galaxy_pmin` = 10, `fof_linking_length` = 0.168,
    `sod_pmin` = 100, `NPERH_AGN` = 2.25. **The 400 h⁻¹Mpc suite's settings are unknown**
    (run and post-processed on OLCF Frontier).

## 3. Ranked hypotheses

1. **Weaker late-time quenching in the 400-suite HACC runs** — different HACC build or
   run parameters (AGN radiative efficiency, `NPERH_AGN`, kinetic-jet implementation,
   softening `RSM`/`PROPER_RSM`, star-formation / wind / cooling / UVB tables). Evidence:
   items 6-7, 9.
2. **Galaxy finder / stellar-mass assignment** in the 400-suite cosmotools run (aperture
   radius, DBSCAN neighbours, `galaxy_pmin`, particle threshold, cosmotools build; stars in
   satellites / ICL attached to centrals). Evidence: items 8, and the top-bin excess already
   present at z = 1 when the CSFR difference is only 4 %.
3. **Parameter unit / scaling mismatch** between `FinalDesign.txt` and what was written to
   the 400-run `indat.params` (M_seed × 10⁶, v_kin × 10⁴, ε_kin × 10, e_w, κ_w). Argued
   against by matching parameter responses and f_gas, but cheap to verify.

Excluded: mass-axis convention, cosmology handling, box size / resolution, the emulator.

## 4. Data conventions you will meet

- HAVOCC extract `GalStellarMassFunction_<step>.txt`: columns `Stellar_Mass` [M☉, i.e.
  `gal_mass_star`/h], `GSMF_Aperture` [(h⁻¹Mpc)⁻³ dex⁻¹, **linear**, not log],
  `GSMF_Aperture_err`, `GSMF_UM_z0.01`, `GSMF_UM_z0.00`, `GSMF_Trinity_z0.10`.
  39 bins, 3.6×10⁸-8.8×10¹² M☉; emulators use the 16 bins in (5×10⁹, 3×10¹¹).
- HAVOCC `HaloMassFunction_<step>.txt`: `Halo_Mass` [M☉/h], `HMF_SOD`, `HMF_SOD_err`,
  `halo_counts`, `HMF_TINKER_2008` (own cosmology).
- HAVOCC `CSFR.txt`: scale factor, CSFR [M☉ yr⁻¹ (h⁻¹Mpc)⁻³] (400 suite has a third column
  `dMstardt`). `Mgas_M500_Ratio_<step>.txt`: log M500c [M☉/h] bins, `fgas_mean` column 3.
- HACC galaxy catalogs (`galaxyproperties`) store masses in **M☉/h**; the OpenCosmo portal
  filters in M☉. Steps ↔ z: 624/0, 567/0.1, 498/0.25, 415/0.5, 310/1, 247/1.5, 205/2
  (a = (step+1)/625).
- CosmoHydro design: `CosmoHydro/data/FinalDesign.txt`, row K ↔ RUNK (0-indexed), columns
  kappa_W, e_W, M_seed [M☉], v_kin [km/s], eps_kin, omega_m, sigma_8; emulator trained on
  RUN000-099, RUN100-109 held out. 128-suite runs are named
  `KAPPA_<>_EGW_<>_SEED_<>_VKIN_<>_EPS_<>` (raw units).
- Frontier-E `indat.params` (copy in `data_sims/frontier_e/pk_hydro/indat.params`) subgrid
  keys: `KAPPA_W 3.0`, `EGY_W 0.5`, `NPERH_AGN 2.25`, `AGN_SEED_MASS 8e5`,
  `AGN_KINETIC_JET_VEL 5100.0`, `AGN_KINETIC_JET_EPS 1.3`; also `RSM 0.04`,
  `PROPER_RSM 0.024`, `RCB_TREE_PPN_SPH 128`, `CM_SIZE_SPH 4.0`, `HYDRO_EDGE 0.9`,
  `UVB_RATES_PATH .../CloudyRates_FG20_Shielded.bin`, `COSMOTOOLS_CONFIG
  params/cosmotools-config.dat`. The 400-suite HAVOCC `config.toml` additionally lists
  `AGN_RAD_EFF = 0.2` under `[HACC]`.
- Known original locations (from headers / logs; adapt to the cluster copy):
  400 suite: `/lustre/orion/cos006/proj-shared/SCIDAC_RUNS/RUNS/RUNxxx/{output,analysis}`
  with HAVOCC in `/lustre/orion/cos006/proj-shared/mbuehlmann/SCIDAC_RUNS/HAvoCC`;
  128 suite: `/eagle/CosDiscover/nfrontiere/SCIDAC_RUNS/128MPC_RUNS_HACC_5PARAM/<run>/`;
  Frontier-E-Small: `Data/ProfileData/SCIDAC_RUNS/SMALL_FRONTIERE/`.

## 5. Investigation plan (do these in order; each is decisive on its own)

**Step 0 — inventory.** Locate for (a) one or more 400-suite runs (ideally the three
nearest the Frontier-E point: RUN073, RUN092, RUN059, plus RUN000), (b) one 128-suite run,
(c) Frontier-E-Small, (d) Frontier-E if present: `indat.params`, `cosmotools-config.dat`,
the HACC / cosmotools build info (git hash, module list, build logs, `*.out` job logs),
`galaxyproperties` and `haloproperties` GenericIO files at step 624 (and 310), and the
HAVOCC `config.toml` / extracts.

**Step 1 — diff the HACC run parameters (hypothesis 1 and 3).** Diff every non-path key of
`indat.params` between a 400-suite run and Frontier-E / the 128-suite run. Report
differences in: all `AGN_*`, `NPERH_AGN`, `KAPPA_W`, `EGY_W`, star-formation / wind /
cooling / metal / UVB keys, `RSM`, `PROPER_RSM`, `CM_SIZE_SPH`, `HYDRO_EDGE`,
`RCB_TREE_PPN_SPH`, `N_SUB`, `NG`/`NP`, initial-condition settings (`TRANS`, `Z_IN`,
`USE_WHITE_NOISE_INIT`). Verify that the 400-run values equal `FinalDesign.txt` × the scale
factors. Then diff the HACC source version (git hash / build date) — a different build is
a finding even if the parameters match.

**Step 2 — diff the cosmotools galaxy finder (hypothesis 2).** From
`cosmotools-config.dat` and from the `galaxyproperties` GenericIO headers (or their
OpenCosmo re-format if present) extract `galaxy_aperture_radius`, `galaxy_dbscan_neighbors`,
`galaxy_pmin`, `npart_threshold_galaxyproperties`, the DBSCAN epsilon / linking settings,
and the cosmotools version. Compare with 50 / 10 / 10 / (Frontier-E). Any difference here
is the answer for the assignment component.

**Step 3 — measure the assignment directly (hypothesis 2).** On one 400-suite run and one
128-suite run (or Frontier-E-Small) at step 624, from `galaxyproperties`:
(a) GSMF from `gal_mass_star` vs from `gal_2Rhalf_stellar_mass` vs from
`gal_dbscan_mstar` — if the excess appears only in the aperture mass, the aperture/finder
is responsible; (b) central-only vs satellite-only GSMF; (c) stellar mass–halo mass
relation (`StellarMass_HaloMass`), or simply M*(central)/M_halo at 10¹³-10¹⁴ M☉/h; (d) the
total stellar mass in galaxies vs the total stellar mass in all star particles (from
`haloproperties`/global statistics) — reproduce the 0.60 vs 0.54 fraction from item 8.
HAVOCC modules `ApertureStellarMass_DBScanStellarMass`, `StellarMass_HaloMass(_Central,
_Satellite)`, `GlobalStellarDensity` do this if re-run on a 400 box with the local
`config.toml` switched on.

**Step 4 — quenching (hypothesis 1).** Compare, at matched parameters, the specific SFR
distribution / quenched fraction of galaxies with M* > 10¹¹ M☉ (`gal_sfr`, `gal_mass_star`)
and black-hole masses (`gal_mmagn_mass`, `BHMass_StellarMass` module) between a 400-suite
run and the 128-suite / Frontier-E-Small. Higher sSFR or lower M_BH at fixed M* in the 400
run confirms weaker AGN quenching; equal sSFR with more mass points back to Step 3.

**Step 5 — write up.** Put results, with the exact files inspected and the diffs, in a new
notebook `notebooks/nb7_cosmohydro_gsmf_excess_cluster.ipynb` (plots + printed tables) and
a short `investigations/cosmohydro_gsmf_excess/REPORT.md` with: the identified cause(s),
which 400-suite runs are affected (all, or a subset?), and what a fix would look like
(re-run cosmotools/HAVOCC on the 400 outputs with Frontier-E settings vs re-simulate).

## 6. Ground rules

- Do not modify the emulator packages, the simulation outputs, or existing HAVOCC extracts.
  Read-only on the raw data; write only into this repo.
- Keep analysis in notebooks; the only helper `.py` allowed is
  `data_observational/load_obs_data.py`. Small readers for GenericIO can live inside the
  notebook.
- Report what was actually checked; if a file is missing, say so rather than inferring.
- Existing local numbers to compare against are in nb6 (sections F, G) and
  `data_sims/frontier_e_small/GalStellarMassFunction_624.txt`,
  `data_sims/frontier_e/catalogs/*.npz` (survey-scale Frontier-E GSMF histograms).
