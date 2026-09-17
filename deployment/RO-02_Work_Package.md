# RO-02 – Work Package
**On-air window: Jul 2027 – Sep 2027 (M7–M9) · 465 sites · 1395 sectors · 10 hubs · 445 km access/aggregation fiber · 194 km backbone · 18 indoor venues**

After this rollout: 771 sites on air (12 % of programme), ≈ 18.4 % of population covered, 117 km² of 1 Gbps footprint. Site list: filter `rollout = RO-02` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 2.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 176 | | Rooftop | 452 |
| Urban | 289 | | Monopole / greenfield | 13 |
| Suburban | 0 | | Lattice tower | 0 |
| Rural | 0 | | | |
| Highway | 0 | | **Total** | **465** |

**Areas:** Amman-Zarqa Metro (375), Irbid (90).
**Governorates:** Amman 375, Irbid 90.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-52 | Hub cluster | Amman-Zarqa Metro | 54 |
| HUB-IRB-15 | Hub cluster | Irbid | 52 |
| HUB-AMM-57 | Hub cluster | Amman-Zarqa Metro | 51 |
| HUB-AMM-41 | Hub cluster | Amman-Zarqa Metro | 50 |
| HUB-AMM-45 | Hub cluster | Amman-Zarqa Metro | 46 |
| HUB-AMM-59 | Hub cluster | Amman-Zarqa Metro | 45 |
| HUB-AMM-23 | Hub cluster | Amman-Zarqa Metro | 43 |
| HUB-AMM-64 | Hub cluster | Amman-Zarqa Metro | 43 |
| HUB-AMM-35 | Hub cluster | Amman-Zarqa Metro | 43 |
| HUB-IRB-01 | Hub cluster | Irbid | 38 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1395 | | Hubs / DU hotels | 10 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 20 |
| Passive 2L4H antenna + RET | 1395 | | Cell-site routers 25GE | 0 |
| n28 RRU | 1395 | | Access-ring fiber km | 381 |
| n1/n3 RRU | 1395 | | Aggregation fiber km | 64 |
| Pooled DU (C-RAN, 0.75 per site) | 349 | | Backbone add/drop spur km | 0 |
| Site DU (D-RAN) | 0 | | Backbone / metro core km lit | 194 |
| Fronthaul gateways (C-RAN) | 465 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 1740 / 58 | | Power systems (rectifier + battery) | 465 |

## 4. Prerequisites (entry criteria)
- RO-01 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Amman-Zarqa-Mafraq-Jaber (74 km); Mafraq-Ramtha-Irbid (52 km); Irbid-Jerash-Amman (R35) (68 km)
- Backbone already in service from earlier rollouts: Amman metro core ring

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M1 · Jan 2027 | M4 · Apr 2027 |
| Detailed RF / transport design freeze, material call-off | M2 · Feb 2027 | M4 · Apr 2027 |
| Civil works, power, fiber build to hubs and rings | M3 · Mar 2027 | M6 · Jun 2027 |
| Hub / DU-hotel and router commissioning | M5 · May 2027 | M7 · Jul 2027 |
| Radio install, commissioning, integration to 5GC | M6 · Jun 2027 | M9 · Sep 2027 |
| Single-site verification (SSV) | M7 · Jul 2027 | M9 · Sep 2027 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M8 · Aug 2027 | M11 · Nov 2027 |
| Commercial launch of rollout area / hand-over to operations | M10 · Oct 2027 | M11 · Nov 2027 |

Required run-rate: ≈ 155 sites on air per month; ≈ 149 km of access/aggregation fiber per month.

## 6. Resources
13 acquisition agents · 80 civil crews · 38 urban fiber crews · 2 backbone crews · 23 radio install crews · 3 SSV teams · 4 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| Abdali Mall | mall | 248 | 10 |
| The Boulevard - Abdali | mixed-use | 110 | 4 |
| Galleria Mall | mall | 66 | 4 |
| Al Baraka Mall | mall | 50 | 4 |
| Istiklal Mall | mall | 66 | 4 |
| Four Seasons Amman | hotel | 66 | 2 |
| The St. Regis Amman | hotel | 88 | 2 |
| The Ritz-Carlton Amman | hotel | 79 | 2 |
| Fairmont Amman | hotel | 103 | 4 |
| W Amman | hotel | 86 | 2 |
| Amman Rotana | hotel | 125 | 4 |
| InterContinental Jordan | hotel | 130 | 4 |
| Amman Marriott | hotel | 89 | 2 |
| Kempinski Amman | hotel | 83 | 2 |
| Le Royal Amman | hotel | 105 | 2 |
| Sheraton Amman | hotel | 84 | 2 |
| Landmark Amman | hotel | 79 | 2 |
| Crowne Plaza Amman | hotel | 83 | 2 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-03.

## 9. Rollout-specific notes
- Dense-urban rooftops: structural screening and owner negotiations dominate; C-RAN fronthaul ≤ 10 km to the DU hotel must be verified per site.
- More than half the sites are rooftops – prioritise existing shared rooftops; antenna must clear local roofs by 8 m (heights in `rollout_sites.csv`).
