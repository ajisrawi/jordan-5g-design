# RO-06 – Work Package
**On-air window: Jul 2028 – Sep 2028 (M19–M21) · 770 sites · 2303 sectors · 19 hubs · 922 km access/aggregation fiber · 174 km backbone · 9 indoor venues**

After this rollout: 3,646 sites on air (58 % of programme), ≈ 60.3 % of population covered, 755 km² of 1 Gbps footprint. Site list: filter `rollout = RO-06` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 6.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 225 |
| Urban | 455 | | Monopole / greenfield | 538 |
| Suburban | 308 | | Lattice tower | 7 |
| Rural | 0 | | | |
| Highway | 7 | | **Total** | **770** |

**Areas:** Irbid (283), Amman-Zarqa Metro (144), Madaba (122), Mafraq (75), Tafilah (42), Karak (38), Ma'an (35), Aqaba (24), King's Highway Madaba-Karak-Tafilah-Petra-Ma'an (7).
**Governorates:** Irbid 283, Amman 131, Madaba 87, Mafraq 75, Zarqa 48, Tafilah 43, Ma'an 41, Karak 38, Aqaba 24.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-IRB-13 | Hub cluster | Irbid | 71 |
| HUB-IRB-06 | Hub cluster | Irbid | 60 |
| HUB-IRB-18 | Hub cluster | Irbid | 42 |
| HUB-TAF-02 | Hub cluster | Tafilah | 42 |
| HUB-MAD-04 | Hub cluster | Madaba | 42 |
| HUB-AMM-81 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-MAD-02 | Hub cluster | Madaba | 41 |
| HUB-MAF-05 | Hub cluster | Mafraq | 39 |
| HUB-MAD-03 | Hub cluster | Madaba | 39 |
| HUB-IRB-04 | Hub cluster | Irbid | 38 |
| HUB-KAR-03 | Hub cluster | Karak | 38 |
| HUB-IRB-09 | Hub cluster | Irbid | 37 |
| HUB-AMM-60 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-MAF-02 | Hub cluster | Mafraq | 36 |
| HUB-MA-02 | Hub cluster | Ma'an | 35 |
| HUB-IRB-19 | Hub cluster | Irbid | 35 |
| HUB-AMM-76 | Hub cluster | Amman-Zarqa Metro | 33 |
| HUB-AMM-06 | Hub cluster | Amman-Zarqa Metro | 33 |
| HUB-AQB-02 | Hub cluster | Aqaba | 24 |
| HW|King's Highway Madaba-Karak-Tafilah-Petra-Ma'an | Highway corridor | King's Highway Madaba-Karak-Tafilah-Petra-Ma'an | 7 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 2289 | | Hubs / DU hotels | 19 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 38 |
| Passive 2L4H antenna + RET | 2303 | | Cell-site routers 25GE | 173 |
| n28 RRU | 2303 | | Access-ring fiber km | 810 |
| n1/n3 RRU | 2303 | | Aggregation fiber km | 106 |
| Pooled DU (C-RAN, 0.75 per site) | 448 | | Backbone add/drop spur km | 6 |
| Site DU (D-RAN) | 173 | | Backbone / metro core km lit | 174 |
| Fronthaul gateways (C-RAN) | 597 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 650 / 28 | | Power systems (rectifier + battery) | 770 |

## 4. Prerequisites (entry criteria)
- RO-05 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Jordan Valley (R65 north) (127 km); Irbid-Ajloun-Jerash (47 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Salt-Deir Alla; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Jerash-Amman; King's Highway Madaba-Karak-Tafilah-Petra-Ma'an; Mafraq-Ramtha-Irbid

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M13 · Jan 2028 | M16 · Apr 2028 |
| Detailed RF / transport design freeze, material call-off | M14 · Feb 2028 | M16 · Apr 2028 |
| Civil works, power, fiber build to hubs and rings | M15 · Mar 2028 | M18 · Jun 2028 |
| Hub / DU-hotel and router commissioning | M17 · May 2028 | M19 · Jul 2028 |
| Radio install, commissioning, integration to 5GC | M18 · Jun 2028 | M21 · Sep 2028 |
| Single-site verification (SSV) | M19 · Jul 2028 | M21 · Sep 2028 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M20 · Aug 2028 | M23 · Nov 2028 |
| Commercial launch of rollout area / hand-over to operations | M22 · Oct 2028 | M23 · Nov 2028 |

Required run-rate: ≈ 257 sites on air per month; ≈ 308 km of access/aggregation fiber per month.

## 6. Resources
22 acquisition agents · 221 civil crews · 77 urban fiber crews · 2 backbone crews · 37 radio install crews · 5 SSV teams · 6 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| Kempinski Ishtar Dead Sea | hotel | 111 | 4 |
| Movenpick Dead Sea | hotel | 109 | 4 |
| Dead Sea Marriott | hotel | 80 | 2 |
| Hilton Dead Sea | hotel | 90 | 2 |
| Crowne Plaza Dead Sea | hotel | 126 | 4 |
| King Hussein Bin Talal Convention Centre | convention | 42 | 6 |
| Movenpick Petra | hotel | 52 | 2 |
| Petra Marriott | hotel | 31 | 2 |
| Petra Visitor Centre | venue | 9 | 2 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-07.

## 9. Rollout-specific notes
- Standard process applies.
