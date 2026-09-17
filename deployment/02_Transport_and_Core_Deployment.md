# 02 – Transport and Core Deployment Plan

## 1. 5G core
| Phase | Months | Scope |
|---|---|---|
| C0 | M1–M2 | DC1 (Amman West) and DC2 (Amman East) facility readiness, cloud platform, IP fabric, security zones |
| C1 | M2–M4 | 5GC control plane (AMF, SMF, AUSF, UDM/UDR, PCF, NRF, NSSF, SCP, CHF), UPF pool 1, IMS/VoNR, OSS, lawful intercept; interconnect and roaming tests; **first call M4** |
| C2 | M6–M9 | Geo-redundancy failover tests DC1↔DC2; Amman Centre and Zarqa edge UPF + CDN (with RO-02) |
| C3 | M8–M12 | Irbid regional DC: edge UPF/MEC, UDR replica (with RO-02/03); Aqaba regional DC and international gateway (with RO-03) |
| C4 | M13–M30 | UPF capacity steps following traffic: +400 Gbps per 600 accepted city sites; slice catalogue (eMBB-1G GFBR, FWA, enterprise); NEF exposure |
| C5 | M31–M36 | Final dimensioning to ≈ 2,492 Gbps busy hour (N+1), DR drill, hand-over |

## 2. Backbone and metro core (must be lit before the dependent rollout opens)
| Rollout | Routes lit | Route km |
|---|---|---|
| RO-01 | Amman metro core ring (87 km) | 87 |
| RO-02 | Amman-Zarqa-Mafraq-Jaber (74 km); Mafraq-Ramtha-Irbid (52 km); Irbid-Jerash-Amman (R35) (68 km) | 194 |
| RO-03 | Desert Highway (R15) Amman-Aqaba (340 km) | 340 |
| RO-04 | Dead Sea - Wadi Araba (R65) Amman-Aqaba (337 km) | 337 |
| RO-05 | King's Highway Madaba-Karak-Tafilah-Petra-Ma'an (241 km); Amman-Salt-Deir Alla (37 km) | 278 |
| RO-06 | Jordan Valley (R65 north) (127 km); Irbid-Ajloun-Jerash (47 km) | 174 |
| RO-07 | Karak-Qatraneh (39 km); Tafilah-Jurf (34 km); Amman-Azraq (R40) (112 km) | 185 |
| RO-08 | Zarqa-Azraq-Safawi (137 km); Mafraq-Safawi-Ruwaished (R10) (302 km); Quweira-Wadi Rum (32 km) | 471 |
| RO-09 | – | 0 |
| RO-10 | – | 0 |

Sequence logic: metro core (RO-01) → northern ring Amman–Zarqa–Mafraq–Irbid–Jerash (RO-02) → Desert Highway to Aqaba incl. cable-landing access (RO-03) → Wadi Araba–Dead Sea closes the southern national ring (RO-04) → King’s Highway and Salt (RO-05) → Jordan Valley, Ajloun (RO-06) → cross-links and Azraq (RO-07) → eastern desert and Wadi Rum (RO-08). First light may use leased/swapped dark fiber; DWDM/OTN nodes at every PoP; ring protection verified (< 50 ms) before the rollout gate G2.

## 3. Hubs, aggregation and access rings
| Rollout | Hubs commissioned | Hub routers | Access-ring km | Aggregation km | Spur km | Microwave hops | Pooled DUs (C-RAN) | Site DUs (D-RAN) |
|---|---|---|---|---|---|---|---|---|
| RO-01 | 6 | 12 | 228 | 32 | 0 | 0 | 230 | 0 |
| RO-02 | 10 | 20 | 381 | 64 | 0 | 0 | 349 | 0 |
| RO-03 | 15 | 30 | 537 | 108 | 0 | 0 | 453 | 14 |
| RO-04 | 16 | 32 | 611 | 108 | 30 | 0 | 515 | 33 |
| RO-05 | 19 | 38 | 697 | 109 | 30 | 0 | 513 | 85 |
| RO-06 | 19 | 38 | 810 | 106 | 6 | 0 | 448 | 173 |
| RO-07 | 13 | 26 | 463 | 53 | 60 | 246 | 320 | 340 |
| RO-08 | 18 | 36 | 667 | 107 | 28 | 107 | 99 | 586 |
| RO-09 | 17 | 34 | 764 | 121 | 47 | 7 | 0 | 669 |
| RO-10 | 17 | 34 | 579 | 80 | 0 | 0 | 0 | 471 |
| **Total** | 150 | 300 | 5,737 | 888 | 201 | 360 | 2927 | 2,371 |

Build order inside a rollout: (1) hub room (power 2N, cooling, GNSS, racks) → (2) aggregation ring to PoP, routers, PTP grandmaster/boundary-clock chain verified (±1.5 µs; ±130 ns inside C-RAN cluster) → (3) access rings, both directions spliced and OTDR-tested before radio integration → (4) DU pool commissioning → (5) sites. A ring is accepted only when closed: single-homed sites are not counted as on-air for gate G3.

Fiber acceptance: OTDR both directions 1310/1550 nm, splice ≤ 0.1 dB, span loss within budget for 25GE-LR / eCPRI (≤ 10 km fronthaul), as-built GIS route uploaded.
