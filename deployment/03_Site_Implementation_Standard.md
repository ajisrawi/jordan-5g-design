# 03 – Site Implementation Standard (survey → acceptance)

## 1. Process and target durations
| Step | Output | Target | Owner |
|---|---|---|---|
| 1. Nominal release | Search ring (0.2 × ISD), target height, azimuth/tilt from `output/sectors.csv` | T−6 | RF planning |
| 2. Candidate search, TSSR | ≥ 2 candidates; TSSR with panoramic photos, roof height, structural notes, line-of-sight to neighbours, power and fiber entry | 3 weeks | Acquisition + RF + civil |
| 3. RF validation | Candidate accepted if height ≥ nominal −3 m, offset ≤ search ring, no main-beam blockage within 100 m; re-run prediction if moved > 0.15 × ISD | 3 days | RF planning |
| 4. Lease and permits | Lease, municipality permit, EMF file, civil-aviation clearance near QAIA/Marka/Aqaba airports | 6–10 weeks (shared site 2–4) | Acquisition |
| 5. Detailed design | Structural calculation (rooftop loading for 64T64R AAU + passive antenna), power, grounding, fiber entry drawings | 2 weeks | Civil |
| 6. Civil and power | Poles/monopole/tower, cabinets, rectifier + Li-ion backup (4 h city, 8 h rural + solar hybrid off-grid), grid connection | 2–6 weeks | Civil contractor |
| 7. Fiber / microwave | Drop cable to ring, splice, OTDR; or microwave LOS survey, install, link test | parallel with 6 | Transport |
| 8. Radio install | AAU, passive antenna, RRUs, DU or fronthaul, GNSS; azimuth ±3°, mechanical tilt ±0.5° with digital inclinometer/AAT photos | 2–3 days | RAN vendor |
| 9. Commissioning and integration | Software, licences, cell parameters (PCI, RSI, TAC, neighbours, RET, digital tilt), alarms clear, integration to 5GC and OSS | 1 day | RAN vendor |
| 10. SSV | Single-site verification (section 5) | ≤ 5 days after on-air | RAN vendor |
| 11. Cluster optimisation and acceptance | Section 6 | when ≥ 90 % of cluster on air | Optimisation |
| 12. Hand-over | As-built pack, asset register, spares, O&M acceptance | T+4 | PMO |

## 2. Configuration by site type
| Type | Structure | Radio line-up per sector |
|---|---|---|
| City rooftop | 3–6 m poles or stub tower so antenna ≥ roof max + 8 m | n78 64T64R AAU + 2L4H passive antenna, n28 RRU, n1/n3 dual-band RRU |
| City monopole | 25–35 m monopole, camouflaged where required by municipality | same |
| Rural tower | 45 m lattice | 2.6 m passive antenna, n28 + n1/n3 4T4R, n78 8T8R |
| Highway tower | 45 m lattice, 2 sectors along road | n28 + n3 4T4R |

## 3. Installation quality checklist (photo evidence mandatory)
Antenna azimuth, mechanical tilt, height label · RET calibrated and addressable · AAU fan clearance and bracket torque · connector torque and weatherproofing · grounding ≤ 5 Ω, lightning protection · fiber bend radius and labelling both ends · GNSS sky view · cabinet sealing, battery test · site tidy, EMF signage, access safety (roof edge protection, ladder cage).

## 4. HSE
Work-at-height certification for all riggers, permit-to-work per site, RF-off procedure on shared structures, daily toolbox talk, heat-stress rules (no tower climbing 12:00–15:00 June–August), traffic management for street fiber works, zero-fatality target, LTIFR < 0.5.

## 5. Single-site verification (per sector unless stated)
| Test | Pass criterion |
|---|---|
| Alarms / VSWR / RET / GNSS lock | none active / < 1.4 / responds / locked |
| Sector swap and azimuth check (drive around) | PCI footprint matches plan |
| Static DL near-cell (SS-RSRP ≥ −80 dBm, 3CC n78 + FDD CA) | **≥ 1.5 Gbps** peak, ≥ 1.2 Gbps 30 s average |
| Static UL | ≥ 100 Mbps |
| Latency to edge UPF | ≤ 15 ms RTT |
| VoNR call set-up, 2 min hold | success, MOS ≥ 4.0 |
| Intra-site and inter-site handover | 100 % success on test route |
| Backhaul | 25GE link up, PTP locked, throughput test ≥ 8 Gbps |

## 6. Cluster acceptance – the 1 Gbps KPI
Drive test on all accessible roads of the cluster with a 3CC-capable UE, network in live low-load condition (night or pre-launch), 50 m bins:
| KPI | Target |
|---|---|
| Bins with single-user DL ≥ 1 Gbps | **≥ 95 %** dense urban / urban, ≥ 93 % suburban |
| 5th-percentile DL | ≥ 700 Mbps |
| SS-RSRP ≥ −105 dBm | ≥ 98 % of bins |
| SS-SINR ≥ 13 dB | ≥ 90 % of bins |
| UL ≥ 20 Mbps | ≥ 95 % of bins |
| Session set-up success / drop rate | ≥ 99.5 % / ≤ 0.3 % |
| Handover success | ≥ 99.5 % |
| Stationary indoor sample (10 light-indoor points per cluster) | ≥ 80 % of points ≥ 1 Gbps |
Failing bins are analysed against the terrain-aware prediction (map layer “1 Gbps compliance”): actions in order – digital tilt/beam-set change, azimuth change, neighbour/PCI fix, add n258 or infill site (change request). Rural/highway acceptance: n28 SS-RSRP ≥ −110 dBm on ≥ 95 % of the route, DL ≥ 10 Mbps, no call drop on the corridor.

After launch the operating KPI is busy-hour PRB utilisation: > 20 % on a sector for 4 weeks triggers capacity action, protecting the single-user 1 Gbps experience.
