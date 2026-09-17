# LLD-03 – Transport Network Design (vendor-neutral)
Ports and router classes per node, optics, DWDM wavelength plan, IP/MPLS design and microwave link design. Tables: `transport_hub_ports.csv`, `transport_pop_ports.csv`, `transport_agg_ring_optics.csv`, `dwdm_wavelength_plan.csv`, `microwave_links.csv`.

## 1. Node classes
| Class | Where | Ports | Quantity |
|---|---|---|---|
| CSR | every D-RAN site | 4 × 25GE + 8 × 10GE, Class-C BC | 2,371 |
| FHGW / passive WDM | every C-RAN site | 12 λ × 25G on one fibre pair (+ protection pair) | 3,899 |
| HUB-R1 | hub (pair per hub) | 24×25GE + 4×100GE | 117 hubs → 234 routers |
| HUB-R2 | hub (pair per hub) | 48×25GE + 8×100GE | 33 hubs → 66 routers |
| POP-R1 | PoP / core site (pair) | 16×100GE + 4×400GE | 24 PoPs → 48 routers |
| DWDM | backbone nodes | ROADM / FOADM, 400G coherent line cards | 15 routes, 37 wavelengths day 1 (400G on rings, 100G on light spurs) |


## 2. Access and aggregation dimensioning
* **Access ring (D-RAN), 25GE:** ≤ 8 sites, dual-homed on the hub router pair. Design load = 1.5 × busy-hour mean + one sector at its 5.2 Gbps peak. Result over 269 D-RAN rings: mean 7.9 Gbps, max 10.3 Gbps → **≤ 41 % of 25GE**; upgrade path 50GE optics on the same fibre.
* **C-RAN access ring:** physical fibre ring carrying point-to-point fronthaul wavelengths (9 × 25G eCPRI for the AAUs + 3 × 10G for FDD RRUs per site, passive WDM, both directions of the ring for protection). Optical budget: 25G LR ≤ 10 km, ≤ 6.3 dB path + 2 × 2.5 dB mux.
* **Hub routers:** one end of every access ring per router + half of the pooled DUs + 100GE uplinks; peak hub load max 70.5 Gbps, uplink utilisation at peak ≤ 29 %.
* **Aggregation rings, 100GE:** ≤ 5 hubs per ring; optic by mean span: 39 × 100G-LR4 (10 km), 2 × 100G-ER4 (40 km). Ring load = sum of hub peaks × 0.7 diversity; rings above 60 Gbps are split or moved to 2 × 100GE LAG (check column peak_Gbps per PoP).
* **PoP routers:** aggregation rings on 100GE, 400GE to DWDM / core; busiest PoP POP-IRB 298.1 Gbps busy hour.

## 3. DWDM backbone – wavelength plan (day 1, 400G coherent, 75 GHz flex-grid, 64 slots per fibre pair)
| Route | Ring | km | Design demand Gbps | λ day 1 | Channel plan | In-line amplifier sites | Node type | Line optics |
|---|---|---|---|---|---|---|---|---|
| Desert Highway (R15) Amman-Aqaba | Southern ring | 340 | 1340 | 4 | 4 × 400G (of 64 × 75 GHz C-band slots) | 4 | ROADM (2-degree, 3 at junctions) | 400G ZR+/OTN coherent, FlexO |
| Dead Sea - Wadi Araba (R65) Amman-Aqaba | Southern ring | 337 | 1340 | 4 | 4 × 400G (of 64 × 75 GHz C-band slots) | 4 | ROADM (2-degree, 3 at junctions) | 400G ZR+/OTN coherent, FlexO |
| Amman-Zarqa-Mafraq-Jaber | Northern ring | 74 | 1039 | 3 | 3 × 400G (of 64 × 75 GHz C-band slots) | 0 | ROADM (2-degree, 3 at junctions) | 400G ZR+/OTN coherent, FlexO |
| Mafraq-Ramtha-Irbid | Northern ring | 52 | 1039 | 3 | 3 × 400G (of 64 × 75 GHz C-band slots) | 0 | ROADM (2-degree, 3 at junctions) | 400G ZR+/OTN coherent, FlexO |
| Irbid-Jerash-Amman (R35) | Northern ring | 68 | 1039 | 3 | 3 × 400G (of 64 × 75 GHz C-band slots) | 0 | ROADM (2-degree, 3 at junctions) | 400G ZR+/OTN coherent, FlexO |
| King's Highway Madaba-Karak-Tafilah-Petra-Ma'an | spur / regional | 241 | 509 | 2 | 2 × 400G (of 64 × 75 GHz C-band slots) | 3 | FOADM / terminal | 400G ZR+/OTN coherent, FlexO |
| Jordan Valley (R65 north) | spur / regional | 127 | 10 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 1 | FOADM / terminal | 100G coherent |
| Amman-Salt-Deir Alla | spur / regional | 37 | 145 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 0 | FOADM / terminal | 100G coherent |
| Irbid-Ajloun-Jerash | spur / regional | 47 | 79 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 0 | FOADM / terminal | 100G coherent |
| Karak-Qatraneh | spur / regional | 39 | 0 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 0 | FOADM / terminal | 100G coherent |
| Tafilah-Jurf | spur / regional | 34 | 0 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 0 | FOADM / terminal | 100G coherent |
| Amman-Azraq (R40) | spur / regional | 112 | 16 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 1 | FOADM / terminal | 100G coherent |
| Zarqa-Azraq-Safawi | spur / regional | 137 | 0 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 1 | FOADM / terminal | 100G coherent |
| Mafraq-Safawi-Ruwaished (R10) | spur / regional | 302 | 0 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 3 | FOADM / terminal | 100G coherent |
| Quweira-Wadi Rum | spur / regional | 32 | 0 | 2 | 2 × 100G (of 64 × 75 GHz C-band slots) | 0 | FOADM / terminal | 100G coherent |

Demand = busy-hour traffic of the clusters homed on the route × 1.3 peak × 1.5 growth; ring routes carry the **whole ring demand** so any single fibre cut is survivable (OTN 1+1 / ROADM restoration < 50 ms for protected services). The southern ring also carries ≈ 399 Gbps of international transit from the Aqaba cable landing (40 % of internet volume, after 60 % in-country cache hit). EDFA every ≤ 80 km (Raman on > 100 km desert spans), G.652.D fibre, span loss budget 0.22 dB/km + 0.5 dB per splice-km allowance; OSNR ≥ 24 dB end-to-end for 400G 16-QAM. Fill after 3 years ≈ 4 % of slots – ample headroom.

## 4. IP / MPLS design
* **IGP:** IS-IS L2, one instance per domain (metro Amman, north, south, east), multi-instance at PoP border routers; **SR-MPLS with TI-LFA (< 50 ms)**, SRv6-ready hardware; BFD 3 × 10 ms on ring links.
* **Services:** BGP EVPN / L3VPN per function – RAN-CP (N2), RAN-UP (N3), F1 (C-RAN midhaul), O&M, Sync, Enterprise; route reflectors in DC1 / DC2 / Irbid; inter-domain with BGP-LU + seamless MPLS.
* **Slicing:** FlexE / flex-algo hard slices for eMBB-1G (low-delay flex-algo), FWA, enterprise, O&M.
* **QoS (8 classes):** PTP/sync EF-strict · network control CS6 · RAN control + VoNR signalling CS5 · VoNR media EF · eMBB-1G GFBR AF41 · FWA / premium data AF31 · best-effort data BE · O&M AF21; 5QI→DSCP mapping done in DU/CU and UPF; ring links shaped at 95 %.
* **MTU 9,100** end-to-end (GTP-U + SRv6 headroom); IPv6 on all infrastructure links, IPv4 only where a legacy management system needs it.
* **Addressing:** loopbacks 10.255.<domain>.0/24, p2p /31 from 10.254.0.0/16, IPv6 /127 from the infrastructure /40; site subnets summarised per hub.
* **Synchronisation:** ePRTC + GNSS at DC1, DC2, Irbid, Aqaba; PRTC-B at every hub; G.8275.1 full on-path support, every router Class-C boundary clock; budget ±1.5 µs network, ±130 ns relative inside a C-RAN cluster; SyncE everywhere; GNSS holdover 24 h at hubs.
* **Security:** MACsec on owned fibre rings, IPsec (N2/N3) from sites on leased or microwave links, control-plane policing, RTBH / flowspec, out-of-band management network via LTE-free DCN on dedicated VPN.

## 5. Microwave design (360 rural / highway sites)
| Radio configuration | Hops |
|---|---|
| E-band + 18 GHz multiband (carrier-bonded) | 218 |
| 18 GHz XPIC 2+0, 2 × 112 MHz, 2048-QAM | 135 |
| E-band 80 GHz 1+0, 2 GHz channel | 7 |

* Per-hop budget in `microwave_links.csv`: free-space loss, antenna gain, receive level, fade margin, ITU-R P.530/P.838 rain attenuation at R0.01 = 22 mm/h, and a **terrain line-of-sight check on the Copernicus DEM** (60 % of the first Fresnel zone, k = 4/3, antennas 3 m below tower top).
* Result: **251 hops clear, 109 blocked by terrain** – those need a taller structure, a relay / passive repeater, or a different far end (column `terrain_line_of_sight` gives the missing clearance); 0 hops are rain-limited and take the next dish size.
* Hops longer than 16 km deliver ≤ 1.3 Gbps: those sites start with one 100 MHz n78 carrier on the rural 8T8R radio and move to fibre or a second hop when traffic requires.
* Frequency coordination and licensing with TRC per hop; E-band under light licensing where available; XPIC with ACM down to QPSK for 99.999 % of the control / voice traffic class.
