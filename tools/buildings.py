"""GHSL GHS-BUILT-H R2023A (EU JRC, open data): average net building height (ANBH, m) on a 100 m Mollweide grid.
Tile R6_C22 covers Jordan south of ~33.1 deg N (everything that is built-up)."""
import math, os
import numpy as np
import tifffile

R = 6378137.0
class BuildingHeights:
    def __init__(self, tif):
        with tifffile.TiffFile(tif) as t:
            p = t.pages[0]
            tp = p.tags["ModelTiepointTag"].value; ps = p.tags["ModelPixelScaleTag"].value
            self.x0, self.y0, self.res = tp[3], tp[4], ps[0]
            a = p.asarray().astype(np.float32)
        a[a >= 255] = 0
        self.a = a

    @staticmethod
    def moll(lat, lon):
        phi, lam = np.radians(np.asarray(lat, float)), np.radians(np.asarray(lon, float))
        th = phi.copy()
        for _ in range(12):
            th = th - (2 * th + np.sin(2 * th) - np.pi * np.sin(phi)) / (2 + 2 * np.cos(2 * th))
        return 2 * math.sqrt(2) / math.pi * R * lam * np.cos(th), math.sqrt(2) * R * np.sin(th)

    def sample(self, lat, lon):
        x, y = self.moll(lat, lon)
        c = np.floor((x - self.x0) / self.res).astype(int); r = np.floor((self.y0 - y) / self.res).astype(int)
        ok = (c >= 0) & (c < self.a.shape[1]) & (r >= 0) & (r < self.a.shape[0])
        out = np.zeros(np.shape(c), np.float32)
        out[ok] = self.a[r[ok], c[ok]]
        return out

    def stats(self, lat, lon, radius_m=250):
        """(mean of built cells, max, built fraction) in a square window around the point."""
        x, y = self.moll(lat, lon)
        c = int((x - self.x0) // self.res); r = int((self.y0 - y) // self.res); n = int(round(radius_m / self.res))
        if r - n < 0 or c - n < 0 or r + n >= self.a.shape[0] or c + n >= self.a.shape[1]: return 0.0, 0.0, 0.0
        w = self.a[r - n:r + n + 1, c - n:c + n + 1]; b = w[w > 0]
        return (float(b.mean()) if b.size else 0.0, float(w.max()), float(b.size) / w.size)

    def overlay_png(self, path, south, west, north, east, px_m=120):
        """RGBA overlay with Web-Mercator-spaced rows so Leaflet imageOverlay registers correctly."""
        from PIL import Image
        W = int((east - west) * 111320 * math.cos(math.radians((south + north) / 2)) / px_m)
        my = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
        H = int(W * (my(north) - my(south)) / math.radians(east - west))
        ys = np.linspace(my(north), my(south), H); lats = np.degrees(2 * np.arctan(np.exp(ys)) - math.pi / 2)
        lons = np.linspace(west, east, W)
        LA, LO = np.meshgrid(lats, lons, indexing="ij")
        v = self.sample(LA, LO)
        rgba = np.zeros((H, W, 4), np.uint8)
        ramp = [(0.5, (255, 255, 178)), (6, (254, 204, 92)), (10, (253, 141, 60)), (15, (240, 59, 32)), (22, (189, 0, 38)), (35, (110, 1, 107))]
        for lo_v, col in ramp:
            m = v >= lo_v; rgba[m, :3] = col; rgba[m, 3] = 200
        Image.fromarray(rgba, "RGBA").save(path, optimize=True)
        return [[south, west], [north, east]], ramp
