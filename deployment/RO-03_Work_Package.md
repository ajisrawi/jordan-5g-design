# RO-03 – Work Package
**On-air window: Oct 2027 – Dec 2027 (M10–M12) · 617 sites · 1851 sectors · 15 hubs · 645 km access/aggregation fiber · 340 km backbone · 5 indoor venues**

After this rollout: 1,388 sites on air (22 % of programme), ≈ 28.5 % of population covered, 236 km² of 1 Gbps footprint. Site list: filter `rollout = RO-03` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 3.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 8 | | Rooftop | 487 |
| Urban | 589 | | Monopole / greenfield | 130 |
| Suburban | 20 | | Lattice tower | 0 |
| Rural | 0 | | | |
| Highway | 0 | | **Total** | **617** |

**Areas:** Amman-Zarqa Metro (456), Aqaba (123), Irbid (38).
**Governorates:** Amman 444, Aqaba 123, Irbid 38, Balqa 12.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AQB-05 | Hub cluster | Aqaba | 57 |
| HUB-AQB-06 | Hub cluster | Aqaba | 52 |
| HUB-AMM-56 | Hub cluster | Amman-Zarqa Metro | 49 |
| HUB-AMM-83 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-47 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-44 | Hub cluster | Amman-Zarqa Metro | 44 |
| HUB-AMM-79 | Hub cluster | Amman-Zarqa Metro | 41 |
| HUB-AMM-05 | Hub cluster | Amman-Zarqa Metro | 40 |
| HUB-AMM-02 | Hub cluster | Amman-Zarqa Metro | 39 |
| HUB-IRB-05 | Hub cluster | Irbid | 38 |
| HUB-AMM-49 | Hub cluster | Amman-Zarqa Metro | 38 |
| HUB-AMM-11 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-AMM-27 | Hub cluster | Amman-Zarqa Metro | 36 |
| HUB-AMM-04 | Hub cluster | Amman-Zarqa Metro | 36 |
| HUB-AQB-07 | Hub cluster | Aqaba | 14 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1851 | | Hubs / DU hotels | 15 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 30 |
| Passive 2L4H antenna + RET | 1851 | | Cell-site routers 25GE | 14 |
| n28 RRU | 1851 | | Access-ring fiber km | 537 |
| n1/n3 RRU | 1851 | | Aggregation fiber km | 108 |
| Pooled DU (C-RAN, 0.75 per site) | 453 | | Backbone add/drop spur km | 0 |
| Site DU (D-RAN) | 14 | | Backbone / metro core km lit | 340 |
| Fronthaul gateways (C-RAN) | 603 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 573 / 38 | | Power systems (rectifier + battery) | 617 |

## 4. Prerequisites (entry criteria)
- RO-02 gate G2 passed (teams and process release)
- Backbone lit in this rollout before G2: Desert Highway (R15) Amman-Aqaba (340 km)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Zarqa-Mafraq-Jaber; Irbid-Jerash-Amman; Mafraq-Ramtha-Irbid
- Cross-border coordination filed for 64 flagged sectors in this rollout

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M4 · Apr 2027 | M7 · Jul 2027 |
| Detailed RF / transport design freeze, material call-off | M5 · May 2027 | M7 · Jul 2027 |
| Civil works, power, fiber build to hubs and rings | M6 · Jun 2027 | M9 · Sep 2027 |
| Hub / DU-hotel and router commissioning | M8 · Aug 2027 | M10 · Oct 2027 |
| Radio install, commissioning, integration to 5GC | M9 · Sep 2027 | M12 · Dec 2027 |
| Single-site verification (SSV) | M10 · Oct 2027 | M12 · Dec 2027 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M11 · Nov 2027 | M14 · Feb 2028 |
| Commercial launch of rollout area / hand-over to operations | M13 · Jan 2028 | M14 · Feb 2028 |

Required run-rate: ≈ 206 sites on air per month; ≈ 215 km of access/aggregation fiber per month.

## 6. Resources
18 acquisition agents · 125 civil crews · 54 urban fiber crews · 4 backbone crews · 30 radio install crews · 4 SSV teams · 5 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| Taj Lifestyle Center | mall | 164 | 6 |
| Grand Hyatt Amman | hotel | 99 | 4 |
| Al-Bashir Hospital | hospital | 130 | 2 |
| Amman Intl Stadium / Al-Hussein Youth City | stadium | 50 | 24 |
| Yarmouk University | campus | 130 | 2 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-04.

## 9. Rollout-specific notes
- More than half the sites are rooftops – prioritise existing shared rooftops; antenna must clear local roofs by 8 m (heights in `rollout_sites.csv`).
- Aqaba: ASEZA permitting and customs regime; sectors facing Eilat/Taba carry +2° tilt and coordination limits.
