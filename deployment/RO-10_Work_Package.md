# RO-10 – Work Package
**On-air window: Jul 2029 – Sep 2029 (M31–M33) · 471 sites · 1413 sectors · 17 hubs · 659 km access/aggregation fiber · 0 km backbone · 2 indoor venues**

After this rollout: 6,270 sites on air (100 % of programme), ≈ 93.0 % of population covered, 1,491 km² of 1 Gbps footprint. Site list: filter `rollout = RO-10` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 10.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 42 |
| Urban | 6 | | Monopole / greenfield | 429 |
| Suburban | 465 | | Lattice tower | 0 |
| Rural | 0 | | | |
| Highway | 0 | | **Total** | **471** |

**Areas:** Amman-Zarqa Metro (208), Irbid (71), Mutah-Mazar (36), Aqaba (34), Azraq (32), Deir Alla (24), Ghor Safi (23), South Shuna (23), North Shuna (20).
**Governorates:** Balqa 113, Zarqa 110, Irbid 94, Karak 59, Amman 58, Aqaba 34, Ajloun 3.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-80 | Hub cluster | Amman-Zarqa Metro | 50 |
| HUB-AMM-75 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-MUT-01 | Hub cluster | Mutah-Mazar | 36 |
| HUB-AMM-48 | Hub cluster | Amman-Zarqa Metro | 35 |
| HUB-AQB-01 | Hub cluster | Aqaba | 34 |
| HUB-AZR-01 | Hub cluster | Azraq | 32 |
| HUB-IRB-20 | Hub cluster | Irbid | 26 |
| HUB-IRB-14 | Hub cluster | Irbid | 24 |
| HUB-AMM-08 | Hub cluster | Amman-Zarqa Metro | 24 |
| HUB-DEI-01 | Hub cluster | Deir Alla | 24 |
| HUB-GHO-01 | Hub cluster | Ghor Safi | 23 |
| HUB-SOU-01 | Hub cluster | South Shuna | 23 |
| HUB-AMM-17 | Hub cluster | Amman-Zarqa Metro | 22 |
| HUB-AMM-12 | Hub cluster | Amman-Zarqa Metro | 21 |
| HUB-IRB-10 | Hub cluster | Irbid | 21 |
| HUB-NOR-01 | Hub cluster | North Shuna | 20 |
| HUB-AMM-09 | Hub cluster | Amman-Zarqa Metro | 19 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1413 | | Hubs / DU hotels | 17 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 34 |
| Passive 2L4H antenna + RET | 1413 | | Cell-site routers 25GE | 471 |
| n28 RRU | 1413 | | Access-ring fiber km | 579 |
| n1/n3 RRU | 1413 | | Aggregation fiber km | 80 |
| Pooled DU (C-RAN, 0.75 per site) | 0 | | Backbone add/drop spur km | 0 |
| Site DU (D-RAN) | 471 | | Backbone / metro core km lit | 0 |
| Fronthaul gateways (C-RAN) | 0 | | | |
| n258 street cells | 480 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 424 / 17 | | Power systems (rectifier + battery) | 471 |

## 4. Prerequisites (entry criteria)
- RO-09 gate G2 passed (teams and process release)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Azraq; Amman-Salt-Deir Alla; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Ajloun-Jerash; Irbid-Jerash-Amman …
- Cross-border coordination filed for 27 flagged sectors in this rollout

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M25 · Jan 2029 | M28 · Apr 2029 |
| Detailed RF / transport design freeze, material call-off | M26 · Feb 2029 | M28 · Apr 2029 |
| Civil works, power, fiber build to hubs and rings | M27 · Mar 2029 | M30 · Jun 2029 |
| Hub / DU-hotel and router commissioning | M29 · May 2029 | M31 · Jul 2029 |
| Radio install, commissioning, integration to 5GC | M30 · Jun 2029 | M33 · Sep 2029 |
| Single-site verification (SSV) | M31 · Jul 2029 | M33 · Sep 2029 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M32 · Aug 2029 | M35 · Nov 2029 |
| Commercial launch of rollout area / hand-over to operations | M34 · Oct 2029 | M35 · Nov 2029 |

Required run-rate: ≈ 157 sites on air per month; ≈ 220 km of access/aggregation fiber per month.

## 6. Resources
14 acquisition agents · 150 civil crews · 55 urban fiber crews · 0 backbone crews · 23 radio install crews · 3 SSV teams · 4 optimisation teams.

## 7. Indoor venues in this rollout
| Venue | Type | pRRU | n258 |
|---|---|---|---|
| Queen Alia Intl Airport terminal | airport | 172 | 13 |
| Tala Bay resort cluster | resort | 252 | 4 |


## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to operations.

## 9. Rollout-specific notes
- Aqaba: ASEZA permitting and customs regime; sectors facing Eilat/Taba carry +2° tilt and coordination limits.
- Includes 480 n258 street small cells for dense-urban hotspots (municipal street-furniture agreement required).
- Final rollout: network-wide parameter audit, neighbour clean-up, as-built documentation and O&M hand-over run in parallel (M34–M36).
