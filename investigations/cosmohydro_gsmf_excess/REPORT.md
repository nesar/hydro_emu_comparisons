# Report: the CosmoHydro 400 h⁻¹Mpc GSMF excess

Cluster investigation of `BRIEF.md`, done 2026-09-18 on Polaris with read-only access to `/eagle/CosDiscover`.
All numbers, tables and figures are in `notebooks/nb7_cosmohydro_gsmf_excess_cluster.ipynb` (executed).

## Answer

**The cause is the HACC build.** The 400 h⁻¹Mpc CosmoHydro suite was run with a newer CRK-HACC code state than the
one used for the 128 h⁻¹Mpc subgrid suite, Frontier-E-Small and Frontier-E. That code state forms more stars in massive
galaxies at late times, because black holes grow less and quench later, and it keeps more of each star particle's mass.

It is **not** the parameters, cosmotools/galaxy finder, HAVOCC, cosmology, box size or the emulator. Re-running
cosmotools/HAVOCC cannot fix it.

## Evidence

1. **Parameters and finder are identical** (nb7 §1a, §2).
   - The `indat.params` of the raw 400 copies (RUN008/032/040) equal `FinalDesign.txt` in raw units. Every other physics
     key (NPERH_AGN, RSM, PROPER_RSM, CM_SIZE_SPH, HYDRO_EDGE, N_SUB, Z_IN, TRANS, I_SEED, ...) equals the 128 suite and
     Frontier-E. The spacing is the same 0.25 h⁻¹Mpc everywhere.
   - `cosmotools-config.dat` is identical apart from the GPU count: 50 kpc aperture, DBSCAN 10, pmin 10.
   - The 400 RUN000 training extract equals a plain histogram of its own `gal_mass_star` catalogue in all 16 emulator bins.
2. **Builds differ** (nb7 §1b).
   - The 128 suite (all 64 binaries) and the 256-2PARAM suite use `hacc_hydro--a4ce989a` (Aug 2024).
   - FE-Small uses `942a84f9` (Jan 2025).
   - The 256 h⁻¹Mpc COSMO runs use `67cebcfb` (Nov 2025), with local switches `SF_FULL_SFR` **on** and
     `CHEM_USE_INIT_STAR_MASS` **off**.
   - No binary, job log or source diff exists for the 400 runs on Eagle (OpenCosmo header: `hacc_version 0.0.0`).
3. **Controlled build test** (nb7 §3). `SCIDAC_COSMO_P_BASE` (67cebcfb) and FE-Small (942a84f9) have identical
   parameters, box, resolution and ICs. Their ratio reproduces the 400 excess (log₁₀ ratio to FE-Small at z = 0):

   | | 3×10¹⁰ | 10¹¹ | 2×10¹¹ | 2.8×10¹¹ M☉ |
   |---|---|---|---|---|
   | 400 suite, ridge fit to 58 raw extracts at the FE point | −0.01 | **+0.13** | +0.21 | **+0.23** |
   | P_BASE (new build, one run at the FE point) | −0.03 | **+0.12** | +0.18 | **+0.17** |
   | 128 suite fit at FE (old build) | −0.01 | −0.00 | +0.01 | +0.03 |
   | 256-2PARAM fit at FE (old build) | −0.00 | +0.00 | +0.01 | −0.01 |

   The same fit over **all 110 training extracts** (nb7 §3a, cached in `data_sims/cosmohydro_400/`) gives −0.01 / +0.11 /
   +0.19 / +0.20 dex at the FE point, i.e. the 58-run tarball subset is representative; 25-30 % of the individual
   extracts lie above FE-Small at 10¹¹-2.8×10¹¹ M☉ (the rest have stronger feedback than Frontier-E).

   It matches the other nb6 signatures too:
   - **Redshift trend (item 6):** at 10¹¹ M☉ the excess is +0.12, +0.06, +0.03, +0.03 dex at z = 0, 0.5, 1, 2. At
     2.8×10¹¹ M☉ it is +0.17 to +0.19 dex up to z = 1, and +0.08 at z = 2.
   - **CSFR boost (item 7):** 1.20, 1.13, 1.10, 1.04 at z = 0, 0.5, 1, 2.
   - **Formed-stars-in-galaxies fraction (item 8):** 0.601 vs 0.549.
   - **Haloes:** unchanged to 1-3 %.
   - **Other cosmologies:** the 400-suite fit also reproduces the new-build runs at ωₘ = 0.155, σ₈ = 0.7 and 0.9, within
     0.03-0.05 dex below 2×10¹¹ M☉.
4. **The 400 runs carry the new build's fingerprint** (nb7 §4). The retained fraction of a star particle's initial mass at
   fixed formation epoch depends only weakly on the physics parameters.

   | median retained fraction at a_form ≈ 0.55 | value |
   |---|---|
   | 128 suite, all 64 runs (a4ce989a) | 0.659-0.703 |
   | FE-Small (942a84f9) | 0.688 |
   | P_BASE (67cebcfb) | 0.734 |
   | **400 RUN000** | **0.733** (equals P_BASE to ≤ 0.003 in every bin) |
   | **400 RUN001** | **0.723** (above the old-build maximum) |

   In the raw z = 0 snapshots (median star-particle mass / m_b):
   - 128 suite: 0.707-0.739
   - FE-Small: 0.732
   - P_BASE: 0.773
   - 400 RUN032 and RUN040: 0.768 and 0.766, both with P_BASE
   - 400 RUN008: 0.744, just above the 128 range and not decisive on its own
5. **Mechanism** (nb7 §6, catalogues of P_BASE vs FE-Small at identical parameters).
   - **Not a finder effect:** the excess appears in the 50 kpc aperture, DBSCAN and 2R½ masses, and in both centrals and
     satellites.
   - **Lighter black holes:** central BH masses are 0.10 dex lower at fixed M* below 10¹¹ M☉ and 0.16-0.19 dex lower above.
   - **Later quenching:** the quenched fraction of 10^10.4-10^11.1 M☉ centrals is 0.06-0.12 lower, and their sSFR is
     1.4-3× higher.
   - **More stellar mass:** +19 % in galaxies overall, of which ≈ +6.6 % is the retained-mass change.
   - **Seen in a real 400 run:** 400 RUN000's central BHs sit 0.09-0.14 dex below the 128 suite at the same subgrid
     parameters. That is the same offset as P_BASE vs FE-Small, while FE-Small itself matches the 128 suite to ≤ 0.01 dex.
   - **Side effect on P(k):** P_m(k) is higher by 1.2 % at k = 2, 3.5 % at k = 5 and 5.3 % at k = 10 h Mpc⁻¹ (z = 0).
     This also affects CosmoHydro_emu's P_hydro.
6. **When the change came in** (nb7 §5). The 2025 development runs are 128 h⁻¹Mpc runs at FE parameters with the same ICs.
   - Every default-setup run up to UPSFGAS (`ffb10d7a`, 2025-07-19) matches the old GSMF within ±0.05 dex and has the old
     mass-loss curve.
   - Experiments that weaken BH accretion (`VBH_20`, a larger minimum BH velocity in the Bondi rate) give the same GSMF shape
     (+0.26/+0.49 dex) with no mass-loss change. So the massive-end excess is a BH-growth effect, and the mass-return switch
     is a separate ≈ +6 % stellar-mass shift.
   - No build between 2025-07-19 and 2025-11-02 exists on Eagle. The HACC repository is private.

## Which runs are affected

Every 400 run that could be checked:
- Clean per-particle fingerprint: RUN000, RUN001.
- Snapshot fingerprint: RUN032, RUN040, and RUN008 (marginal).

The 58-run suite-level fit is shifted as a whole (in-sample rms 0.017 dex, no sub-population near the old build). RUN056-109
(except 060 and 063) have no extracts or catalogues on Eagle and were not inspected individually.

## What a fix looks like

- **No post-processing fix.** cosmotools/HAVOCC re-runs cannot remove the excess.
- **Decide which model is "the" model.** Frontier-E(-Small) and the 128 suite are one code state; the 400 suite is another.
  - If the new code state is intended, then the Frontier-E subgrid parameters are no longer calibrated for it. CosmoHydro_emu
    at the FE point is then *not* a proxy for Frontier-E, and the new model needs re-calibration (for example with
    Subgrid_emu-style runs on the new build).
  - If the old state is the target, the 400 suite must be re-simulated with the Frontier-E build/configuration.
- **Interim correction (only near the FE point):** multiply CosmoHydro_emu predictions by the measured
  FE-Small / P_BASE ratio (GSMF: nb7 §3; P(k): nb7 §6a). Don't apply it far from FE, because the ratio depends on the
  parameters.
- **Before deciding, ask the 400-suite owners (OLCF, `/lustre/orion/cos006/proj-shared/SCIDAC_RUNS/RUNS`)** for:
  1. The `hacc_tpm` "Source Checkout" line or a job log, plus `output/repo/*.diff`, to confirm 67cebcfb (or later) with the
     P_BASE switches.
  2. Whether the `SF_FULL_SFR` / `CHEM_USE_INIT_STAR_MASS` change and the commits after `ffb10d7a` were intended.
  3. The compiled defaults of `AGN_BETA`, `AGN_TEXP`, `WIND_FSN`, `WIND_VEL`. The 400 `indat.params` omit these four keys,
     while every 2025 run, P_BASE included, sets them (0.0, 9.0, 0.3387, 199.986). The 400-vs-P_BASE agreement
     (≤ 0.03 dex below 10¹¹ M☉) suggests any effect is small.

## Files inspected (read-only)

- **400 suite**
  - `/eagle/CosDiscover/SCIDAC_RUNS/RUNS/RUN{008,032,040}/`: `params/{indat.params,cosmotools-config.dat}`, z = 0
    haloproperties and full snapshots
  - `/eagle/CosDiscover/SCIDAC_RUNS/FinalDesign.txt`
  - `/eagle/CosDiscover/mbuehlmann/SCIDAC_RUNS/400MPC_RUNS_5SG_2COSMO_PARAM/`:
    - `HAvoCC_Mar23/RUN000` (training extract, config)
    - `scidac-frontier-havocc.tar.zstd` (58 runs; GSMF cache in `data_sims/cosmohydro_400/`)
    - `OpenCosmo/RUN00{0,1}` (galaxyproperties, star particles)
- **128 suite:** `/eagle/CosDiscover/nfrontiere/SCIDAC_RUNS/128MPC_RUNS_HACC_5PARAM/*` (hacc_tpm, diff.txt, params,
  analysis_pipeline/extract2, z = 0 snapshots) and `/eagle/CosDiscover/mbuehlmann/SCIDAC_RUNS/128MPC_RUNS_HACC_5PARAM/reformat/*`
  (catalogues, star particles)
- **256 suites:** `/eagle/CosDiscover/nfrontiere/SCIDAC_RUNS/256MPC_RUNS_HACC_2PARAM{,_2}/*`,
  `/eagle/CosDiscover/mbuehlmann/SCIDAC_RUNS/256MPC_RUNS_HACC_2PARAM{,_2}/*/extract`, and
  `/eagle/CosDiscover/nfrontiere/SCIDAC_RUNS/256MPC_RUNS_HACC_COSMO/SCIDAC_COSMO_*`
- **FE-Small:** `/eagle/CosDiscover/nfrontiere/Default_256MPC_NEW_KIN_JET_E_1.3_V_5100_S_8e5_SS_ZINI_0.25` and
  `/eagle/CosDiscover/mbuehlmann/INCITE_Hydro/256MPC/havocc/{extract_14.6,config_14.6.toml}`
- **Development runs:** `/eagle/CosDiscover/nfrontiere/Default_*` (128 h⁻¹Mpc ones)

**Missing:** raw 400 galaxy catalogues; any 400 build record (binary, logs, diff); Mar-23 extracts for runs other than
RUN000; 400 runs RUN056-109 apart from 060/063; the HACC source repository (private).

## Environment note

The repo `.venv` on Polaris was created from `conda/2025-09-25` with `pygio`, `hdf5plugin` and `blosc`, and registered as
kernel `hydro-emu-venv`. The kernel's `env` carries `LD_LIBRARY_PATH` (CUDA 13 runtime for h5py, plus Cray libfabric).
The pip `pygio` crashes on multi-file GenericIO without `MPI_Init`, so nb7 has its own small BLOSC sub-file reader,
validated against `pygio`.
