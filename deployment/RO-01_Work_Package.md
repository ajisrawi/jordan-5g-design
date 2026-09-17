# RO-01 – Work Package
**On-air window: Apr 2027 – Jun 2027 (M4–M6) · 306 sites · 918 sectors · 6 hubs · 260 km access/aggregation fiber · 87 km backbone · 0 indoor venues**

After this rollout: 306 sites on air (5 % of programme), ≈ 8.6 % of population covered, 40 km² of 1 Gbps footprint. Site list: filter `rollout = RO-01` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to 1.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | 293 | | Rooftop | 306 |
| Urban | 13 | | Monopole / greenfield | 0 |
| Suburban | 0 | | Lattice tower | 0 |
| Rural | 0 | | | |
| Highway | 0 | | **Total** | **306** |

**Areas:** Amman-Zarqa Metro (306).
**Governorates:** Amman 306.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
| HUB-AMM-28 | Hub cluster | Amman-Zarqa Metro | 61 |
| HUB-AMM-69 | Hub cluster | Amman-Zarqa Metro | 55 |
| HUB-AMM-14 | Hub cluster | Amman-Zarqa Metro | 51 |
| HUB-AMM-82 | Hub cluster | Amman-Zarqa Metro | 48 |
| HUB-AMM-13 | Hub cluster | Amman-Zarqa Metro | 47 |
| HUB-AMM-38 | Hub cluster | Amman-Zarqa Metro | 44 |

## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | 918 | | Hubs / DU hotels | 6 |
| n78 8T8R (rural) | 0 | | Hub aggregation routers | 12 |
| Passive 2L4H antenna + RET | 918 | | Cell-site routers 25GE | 0 |
| n28 RRU | 918 | | Access-ring fiber km | 228 |
| n1/n3 RRU | 918 | | Aggregation fiber km | 32 |
| Pooled DU (C-RAN, 0.75 per site) | 230 | | Backbone add/drop spur km | 0 |
| Site DU (D-RAN) | 0 | | Backbone / metro core km lit | 87 |
| Fronthaul gateways (C-RAN) | 306 | | | |
| n258 street cells | 0 | | Microwave hops | 0 |
| Indoor pRRU / n258 heads | 0 / 0 | | Power systems (rectifier + battery) | 306 |

## 4. Prerequisites (entry criteria)
- Spectrum licence and type approval
- DC1/DC2 core ready, first call (M4)
- Amman metro core ring lit
- Site-sharing and dark-fiber frameworks signed
- CW model-calibration campaign complete
- Backbone lit in this rollout before G2: Amman metro core ring (87 km)

## 5. Schedule
| Activity | Start | End |
|---|---|---|
| Nominal release, TSSR surveys, site acquisition & permits | M1 · Jan 2027 | M1 · Jan 2027 |
| Detailed RF / transport design freeze, material call-off | M1 · Jan 2027 | M1 · Jan 2027 |
| Civil works, power, fiber build to hubs and rings | M1 · Jan 2027 | M3 · Mar 2027 |
| Hub / DU-hotel and router commissioning | M2 · Feb 2027 | M4 · Apr 2027 |
| Radio install, commissioning, integration to 5GC | M3 · Mar 2027 | M6 · Jun 2027 |
| Single-site verification (SSV) | M4 · Apr 2027 | M6 · Jun 2027 |
| Cluster optimisation & acceptance (1 Gbps drive test) | M5 · May 2027 | M8 · Aug 2027 |
| Commercial launch of rollout area / hand-over to operations | M7 · Jul 2027 | M8 · Aug 2027 |

Required run-rate: ≈ 102 sites on air per month; ≈ 87 km of access/aggregation fiber per month.

## 6. Resources
9 acquisition agents · 51 civil crews · 22 urban fiber crews · 1 backbone crews · 15 radio install crews · 2 SSV teams · 3 optimisation teams.

## 7. Indoor venues in this rollout
None.

## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to RO-02.

## 9. Rollout-specific notes
- Dense-urban rooftops: structural screening and owner negotiations dominate; C-RAN fronthaul ≤ 10 km to the DU hotel must be verified per site.
- More than half the sites are rooftops – prioritise existing shared rooftops; antenna must clear local roofs by 8 m (heights in `rollout_sites.csv`).
- Pilot rollout: 3-week extra optimisation buffer; acceptance results recalibrate the prediction model for all later rollouts.
