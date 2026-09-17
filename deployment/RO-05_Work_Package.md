# RO-05 – Work Package
**On-air window: Apr 2028 – Jun 2028 (M16–M18) · 769 sites · 2275 sectors · 19 hubs · 836 km access/aggregation fiber · 278 km backbone · 1 indoor venues**

After this rollout: 2,876 sites on air (46 % of programme), ≈ 50.1 % of population covered, 550 km² of 1 Gbps footprint. Site list: filter `rollout = RO-05` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 5.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 359 |
| Urban | 561 | | Monopole / greenfield | 378 |
| Suburban | 176 | | Lattice tower | 32 |
| Rural | 0 | | | |
| Highway | 32 | | **Total** | **769** |

**Areas:** Amman-Zarqa Metro (618), Wadi Musa / Petra (65), Irbid (35), Dead Sea - Wadi Araba (R65) Amman-Aqaba (32), Dead Sea (19).
**Governorates:** Amman 288, Zarqa 271, Balqa 71, Ma'an 65, Irbid 35, Aqaba 17, Madaba 11, Karak 8, Tafilah 3.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-33 | Hub cluster | Amman-Zarqa Metro | 52 |
| HUB-AMM-70 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-46 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-86 | Hub cluster | Amman-Zarqa Metro | 47 |
| HUB-AMM-62 | Hub cluster | Amman-Zarqa Metro | 46 |
| HUB-AMM-66 | Hub cluster | Amman-Zarqa Metro | 42 |
| HUB-AMM-77 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-AMM-19 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-AMM-61 | Hub cluster | Amman-Zarqa Metro | 39 |
| HUB-AMM-72 | Hub cluster | Amman-Zarqa Metro | 39 |
| HUB-AMM-65 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-AMM-22 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-AMM-85 | Hub cluster | Amman-Zarqa Metro | 35 |
| HUB-IRB-03 | Hub cluster | Irbid | 35 |
| HUB-WAD-01 | Hub cluster | Wadi Musa / Petra | 34 |
| HUB-AMM-63 | Hub cluster | Amman-Zarqa Metro | 33 |
| HUB-AMM-42 | Hub cluster | Amman-Zarqa Metro | 33 |
| HW|Dead Sea - Wadi Araba (R65) Amman-Aqaba | Highway corridor | Dead Sea - Wadi Araba (R65) Amman-Aqaba | 32 |
| HUB-WAD-02 | Hub cluster | Wadi Musa / Petra | 31 |
| HUB-DEA-01 | Hub cluster | Dead Sea | 19 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 2211 | | Hubs / DU hotels | 19 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 38 |
| Passive 2L4H antenna + RET | 2275 | | Cell-site routers 25GE | 85 |
| n28 RRU | 2275 | | Access-ring fiber km | 697 |
| n1/n3 RRU | 2275 | | Aggregation fiber km | 109 |
| Pooled DU (C-RAN, 0.75 per site) | 513 | | Backbone add/drop spur km | 30 |
| Site DU (D-RAN) | 85 | | Backbone / metro core km lit | 278 |
| Fronthaul gateways (C-RAN) | 684 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 88 / 4 | | Power systems (rectifier + battery) | 769 |

## 4. Prerequisites (entry criteria)
- RO-04 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: King's Highway Madaba-Karak-Tafilah-Petra-Ma'an (241 km); Amman-Salt-Deir Alla (37 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Jerash-Amman; Mafraq-Ramtha-Irbid

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M10 · Oct 2027 | M13 · Jan 2028 |
| Detailed RF / transport design freeze, material call-off | M11 · Nov 2027 | M13 · Jan 2028 |
| Civil works, power, fiber build to hubs and rings | M12 · Dec 2027 | M15 · Mar 2028 |
| Hub / DU-hotel and router commissioning | M14 · Feb 2028 | M16 · Apr 2028 |
| Radio install, commissioning, integration to 5GC | M15 · Mar 2028 | M18 · Jun 2028 |
| Single-site verification (SSV) | M16 · Apr 2028 | M18 · Jun 2028 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M17 · May 2028 | M20 · Aug 2028 |
| Commercial launch of rollout area / hand-over to operations | M19 · Jul 2028 | M20 · Aug 2028 |

Required run-rate: ≈ 256 sites on air per month; ≈ 279 km of access/aggregation fiber per month.

## 6. Resources
22 acquisition agents · 202 civil crews · 70 urban fiber crews · 3 backbone crews · 37 radio install crews · 5 SSV teams · 6 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| Irbid City Centre | mall | 88 | 4 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-06.

## 9. Rollout-specific notes
- Aqaba: ASEZA permitting and customs regime; sectors facing Eilat/Taba carry +2° tilt and coordination limits.
- Tourism zones (Dead Sea / Petra): camouflage structures, heritage-authority approval (PDTRA for Petra), work outside peak season where possible.
