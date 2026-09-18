# Prompt to run in Claude Code on the cluster

Paste the block below as the first message (edit the two paths). The repo's `CLAUDE.md`
and `investigations/cosmohydro_gsmf_excess/BRIEF.md` carry the full context.

```
Read CLAUDE.md, SETUP.md and investigations/cosmohydro_gsmf_excess/BRIEF.md first, then
open notebooks/nb6_gsmf_z0_comparison.ipynb (sections F, G and the final summary cell)
to see the evidence and numbers already established.

Task: find out why the 400 h^-1 Mpc CosmoHydro training simulations have 30-70 % more
galaxies above 1e11 Msun at z <= 1 than the 128 h^-1 Mpc subgrid suite, Frontier-E-Small
and Frontier-E at the same parameters. The GP emulator itself is fine; the raw HAVOCC
extracts are high. Two components were isolated locally: (1) 10-30 % more star formation
at z < 1 at matched parameters (weaker late-time quenching), and (2) a larger fraction of
formed stars counted inside galaxies (0.60 vs 0.54). Haloes, gas fractions, cosmology and
the mass-axis convention are already excluded.

Raw simulation / cosmotools / HAVOCC outputs are under:
  400 h^-1 Mpc suite (RUN000-RUN109):   <PATH_400>
  128 h^-1 Mpc suite, Frontier-E-Small, Frontier-E: <PATH_OTHER>
Treat all of that as read-only. Write only into this repo.

Follow the plan in BRIEF.md section 5, in order:
  Step 0  inventory the parameter files, cosmotools configs, build/version info and
          galaxyproperties/haloproperties files for RUN073, RUN092, RUN059, RUN000, one
          128-suite run, Frontier-E-Small (and Frontier-E if present).
  Step 1  diff indat.params (all AGN_*, NPERH_AGN, KAPPA_W, EGY_W, SF/wind/cooling/UVB,
          RSM, PROPER_RSM, CM_SIZE_SPH, HYDRO_EDGE, N_SUB, IC settings) and the HACC
          build/version; verify the 400-run values equal FinalDesign.txt x scale factors.
  Step 2  diff the cosmotools galaxy-finder settings (aperture radius, DBSCAN neighbours,
          galaxy_pmin, particle thresholds, cosmotools version) against 50/10/10.
  Step 3  from galaxyproperties at step 624, measure the GSMF with gal_mass_star vs
          gal_2Rhalf_stellar_mass vs gal_dbscan_mstar, central vs satellite, and the
          fraction of all stellar mass that sits in catalogued galaxies, for a 400 run
          and a 128 run / Frontier-E-Small.
  Step 4  compare sSFR and black-hole mass at fixed M* > 1e11 Msun between the suites.
  Step 5  write notebooks/nb7_cosmohydro_gsmf_excess_cluster.ipynb (executed, with
          figures and printed tables) and investigations/cosmohydro_gsmf_excess/REPORT.md
          naming the cause(s), which runs are affected, and the fix options.

Rules: no changes to the emulator packages or simulation data; analysis in notebooks
only (no new .py files except inside the notebook); state explicitly which files you
inspected and which were missing. Use the repo venv if it exists, otherwise any Python
with numpy/matplotlib/h5py and the site's GenericIO reader.
```
