CosmoHydro_emu: https://github.com/nesar/cosmohydro_emu
Subgrid_emu: https://github.com/nesar/subgrid_emu
MiraTitan-IV emu: https://ccl.readthedocs.io/en/latest/api/pyccl.emulators.cosmicemu_pk.html#pyccl.emulators.cosmicemu_pk.CosmicemuMTIVPk 
For linear P(k): https://ccl.readthedocs.io/en/latest/api/pyccl.emulators.baccoemu_linear_pk.html

Check the following. Avoid writing additional .py files (except for observational data loading) for now. Use .ipynb notebooks so that it's easy to follow. Most of the codes need to load the emulators (install as neeed). Use 1 notebook per query below:  

(1) CosmoHydro with cosmology fixes to Subgrid, how do the common emulated quantities compare?

(2) How does the Pk_GO and Pk_Hydro from CosmoHydro_emu compare with MiraTitan-IV emu (with fixed cosmologies where CosmoHydro doesn't vary)

(3) Check linear P(k) vs non-linear P(k) againt data for linear (a lot of surveys for this, will provide data) vs non-linear (KiDS for instance)

(4) Check emulated quantities against Frontier-E simulation (survey-scale) datasets, for all 3 emulators.


If you need the 'fixed parameters' in any of these, search online for Frontier-E sim, subgrid-emu paper etc. Keep them all in a text file and load it from there. 
