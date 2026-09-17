# LLD-02 – 5G Core Network Design (vendor-neutral)
Cloud-native 5GC (3GPP Rel-17 SBA) sized for **4,204,435 subscribers** and **2,492 Gbps busy-hour user plane**. Tables: `lld/core_nf_sizing.csv`, `lld/core_site_sizing.csv`.

## 1. Dimensioning inputs
| Parameter | Value |
|---|---|
| Provisioned subscribers | 4,204,435 |
| Simultaneously registered | 85 % → 3,573,770 |
| PDU sessions per registered sub | 1.6 (internet + IMS) → 5,718,032 |
| Busy-hour user plane | 2,492 Gbps average, × 1.2 peak-to-mean |
| VoNR subscribers | 60 % → 63,067 Erlang (1 BHCA, 90 s) |
| Design utilisation | 70 % of rated capacity, N+1 per function, geo-redundant 1+1 between DC1 and DC2 |

Busy-hour signalling load (transactions per second): registration 1,191, pdu session 2,978, service request 11,913, handover 7,942, paging 3,971 → **27,995 procedures/s**, ≈ 167,967 SBI transactions/s.

## 2. Network-function sizing (per data centre – each DC carries 100 % on failure of the other)
| Network function | Driver | Unit | Capacity / instance | Instances (N+1) | vCPU |
|---|---|---|---|---|---|
| AMF | 3,573,770 | registered subs | 2,000,000 | 4 | 2560 |
| SMF | 5,718,032 | PDU sessions | 3,000,000 | 4 | 2880 |
| AUSF + UDM | 4,204,435 | provisioned subs | 5,000,000 | 3 | 1440 |
| UDR (subscriber DB) | 4,204,435 | provisioned subs, 3 replicas | 10,000,000 | 2 | 1920 |
| PCF + BSF | 5,718,032 | policy sessions | 3,000,000 | 4 | 2240 |
| CHF (charging) | 5,718,032 | charging sessions | 4,000,000 | 4 | 2560 |
| NRF + NSSF + SCP | 167,967 | SBI transactions/s (≈ 6 per procedure) | 60,000 | 5 | 1600 |
| NEF + NWDAF | 4,204,435 | exposure / analytics | 10,000,000 | 2 | 960 |
| IMS (P/I/S-CSCF, TAS, MRF, SBC) | 2,522,661 | VoNR subs | 1,500,000 | 4 | 4400 |
| SEPP + roaming / interconnect GW | 210,222 | roamers | 1,000,000 | 2 | 480 |
| SMSF + CBCF (SMS, public warning) | 4,204,435 | subs | 10,000,000 | 2 | 400 |
| OSS, observability, LI mediation, security | 4,204,435 | platform | 5,000,000 | 3 | 2700 |

Control plane per DC: **24,140 vCPU** + 25 % platform overhead → **315 servers** (2-socket, 96 usable vCPU, 512 GB RAM, 2 × 100GE). Subscriber database (UDR) synchronously replicated DC1↔DC2, asynchronous third replica in Irbid.

## 3. Site sizing (user plane distributed, control plane central)
| Site | UP share | Peak Gbps | UPF servers (N+1) | CP servers | Total servers | Racks | IT load kW | 400GE ports to transport |
|---|---|---|---|---|---|---|---|---|
| DC1 Amman West | 27.5 % | 822 | 8 | 315 | 323 | 23 | 254 | 6 |
| DC2 Amman East | 27.5 % | 822 | 8 | 315 | 323 | 23 | 254 | 6 |
| Amman Centre edge | 8.0 % | 239 | 3 | 0 | 9 | 3 | 19 | 2 |
| Zarqa edge | 7.0 % | 209 | 3 | 0 | 9 | 3 | 19 | 2 |
| Irbid regional DC | 15.0 % | 449 | 5 | 0 | 17 | 4 | 25 | 4 |
| Aqaba regional DC | 8.0 % | 239 | 3 | 0 | 15 | 3 | 23 | 2 |
| Regional PoPs (Karak, Ma'an, Mafraq) | 7.0 % | 209 | 3 | 0 | 9 | 3 | 19 | 2 |

UPF server: 2 × 100GE SmartNIC, ≈ 180 Gbps per server at 70 % load with full feature set (charging, LI, DPI-lite). UPF selection by TAC / DNAI so traffic breaks out at the nearest site; CDN caches and MEC hosts co-located on the N6 side of every UPF site.

## 4. Logical design
* **PLMN** 416-xx (MCC 416 Jordan; MNC from TRC). **TAC**: one per hub cluster (150 + rural TACs), TA lists sized ≤ 16 TACs to keep paging below 3,971 /s.
* **Slices (S-NSSAI):** SST 1 / SD 000001 eMBB-1G (GFBR 1 Gbps tariff, 5QI 6/8/9 + dedicated GBR flow for the premium tier) · SST 1 / SD 000002 FWA · SST 1 / SD 000010 enterprise / private DNNs · SST 2 URLLC (future) · SST 1 / SD 0000FF public safety · O&M.
* **DNNs:** internet, ims, fwa, enterprise-<customer>, iot, sos.
* **Addressing:** IPv6-first. UE pools: one /40 per UPF site from the operator's RIPE NCC /29–/32 allocation (a /64 per UE session), IPv4 via NAT64/464XLAT and a CGNAT pool (≈ 1 public IPv4 per 64 users). Infrastructure: loopbacks 10.255.0.0/16, SBI 10.10.0.0/16 per DC, N2/N3 10.20.0.0/14 regionalised, O&M 10.250.0.0/16, all dual-stack with IPv6 ULA-free GUA on N3.
* **Naming / discovery:** 3GPP FQDNs (`amf1.set01.region01.amf.5gc.mnc0xx.mcc416.3gppnetwork.org`), NRF hierarchical (one per DC + PLMN-level), SCP model C for indirect communication, DNS anycast pairs in every site.
* **Voice:** IMS with VoNR only (no LTE layer in a pure-SA network) – EVS-WB, SRVCC not applicable; emergency calls on n28/n3; interconnect to other operators through SBC pair in DC1/DC2 (SIP-I / SIP), roaming through SEPP (N32) and IPX; devices without VoNR are a launch risk (see deployment risk register).
* **Security:** zones Untrust (N6/internet) – DMZ (SEPP, SBC, NEF) – Core SBA – O&M – LI; mutual TLS on all SBI with operator PKI; SUCI concealment (profile A) enabled; N2/N3 protected by IPsec from D-RAN sites / MACsec on owned fibre; firewalls + DDoS scrubbing on N6 (≥ 20 % of N6 capacity); LI (X1/X2/X3) mediation in both DCs.
* **Cloud platform:** Kubernetes CaaS on bare metal, SR-IOV / DPDK for UPF, separate clusters per zone, GitOps lifecycle, in-service upgrade with canary; observability (metrics, traces, logs) and NWDAF feeding the capacity trigger (sector PRB > 20 %).
* **Charging / policy:** converged CHF (online + offline), PCF rules for fair-use shaping that protects the single-user 1 Gbps experience; BSS integration over REST/TMF APIs.

## 5. Build phases
C0 facilities (M1–M2) → C1 control plane, UPF pool 1, IMS, first call (M2–M4) → C2 geo-redundancy tests, Amman Centre + Zarqa edge (M6–M9) → C3 Irbid and Aqaba regional DCs (M8–M12) → C4 UPF capacity steps of ≈ 400 Gbps per 600 accepted city sites (M13–M30) → C5 final dimensioning, DR drill, hand-over (M31–M36).
