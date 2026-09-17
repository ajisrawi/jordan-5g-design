"""Copernicus GLO-90 DEM (ESA / AWS open data) mosaic for Jordan + vectorised bilinear sampling."""
import os, urllib.request
import numpy as np
import tifffile

LAT_S, LAT_N, LON_W, LON_E = 29, 34, 34, 40        # integer-degree mosaic extent
PPD = 1200                                          # 3 arc-second posts per degree
URL = "https://copernicus-dem-90m.s3.amazonaws.com/{n}/{n}.tif"

class Terrain:
    def __init__(self, cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
        npy = os.path.join(cache_dir, "jordan_glo90.npy")
        if os.path.exists(npy):
            self.z = np.load(npy); return
        H, W = (LAT_N - LAT_S) * PPD, (LON_E - LON_W) * PPD
        z = np.zeros((H, W), np.int16)
        for lat in range(LAT_S, LAT_N):
            for lon in range(LON_W, LON_E):
                n = f"Copernicus_DSM_COG_30_N{lat:02d}_00_E{lon:03d}_00_DEM"
                f = os.path.join(cache_dir, n + ".tif")
                if not os.path.exists(f):
                    try:
                        raw = urllib.request.urlopen(urllib.request.Request(URL.format(n=n), headers={"User-Agent": "Mozilla/5.0"}), timeout=180).read()
                        open(f, "wb").write(raw); print("  DEM tile", n, len(raw) // 1024, "KB")
                    except Exception as e:
                        print("  DEM tile missing", n, e); continue
                a = tifffile.imread(f)
                if a.shape != (PPD, PPD):
                    print("  unexpected shape", a.shape, n); continue
                r0 = (LAT_N - 1 - lat) * PPD; c0 = (lon - LON_W) * PPD
                z[r0:r0 + PPD, c0:c0 + PPD] = np.round(a).astype(np.int16)
        np.save(npy, z); self.z = z

    def sample(self, lat, lon):
        lat = np.asarray(lat, float); lon = np.asarray(lon, float)
        r = (LAT_N - lat) * PPD - 0.5; c = (lon - LON_W) * PPD - 0.5
        r = np.clip(r, 0, self.z.shape[0] - 1.001); c = np.clip(c, 0, self.z.shape[1] - 1.001)
        r0 = r.astype(int); c0 = c.astype(int); fr = r - r0; fc = c - c0
        z = self.z
        return ((z[r0, c0] * (1 - fc) + z[r0, c0 + 1] * fc) * (1 - fr) + (z[r0 + 1, c0] * (1 - fc) + z[r0 + 1, c0 + 1] * fc) * fr)
