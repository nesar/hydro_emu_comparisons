"""Loaders for observational data used across the emu_comparisons notebooks.

This is the only .py module in emu_comparisons (per README.txt, .py files are
reserved for observational data loading). Notebooks import it with:

    import sys; sys.path.insert(0, '../data_observational')
    import load_obs_data

Directory layout
----------------
RealData/       linear-P(k) datasets provided by the user (2026-08-31):
                  reid_DR7.txt, wmap_act.txt, DR14_pm3d_19kbins.txt,
                  mpk_compilation/ (Chabanier+2019 repo),
                  PowerSpectraObservationData.{csv,xlsx} -- NOT used: these are
                  plot-digitizer exports whose axes were never calibrated
                  (k "values" of 3.5-9.6 for every survey); the same surveys
                  are covered by the calibrated files above.
kids_legacy/    KiDS-Legacy deprojected Pm(k, z) (Broxterman+2025, A&A 703 L3),
                copied from CosmoHydro/data/Power_spec_targets/
                nonlinear_pk_targets/kids_legacy/ (see ReadMe there).
gsmf/           Driver et al. 2022 (GAMA DR4) GSMF -- the Inference-pipeline
                calibration target.
cgd/            Cluster gas density profiles: McDonald+2017 (avg/median),
                Ghirardini+2019, Lehle+2023, Braspenning+2023, copied from the
                HAvoCC ClusterGasDensityProfile module data.
fgas/           Kugel+2023 Table 5 cluster gas fractions.
user_pk/        drop-in [k, P, (err)] text files, k in h/Mpc, P in (Mpc/h)^3
                at z = 0; name '*_nl.txt' for nonlinear-scale measurements.

Unit conventions (verified numerically against linear theory at the Frontier-E
cosmology where applicable): k in h Mpc^-1 and P in (h^-1 Mpc)^3 unless stated.
"""

import glob
import os

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REAL = os.path.join(_HERE, 'RealData')


# ---------------------------------------------------------------------------
# Linear P(k) datasets (z = 0)
# ---------------------------------------------------------------------------
def load_lya_dr14(h=0.6766):
    """eBOSS DR14 Lya-forest-derived linear P(k), rescaled to z = 0
    (Chabanier+2019 compilation). File stores k in Mpc^-1 (no h) and P in
    (Mpc/h)^3 -- verified vs linear theory (chi2/dof ~ 0.5)."""
    k_mpc, pk, err = np.loadtxt(os.path.join(_REAL, 'DR14_pm3d_19kbins.txt')).T
    return {
        'k': k_mpc / h, 'P': pk, 'err': err,
        'label': r'eBOSS DR14 Ly$\alpha$ (Chabanier+19)',
        'kind': 'linear',
    }


def load_reid_dr7():
    """SDSS DR7 LRG-derived linear matter P(k) at z = 0 (Reid et al. 2010,
    as distributed with cmb.wintherscoming.no/milestone4). Columns already
    k [h/Mpc], P and err [(Mpc/h)^3]; agrees with linear theory to ~5%."""
    k, pk, err = np.loadtxt(os.path.join(_REAL, 'reid_DR7.txt')).T
    return {'k': k, 'P': pk, 'err': err,
            'label': 'SDSS DR7 LRG (Reid+10)', 'kind': 'linear'}


def load_wmap_act():
    """CMB-derived linear matter P(k) at z = 0 (WMAP+ACT, Hlozek et al. 2012,
    arXiv:1105.4887; via cmb.wintherscoming.no/milestone4). Third column is
    the upper bound -> symmetric error = P_upper - P."""
    k, pk, p_hi = np.loadtxt(os.path.join(_REAL, 'wmap_act.txt')).T
    return {'k': k, 'P': pk, 'err': p_hi - pk,
            'label': 'CMB: WMAP+ACT (Hlozek+12)', 'kind': 'linear'}


def load_user_pk(subdir='user_pk'):
    """Any user-provided P(k) files in data_observational/user_pk/."""
    out = []
    for path in sorted(glob.glob(os.path.join(_HERE, subdir, '*.txt'))):
        data = np.loadtxt(path)
        if data.ndim != 2 or data.shape[1] < 2:
            continue
        name = os.path.splitext(os.path.basename(path))[0]
        out.append({'k': data[:, 0], 'P': data[:, 1],
                    'err': data[:, 2] if data.shape[1] > 2 else None,
                    'label': name.replace('_', ' '),
                    'kind': 'nonlinear' if name.endswith('_nl') else 'linear'})
    return out


def load_all_linear(h=0.6766):
    """All z = 0 linear P(k) datasets (+ user drop-ins tagged 'linear')."""
    out = [load_lya_dr14(h=h), load_reid_dr7(), load_wmap_act()]
    out.extend(d for d in load_user_pk() if d['kind'] == 'linear')
    return out


# ---------------------------------------------------------------------------
# KiDS-Legacy deprojected matter power spectrum (nonlinear, tomographic)
# ---------------------------------------------------------------------------
def load_kids_legacy(nz='nz3', z_bins=None, k_min=None, k_max=None):
    """KiDS-Legacy deprojected Pm(k, z) = fdelta * Pdmo (Broxterman et al.
    2025, A&A 703, L3). Mirrors CosmoHydro/Inference_cosmo/targets.py.

    nz='nz1' (one bin, z_fid = 0.3) or 'nz3' (z_fid = 0.15, 0.45, 1.3).
    Returns dict with k, z, P (posterior median Pm), err (symmetrized 68% CI
    of fdelta times fiducial Pdmo), cov (correlation x sigma outer product).
    This is a *nonlinear total-matter* measurement: compare with emulated
    hydro P(k, z_fid), not with linear theory.
    """
    kdir = os.path.join(_HERE, 'kids_legacy')
    d = np.loadtxt(os.path.join(kdir, f'KiDSLegacy_{nz}_Pm.txt'))
    corr = np.loadtxt(os.path.join(kdir, f'{nz}-pmcm.dat'))

    k, z, pm = d[:, 0], d[:, 1], d[:, 2]
    fdelta, pdmo = d[:, 5], d[:, 8]
    sigma = 0.5 * (d[:, 7] - d[:, 6]) * pdmo
    corr = 0.5 * (corr + corr.T)
    cov = corr * np.outer(sigma, sigma)

    keep = np.ones(k.size, dtype=bool)
    if k_min is not None:
        keep &= k >= k_min
    if k_max is not None:
        keep &= k <= k_max
    if z_bins is not None:
        keep &= np.isin(z, np.asarray(z_bins, dtype=float))
    idx = np.where(keep)[0]
    return {'k': k[idx], 'z': z[idx], 'P': pm[idx], 'err': sigma[idx],
            'cov': cov[np.ix_(idx, idx)],
            'fdelta': fdelta[idx], 'pdmo': pdmo[idx],
            'label': f'KiDS-Legacy $P_m$ ({nz})', 'kind': 'nonlinear',
            'ref': 'Broxterman et al. 2025, A&A 703, L3'}


# ---------------------------------------------------------------------------
# GSMF / CGD / fGas calibration targets (as in the Inference pipeline)
# ---------------------------------------------------------------------------
def load_gsmf_driver2022(hubble=0.681):
    """GAMA DR4 GSMF (Driver et al. 2022) in the exact convention of the
    CosmoHydro Inference pipeline (load_hacc.load_gsmf_obs): x = M* [Msun],
    phi = 10^log10phi / h^3 [(Mpc/h)^-3 dex^-1], err = lower error magnitude."""
    d = np.loadtxt(os.path.join(_HERE, 'gsmf', 'Driver2022.txt'))
    good = np.isfinite(d[:, 1])
    d = d[good]
    phi = 10**d[:, 1] / hubble**3
    err_lo = np.abs(10**(d[:, 1] - d[:, 2]) / hubble**3 - phi)
    err_hi = np.abs(10**(d[:, 1] + d[:, 2]) / hubble**3 - phi)
    return {'x': 10**d[:, 0], 'y': phi, 'yerr': (err_lo, err_hi),
            'label': 'GAMA DR4 (Driver+22)'}


def load_cgd_obs():
    """Cluster gas density profiles rho_gas/rho_crit vs r/R500c at z ~ 0.

    Returns dict of datasets:
      mcdonald2017 : points (x, y) -- bin_0 (0 < z < 0.1) of the McDonald+2017
                     average profiles (the Inference-pipeline CGD target)
      ghirardini2019, lehle2023 : (x, y, yerr_lo, yerr_hi) comparison profiles
    """
    cdir = os.path.join(_HERE, 'cgd')
    mc = np.loadtxt(os.path.join(cdir, 'mcdonald2017_avg.txt'))
    gh = np.loadtxt(os.path.join(cdir, 'ghirardini2019_rho_z0.txt'))
    le = np.loadtxt(os.path.join(cdir, 'lehle2023_rho_z0.txt'))
    return {
        'mcdonald2017': {'x': mc[:, 0], 'y': mc[:, 1],
                         'label': 'McDonald+17 (0<z<0.1)'},
        'ghirardini2019': {'x': gh[:, 0], 'y': gh[:, 1],
                           'yerr': (gh[:, 2], gh[:, 3]),
                           'label': 'Ghirardini+19 (X-COP)'},
        'lehle2023': {'x': le[:, 0], 'y': le[:, 1],
                      'label': 'Lehle+23 (eROSITA)'},
    }


def load_fgas_kugel2023(hubble=0.681):
    """Cluster gas fractions (Kugel+2023 Table 5), Inference-pipeline
    convention: x = 10^log10(M500c) * h [Msun/h]."""
    d = np.loadtxt(os.path.join(_HERE, 'fgas', 'kugel2023_table5.txt'))
    return {'x': 10**d[:, 0] * hubble, 'y': d[:, 1], 'yerr': d[:, 2],
            'label': 'X-ray+WL compilation (Kugel+23 T5)'}
