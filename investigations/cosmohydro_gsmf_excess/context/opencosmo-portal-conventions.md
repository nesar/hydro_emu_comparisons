---
name: opencosmo-portal-conventions
description: "How OpenCosmo galaxy-catalog queries on Frontier-E behave (units, 5e6-row cap = uniform subsample, download URL pattern, run time)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 288b244b-a542-4e5f-9cbf-53460e84a140
  modified: 2026-09-17T20:38:18.499Z
---

Learned 2026-09-17 while building nb6 (GSMF comparisons):

- `run_galaxy_catalog_query` mass filters are in **M☉**, but the returned HDF5
  (`data/gal_mass_star`, etc.) stores **M☉/h** (HAVOCC divides by h). Header carries
  `header/simulation/cosmology` (h = 0.6766) and `parameters` (box_size = 3150).
- The `limit` cap (max 1e9, default 1e3) truncates to a **spatially uniform random
  subsample**, not a sub-volume: a 5e6-row cap on M* > 2e11 M☉ filled every level-5
  octree cell with sampling fraction f = 0.497, constant across mass. Normalise with a
  second, uncapped query at a higher mass threshold (M* > 1e12 M☉ gives 3.9e4 galaxies).
- Runs take ~3 min; result files are public HTTPS at
  `https://g-45a93.fd635.8443.data.globus.org/ComputePortal/galaxyquery/<external_run_id>/filtered_galaxy_catalog.hdf5`
  (≈300 B per galaxy; 5e6 rows = 1.5 GB). `preview.json` holds plotly histograms
  (base64 `bdata`) of log10 masses in M☉ — enough for a quick count check.
- The portal's `run_havocc_GSMF` only covers the scidac-128-sg5 suite, not Frontier-E.

**Why:** the nb4 catalog section was left as a skip-if-absent placeholder; these details
make the survey-scale Frontier-E GSMF/HMF reproducible.

**How to apply:** store only small histograms/npz in `data_sims/frontier_e/catalogs/`
(with run ids), never the raw HDF5. See also [[venv-nbconvert-execution]].
