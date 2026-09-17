# LLD-01 – RAN Equipment Design (vendor-neutral)
Low-level design of radio, baseband, antenna-line and site power equipment for all 6,270 sites. Per-site result: `lld/ran_site_equipment.csv`; per-hub baseband pools: `lld/ran_hub_baseband.csv`. Unit capacities and power figures are typical 2026 carrier-grade values – replace with the chosen vendor's datasheet in `tools/lld_design.py` and re-run.

## 1. Equipment standards
| Code | Equipment | Key specification | Avg / peak power | Network quantity |
|---|---|---|---|---|
| AAU-64 | n78 64T64R massive-MIMO AAU | 3400–3800 MHz, 400 MHz IBW / 300 MHz OBW, 320 W, 192 elements, 24 dBi, eCPRI 3 × 25GE, ≤ 30 kg, ≤ 0.5 m², IP65, −40…+55 °C | 900 / 1,300 W | 17,076 |
| R-8T | n78 8T8R radio + 8-port antenna (rural) | 8 × 40 W, 300 MHz OBW, 17.5 dBi | 750 / 1,050 W | 1,331 |
| RRU-L2 | n28 2T4R RRU (city) | 2 × 60 W, 703–748 / 758–803 MHz | 350 / 500 W | 17,076 |
| RRU-L4 | n28 4T4R RRU (rural / highway) | 4 × 40 W | 550 / 750 W | 1,599 |
| RRU-M | n1 + n3 dual-band 4T4R RRU | 4 × 60 W shared, 1800 + 2100 MHz | 700 / 950 W | 11,672 |
| RRU-M3 | n3 4T4R RRU (suburban / highway) | 4 × 40 W | 450 / 620 W | 7,003 |
| ANT | Passive antenna 2L4H + RET | 2 × 698–960 (15.5 dBi) + 4 × 1695–2690 MHz (17.5 dBi), 2.0 m city / 2.6 m rural, AISG 2.0 RET per band | – | 18,675 |
| DU | Distributed unit (baseband) | ≥ 9 × 100 MHz 64T64R carriers + 12 FDD cells, 6 × 25GE fronthaul, 2 × 25GE midhaul, Class-C PTP, GNSS | 350 / 500 W | 2,371 at site + 2,960 pooled |
| FHGW | Fronthaul gateway / passive WDM mux (C-RAN site) | 12-λ MWDM/LWDM 25G, CPRI→eCPRI conversion for FDD RRUs, site alarms | 60 / 80 W | 3,899 |
| CSR | Cell-site router (D-RAN site) | 4 × 25GE + 8 × 10GE, SR-MPLS/SRv6, Class-C boundary clock, SyncE | 120 / 150 W | 2,371 |

Total NR cells: **104,243** (city sector = 3 × n78 + n28 + n1 + n3; suburban without n1; rural = 3 × n78 + n28 + n1 + n3; highway = n28 + n3). Software licences follow cells, carriers, MIMO layers and CA combinations (n3 PCell + n1 + 3 × n78 DL CA; UL on n78 or FDD).

## 2. Standard site configurations
| Configuration | Sites | Cells | Avg load W | Peak load W | Rectifier kW (N+1) | Li-ion battery kWh | Grid kVA |
|---|---|---|---|---|---|---|---|
| U C-RAN 3-sector | 2782 | 18 | 6,060 | 8,530 | 21 | 33.6 | 15 |
| SU D-RAN 3-sector | 1605 | 15 | 5,720 | 8,110 | 21 | 33.6 | 15 |
| SU C-RAN 3-sector | 640 | 15 | 5,310 | 7,540 | 18 | 28.8 | 15 |
| DU C-RAN 3-sector | 477 | 18 | 6,060 | 8,530 | 21 | 33.6 | 15 |
| R D-RAN 3-sector | 443 | 18 | 6,620 | 9,100 | 30 | 72.0 | 15 |
| U D-RAN 3-sector | 188 | 18 | 6,470 | 9,100 | 21 | 38.4 | 15 |
| HW D-RAN 2-sector | 134 | 4 | 2,620 | 3,590 | 15 | 28.8 | 5 |

* DC power −48 V, 3 kW rectifier modules, N+1, sized for peak load + 0.2C battery recharge. Battery autonomy **4 h city, 8 h rural / highway** at average load (80 % depth of discharge). Li-ion with anti-theft lock and remote BMS.
* **360 rural / highway sites without fibre or grid nearby are designed off-grid:** solar PV ≈ 23.1 kWp (traffic-adaptive radio sleep, 5.5 peak-sun-hours) + battery + 15 kVA stand-by generator.
* Energy saving features mandatory in the tender: symbol / channel shutdown, carrier shutdown of 2nd–3rd n78 carrier at night, deep-sleep AAU – target ≥ 25 % energy reduction versus the averages above.
* Outdoor cabinets IP55 with heat exchanger (no air-conditioning) up to 50 °C ambient; Aqaba and Jordan Valley sites use the 55 °C variant with sun shield.

## 3. Baseband architecture
* **Dense urban / urban: C-RAN.** AAUs and RRUs connect over passive-WDM fronthaul (≤ 10 km, ≤ 75 µs one-way, 12-core drop) to the DU pool in their hub. Pool size = 0.75 DU per site (25 % pooling gain from non-coincident busy hours); inter-site CA, DL CoMP and coordinated scheduling run inside the pool – this is what lifts the cell-edge pixels to 1 Gbps.
* **Suburban / rural / highway: D-RAN.** DU in the site cabinet, 25GE midhaul on the access ring.
* **CU (CU-CP / CU-UP) virtualised** on the edge cloud at the six core / edge sites; one CU cluster per ≈ 500 sites; F1 over the aggregation network, latency budget ≤ 5 ms.
* **150 hubs**, of which 93 are DU hotels with **2,960 pooled DUs**; largest hub 54 DUs / 7 racks / 43.7 kW facility load. Hub rooms: 2N power feeds, N+1 cooling, 4 h battery + generator, GNSS antenna pair, fire suppression, access control.

## 4. Antenna line and installation standards
Jumpers ≤ 3 m, ½″ super-flex, 4.3-10 connectors, PIM ≤ −153 dBc; AISG RET daisy-chain per sector; AAU on independent bracket with ±15° mechanical azimuth and 0–10° tilt adjustment; wind load design 160 km/h; rooftop pole loading checked for 75 kg per sector (AAU + passive antenna + RRUs). GNSS receiver per D-RAN site and per hub; PTP as backup (and primary for C-RAN radios).

## 5. Parameter baseline (common to all vendors)
SCS 30 kHz (n78) / 15 kHz (FDD); TDD pattern DDDSU, special slot 10:2:2; SSB 8 beams n78; PCI from `output/sectors.csv`; digital tilt and RET per sector from the same file; max 4 DL layers per UE, MU-MIMO up to 16 layers; 256-QAM DL / 64-QAM UL (256-QAM UL where supported); n3 PCell with n78 SCells, UL Tx switching enabled; VoNR on n28/n3 with EVS-WB; inactivity timer 10 s; A3 offset 3 dB, TTT 320 ms (city) / 640 ms (rural).
