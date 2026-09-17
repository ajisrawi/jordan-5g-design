#!/usr/bin/env python3
"""Jordan nationwide 5G SA nominal design generator.

Produces: site grid, sector azimuth / tilt / PCI plan, fiber access + aggregation rings,
backbone, indoor venue dimensioning, link budgets, capacity and 1 Gbps compliance stats.

Run:  python tools/generate_design.py [--no-elev]
Outputs: data/design.js (for index.html), output/*.csv, output/summary.json
"""
import csv, json, math, os, sys, time, urllib.request
import numpy as np
from shapely.geometry import Point, Polygon, LineString, shape
from shapely.ops import unary_union
from shapely.prepared import prep

sys.path.insert(0, os.path.dirname(__file__))
import rf_model as rf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "output")
os.makedirs(OUT, exist_ok=True)
USE_ELEV = "--no-elev" not in sys.argv

# ----------------------------------------------------------------------------
# Projection (local equirectangular, km). <2 % scale error over Jordan: fine for nominal work.
# ----------------------------------------------------------------------------
LAT0, LON0 = 31.2, 36.2
KX, KY = 111.320 * math.cos(math.radians(LAT0)), 110.574
def xy(lat, lon): return ((lon - LON0) * KX, (lat - LAT0) * KY)
def ll(x, y): return (y / KY + LAT0, x / KX + LON0)
def poly_ll(pts): return Polygon([xy(a, b) for a, b in pts])
def ellipse(lat, lon, a_km, b_km, n=48):
    cx, cy = xy(lat, lon)
    return Polygon([(cx + a_km * math.cos(2 * math.pi * i / n), cy + b_km * math.sin(2 * math.pi * i / n)) for i in range(n)])

# ----------------------------------------------------------------------------
# Design classes
# ----------------------------------------------------------------------------
CLS = {
    "DU": dict(name="Dense urban", isd=0.375, h=25, pen=15.0, sfm=6.8, pop_km2=25000, model="uma",
               config="3-sector | n78 64T64R 3x100 MHz + n1/n3 4T4R + n28 2T4R | n258 street small cells in hotspots"),
    "U":  dict(name="Urban", isd=0.450, h=30, pen=13.0, sfm=6.8, pop_km2=10000, model="uma",
               config="3-sector | n78 64T64R 3x100 MHz + n1/n3 4T4R + n28 2T4R"),
    "SU": dict(name="Suburban", isd=0.650, h=32, pen=10.0, sfm=4.0, pop_km2=2500, model="uma",
               config="3-sector | n78 64T64R 3x100 MHz + n3 4T4R + n28 2T4R"),
    "R":  dict(name="Rural populated", isd=4.5, h=45, pen=8.0, sfm=5.5, pop_km2=150, model="rma",
               config="3-sector | n28 4T4R + n1/n3 4T4R + n78 8T8R 3x100 MHz"),
    "HW": dict(name="Highway / desert corridor", isd=7.0, h=45, pen=8.0, sfm=5.5, pop_km2=5, model="rma",
               config="2-sector along road | n28 4T4R + n3 4T4R"),
}
RANGE = {k: (v["isd"] / 1.5 if k != "HW" else 5.0) for k, v in CLS.items()}   # 3GPP hex layout: ISD = 3R_hex = 1.5 x cell range
AZ3 = (30, 150, 270)     # boresights point at neighbour sites of the hex lattice (3GPP 38.901 layout)

# ----------------------------------------------------------------------------
# Clutter / service zones.  (lat, lon) vertices or ellipses. Approximate built-up extents
# digitised from satellite imagery at nominal-planning accuracy.
# ----------------------------------------------------------------------------
Z = []
def zone(name, cluster, cls, geom): Z.append(dict(name=name, cluster=cluster, cls=cls, geom=geom))

zone("Amman core", "Amman-Zarqa Metro", "DU", poly_ll([(31.985,35.890),(31.990,35.930),(31.975,35.960),(31.950,35.965),
     (31.930,35.945),(31.935,35.910),(31.945,35.875),(31.955,35.850),(31.975,35.855)]))
zone("Amman", "Amman-Zarqa Metro", "U", poly_ll([(32.045,35.835),(32.050,35.880),(32.035,35.930),(32.010,35.970),(32.000,36.010),
     (31.970,36.030),(31.930,36.000),(31.900,35.970),(31.885,35.930),(31.895,35.890),(31.915,35.850),(31.935,35.815),
     (31.970,35.800),(32.010,35.810)]))
zone("Amman outskirts", "Amman-Zarqa Metro", "SU", poly_ll([(32.090,35.800),(32.100,35.900),(32.070,35.980),(32.030,36.040),
     (31.970,36.070),(31.900,36.050),(31.840,36.020),(31.820,35.950),(31.840,35.880),(31.870,35.820),(31.910,35.770),
     (31.970,35.750),(32.030,35.760)]))
zone("Zarqa", "Amman-Zarqa Metro", "U", ellipse(32.070, 36.090, 4.0, 5.0))
zone("Russeifa", "Amman-Zarqa Metro", "U", ellipse(32.020, 36.045, 3.2, 2.3))
zone("Zarqa outskirts", "Amman-Zarqa Metro", "SU", ellipse(32.065, 36.085, 6.5, 7.5))
zone("Baqa'a", "Amman-Zarqa Metro", "U", ellipse(32.078, 35.843, 1.4, 1.4))
zone("QAIA airport", "Amman-Zarqa Metro", "SU", ellipse(31.7226, 35.9932, 2.6, 2.6))
zone("Irbid core", "Irbid", "DU", ellipse(32.555, 35.850, 1.7, 1.4))
zone("Irbid", "Irbid", "U", ellipse(32.545, 35.855, 5.2, 4.2))
zone("Irbid outskirts", "Irbid", "SU", ellipse(32.540, 35.860, 8.0, 6.5))
zone("Ramtha", "Irbid", "U", ellipse(32.560, 36.005, 2.2, 2.2))
zone("Ramtha outskirts", "Irbid", "SU", ellipse(32.558, 36.000, 3.3, 3.3))
zone("Aqaba", "Aqaba", "U", poly_ll([(29.575,35.000),(29.580,35.030),(29.550,35.045),(29.510,35.035),(29.490,35.015),
     (29.515,35.000),(29.530,34.995),(29.548,34.978),(29.560,34.985)]))
zone("Aqaba north / ASEZA", "Aqaba", "SU", poly_ll([(29.575,34.990),(29.640,35.000),(29.640,35.040),(29.580,35.045),(29.550,35.055),(29.500,35.045),(29.485,35.020)]))
zone("Aqaba south coast", "Aqaba", "SU", poly_ll([(29.490,34.995),(29.490,35.020),(29.370,34.990),(29.370,34.962)]))
for nm, la, lo, a, b in [("Salt",32.040,35.730,2.4,1.9),("Madaba",31.717,35.795,2.4,2.4),("Mafraq",32.343,36.208,2.8,2.4),
                         ("Jerash",32.280,35.895,1.9,1.9),("Ajloun",32.333,35.752,1.5,1.5),("Karak",31.180,35.705,1.9,1.9),
                         ("Tafilah",30.838,35.605,1.4,1.8),("Ma'an",30.195,35.735,2.3,2.3),("Wadi Musa / Petra",30.322,35.480,1.5,1.5)]:
    zone(nm, nm, "U", ellipse(la, lo, a, b))
    zone(nm + " outskirts", nm, "SU", ellipse(la, lo, a + 1.3, b + 1.3))
zone("Dead Sea hotel zone", "Dead Sea", "SU", ellipse(31.715, 35.597, 0.9, 3.4))
for nm, la, lo, a, b in [("Azraq",31.880,36.830,2.2,2.2),("North Shuna",32.610,35.610,1.3,1.8),("Deir Alla",32.190,35.620,1.3,2.2),
                         ("South Shuna",31.900,35.625,1.8,1.8),("Ghor Safi",31.035,35.470,1.6,2.2),("Mutah-Mazar",31.085,35.700,1.8,2.4)]:
    zone(nm, nm, "SU", ellipse(la, lo, a, b))
zone("North-west highlands", "Rural", "R", poly_ll([(32.700,35.700),(32.710,35.850),(32.650,35.970),(32.580,36.020),(32.510,36.180),
     (32.420,36.380),(32.250,36.400),(31.950,36.250),(31.650,36.100),(31.450,35.950),(31.450,35.640),(31.780,35.620),
     (31.800,35.580),(32.200,35.580),(32.550,35.580)]))
zone("Karak-Tafilah plateau", "Rural", "R", poly_ll([(31.450,35.640),(31.450,35.950),(30.950,35.900),(30.700,35.750),(30.700,35.560),(30.950,35.580)]))

# Highways = coverage corridors AND long-haul fiber routes
ROUTES = [
    ("Desert Highway (R15) Amman-Aqaba", "national", [(31.895,35.925),(31.800,35.940),(31.720,35.960),(31.600,35.990),(31.250,36.050),
        (30.850,35.970),(30.690,35.860),(30.400,35.790),(30.200,35.780),(29.990,35.500),(29.800,35.310),(29.660,35.150),(29.580,35.030),(29.550,35.020)]),
    ("Dead Sea - Wadi Araba (R65) Amman-Aqaba", "national", [(31.9725,35.833),(31.930,35.800),(31.875,35.830),(31.830,35.700),(31.840,35.640),
        (31.770,35.605),(31.710,35.597),(31.600,35.580),(31.470,35.580),(31.260,35.530),(31.040,35.475),(30.930,35.420),(30.700,35.330),
        (30.400,35.250),(30.080,35.200),(29.800,35.090),(29.640,35.020),(29.550,35.020)]),
    ("Amman-Zarqa-Mafraq-Jaber", "national", [(31.978,35.985),(32.020,36.045),(32.065,36.090),(32.200,36.150),(32.343,36.208),(32.500,36.200)]),
    ("Mafraq-Ramtha-Irbid", "national", [(32.343,36.208),(32.450,36.080),(32.560,36.005),(32.550,35.860)]),
    ("Irbid-Jerash-Amman (R35)", "national", [(32.550,35.860),(32.480,35.880),(32.280,35.895),(32.160,35.870),(32.080,35.860),(32.025,35.885)]),
    ("King's Highway Madaba-Karak-Tafilah-Petra-Ma'an", "regional", [(31.895,35.925),(31.800,35.850),(31.717,35.795),(31.500,35.780),(31.400,35.760),
        (31.180,35.705),(31.085,35.700),(30.838,35.605),(30.520,35.560),(30.322,35.480),(30.250,35.600),(30.195,35.735)]),
    ("Jordan Valley (R65 north)", "regional", [(32.550,35.860),(32.600,35.700),(32.610,35.610),(32.440,35.600),(32.190,35.620),(31.950,35.600),(31.900,35.625),(31.840,35.640)]),
    ("Amman-Salt-Deir Alla", "regional", [(31.9725,35.833),(32.040,35.730),(32.110,35.680),(32.190,35.620)]),
    ("Irbid-Ajloun-Jerash", "regional", [(32.550,35.860),(32.440,35.780),(32.333,35.752),(32.280,35.895)]),
    ("Karak-Qatraneh", "regional", [(31.180,35.705),(31.220,35.880),(31.250,36.050)]),
    ("Tafilah-Jurf", "regional", [(30.838,35.605),(30.760,35.740),(30.690,35.860)]),
    ("Amman-Azraq (R40)", "regional", [(31.978,35.985),(31.870,36.005),(31.810,36.100),(31.730,36.460),(31.880,36.830)]),
    ("Zarqa-Azraq-Safawi", "regional", [(32.065,36.090),(31.980,36.400),(31.880,36.830),(32.200,37.130)]),
    ("Mafraq-Safawi-Ruwaished (R10)", "regional", [(32.343,36.208),(32.300,36.600),(32.200,37.130),(32.380,37.700),(32.500,38.200),(32.800,38.800)]),
    ("Quweira-Wadi Rum", "regional", [(29.800,35.310),(29.690,35.400),(29.575,35.420)]),
]

# Core / transport PoPs
POPS = [
    dict(id="DC1", name="Amman West DC (5GC CP + UPF + IMS)", role="core", lat=31.9725, lon=35.8330, cluster="Amman-Zarqa Metro"),
    dict(id="DC2", name="Amman East DC (5GC CP geo-redundant + UPF)", role="core", lat=31.9780, lon=35.9850, cluster="Amman-Zarqa Metro"),
    dict(id="POP-AMM-C", name="Amman Centre PoP (edge UPF/MEC)", role="edge", lat=31.9570, lon=35.9120, cluster="Amman-Zarqa Metro"),
    dict(id="POP-AMM-N", name="Amman North PoP", role="agg", lat=32.0250, lon=35.8850, cluster="Amman-Zarqa Metro"),
    dict(id="POP-AMM-S", name="Amman South PoP", role="agg", lat=31.8950, lon=35.9250, cluster="Amman-Zarqa Metro"),
    dict(id="POP-ZRQ", name="Zarqa PoP (edge UPF)", role="edge", lat=32.0650, lon=36.0900, cluster="Amman-Zarqa Metro"),
    dict(id="POP-IRB", name="Irbid regional DC (edge UPF/MEC, DR for UDM/UDR)", role="edge", lat=32.5500, lon=35.8600, cluster="Irbid"),
    dict(id="POP-AQB", name="Aqaba regional DC (edge UPF, international gateway / cable landing)", role="edge", lat=29.5500, lon=35.0200, cluster="Aqaba"),
]
TOWN_POP = {"Salt":(32.040,35.730),"Madaba":(31.717,35.795),"Mafraq":(32.343,36.208),"Jerash":(32.280,35.895),"Ajloun":(32.333,35.752),
            "Karak":(31.180,35.705),"Tafilah":(30.838,35.605),"Ma'an":(30.195,35.735),"Wadi Musa / Petra":(30.322,35.480),
            "Dead Sea":(31.710,35.597),"Azraq":(31.880,36.830),"North Shuna":(32.610,35.610),"Deir Alla":(32.190,35.620),
            "South Shuna":(31.900,35.625),"Ghor Safi":(31.040,35.475),"Mutah-Mazar":(31.085,35.700)}
for k, (la, lo) in TOWN_POP.items():
    POPS.append(dict(id="POP-" + k[:3].upper().replace("'", ""), name=k + " PoP", role="agg", lat=la, lon=lo, cluster=k))

# Indoor venues (coordinates approximate - confirm at site survey). area = served floor area m2
VENUES = [
 # name, type, lat, lon, area_m2, rooms
 ("City Mall","mall",31.9803,35.8368,160000,0),("Mecca Mall","mall",31.9769,35.8433,190000,0),("Taj Lifestyle Center","mall",31.9408,35.8881,150000,0),
 ("Abdali Mall","mall",31.9650,35.9075,227000,0),("The Boulevard - Abdali","mixed-use",31.9637,35.9085,100000,0),("Galleria Mall","mall",31.9557,35.8643,60000,0),
 ("Al Baraka Mall","mall",31.9570,35.8610,45000,0),("Istiklal Mall","mall",31.9760,35.9230,60000,0),
 ("Four Seasons Amman","hotel",31.9583,35.8787,45000,192),("The St. Regis Amman","hotel",31.9560,35.8870,60000,260),("The Ritz-Carlton Amman","hotel",31.9570,35.8760,55000,228),
 ("Fairmont Amman","hotel",31.9560,35.8800,65000,317),("W Amman","hotel",31.9640,35.9080,50000,280),("Amman Rotana","hotel",31.9645,35.9095,70000,412),
 ("Grand Hyatt Amman","hotel",31.9520,35.9050,60000,311),("InterContinental Jordan","hotel",31.9525,35.9105,70000,440),("Amman Marriott","hotel",31.9710,35.9050,50000,292),
 ("Kempinski Amman","hotel",31.9690,35.8990,45000,278),("Le Royal Amman","hotel",31.9535,35.9085,80000,283),("Sheraton Amman","hotel",31.9575,35.8830,50000,267),
 ("Landmark Amman","hotel",31.9660,35.9040,45000,260),("Crowne Plaza Amman","hotel",31.9600,35.8690,45000,279),
 ("Queen Alia Intl Airport terminal","airport",31.7226,35.9932,103000,0),("King Hussein Business Park","campus",31.9725,35.8330,120000,0),
 ("University of Jordan","campus",32.0160,35.8700,250000,0),("Jordan University Hospital","hospital",32.0090,35.8740,95000,0),
 ("King Hussein Cancer Center","hospital",32.0040,35.8760,110000,0),("Al-Bashir Hospital","hospital",31.9390,35.9430,120000,0),
 ("Amman Intl Stadium / Al-Hussein Youth City","stadium",31.9850,35.9010,40000,0),
 ("Kempinski Ishtar Dead Sea","hotel",31.7180,35.5880,70000,345),("Movenpick Dead Sea","hotel",31.7150,35.5885,65000,346),("Dead Sea Marriott","hotel",31.7120,35.5890,50000,250),
 ("Hilton Dead Sea","hotel",31.7080,35.5890,55000,285),("Crowne Plaza Dead Sea","hotel",31.7000,35.5885,70000,420),("King Hussein Bin Talal Convention Centre","convention",31.7095,35.5900,25000,0),
 ("Ayla Oasis / Hyatt Regency","resort",29.5480,34.9880,90000,286),("Al Manara - Saraya Aqaba","hotel",29.5360,34.9990,45000,207),("Kempinski Aqaba","hotel",29.5330,35.0000,40000,200),
 ("InterContinental Aqaba","hotel",29.5350,34.9975,50000,255),("Movenpick Aqaba","hotel",29.5310,35.0010,50000,296),("Tala Bay resort cluster","resort",29.4080,34.9780,120000,900),
 ("Aqaba Gateway / City Center","mall",29.5290,35.0020,40000,0),("King Hussein Intl Airport (Aqaba)","airport",29.6116,35.0181,15000,0),
 ("Movenpick Petra","hotel",30.3245,35.4690,25000,183),("Petra Marriott","hotel",30.3130,35.4900,18000,100),("Petra Visitor Centre","venue",30.3240,35.4680,8000,0),
 ("Arabella Mall Irbid","mall",32.5385,35.8470,50000,0),("Irbid City Centre","mall",32.5340,35.8640,80000,0),("Yarmouk University","campus",32.5365,35.8540,120000,0),
 ("JUST campus","campus",32.4950,35.9890,200000,0),("King Abdullah University Hospital","hospital",32.4985,35.9920,95000,0),
]

GOV_POP = {"Amman":4744700,"Irbid":2094200,"Zarqa":1612800,"Mafraq":651100,"Balqa":581000,"Karak":374500,"Jerash":280000,
           "Madaba":223900,"Aqaba":232800,"Ajloun":208500,"Ma'an":187600,"Tafilah":113900}   # DoS end-2023 estimates (rounded)

# ----------------------------------------------------------------------------
# Boundaries
# ----------------------------------------------------------------------------
adm0 = json.load(open(os.path.join(RAW, "JOR_ADM0.geojson"), encoding="utf-8"))
adm1 = json.load(open(os.path.join(RAW, "JOR_ADM1.geojson"), encoding="utf-8"))
def geo_to_xy(g):
    s = shape(g)
    from shapely.ops import transform
    return transform(lambda lon, lat, z=None: ((lon - LON0) * KX, (lat - LAT0) * KY), s)
JOR = geo_to_xy(adm0["features"][0]["geometry"]).buffer(0)
JOR_IN = JOR.buffer(-0.25)
JOR_P = prep(JOR)
GOVS = [(f["properties"]["shapeName"], prep(geo_to_xy(f["geometry"]).buffer(0))) for f in adm1["features"]]
def gov_of(x, y):
    p = Point(x, y)
    for n, g in GOVS:
        if g.contains(p): return n
    return "n/a"

# ----------------------------------------------------------------------------
# 1. Site grid
# ----------------------------------------------------------------------------
PRI = ["DU", "U", "SU", "R"]
eff, taken = {}, None
for c in PRI:
    u = unary_union([z["geom"] for z in Z if z["cls"] == c]).intersection(JOR_IN if c != "R" else JOR.buffer(-1.5))
    eff[c] = u if taken is None else u.difference(taken)
    taken = u if taken is None else taken.union(u)
CITY = prep(unary_union([eff["DU"], eff["U"], eff["SU"]]))

def hexgrid(geom, isd):
    minx, miny, maxx, maxy = geom.bounds
    dy = isd * math.sqrt(3) / 2
    pg = prep(geom); pts = []
    j0, j1 = math.floor(miny / dy), math.ceil(maxy / dy)
    for j in range(j0, j1 + 1):
        off = (isd / 2) if j % 2 else 0.0
        i0, i1 = math.floor((minx - off) / isd), math.ceil((maxx - off) / isd)
        for i in range(i0, i1 + 1):
            x, y = i * isd + off, j * dy
            if pg.contains(Point(x, y)): pts.append((x, y))
    return pts

class Hash:
    def __init__(s, cell): s.c, s.d = cell, {}
    def add(s, x, y, v): s.d.setdefault((int(x // s.c), int(y // s.c)), []).append((x, y, v))
    def near(s, x, y, r):
        n = int(r // s.c) + 1; cx, cy = int(x // s.c), int(y // s.c)
        for i in range(cx - n, cx + n + 1):
            for j in range(cy - n, cy + n + 1):
                for (px, py, v) in s.d.get((i, j), ()):
                    if (px - x) ** 2 + (py - y) ** 2 <= r * r: yield (px, py, v)

sites, H = [], Hash(1.0)
def zone_of(x, y, c):
    p = Point(x, y)
    for z in Z:
        if z["cls"] == c and z["geom"].contains(p): return z
    return None
for c in PRI:
    for (x, y) in hexgrid(eff[c], CLS[c]["isd"]):
        if any(True for _ in H.near(x, y, 0.55 * CLS[c]["isd"])): continue
        z = zone_of(x, y, c)
        s = dict(x=x, y=y, cls=c, zone=z["name"], cluster=z["cluster"], az=list(AZ3))
        sites.append(s); H.add(x, y, len(sites) - 1)

def bearing(p, q): return (math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])) + 360) % 360
for (rname, tier, pts) in ROUTES:
    line = LineString([xy(a, b) for a, b in pts]); L = line.length; d = CLS["HW"]["isd"] / 2
    while d < L:
        p = line.interpolate(d); x, y = p.x, p.y
        if JOR_P.contains(p) and not CITY.contains(p) and not any(True for _ in H.near(x, y, 3.2)):
            a = line.interpolate(max(d - 0.5, 0)); b = line.interpolate(min(d + 0.5, L))
            fwd = round(bearing((a.x, a.y), (b.x, b.y)))
            s = dict(x=x, y=y, cls="HW", zone=rname, cluster="Highway", az=[fwd, (fwd + 180) % 360])
            sites.append(s); H.add(x, y, len(sites) - 1)
        d += CLS["HW"]["isd"]

for s in sites:
    s["lat"], s["lon"] = ll(s["x"], s["y"])
    s["h"] = CLS[s["cls"]]["h"]

# ----------------------------------------------------------------------------
# 1a. Terrain (Copernicus GLO-90 DEM): drop sites on water, move each nominal onto the local high point
# ----------------------------------------------------------------------------
from terrain import Terrain
from buildings import BuildingHeights
DEM = Terrain(os.path.join(RAW, "dem"))
BH = BuildingHeights(os.path.join(RAW, "GHS_BUILT_H_ANBH_E2018_GLOBE_R2023A_54009_100_V1_0_R6_C22.tif"))
elev_ok = True
SEARCH = {"DU": 0.20, "U": 0.20, "SU": 0.20, "R": 0.12, "HW": 0.05}      # search-ring radius as a fraction of ISD
n0 = len(sites)
sites = [s for s in sites if float(DEM.sample(*ll(s["x"], s["y"]))) > -418]   # Dead Sea surface is ~ -430 m
print("dropped", n0 - len(sites), "sites on Dead Sea water")
moved, gain = 0, []
for s in sites:
    r = SEARCH[s["cls"]] * CLS[s["cls"]]["isd"]
    offs = [(i * r / 2, j * r / 2) for i in range(-2, 3) for j in range(-2, 3) if i * i + j * j <= 4]
    pts = [ll(s["x"] + dx, s["y"] + dy) for dx, dy in offs]
    la, lo = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    z = DEM.sample(la, lo); score = z + BH.sample(la, lo)
    for k, (dx, dy) in enumerate(offs):
        if z[k] < -418 or not JOR_P.contains(Point(s["x"] + dx, s["y"] + dy)): score[k] = -9999
    k, b = int(np.argmax(score)), offs.index((0.0, 0.0))
    if score[k] - score[b] >= 4:
        s["x"] += offs[k][0]; s["y"] += offs[k][1]; moved += 1; gain.append(float(score[k] - score[b]))
    s["lat"], s["lon"] = ll(s["x"], s["y"])
    s["elev"] = int(round(float(DEM.sample(s["lat"], s["lon"]))))
print(f"moved {moved} sites to local high points, mean gain {np.mean(gain):.1f} m")

# ----------------------------------------------------------------------------
# 1b. Building heights (GHSL GHS-BUILT-H 2018, 100 m ANBH): rooftop clearance, site type, pruning of empty land
# ----------------------------------------------------------------------------
ROOF_CLEARANCE, H_MAX = 8.0, 60
route_union = unary_union([LineString([xy(a, b) for a, b in pts]) for _, _, pts in ROUTES])
kept, pruned = [], 0
for s in sites:
    c = s["cls"]
    mean, mx, frac = BH.stats(s["lat"], s["lon"], 250)
    _, _, frac_cell = BH.stats(s["lat"], s["lon"], max(300, RANGE[c] * 1000)) if c in ("U", "SU") else (0, 0, 1)
    if c in ("U", "SU") and frac_cell < 0.03 and route_union.distance(Point(s["x"], s["y"])) > 0.5:
        pruned += 1; continue                      # hand-drawn zone but no buildings in the whole cell: not built in phase 1
    s["bldg"], s["bldg_max"], s["built"] = round(mean, 1), round(mx, 1), round(frac, 2)
    if c in ("DU", "U", "SU"):
        if mx >= 9:
            s["stype"] = "Rooftop"; s["h"] = int(min(H_MAX, max(CLS[c]["h"], math.ceil(mx + ROOF_CLEARANCE))))
        else:
            s["stype"] = "Monopole / greenfield"
    else:
        s["stype"] = "Lattice tower"
    kept.append(s)
sites = kept
print("pruned", pruned, "sites with no built-up area in their cell;", len(sites), "remain")
bh_bounds, bh_ramp = BH.overlay_png(os.path.join(ROOT, "data", "bldg_height.png"), 29.15, 34.9, 33.1, 39.35, 120)

# ----------------------------------------------------------------------------
# 3. Sectors: border handling, tilt, PCI
# ----------------------------------------------------------------------------
V3 = dict(n78=6.0, mid=5.5, low=9.0)       # vertical HPBW of SSB/common beam per layer, deg
def edge_pt(s, az, frac=1.0):
    r = RANGE[s["cls"]] * frac
    return ll(s["x"] + r * math.sin(math.radians(az)), s["y"] + r * math.cos(math.radians(az)))
for s in sites:
    c = s["cls"]
    secs = []
    for az in s["az"]:
        la, lo = edge_pt(s, az, 0.7 if c in ("R", "HW") else max(0.7, 2.0 / RANGE[c]))   # city sectors: flag if boresight crosses a border/sea within 2 km
        outside = not JOR_P.contains(Point(*xy(la, lo)))
        if outside and c in ("R", "HW"): continue                    # do not radiate across the border / sea from rural sites
        fp = [ll(s["x"] + RANGE[c] * f * math.sin(math.radians(az + da)), s["y"] + RANGE[c] * f * math.cos(math.radians(az + da)))
              for f in (0.5, 0.75, 1.0) for da in (-30, 0, 30)]
        zf = DEM.sample([q[0] for q in fp], [q[1] for q in fp]); zf = zf[zf > -418]
        dz = float(s["elev"] - zf.mean()) if zf.size else 0.0          # site ground minus mean ground of the sector footprint
        geo = math.degrees(math.atan2(s["h"] - 1.5 + dz, RANGE[c] * 1000))
        flat = math.degrees(math.atan2(s["h"] - 1.5, RANGE[c] * 1000))
        def tot(v): return int(round(min(14, max(2, geo + v / 2 + (2 if outside else 0)))))
        t78, tmid, tlow = tot(V3["n78"]), tot(V3["mid"]), tot(V3["low"])
        mech = max(0, max(t78 - 9, tlow - 12, tmid - 12))            # AAU digital tilt <= 9 deg, RET range 2-12 deg
        secs.append(dict(az=az, mech=mech, t78=t78, e78=t78 - mech, retM=max(2, tmid - mech), retL=max(2, tlow - mech),
                         flat=round(flat + 3, 1), border=outside, dz=round(dz)))
    s["sec"] = secs
sites = [s for s in sites if s["sec"]]

# PCI: greedy group colouring, 336 groups x 3
order = sorted(range(len(sites)), key=lambda i: (PRI + ["HW"]).index(sites[i]["cls"]))
H2 = Hash(2.0)
for i, s in enumerate(sites): H2.add(s["x"], s["y"], i)
for i in order:
    s = sites[i]; r = max(6 * CLS[s["cls"]]["isd"], 2.5)
    used = {sites[v].get("grp") for _, _, v in H2.near(s["x"], s["y"], r)}
    s["grp"] = next(g for g in range(336) if g not in used) if len(used - {None}) < 336 else i % 336
    for k, se in enumerate(s["sec"]): se["pci"] = 3 * s["grp"] + k

# IDs + governorate
PFX = {"Amman-Zarqa Metro": "AMM", "Irbid": "IRB", "Aqaba": "AQB", "Highway": "HWY", "Rural": "RUR"}
cnt = {}
for s in sites:
    s["gov"] = gov_of(s["x"], s["y"])
    p = PFX.get(s["cluster"], s["cluster"][:3].upper().replace("'", ""))
    cnt[p] = cnt.get(p, 0) + 1
    s["id"] = f"{p}-{s['cls']}-{cnt[p]:04d}"

# ----------------------------------------------------------------------------
# 4. Transport: hubs (C-RAN / pre-agg), access rings, aggregation rings, MW
# ----------------------------------------------------------------------------
ROUTE_F = 1.35       # street-route factor on straight-line distances
rng = np.random.default_rng(7)
def dist(a, b): return math.hypot(a[0] - b[0], a[1] - b[1])
def kmeans(P, k):
    C = P[rng.choice(len(P), k, replace=False)]
    for _ in range(25):
        lab = np.argmin(((P[:, None, :] - C[None]) ** 2).sum(-1), 1)
        for j in range(k):
            if (lab == j).any(): C[j] = P[lab == j].mean(0)
    return lab, C
def ring_path(center, members, pos):
    """members sorted by angle already; go out on first half, come back on second half."""
    h = len(members) // 2 + len(members) % 2
    a = sorted(members[:h], key=lambda m: dist(pos(m), center))
    b = sorted(members[h:], key=lambda m: -dist(pos(m), center))
    return a + b
def chunk_by_angle(center, members, pos, n):
    ms = sorted(members, key=lambda m: math.atan2(pos(m)[1] - center[1], pos(m)[0] - center[0]))
    k = math.ceil(len(ms) / n) if ms else 0
    size = math.ceil(len(ms) / k) if k else 0
    return [ms[i:i + size] for i in range(0, len(ms), size)] if size else []

hubs, arings, grings = [], [], []
clusters = sorted({s["cluster"] for s in sites} - {"Highway", "Rural"})
for cl in clusters:
    idx = [i for i, s in enumerate(sites) if s["cluster"] == cl]
    P = np.array([[sites[i]["x"], sites[i]["y"]] for i in idx])
    k = max(1, math.ceil(len(idx) / 40))
    lab, C = kmeans(P, k) if k > 1 else (np.zeros(len(idx), int), P.mean(0, keepdims=True))
    cl_hubs = []
    for j in range(k):
        mem = [idx[m] for m in np.where(lab == j)[0]]
        if not mem: continue
        hub_site = min(mem, key=lambda i: dist((sites[i]["x"], sites[i]["y"]), C[j]))
        hid = f"HUB-{PFX.get(cl, cl[:3].upper())}-{len(cl_hubs) + 1:02d}".replace("'", "")
        hs = sites[hub_site]; hs["is_hub"] = True
        cran = sum(1 for i in mem if sites[i]["cls"] in ("DU", "U")) > len(mem) / 2
        hub = dict(id=hid, site=hs["id"], x=hs["x"], y=hs["y"], lat=hs["lat"], lon=hs["lon"], cluster=cl, n=len(mem),
                   type="C-RAN DU hotel + pre-aggregation" if cran else "Pre-aggregation (D-RAN sites)")
        hubs.append(hub); cl_hubs.append(hub)
        others = [i for i in mem if i != hub_site]
        for r_i, ch in enumerate(chunk_by_angle((hs["x"], hs["y"]), others, lambda i: (sites[i]["x"], sites[i]["y"]), 7)):
            path = ring_path((hs["x"], hs["y"]), ch, lambda i: (sites[i]["x"], sites[i]["y"]))
            nodes = [hub_site] + path + [hub_site]
            km = sum(dist((sites[a]["x"], sites[a]["y"]), (sites[b]["x"], sites[b]["y"])) for a, b in zip(nodes, nodes[1:])) * ROUTE_F
            rid = f"{hid}-R{r_i + 1:02d}"
            for i in nodes: sites[i]["hub"], sites[i]["ring"] = hid, sites[i].get("ring") or rid
            arings.append(dict(id=rid, hub=hid, km=round(km, 2), n=len(path), cran=cran,
                               path=[[round(sites[i]["lat"], 5), round(sites[i]["lon"], 5)] for i in nodes]))
        hs["hub"] = hid; hs["ring"] = hs.get("ring") or hid
    # aggregation rings: hubs -> nearest PoP of the cluster
    pops = [p for p in POPS if p["cluster"] == cl and p["role"] != "edge-only"]
    if not pops:
        continue
    byp = {}
    for hb in cl_hubs:
        p = min(pops, key=lambda p: dist(xy(p["lat"], p["lon"]), (hb["x"], hb["y"])))
        hb["pop"] = p["id"]; byp.setdefault(p["id"], []).append(hb)
    for pid, hl in byp.items():
        p = next(q for q in POPS if q["id"] == pid); pc = xy(p["lat"], p["lon"])
        for r_i, ch in enumerate(chunk_by_angle(pc, hl, lambda h: (h["x"], h["y"]), 5)):
            path = ring_path(pc, ch, lambda h: (h["x"], h["y"]))
            pts = [pc] + [(h["x"], h["y"]) for h in path] + [pc]
            km = sum(dist(a, b) for a, b in zip(pts, pts[1:])) * ROUTE_F
            grings.append(dict(id=f"AGG-{pid}-{r_i + 1:02d}", pop=pid, km=round(km, 1), n=len(path),
                               path=[[round(v, 5) for v in ll(*q)] for q in pts]))

# Rural / highway backhaul
route_lines = [LineString([xy(a, b) for a, b in pts]) for _, _, pts in ROUTES]
mw_links = []
fibered = Hash(3.0)
for i, s in enumerate(sites):
    if s["cls"] in ("DU", "U", "SU"): s["bh"] = "Fiber ring"; fibered.add(s["x"], s["y"], i)
for i, s in enumerate(sites):
    if s["cls"] in ("R", "HW"):
        d = min(l.distance(Point(s["x"], s["y"])) for l in route_lines)
        if d <= 2.0:
            s["bh"] = "Fiber (backbone add/drop spur)"; s["spur_km"] = round(d * ROUTE_F + 0.3, 2); fibered.add(s["x"], s["y"], i)
for i, s in enumerate(sites):
    if "bh" not in s:
        near = sorted(fibered.near(s["x"], s["y"], 25.0), key=lambda t: dist((t[0], t[1]), (s["x"], s["y"])))
        if near:
            t = near[0]; d = dist((t[0], t[1]), (s["x"], s["y"]))
            s["bh"] = "Microwave E-band 10G" if d <= 6 else "Microwave 6-18 GHz XPIC 2x1G-4x1G"
            s["mw_to"] = sites[t[2]]["id"]; s["mw_km"] = round(d, 1)
            mw_links.append([[round(s["lat"], 5), round(s["lon"], 5)], [round(sites[t[2]]["lat"], 5), round(sites[t[2]]["lon"], 5)]])
        else:
            s["bh"] = "Multi-hop microwave / LEO-GEO satellite backhaul"

backbone = []
for (n, tier, pts) in ROUTES:
    km = LineString([xy(a, b) for a, b in pts]).length * 1.15
    backbone.append(dict(name=n, tier=tier, km=round(km), path=[[a, b] for a, b in pts]))
metro_core = dict(name="Amman metro core ring (DC1 - North - Zarqa - DC2 - South - DC1, Centre PoP dual-homed)", tier="metro",
                  path=[[31.9725,35.8330],[32.0250,35.8850],[32.0650,36.0900],[31.9780,35.9850],[31.8950,35.9250],[31.9725,35.8330]])
metro_core["km"] = round(LineString([xy(a, b) for a, b in metro_core["path"]]).length * ROUTE_F)
metro_spurs = [[[31.9570,35.9120],[31.9725,35.8330]], [[31.9570,35.9120],[31.9780,35.9850]]]

# ----------------------------------------------------------------------------
# 5. Link budgets, capacity, compliance
# ----------------------------------------------------------------------------
R78, R28 = rf.RADIO["n78_64T"], rf.RADIO["n28_4T"]
LB = []
for bw in (100, 200, 300):
    req = rf.sinr_for_tp(1000, bw)
    for c in ("DU", "U", "SU"):
        k = CLS[c]; eirp = rf.eirp_per_sc(R78, "traffic", bw); n = rf.noise_per_sc(30, rf.UE_NF); im = 3.0
        if req is None: LB.append(dict(layer=f"n78 {bw} MHz DL 1 Gbps", cls=c, feasible=False)); continue
        mapl = eirp - n - req - im - k["sfm"] - k["pen"]
        d = rf.range_for_mapl(mapl, "uma", 3.5, k["h"])
        LB.append(dict(layer=f"n78 {bw} MHz DL 1 Gbps", cls=c, eirp_sc=round(eirp, 1), noise_sc=round(n, 1), sinr_req=round(req, 1),
                       im=im, sfm=k["sfm"], pen=k["pen"], mapl=round(mapl, 1), range_m=round(d), design_range_m=round(RANGE[c] * 1000),
                       margin_db=round(float(mapl - rf.pl_uma(np.array([RANGE[c] * 1000]), 3.5, k["h"])[0]), 1)))
# UL: n78 (PC2 26 dBm, full band) and n3 FDD fallback (PC3 23 dBm, 20 MHz)
for c in ("DU", "U", "SU"):
    k = CLS[c]
    psd = 26 - 10 * math.log10(3276); n = rf.noise_per_sc(30, rf.GNB_NF)
    se = 20e6 / (rf.RE_PER_S_100MHZ * rf.TDD_UL * (1 - rf.OH_UL)); sinr = 10 * math.log10(2 ** (se / rf.IMPL) - 1)
    mapl = psd + 24 - n - sinr - 2 - k["sfm"] - k["pen"]
    LB.append(dict(layer="n78 UL 20 Mbps (PC2 UE, one 100 MHz carrier)", cls=c, eirp_sc=round(psd, 1), noise_sc=round(n, 1), sinr_req=round(sinr, 1), im=2, sfm=k["sfm"],
                   pen=k["pen"], mapl=round(mapl, 1), range_m=round(rf.range_for_mapl(mapl, "uma", 3.5, k["h"])), design_range_m=round(RANGE[c] * 1000)))
    psd = 23 - 10 * math.log10(1272); n = rf.noise_per_sc(15, 2.5)
    se = 10e6 / (1272 * 14000 * (1 - rf.OH_UL)); sinr = 10 * math.log10(2 ** (se / rf.IMPL) - 1)
    mapl = psd + 17.5 - n - sinr - 2 - k["sfm"] - (k["pen"] - 3)
    LB.append(dict(layer="n3 UL 10 Mbps (PC3 UE, 20 MHz FDD)", cls=c, eirp_sc=round(psd, 1), noise_sc=round(n, 1), sinr_req=round(sinr, 1), im=2, sfm=k["sfm"],
                   pen=k["pen"] - 3, mapl=round(mapl, 1), range_m=round(rf.range_for_mapl(mapl, "uma", 1.8, k["h"])), design_range_m=round(RANGE[c] * 1000)))
for c, tgt in (("R", 10), ("HW", 10)):
    k = CLS[c]; eirp = rf.eirp_per_sc(R28); n = rf.noise_per_sc(15, rf.UE_NF)
    se = tgt * 1e6 / (624 * 14000 * (1 - rf.OH_DL)); sinr = 10 * math.log10(2 ** (se / rf.IMPL) - 1)
    mapl = eirp - n - sinr - 2 - k["sfm"] - k["pen"]
    LB.append(dict(layer=f"n28 10 MHz DL {tgt} Mbps edge (in-car)", cls=c, eirp_sc=round(eirp, 1), noise_sc=round(n, 1), sinr_req=round(sinr, 1), im=2,
                   sfm=k["sfm"], pen=k["pen"], mapl=round(mapl, 1), range_m=round(rf.range_for_mapl(mapl, "rma", 0.7, k["h"])), design_range_m=round(RANGE[c] * 1000)))

# Capacity
SUB_PEN, GB_MONTH, BH_SHARE, CELL_SE = 0.40, 80, 0.10, 10.0
bh_mbps = GB_MONTH * 8e3 / 30 * BH_SHARE / 3600
CAP = []
area = {c: eff[c].area for c in PRI}
nsite = {c: sum(1 for s in sites if s["cls"] == c) for c in CLS}
for c in ("DU", "U", "SU", "R"):
    k = CLS[c]; pop = area[c] * k["pop_km2"]; subs = pop * SUB_PEN
    nsec = sum(len(s["sec"]) for s in sites if s["cls"] == c)
    per_sec = subs / max(nsec, 1); offered = per_sec * bh_mbps
    row = dict(cls=c, area_km2=round(area[c]), pop=round(pop), subs=round(subs), sites=nsite[c], sectors=nsec, subs_per_sector=round(per_sec),
               offered_mbps=round(offered))
    for bw in (100, 200, 300):
        capm = (bw * rf.TDD_DL * CELL_SE) if c != "R" else (45 * 2.5 + bw * rf.TDD_DL * 4.0)   # rural: FDD 45 MHz @2.5 + n78 8T8R @4 b/s/Hz
        row[f"load_{bw}"] = round(100 * offered / capm, 1)
    CAP.append(row)

# Terrain-aware prediction rasters: UMa/RMa median path loss + single knife-edge terrain diffraction (ITU-R P.526)
# on the Copernicus DEM profile, true 3-D antenna geometry (site ground + antenna height vs pixel ground), sector patterns and tilts.
import base64, io, shapely
from PIL import Image
def merc(la): return math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
def predict(bounds, px_m, slist, radio, fc, rad_km_of, bw, tilt_of, K=8):
    S, W, N, E = bounds
    Wpx = int((E - W) * KX * 1000 / px_m); Hpx = int(Wpx * (merc(N) - merc(S)) / math.radians(E - W))
    lats = np.degrees(2 * np.arctan(np.exp(np.linspace(merc(N), merc(S), Hpx))) - math.pi / 2); lons = np.linspace(W, E, Wpx)
    gx, gy = (lons - LON0) * KX, (lats - LAT0) * KY
    LA, LO = np.meshgrid(lats, lons, indexing="ij"); ZG = DEM.sample(LA, LO).astype(np.float32)
    best = np.full((Hpx, Wpx), -300.0, np.float32); tot = np.zeros((Hpx, Wpx)); lam = 0.3 / fc
    eirp = rf.eirp_per_sc(radio, "traffic", bw)
    for s in slist:
        rad = rad_km_of(s)
        c0, c1 = np.searchsorted(gx, [s["x"] - rad, s["x"] + rad]); r0, r1 = np.searchsorted(-gy, [-(s["y"] + rad), -(s["y"] - rad)])
        if c1 <= c0 or r1 <= r0: continue
        dx = gx[None, c0:c1] - s["x"]; dy = gy[r0:r1, None] - s["y"]
        d = np.maximum(np.hypot(dx, dy) * 1000, 10.0)
        za = s["elev"] + s["h"]; zb = ZG[r0:r1, c0:c1] + 1.5
        la_w, lo_w = LA[r0:r1, c0:c1], LO[r0:r1, c0:c1]
        nu = np.full(d.shape, -5.0)
        for tt in np.linspace(0.1, 0.9, K):
            zt = DEM.sample(s["lat"] + (la_w - s["lat"]) * tt, s["lon"] + (lo_w - s["lon"]) * tt) + (tt * d) * ((1 - tt) * d) / (2 * 8.5e6)
            nu = np.maximum(nu, (zt - (za + (zb - za) * tt)) * np.sqrt(2.0 / (lam * d * tt * (1 - tt))))
        J = np.where(nu > -0.78, 6.9 + 20 * np.log10(np.sqrt((nu - 0.1) ** 2 + 1) + nu - 0.1), 0.0); J = np.minimum(J, 30.0)
        dh = np.maximum(za - zb, 1.0)
        pl = (rf.pl_uma(d, fc, dh + 1.5) if s["cls"] in ("DU", "U", "SU") else rf.pl_rma(d, fc, s["h"])) + J
        th = np.degrees(np.arctan2(za - zb, d)); azp = (np.degrees(np.arctan2(dx, dy)) + 360) % 360
        for se in s["sec"]:
            da = np.abs((azp - se["az"] + 180) % 360 - 180)
            pw = eirp - pl + rf.pattern_db(da, th, tilt_of(se), radio)
            best[r0:r1, c0:c1] = np.maximum(best[r0:r1, c0:c1], pw); tot[r0:r1, c0:c1] += 10 ** (pw / 10)
    inter = 10 * np.log10(np.maximum(tot - 10 ** (best.astype(np.float64) / 10), 1e-30))
    X, Y = np.meshgrid(gx, gy)
    return dict(best=best, inter=inter.astype(np.float32), X=X, Y=Y, bounds=[[S, W], [N, E]])
def encode(r, floor_dbm):
    inj = shapely.contains_xy(JOR, r["X"], r["Y"])
    rgba = np.zeros(r["best"].shape + (4,), np.uint8)
    rgba[..., 0] = np.clip((r["best"] + 150) * 2, 0, 255); rgba[..., 1] = np.clip((r["inter"] + 150) * 2, 0, 255)
    for i, c in enumerate(("DU", "U", "SU")):                       # blue channel = service class of the pixel (live statistics in the map)
        rgba[..., 2][shapely.contains_xy(eff[c], r["X"], r["Y"])] = i + 1
    rgba[..., 3] = np.where(inj & (r["best"] > floor_dbm), 255, 0)
    buf = io.BytesIO(); Image.fromarray(rgba, "RGBA").save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

t0 = time.time(); RASTERS = []; acc = {c: [] for c in ("DU", "U", "SU")}
city = [s for s in sites if s["cls"] in ("DU", "U", "SU")]
for cl in sorted({s["cluster"] for s in city}):
    ss = [s for s in city if s["cluster"] == cl]
    S_, N_ = min(s["lat"] for s in ss) - 0.012, max(s["lat"] for s in ss) + 0.012
    W_, E_ = min(s["lon"] for s in ss) - 0.014, max(s["lon"] for s in ss) + 0.014
    cx0, cy0 = xy(S_, W_); cx1, cy1 = xy(N_, E_)
    near = [s for s in city if cx0 - 2.5 < s["x"] < cx1 + 2.5 and cy0 - 2.5 < s["y"] < cy1 + 2.5]
    r = predict((S_, W_, N_, E_), 50, near, R78, 3.5, lambda s: 2.2 if s["cls"] == "SU" else 1.6, 300, lambda se: se["t78"])
    RASTERS.append(dict(name=cl, layer="n78", bounds=r["bounds"], png=encode(r, -128)))
    for c in acc:
        m = shapely.contains_xy(eff[c], r["X"], r["Y"]) & (r["best"] > -200)
        if m.any(): acc[c].append(np.stack([r["best"][m], r["inter"][m]]))
    print(f"  raster {cl}: {r['best'].shape}, {len(near)} sites, {time.time() - t0:.0f}s")
low = [s for i, s in enumerate(sites) if s["cls"] in ("R", "HW") or i % 4 == 0]
r28 = predict((29.15, 34.90, 33.40, 39.35), 300, low, R28, 0.7, lambda s: 15.0 if s["cls"] in ("R", "HW") else 5.0, 10, lambda se: se["mech"] + se["retL"], K=12)
RASTERS.append(dict(name="Jordan n28 coverage layer", layer="n28", bounds=r28["bounds"], png=encode(r28, -124)))
injo = shapely.contains_xy(JOR, r28["X"], r28["Y"])
n28_geo = {f"rsrp>={th}": round(float(((r28["best"] >= th) & injo).sum() / injo.sum() * 100), 1) for th in (-100, -110, -118)}
print(f"  n28 raster {r28['best'].shape} {time.time() - t0:.0f}s", n28_geo)
with open(os.path.join(ROOT, "data", "rasters.js"), "w") as f:
    f.write("window.RASTERS=" + json.dumps(RASTERS, separators=(",", ":")) + ";")

COMP = {}
Nn = 10 ** (rf.noise_per_sc(30, rf.UE_NF) / 10)
for c, parts in acc.items():
    a = np.concatenate(parts, axis=1); best, inter = a[0].astype(np.float64), a[1].astype(np.float64); res = {}
    res["px"] = int(best.size); res["rsrp_ge_-105"] = round(float(((best - 4) >= -105).mean() * 100), 1); res["rsrp_p5"] = round(float(np.percentile(best - 4, 5)), 1)
    for env, pen in (("outdoor", 0.0), ("light indoor / in-car", 13.0), ("deep indoor", 25.0)):
        for load in (0.1, 0.2, 0.3, 0.5):
            for bw in (100, 200, 300):
                sh = 10 * math.log10(300 / bw) - pen
                sinr = (best + sh) - 10 * np.log10(10 ** ((inter + sh - R78["bf_iso"]) / 10) * load + Nn)
                tp = rf.tp_n78_mbps(sinr, bw) + rf.tp_fdd_mbps(sinr - 5)
                res[f"{env}|{int(load * 100)}|{bw}"] = dict(pct_1g=round(float((tp >= 1000).mean() * 100), 1), p5=round(float(np.percentile(tp, 5))),
                                                           p50=round(float(np.percentile(tp, 50))))
    COMP[CLS[c]["name"]] = res

# Indoor dimensioning
ven = []
for (n, t, la, lo, a, rooms) in VENUES:
    if t in ("hotel", "resort"):
        prru = math.ceil(rooms / 5) + math.ceil(a * 0.3 / 500); mmw = 2 if rooms < 300 else 4
    elif t == "stadium": prru, mmw = math.ceil(a / 800), 24
    elif t in ("airport", "convention"): prru, mmw = math.ceil(a / 600), max(6, math.ceil(a / 8000))
    elif t == "mall" or t == "mixed-use": prru, mmw = math.ceil(a * 0.6 / 550), max(4, math.ceil(a / 25000))
    else: prru, mmw = math.ceil(a * 0.7 / 650), 2
    ven.append(dict(name=n, type=t, lat=la, lon=lo, area=a, rooms=rooms, prru=prru, rhub=math.ceil(prru / 8), mmw=mmw,
                    bbu=max(1, math.ceil(prru / 96)), backhaul="2x25GE diverse" if prru > 60 else "2x10GE diverse"))

# ----------------------------------------------------------------------------
# 6. Outputs
# ----------------------------------------------------------------------------
gov_sites = {}
for s in sites: gov_sites.setdefault(s["gov"], {}).setdefault(s["cls"], 0); gov_sites[s["gov"]][s["cls"]] += 1
cov = unary_union([Point(s["x"], s["y"]).buffer(RANGE[s["cls"]] * (1.0 if s["cls"] in ("R", "HW") else 1.0), 12) for s in sites]).intersection(JOR)
cov1g = unary_union([Point(s["x"], s["y"]).buffer(RANGE[s["cls"]], 12) for s in sites if s["cls"] in ("DU", "U", "SU")]).intersection(JOR)
pop_cov = sum(area[c] * CLS[c]["pop_km2"] for c in PRI)
summary = dict(
    sites_total=len(sites), sectors_total=sum(len(s["sec"]) for s in sites), by_class=nsite, by_governorate=gov_sites,
    area_km2={k: round(v, 1) for k, v in area.items()}, jordan_km2=round(JOR.area), geo_cov_pct=round(100 * cov.area / JOR.area, 1),
    geo_1g_km2=round(cov1g.area), pop_in_zones=round(pop_cov), pop_total=sum(GOV_POP.values()),
    hubs=len(hubs), access_rings=len(arings), access_fiber_km=round(sum(r["km"] for r in arings)), agg_rings=len(grings),
    agg_fiber_km=round(sum(r["km"] for r in grings)), backbone_km=sum(b["km"] for b in backbone), metro_core_km=metro_core["km"],
    spur_km=round(sum(s.get("spur_km", 0) for s in sites)), mw_links=len(mw_links),
    fiber_sites=sum(1 for s in sites if s["bh"].startswith("Fiber")), bh_mbps_per_sub=round(bh_mbps, 3),
    subs_total=round(sum(r["subs"] for r in CAP)), bh_total_gbps=round(sum(r["subs"] for r in CAP) * bh_mbps / 1000),
    indoor=dict(venues=len(ven), prru=sum(v["prru"] for v in ven), mmw=sum(v["mmw"] for v in ven)),
    bldg=dict(pruned=pruned, rooftop=sum(1 for s in sites if s["stype"] == "Rooftop"), greenfield=sum(1 for s in sites if s["stype"].startswith("Mono")),
              towers=sum(1 for s in sites if s["stype"].startswith("Lattice")),
              by_class={c: dict(mean_bldg=round(float(np.mean([s["bldg"] for s in sites if s["cls"] == c])), 1),
                                p95_bldg=round(float(np.percentile([s["bldg_max"] for s in sites if s["cls"] == c], 95)), 1),
                                mean_ant=round(float(np.mean([s["h"] for s in sites if s["cls"] == c])), 1),
                                max_ant=max(s["h"] for s in sites if s["cls"] == c)) for c in ("DU", "U", "SU")}),
    terrain=dict(moved=moved, mean_gain_m=round(float(np.mean(gain)), 1), n28_geo_cov=n28_geo),
    terrain_tilts=elev_ok, border_sectors=sum(1 for s in sites for se in s["sec"] if se["border"]),
    assumptions=dict(SUB_PEN=SUB_PEN, GB_MONTH=GB_MONTH, BH_SHARE=BH_SHARE, CELL_SE=CELL_SE, ROUTE_F=ROUTE_F))
json.dump(dict(summary=summary, link_budget=LB, capacity=CAP, compliance=COMP), open(os.path.join(OUT, "summary.json"), "w"), indent=1)

with open(os.path.join(OUT, "sites.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow("site_id,class,zone,cluster,governorate,lat,lon,ground_elev_m,site_type,local_bldg_height_mean_m,local_bldg_height_max_m,built_fraction,antenna_height_agl_m,sectors,configuration,backhaul,hub,ring,is_hub".split(","))
    for s in sites:
        w.writerow([s["id"], s["cls"], s["zone"], s["cluster"], s["gov"], f"{s['lat']:.5f}", f"{s['lon']:.5f}", s["elev"], s["stype"], s["bldg"], s["bldg_max"], s["built"], s["h"], len(s["sec"]),
                    CLS[s["cls"]]["config"], s["bh"], s.get("hub", ""), s.get("ring", ""), int(bool(s.get("is_hub")))])
with open(os.path.join(OUT, "sectors.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow("cell_id,site_id,class,lat,lon,azimuth_deg,antenna_height_m,mech_tilt_deg,n78_total_tilt_deg,n78_digital_tilt_deg,ret_midband_deg,ret_lowband_deg,terrain_delta_m,pci,border_coordination".split(","))
    for s in sites:
        for k, se in enumerate(s["sec"]):
            w.writerow([f"{s['id']}-{k + 1}", s["id"], s["cls"], f"{s['lat']:.5f}", f"{s['lon']:.5f}", se["az"], s["h"], se["mech"], se["t78"], se["e78"],
                        se["retM"], se["retL"], se["dz"], se["pci"], int(se["border"])])
with open(os.path.join(OUT, "fiber_rings.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["ring_id", "tier", "parent", "nodes", "route_km"])
    for r in arings: w.writerow([r["id"], "access 25GE (eCPRI fronthaul + backhaul)" if r["cran"] else "access 10/25GE", r["hub"], r["n"], r["km"]])
    for r in grings: w.writerow([r["id"], "aggregation 100GE", r["pop"], r["n"], r["km"]])
    for b in backbone: w.writerow([b["name"], "DWDM " + b["tier"], "", "", b["km"]])
with open(os.path.join(OUT, "hubs.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["hub_id", "host_site", "type", "cluster", "pop", "sites_served", "lat", "lon"])
    for h in hubs: w.writerow([h["id"], h["site"], h["type"], h["cluster"], h.get("pop", ""), h["n"], f"{h['lat']:.5f}", f"{h['lon']:.5f}"])
with open(os.path.join(OUT, "indoor_venues.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["venue", "type", "lat", "lon", "served_area_m2", "rooms", "n78_pRRU_4T4R", "RHUB", "n258_mmWave_heads", "BBU_DU", "backhaul"])
    for v in ven: w.writerow([v["name"], v["type"], v["lat"], v["lon"], v["area"], v["rooms"], v["prru"], v["rhub"], v["mmw"], v["bbu"], v["backhaul"]])

CI = {c: i for i, c in enumerate(CLS)}
zones_out = []
for z in Z:
    g = z["geom"].intersection(JOR)
    for p in (g.geoms if hasattr(g, "geoms") else [g]):
        if p.is_empty or p.geom_type != "Polygon": continue
        zones_out.append(dict(name=z["name"], cls=z["cls"], ring=[[round(v, 4) for v in ll(x, y)] for x, y in p.exterior.coords]))
design = dict(
    generated=time.strftime("%Y-%m-%d"), classes={c: dict(name=v["name"], isd=v["isd"], h=v["h"], range=round(RANGE[c], 3), config=v["config"]) for c, v in CLS.items()},
    radio=rf.RADIO, rfc=dict(ue_nf=rf.UE_NF, re100=rf.RE_PER_S_100MHZ, tdd_dl=rf.TDD_DL, oh=rf.OH_DL, impl=rf.IMPL, cap=rf.SE_CAP, pen=rf.RANK_PEN),
    sites=[[s["id"], round(s["lat"], 5), round(s["lon"], 5), CI[s["cls"]], s["zone"], s["gov"], s["h"], s["elev"], s.get("hub", ""), s.get("ring", ""),
            s["bh"], int(bool(s.get("is_hub"))), [[se["az"], se["mech"], se["e78"], se["retM"], se["retL"], se["pci"], int(se["border"]), se["flat"], se["dz"]] for se in s["sec"]], s["bldg"], s["bldg_max"], s["stype"]]
           for s in sites],
    hubs=[[h["id"], round(h["lat"], 5), round(h["lon"], 5), h["type"], h["n"], h.get("pop", "")] for h in hubs],
    arings=[[r["id"], r["km"], int(r["cran"]), r["path"]] for r in arings], grings=[[r["id"], r["km"], r["path"]] for r in grings],
    backbone=backbone, metro_core=metro_core, metro_spurs=metro_spurs, mw=mw_links, pops=POPS, venues=ven, zones=zones_out,
    adm1=adm1, bldg=dict(bounds=bh_bounds, ramp=bh_ramp), summary=summary, link_budget=LB, capacity=CAP, compliance=COMP)
with open(os.path.join(ROOT, "data", "design.js"), "w", encoding="utf-8") as f:
    f.write("window.DESIGN=" + json.dumps(design, separators=(",", ":"), ensure_ascii=False) + ";")
print(json.dumps(summary, indent=1)[:2500])
