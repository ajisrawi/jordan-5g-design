# RO-08 – Work Package
**On-air window: Jan 2029 – Mar 2029 (M25–M27) · 718 sites · 2142 sectors · 18 hubs · 802 km access/aggregation fiber · 471 km backbone · 2 indoor venues**

After this rollout: 5,130 sites on air (82 % of programme), ≈ 83.4 % of population covered, 1,071 km² of 1 Gbps footprint. Site list: filter `rollout = RO-08` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 8.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 181 |
| Urban | 166 | | Monopole / greenfield | 400 |
| Suburban | 415 | | Lattice tower | 137 |
| Rural | 126 | | | |
| Highway | 11 | | **Total** | **718** |

**Areas:** Amman-Zarqa Metro (288), Ajloun (81), Amman governorate (rural) (40), Salt (36), Madaba (36), Karak governorate (rural) (35), Karak (34), Mafraq (31), Tafilah (30), Mafraq governorate (rural) (29), Irbid (27), Irbid governorate (rural) (21), Aqaba (18), Amman-Azraq (R40) (9), Karak-Qatraneh (1), Tafilah-Jurf (1), Madaba governorate (rural) (1).
**Governorates:** Amman 212, Zarqa 105, Ajloun 81, Karak 70, Mafraq 60, Balqa 58, Irbid 48, Madaba 35, Tafilah 31, Aqaba 18.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-37 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-73 | Hub cluster | Amman-Zarqa Metro | 46 |
| RUR|Amman|2 | Rural package | Amman governorate (rural) | 40 |
| HUB-SAL-04 | Hub cluster | Salt | 36 |
| HUB-MAD-01 | Hub cluster | Madaba | 36 |
| HUB-AMM-58 | Hub cluster | Amman-Zarqa Metro | 36 |
| RUR|Karak|2 | Rural package | Karak governorate (rural) | 35 |
| HUB-AMM-21 | Hub cluster | Amman-Zarqa Metro | 35 |
| HUB-KAR-01 | Hub cluster | Karak | 34 |
| HUB-AMM-50 | Hub cluster | Amman-Zarqa Metro | 34 |
| HUB-AMM-20 | Hub cluster | Amman-Zarqa Metro | 33 |
| HUB-MAF-01 | Hub cluster | Mafraq | 31 |
| HUB-TAF-01 | Hub cluster | Tafilah | 30 |
| HUB-AMM-84 | Hub cluster | Amman-Zarqa Metro | 30 |
| RUR|Mafraq|2 | Rural package | Mafraq governorate (rural) | 29 |
| HUB-AJL-02 | Hub cluster | Ajloun | 29 |
| HUB-AJL-03 | Hub cluster | Ajloun | 27 |
| HUB-IRB-12 | Hub cluster | Irbid | 27 |
| HUB-AMM-74 | Hub cluster | Amman-Zarqa Metro | 26 |
| HUB-AJL-01 | Hub cluster | Ajloun | 25 |
| RUR|Irbid|2 | Rural package | Irbid governorate (rural) | 21 |
| HUB-AQB-04 | Hub cluster | Aqaba | 18 |
| HW|Amman-Azraq (R40) | Highway corridor | Amman-Azraq (R40) | 9 |
| HW|Karak-Qatraneh | Highway corridor | Karak-Qatraneh | 1 |
| HW|Tafilah-Jurf | Highway corridor | Tafilah-Jurf | 1 |
| RUR|Madaba|2 | Rural package | Madaba governorate (rural) | 1 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1743 | | Hubs / DU hotels | 18 |
| n78 8T8R (rural) | 377 | | Hub aggregation routers | 36 |
| Passive 2L4H antenna + RET | 2142 | | Cell-site routers 25GE | 586 |
| n28 RRU | 2142 | | Access-ring fiber km | 667 |
| n1/n3 RRU | 2142 | | Aggregation fiber km | 107 |
| Pooled DU (C-RAN, 0.75 per site) | 99 | | Backbone add/drop spur km | 28 |
| Site DU (D-RAN) | 586 | | Backbone / metro core km lit | 471 |
| Fronthaul gateways (C-RAN) | 132 | | | |
| n258 street cells | 0 | | Microwave hops | 107 |
| Indoor pRRU / n258 heads | 319 / 4 | | Power systems (rectifier + battery) | 718 |

## 4. Prerequisites (entry criteria)
- RO-07 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Zarqa-Azraq-Safawi (137 km); Mafraq-Safawi-Ruwaished (R10) (302 km); Quweira-Wadi Rum (32 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Azraq; Amman-Salt-Deir Alla; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Ajloun-Jerash; Irbid-Jerash-Amman …
- Cross-border coordination filed for 17 flagged sectors in this rollout

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M19 · Jul 2028 | M22 · Oct 2028 |
| Detailed RF / transport design freeze, material call-off | M20 · Aug 2028 | M22 · Oct 2028 |
| Civil works, power, fiber build to hubs and rings | M21 · Sep 2028 | M24 · Dec 2028 |
| Hub / DU-hotel and router commissioning | M23 · Nov 2028 | M25 · Jan 2029 |
| Radio install, commissioning, integration to 5GC | M24 · Dec 2028 | M27 · Mar 2029 |
| Single-site verification (SSV) | M25 · Jan 2029 | M27 · Mar 2029 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M26 · Feb 2029 | M29 · May 2029 |
| Commercial launch of rollout area / hand-over to operations | M28 · Apr 2029 | M29 · May 2029 |

Required run-rate: ≈ 239 sites on air per month; ≈ 268 km of access/aggregation fiber per month.

## 6. Resources
20 acquisition agents · 229 civil crews · 67 urban fiber crews · 5 backbone crews · 35 radio install crews · 4 SSV teams · 5 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| JUST campus | campus | 216 | 2 |
| King Abdullah University Hospital | hospital | 103 | 2 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-09.

## 9. Rollout-specific notes
- Rural/highway towers: 45 m lattice, solar-hybrid power where off-grid, backbone add/drop or microwave per `backhaul` column; security fencing standard.
