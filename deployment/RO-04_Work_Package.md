# RO-04 – Work Package
**On-air window: Jan 2028 – Mar 2028 (M13–M15) · 719 sites · 2124 sectors · 16 hubs · 749 km access/aggregation fiber · 337 km backbone · 14 indoor venues**

After this rollout: 2,107 sites on air (34 % of programme), ≈ 39.3 % of population covered, 376 km² of 1 Gbps footprint. Site list: filter `rollout = RO-04` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 4.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 385 |
| Urban | 625 | | Monopole / greenfield | 301 |
| Suburban | 61 | | Lattice tower | 33 |
| Rural | 0 | | | |
| Highway | 33 | | **Total** | **719** |

**Areas:** Amman-Zarqa Metro (466), Irbid (168), Aqaba (52), Desert Highway (R15) Amman-Aqaba (33).
**Governorates:** Amman 240, Zarqa 203, Irbid 168, Aqaba 60, Balqa 27, Ma'an 11, Karak 7, Tafilah 3.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-40 | Hub cluster | Amman-Zarqa Metro | 54 |
| HUB-AMM-03 | Hub cluster | Amman-Zarqa Metro | 53 |
| HUB-AQB-03 | Hub cluster | Aqaba | 52 |
| HUB-AMM-07 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-IRB-11 | Hub cluster | Irbid | 44 |
| HUB-IRB-17 | Hub cluster | Irbid | 42 |
| HUB-AMM-01 | Hub cluster | Amman-Zarqa Metro | 42 |
| HUB-AMM-29 | Hub cluster | Amman-Zarqa Metro | 42 |
| HUB-AMM-24 | Hub cluster | Amman-Zarqa Metro | 42 |
| HUB-IRB-08 | Hub cluster | Irbid | 41 |
| HUB-IRB-07 | Hub cluster | Irbid | 41 |
| HUB-AMM-39 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-AMM-15 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-AMM-54 | Hub cluster | Amman-Zarqa Metro | 38 |
| HUB-AMM-51 | Hub cluster | Amman-Zarqa Metro | 36 |
| HW|Desert Highway (R15) Amman-Aqaba | Highway corridor | Desert Highway (R15) Amman-Aqaba | 33 |
| HUB-AMM-36 | Hub cluster | Amman-Zarqa Metro | 29 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 2058 | | Hubs / DU hotels | 16 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 32 |
| Passive 2L4H antenna + RET | 2124 | | Cell-site routers 25GE | 33 |
| n28 RRU | 2124 | | Access-ring fiber km | 611 |
| n1/n3 RRU | 2124 | | Aggregation fiber km | 108 |
| Pooled DU (C-RAN, 0.75 per site) | 515 | | Backbone add/drop spur km | 30 |
| Site DU (D-RAN) | 33 | | Backbone / metro core km lit | 337 |
| Fronthaul gateways (C-RAN) | 686 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 1545 / 47 | | Power systems (rectifier + battery) | 719 |

## 4. Prerequisites (entry criteria)
- RO-03 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Dead Sea - Wadi Araba (R65) Amman-Aqaba (337 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Zarqa-Mafraq-Jaber; Desert Highway; Irbid-Jerash-Amman; Mafraq-Ramtha-Irbid
- Cross-border coordination filed for 1 flagged sectors in this rollout

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M7 · Jul 2027 | M10 · Oct 2027 |
| Detailed RF / transport design freeze, material call-off | M8 · Aug 2027 | M10 · Oct 2027 |
| Civil works, power, fiber build to hubs and rings | M9 · Sep 2027 | M12 · Dec 2027 |
| Hub / DU-hotel and router commissioning | M11 · Nov 2027 | M13 · Jan 2028 |
| Radio install, commissioning, integration to 5GC | M12 · Dec 2027 | M15 · Mar 2028 |
| Single-site verification (SSV) | M13 · Jan 2028 | M15 · Mar 2028 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M14 · Feb 2028 | M17 · May 2028 |
| Commercial launch of rollout area / hand-over to operations | M16 · Apr 2028 | M17 · May 2028 |

Required run-rate: ≈ 240 sites on air per month; ≈ 250 km of access/aggregation fiber per month.

## 6. Resources
20 acquisition agents · 181 civil crews · 63 urban fiber crews · 4 backbone crews · 35 radio install crews · 4 SSV teams · 5 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| City Mall | mall | 175 | 7 |
| Mecca Mall | mall | 208 | 8 |
| King Hussein Business Park | campus | 130 | 2 |
| University of Jordan | campus | 270 | 2 |
| Jordan University Hospital | hospital | 103 | 2 |
| King Hussein Cancer Center | hospital | 119 | 2 |
| Ayla Oasis / Hyatt Regency | resort | 112 | 2 |
| Al Manara - Saraya Aqaba | hotel | 69 | 2 |
| Kempinski Aqaba | hotel | 64 | 2 |
| InterContinental Aqaba | hotel | 81 | 2 |
| Movenpick Aqaba | hotel | 90 | 2 |
| Aqaba Gateway / City Center | mall | 44 | 4 |
| King Hussein Intl Airport (Aqaba) | airport | 25 | 6 |
| Arabella Mall Irbid | mall | 55 | 4 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-05.

## 9. Rollout-specific notes
- More than half the sites are rooftops – prioritise existing shared rooftops; antenna must clear local roofs by 8 m (heights in `rollout_sites.csv`).
- Aqaba: ASEZA permitting and customs regime; sectors facing Eilat/Taba carry +2° tilt and coordination limits.
