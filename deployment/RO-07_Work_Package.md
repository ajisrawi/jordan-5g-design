# RO-07 – Work Package
**On-air window: Oct 2028 – Dec 2028 (M22–M24) · 766 sites · 2298 sectors · 13 hubs · 576 km access/aggregation fiber · 185 km backbone · 0 indoor venues**

After this rollout: 4,412 sites on air (70 % of programme), ≈ 73.9 % of population covered, 878 km² of 1 Gbps footprint. Site list: filter `rollout = RO-07` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 7.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 132 |
| Urban | 264 | | Monopole / greenfield | 323 |
| Suburban | 191 | | Lattice tower | 311 |
| Rural | 311 | | | |
| Highway | 0 | | **Total** | **766** |

**Areas:** Jerash (117), Ma'an (102), Salt (101), Mafraq (71), Karak governorate (rural) (40), Amman governorate (rural) (40), Madaba governorate (rural) (40), Mafraq governorate (rural) (40), Irbid governorate (rural) (40), Tafilah governorate (rural) (35), Karak (35), Amman-Zarqa Metro (29), Balqa governorate (rural) (28), Ajloun governorate (rural) (19), Jerash governorate (rural) (16), Zarqa governorate (rural) (13).
**Governorates:** Balqa 158, Jerash 133, Mafraq 111, Ma'an 102, Karak 75, Madaba 40, Amman 40, Irbid 40, Tafilah 35, Ajloun 19, Zarqa 13.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| RUR|Karak|1 | Rural package | Karak governorate (rural) | 40 |
| RUR|Amman|1 | Rural package | Amman governorate (rural) | 40 |
| RUR|Madaba|1 | Rural package | Madaba governorate (rural) | 40 |
| RUR|Mafraq|1 | Rural package | Mafraq governorate (rural) | 40 |
| RUR|Irbid|1 | Rural package | Irbid governorate (rural) | 40 |
| HUB-JER-02 | Hub cluster | Jerash | 40 |
| HUB-JER-03 | Hub cluster | Jerash | 39 |
| HUB-JER-01 | Hub cluster | Jerash | 38 |
| HUB-MAF-03 | Hub cluster | Mafraq | 36 |
| RUR|Tafilah|1 | Rural package | Tafilah governorate (rural) | 35 |
| HUB-MA-03 | Hub cluster | Ma'an | 35 |
| HUB-SAL-01 | Hub cluster | Salt | 35 |
| HUB-SAL-02 | Hub cluster | Salt | 35 |
| HUB-MA-01 | Hub cluster | Ma'an | 35 |
| HUB-MAF-04 | Hub cluster | Mafraq | 35 |
| HUB-KAR-02 | Hub cluster | Karak | 35 |
| HUB-MA-04 | Hub cluster | Ma'an | 32 |
| HUB-SAL-03 | Hub cluster | Salt | 31 |
| HUB-AMM-71 | Hub cluster | Amman-Zarqa Metro | 29 |
| RUR|Balqa|1 | Rural package | Balqa governorate (rural) | 28 |
| RUR|Ajloun|1 | Rural package | Ajloun governorate (rural) | 19 |
| RUR|Jerash|1 | Rural package | Jerash governorate (rural) | 16 |
| RUR|Zarqa|1 | Rural package | Zarqa governorate (rural) | 13 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1365 | | Hubs / DU hotels | 13 |
| n78 8T8R (rural) | 933 | | Hub aggregation routers | 26 |
| Passive 2L4H antenna + RET | 2298 | | Cell-site routers 25GE | 340 |
| n28 RRU | 2298 | | Access-ring fiber km | 463 |
| n1/n3 RRU | 2298 | | Aggregation fiber km | 53 |
| Pooled DU (C-RAN, 0.75 per site) | 320 | | Backbone add/drop spur km | 60 |
| Site DU (D-RAN) | 340 | | Backbone / metro core km lit | 185 |
| Fronthaul gateways (C-RAN) | 426 | | | |
| n258 street cells | 0 | | Microwave hops | 246 |
| Indoor pRRU / n258 heads | 0 / 0 | | Power systems (rectifier + battery) | 766 |

## 4. Prerequisites (entry criteria)
- RO-06 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Karak-Qatraneh (39 km); Tafilah-Jurf (34 km); Amman-Azraq (R40) (112 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Salt-Deir Alla; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Ajloun-Jerash; Irbid-Jerash-Amman; Jordan Valley …

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M16 · Apr 2028 | M19 · Jul 2028 |
| Detailed RF / transport design freeze, material call-off | M17 · May 2028 | M19 · Jul 2028 |
| Civil works, power, fiber build to hubs and rings | M18 · Jun 2028 | M21 · Sep 2028 |
| Hub / DU-hotel and router commissioning | M20 · Aug 2028 | M22 · Oct 2028 |
| Radio install, commissioning, integration to 5GC | M21 · Sep 2028 | M24 · Dec 2028 |
| Single-site verification (SSV) | M22 · Oct 2028 | M24 · Dec 2028 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M23 · Nov 2028 | M26 · Feb 2029 |
| Commercial launch of rollout area / hand-over to operations | M25 · Jan 2029 | M26 · Feb 2029 |

Required run-rate: ≈ 255 sites on air per month; ≈ 192 km of access/aggregation fiber per month.

## 6. Resources
22 acquisition agents · 278 civil crews · 48 urban fiber crews · 2 backbone crews · 37 radio install crews · 5 SSV teams · 6 optimisation teams.

## 7. Indoor venues in this rollout
None.

## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-08.

## 9. Rollout-specific notes
- Rural/highway towers: 45 m lattice, solar-hybrid power where off-grid, backbone add/drop or microwave per `backhaul` column; security fencing standard.
