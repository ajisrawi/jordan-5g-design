"""Shared RF model for the Jordan 5G SA nominal design.

Statistical models only (3GPP TR 38.901). No terrain/clutter database is used for
path loss, so every figure produced here is a NOMINAL-planning figure that must be
re-run in a calibrated planning tool (Atoll / Planet / ASSET) before build.
The same formulas are mirrored in app.js so the map and the report agree.
"""
import math
import numpy as np

# ----------------------------------------------------------------------------
# Radio configurations (per sector)
# ----------------------------------------------------------------------------
RADIO = {
    # n78 64T64R massive-MIMO AAU, 400 MHz IBW, 320 W (55.05 dBm) total shared by the active 100 MHz carriers
    "n78_64T": dict(fc=3.5, p_total_dbm=55.05, n_sc=3276, scs_khz=30, g_traffic=24.0, g_ssb=20.0,
                    h3db=90.0, am=25.0, v3db=14.0, sla=20.0, bf_iso=7.0),
    # n28 4T4R RRU 2x... 80 W per 10 MHz carrier on passive antenna
    "n28_4T": dict(fc=0.7, p_carrier_dbm=49.0, n_sc=624, scs_khz=15, g_traffic=15.5, g_ssb=15.5,
                   h3db=65.0, am=25.0, v3db=9.0, sla=18.0, bf_iso=0.0, feeder=0.5),
}
UE_NF = 7.0          # dB
GNB_NF = 3.5         # dB
RE_PER_S_100MHZ = 273 * 12 * 28000   # resource elements / s in one 100 MHz, 30 kHz SCS carrier
TDD_DL = 0.74        # DDDSU, S = 10:2:2
TDD_UL = 0.23
OH_DL = 0.14         # TS 38.306 FR1 DL overhead
OH_UL = 0.08
IMPL = 0.70          # implementation factor on Shannon (link adaptation, CSI ageing, BLER)
SE_CAP = 7.4         # bits/RE per layer: 256QAM x 948/1024
RANK_PEN = {1: 0.0, 2: 1.0, 3: 2.0, 4: 3.0}   # inter-layer interference penalty, dB


def noise_per_sc(scs_khz, nf):
    return -174.0 + 10 * math.log10(scs_khz * 1e3) + nf


def eirp_per_sc(r, beam="traffic", bw_mhz=300):
    g = r["g_traffic"] if beam == "traffic" else r["g_ssb"]
    pc = r["p_total_dbm"] - 10 * math.log10(bw_mhz / 100.0) if "p_total_dbm" in r else r["p_carrier_dbm"]
    return pc - 10 * math.log10(r["n_sc"]) + g - r.get("feeder", 0.0)


def pl_uma(d_m, fc_ghz, hbs, hut=1.5):
    """38.901 UMa, deterministic NLOS with LOS floor. d_m = 2D distance in m."""
    d3 = np.sqrt(np.maximum(d_m, 10.0) ** 2 + (hbs - hut) ** 2)
    nlos = 13.54 + 39.08 * np.log10(d3) + 20 * np.log10(fc_ghz) - 0.6 * (hut - 1.5)
    los = 28.0 + 22 * np.log10(d3) + 20 * np.log10(fc_ghz)
    return np.maximum(np.maximum(nlos, los), 70.0)


def pl_rma(d_m, fc_ghz, hbs, hut=1.5, w=20.0, h=5.0):
    """38.901 RMa NLOS with LOS floor."""
    d3 = np.sqrt(np.maximum(d_m, 10.0) ** 2 + (hbs - hut) ** 2)
    nlos = (161.04 - 7.1 * np.log10(w) + 7.5 * np.log10(h)
            - (24.37 - 3.7 * (h / hbs) ** 2) * np.log10(hbs)
            + (43.42 - 3.1 * np.log10(hbs)) * (np.log10(d3) - 3)
            + 20 * np.log10(fc_ghz) - (3.2 * (np.log10(11.75 * hut)) ** 2 - 4.97))
    los = (20 * np.log10(40 * np.pi * d3 * fc_ghz / 3) + min(0.03 * h ** 1.72, 10) * np.log10(d3)
           - min(0.044 * h ** 1.72, 14.77) + 0.002 * np.log10(h) * d3)
    return np.maximum(np.maximum(nlos, los), 70.0)


def se_total(sinr_db, max_rank=4):
    """Rank-adaptive spectral efficiency (bits/RE summed over layers)."""
    sinr_db = np.asarray(sinr_db, dtype=float)
    best = np.zeros_like(sinr_db)
    for r in range(1, max_rank + 1):
        s = 10 ** ((sinr_db - 10 * math.log10(r) - RANK_PEN[r]) / 10)
        best = np.maximum(best, r * np.minimum(SE_CAP, IMPL * np.log2(1 + s)))
    return best


def tp_n78_mbps(sinr_db, bw_mhz=200):
    return se_total(sinr_db) * RE_PER_S_100MHZ * (bw_mhz / 100.0) * TDD_DL * (1 - OH_DL) / 1e6


def tp_fdd_mbps(sinr_db, bw_mhz=35):
    """n1+n3 FDD carriers aggregated (4T4R, 15 kHz SCS): ~ 52 PRB per 10 MHz."""
    re_s = bw_mhz / 10.0 * 52 * 12 * 14000
    return se_total(sinr_db, 4) * re_s * (1 - OH_DL) / 1e6


def sinr_for_tp(target_mbps, bw_mhz):
    lo, hi = -10.0, 45.0
    if tp_n78_mbps(hi, bw_mhz) < target_mbps:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if tp_n78_mbps(mid, bw_mhz) < target_mbps:
            lo = mid
        else:
            hi = mid
    return hi


def range_for_mapl(mapl, model, fc, hbs):
    f = pl_uma if model == "uma" else pl_rma
    lo, hi = 10.0, 60000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if float(f(np.array([mid]), fc, hbs)[0]) < mapl:
            lo = mid
        else:
            hi = mid
    return lo


def pattern_db(daz_deg, theta_deg, tilt_deg, r):
    """3GPP-style envelope pattern. theta = depression angle to the point."""
    ah = np.minimum(12 * (daz_deg / r["h3db"]) ** 2, r["am"])
    av = np.minimum(12 * ((theta_deg - tilt_deg) / r["v3db"]) ** 2, r["sla"])
    return -np.minimum(ah + av, 30.0)
