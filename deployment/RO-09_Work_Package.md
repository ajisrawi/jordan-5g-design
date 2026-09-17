# RO-09 – Work Package
**On-air window: Apr 2029 – Jun 2029 (M28–M30) · 669 sites · 1956 sectors · 17 hubs · 932 km access/aggregation fiber · 0 km backbone · 0 indoor venues**

After this rollout: 5,799 sites on air (92 % of programme), ≈ 88.9 % of population covered, 1,309 km² of 1 Gbps footprint. Site list: filter `rollout = RO-09` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 9.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 0 | | Rooftop | 83 |
| Urban | 2 | | Monopole / greenfield | 528 |
| Suburban | 609 | | Lattice tower | 58 |
| Rural | 7 | | | |
| Highway | 51 | | **Total** | **669** |

**Areas:** Amman-Zarqa Metro (550), Irbid (61), Mafraq-Safawi-Ruwaished (R10) (34), Zarqa-Azraq-Safawi (13), Amman governorate (rural) (7), Quweira-Wadi Rum (4).
**Governorates:** Amman 361, Zarqa 133, Balqa 71, Irbid 61, Mafraq 39, Aqaba 4.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-78 | Hub cluster | Amman-Zarqa Metro | 55 |
| HUB-AMM-16 | Hub cluster | Amman-Zarqa Metro | 49 |
| HUB-AMM-30 | Hub cluster | Amman-Zarqa Metro | 47 |
| HUB-AMM-32 | Hub cluster | Amman-Zarqa Metro | 42 |
| HUB-AMM-55 | Hub cluster | Amman-Zarqa Metro | 40 |
| HUB-AMM-25 | Hub cluster | Amman-Zarqa Metro | 39 |
| HUB-AMM-53 | Hub cluster | Amman-Zarqa Metro | 37 |
| HUB-AMM-34 | Hub cluster | Amman-Zarqa Metro | 36 |
| HUB-AMM-43 | Hub cluster | Amman-Zarqa Metro | 36 |
| HUB-AMM-31 | Hub cluster | Amman-Zarqa Metro | 35 |
| HW|Mafraq-Safawi-Ruwaished (R10) | Highway corridor | Mafraq-Safawi-Ruwaished (R10) | 34 |
| HUB-IRB-16 | Hub cluster | Irbid | 33 |
| HUB-AMM-68 | Hub cluster | Amman-Zarqa Metro | 33 |
| HUB-AMM-67 | Hub cluster | Amman-Zarqa Metro | 32 |
| HUB-AMM-10 | Hub cluster | Amman-Zarqa Metro | 28 |
| HUB-IRB-02 | Hub cluster | Irbid | 28 |
| HUB-AMM-26 | Hub cluster | Amman-Zarqa Metro | 22 |
| HUB-AMM-18 | Hub cluster | Amman-Zarqa Metro | 19 |
| HW|Zarqa-Azraq-Safawi | Highway corridor | Zarqa-Azraq-Safawi | 13 |
| RUR|Amman|3 | Rural package | Amman governorate (rural) | 7 |
| HW|Quweira-Wadi Rum | Highway corridor | Quweira-Wadi Rum | 4 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 1833 | | Hubs / DU hotels | 17 |
| n78 8T8R (rural) | 21 | | Hub aggregation routers | 34 |
| Passive 2L4H antenna + RET | 1956 | | Cell-site routers 25GE | 669 |
| n28 RRU | 1956 | | Access-ring fiber km | 764 |
| n1/n3 RRU | 1956 | | Aggregation fiber km | 121 |
| Pooled DU (C-RAN, 0.75 per site) | 0 | | Backbone add/drop spur km | 47 |
| Site DU (D-RAN) | 669 | | Backbone / metro core km lit | 0 |
| Fronthaul gateways (C-RAN) | 0 | | | |
| n258 street cells | 480 | | Microwave hops | 7 |
| Indoor pRRU / n258 heads | 0 / 0 | | Power systems (rectifier + battery) | 669 |

## 4. Prerequisites (entry criteria)
- RO-08 gate G2 passed (teams and process release)
- Backbone already in service from earlier rollouts: Amman metro core ring; Amman-Azraq; Amman-Salt-Deir Alla; Amman-Zarqa-Mafraq-Jaber; Dead Sea - Wadi Araba; Desert Highway; Irbid-Ajloun-Jerash; Irbid-Jerash-Amman …

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M22 · Oct 2028 | M25 · Jan 2029 |
| Detailed RF / transport design freeze, material call-off | M23 · Nov 2028 | M25 · Jan 2029 |
| Civil works, power, fiber build to hubs and rings | M24 · Dec 2028 | M27 · Mar 2029 |
| Hub / DU-hotel and router commissioning | M26 · Feb 2029 | M28 · Apr 2029 |
| Radio install, commissioning, integration to 5GC | M27 · Mar 2029 | M30 · Jun 2029 |
| Single-site verification (SSV) | M28 · Apr 2029 | M30 · Jun 2029 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M29 · May 2029 | M32 · Aug 2029 |
| Commercial launch of rollout area / hand-over to operations | M31 · Jul 2029 | M32 · Aug 2029 |

Required run-rate: ≈ 223 sites on air per month; ≈ 311 km of access/aggregation fiber per month.

## 6. Resources
19 acquisition agents · 218 civil crews · 78 urban fiber crews · 0 backbone crews · 32 radio install crews · 4 SSV teams · 5 optimisation teams.

## 7. Indoor venues in this rollout
None.

## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-10.

## 9. Rollout-specific notes
- Rural/highway towers: 45 m lattice, solar-hybrid power where off-grid, backbone add/drop or microwave per `backhaul` column; security fencing standard.
- Includes 480 n258 street small cells for dense-urban hotspots (municipal street-furniture agreement required).
