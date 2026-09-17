#!/usr/bin/env python3
"""Writes the deployment document set (Markdown) from deployment/rollouts.json. Run after deployment_plan.py."""
import csv, json, math, os
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEP = os.path.join(ROOT, "deployment")
RO = json.load(open(os.path.join(DEP, "rollouts.json"), encoding="utf-8"))
S = json.load(open(os.path.join(ROOT, "output", "summary.json")))["summary"]
sched = list(csv.DictReader(open(os.path.join(DEP, "rollout_schedule.csv"), encoding="utf-8")))
site_ro = {r["site_id"]: r["rollout"] for r in csv.DictReader(open(os.path.join(DEP, "rollout_sites.csv"), encoding="utf-8"))}
border = Counter(site_ro[r["site_id"]] for r in csv.DictReader(open(os.path.join(ROOT, "output", "sectors.csv"), encoding="utf-8")) if r["border_coordination"] == "1")
f = lambda n: f"{n:,}"
def w(name, txt):
    open(os.path.join(DEP, name), "w", encoding="utf-8").write(txt.strip() + "\n"); print("wrote", name)

# ------------------------------------------------------------------ resources per rollout
def res(x):
    civil = x["rooftop"] / 2 + x["mono"] / 1 + x["tower"] / 0.7          # crew-months
    fib = x["access_km"] + x["agg_km"] + x["spur_km"]
    return dict(install=math.ceil(x["sites"] / (3 * 7)), civil=math.ceil(civil / 3), fiber=math.ceil(fib / (3 * 4)), bb=math.ceil(x["bb_km"] / (4 * 25)),
                ssv=math.ceil(x["sites"] / (3 * 60)), opt=max(2, math.ceil(x["sites"] / 150)), acq=math.ceil(x["sites"] / (3 * 12)), fib_km=fib)
for x in RO: x["res"] = res(x)
peak = {k: max(x["res"][k] for x in RO) for k in RO[0]["res"]}
Y = lambda a, b: [x for x in RO if a <= x["r"] <= b]
tot = lambda k: sum(x[k] for x in RO)

gantt = "```mermaid\ngantt\n  dateFormat YYYY-MM\n  axisFormat %b %y\n  title Jordan 5G SA – 36-month deployment (10 rollouts)\n  section Programme\n" \
        "  Mobilisation, vendor contracts, spectrum        :m0, 2027-01, 3M\n  5G core DC1/DC2 build and test                 :m1, 2027-01, 4M\n  Final optimisation, acceptance, hand-over      :m9, 2029-10, 3M\n"
for x in RO:
    a = [r for r in sched if r["rollout"] == x["id"]]
    m0 = min(int(r["start_month"]) for r in a); y0, mo0 = 2027 + (m0 - 1) // 12, (m0 - 1) % 12 + 1
    y1, mo1 = 2027 + (x["m_from"] - 1) // 12, (x["m_from"] - 1) % 12 + 1
    gantt += f"  section {x['id']} ({x['sites']} sites)\n  Acquire, design, civil, fiber :a{x['r']}, {y0}-{mo0:02d}, {x['m_from'] - m0}M\n  On-air window                :crit, b{x['r']}, {y1}-{mo1:02d}, 3M\n  Optimise and accept          :c{x['r']}, after b{x['r']}, 2M\n"
gantt += "```"

ro_table = "| Rollout | On-air window | Sites | DU | U | SU | Rural | Hwy | Hubs | Access + agg fiber km | Backbone km | Indoor venues | Cum. sites | Cum. pop. covered | Cum. 1 Gbps km² | Main areas |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
for x in RO:
    c = x["cls"]
    ro_table += f"| **{x['id']}** | {x['window']} | {x['sites']} | {c.get('DU', 0)} | {c.get('U', 0)} | {c.get('SU', 0)} | {c.get('R', 0)} | {c.get('HW', 0)} | {x['hubs']} | {x['access_km'] + x['agg_km']} | {x['bb_km']} | {len(x['venues'])} | {f(x['cum_sites'])} | {x['cum_pop_pct']} % | {f(x['cum_1g_km2'])} | {', '.join(n for n, _ in x['clusters'][:4])} |\n"

# ------------------------------------------------------------------ 00 master plan
w("00_Master_Deployment_Plan.md", f"""
# Jordan 5G SA – Master Deployment Plan
**10 rollouts · 36 months · {f(S['sites_total'])} macro sites · {f(S['sectors_total'])} sectors · ≈ {f(S['access_fiber_km'] + S['agg_fiber_km'] + S['backbone_km'] + S['metro_core_km'] + S['spur_km'])} km fiber · {S['indoor']['venues']} indoor venues**

Programme month 1 (M1) is assumed to be **January 2027**; all dates shift with the actual contract-effective date (`START` in `tools/deployment_plan.py`). This plan implements the nominal design in `5G_Jordan_Design_Report.md`; all quantities are generated from it and regenerate with `python tools/deployment_plan.py && python tools/deployment_docs.py`.

## Document set
| # | Document | Purpose |
|---|---|---|
| 00 | Master Deployment Plan (this file) | Strategy, sequencing, schedule, governance |
| 01 | `01_Programme_Schedule.md` | Month-by-month schedule, milestones, stage gates |
| 02 | `02_Transport_and_Core_Deployment.md` | Core, backbone, hub and ring build sequence |
| 03 | `03_Site_Implementation_Standard.md` | Site process from survey to acceptance, checklists, 1 Gbps acceptance test |
| 04 | `04_Indoor_Deployment_Plan.md` | Venue programme by rollout |
| 05 | `05_Resource_and_Procurement_Plan.md` | Crews, lead times, logistics, call-off calendar |
| 06 | `06_Risk_Register.md` | Risks, owners, mitigations |
| LLD | `../lld/LLD-01…03` | Equipment-level design: RAN, core, transport (ports, DWDM, microwave) |
| RO | `RO-01 … RO-10_Work_Package.md` | One work package per rollout: scope, BoQ, prerequisites, dates, exit criteria |
| Data | `Jordan_5G_Deployment_Plan.xlsx`, `rollout_sites.csv`, `rollout_boq.csv`, `rollout_schedule.csv`, `rollout_venues.csv` | Site-level allocation, bill of quantities, Gantt |
| Map | `index.html` → layer “Rollout phase” + rollout slider | Cumulative build on the satellite map |

## 1. Deployment strategy
1. **Build unit = one hub cluster** (DU hotel / pre-aggregation hub with all its access rings, ≈ 40 sites). Fiber, hub and radio sites of a unit are always in the same rollout, so no site waits for transport and no ring is left open.
2. **Value first, inside-out.** Units are ranked by service class (dense urban > urban > suburban), strategic weight (Amman–Zarqa metro, Irbid, Aqaba gateway, Dead Sea and Petra tourism) and distance from the city centre. Each city therefore grows as a contiguous 1 Gbps island – no isolated sites with a poor-SINR edge.
3. **Transport leads radio.** A unit cannot start before the backbone route feeding its city is lit (see 02). Highway sites go on air one rollout after their route, using the backbone add/drop points.
4. **Ramp, plateau, taper.** {RO[0]['sites']} → {RO[1]['sites']} → {RO[2]['sites']} sites in the first three rollouts while teams, logistics and processes mature, a plateau of ≈ 720–770 sites per rollout (≈ 250 per month) through RO-04…RO-08, taper in RO-09/10 when work moves to distant, low-density areas.
5. **Rural and highway coverage is not left to the end.** National highway corridors go on air one rollout after their backbone route (from RO-04); rural packages start in RO-07 so coverage obligations are met before programme close.
6. **Indoor follows macro by one rollout** so the donor/neighbour layer exists when a venue is integrated; landmark venues (QAIA, Abdali, major malls and 5-star hotels) start in RO-02.
7. **Every rollout ends with a formal cluster acceptance** against the 1 Gbps KPI (03 §6) before commercial launch in that area.

## 2. The ten rollouts
{ro_table}
*Cumulative population = share of Jordan’s population living inside the footprint built so far (design-model estimate).*

**Year 1 (2027, RO-01…RO-03): {f(sum(x['sites'] for x in Y(1, 3)))} sites.** Core live in M3–M4; all of dense-urban Amman and Irbid core, inner urban Amman, Aqaba city; northern backbone ring and Desert Highway lit. ≈ {Y(1, 3)[-1]['cum_pop_pct']} % of population covered.
**Year 2 (2028, RO-04…RO-07): {f(sum(x['sites'] for x in Y(4, 7)))} sites.** Remaining urban Amman, Zarqa, Russeifa, Irbid; most governorate capitals (Ajloun and the last Salt/Madaba clusters follow in RO-08); Dead Sea and Petra; southern backbone ring closed; national highways; first rural packages. ≈ {Y(4, 7)[-1]['cum_pop_pct']} %.
**Year 3 (2029, RO-08…RO-10): {f(sum(x['sites'] for x in Y(8, 10)))} sites.** Suburban rings, remaining rural, eastern desert corridors, n258 hotspot layer in dense urban, indoor phase completion, network-wide optimisation and hand-over. {RO[-1]['cum_pop_pct']} %.

## 3. Timeline
{gantt}

Each rollout runs the same 10-month pipeline, overlapping with its neighbours (three to four rollouts are always in flight):

| Offset from on-air start (T) | Activity |
|---|---|
| T−6 … T−3 | Nominal release, technical site surveys (TSSR), acquisition, permits |
| T−5 … T−3 | Detailed RF and transport design freeze, material call-off |
| T−4 … T−1 | Civil works, power, fiber to hubs and rings |
| T−2 … T | Hub / DU-hotel and router commissioning |
| T−1 … T+2 | Radio installation, commissioning, integration to 5GC |
| T … T+2 | Single-site verification |
| T+1 … T+4 | Cluster optimisation and acceptance |
| T+3 … T+4 | Commercial launch of the area, hand-over to operations |

RO-01 is compressed (acquisition starts in M1): it must use **existing rooftops and towers under sharing agreements** – this is the first critical-path item.

## 4. Critical path and prerequisites
| # | Prerequisite | Needed by | Owner |
|---|---|---|---|
| 1 | Spectrum licence: n78 3×100 MHz, n28, n1/n3, n258; type approval | M1 (RO-01 radios ordered against exact carrier plan) | Regulatory |
| 2 | RAN / core / transport vendor contracts, frame pricing, delivery SLAs | M1 | Procurement |
| 3 | Tower-company / operator site-sharing and dark-fiber framework agreements | M1–M2 | Commercial |
| 4 | DC1 and DC2 ready (power, cooling, cloud platform), 5GC + IMS integrated, first call | M3–M4 | Core |
| 5 | Amman metro core ring and first 6 hubs lit | M3 | Transport |
| 6 | Municipality (GAM, ASEZA, municipalities) master permit / fast-track process, EMF compliance procedure | M2 | Site acquisition |
| 7 | Power utility (JEPCO / IDECO / EDCO) connection framework | M2 | Civil |
| 8 | Northern backbone ring (RO-02), Desert Highway (RO-03), Wadi Araba – Dead Sea (RO-04) | start of the named rollout | Transport |
| 9 | Cross-border coordination for {S['border_sectors']} flagged sectors | before the affected rollout goes on air | Regulatory |
| 10 | 3-CC n78 capable devices / CPE in the market | commercial launch RO-01 (M7) | Marketing |

## 5. Governance
* **Programme board** (monthly): sponsor, CTO, CFO, vendor executives – budget, stage gates, scope changes.
* **PMO** (weekly): rollout managers (one per active rollout), streams for Acquisition, Civil, Transport, RAN, Core, Indoor, Optimisation, HSE/Quality, Logistics.
* **Stage gates per rollout:** G1 design freeze (T−3) · G2 ready-for-installation ≥ 80 % sites (T−1) · G3 on-air ≥ 95 % (T+3) · G4 cluster acceptance (T+4) · G5 hand-over to operations.
* **RACI (summary):** operator – accountable for spectrum, acquisition approvals, acceptance; RAN vendor – responsible for install, commissioning, SSV, optimisation; transport contractor – fiber and routers; tower-co – passive infrastructure; PMO – integrated schedule and reporting.
* **Reporting KPIs:** sites acquired / RFI / installed / on-air / accepted vs plan (weekly S-curve per rollout), fiber km built, first-time-right install rate (target ≥ 92 %), SSV pass rate, % drive-test bins ≥ 1 Gbps, LTIFR, material availability ≥ 98 % at call-off.

## 6. Peak resources (see 05)
Peak in RO-05…RO-07: ≈ {peak['install']} radio install crews, {peak['civil']} civil crews, {peak['fiber']} urban fiber crews, {peak['acq']} acquisition agents, {peak['ssv']} SSV teams and {peak['opt']} optimisation teams; peak build rate ≈ {max(x['rate'] for x in RO)} sites/month and ≈ {max(x['res']['fib_km'] for x in RO) // 3} km of access fiber per month.

## 7. Planning assumptions
* ≥ 50 % of urban sites reuse existing rooftops/towers (sharing) – without this the acquisition lead time moves from 3 to 6–9 months and RO-01…RO-03 slip by one quarter.
* Backbone: leased / swapped dark fiber (existing national OPGW and operator routes) is acceptable for first light; own-build follows within the same rollout year.
* Working calendar 22 days/month; Ramadan and summer-heat productivity factor 0.85 applied to Q2 rollouts in the resource plan buffer.
* Quantities come from a nominal design: expect ±10 % on site count after surveys; each work package is re-baselined at gate G1.
""")

# ------------------------------------------------------------------ 01 schedule
rows = "| Month | Date | Milestones |\n|---|---|---|\n"
MS = {1: ["Contract effective; PMO mobilised; RO-01 acquisition starts; long-lead orders placed"], 2: ["Sharing and dark-fiber frameworks signed; warehouse operational (Amman)"],
      3: ["DC1/DC2 ready; metro core ring lit; first hubs commissioned"], 4: ["5GC + IMS first call; **first site on air**"], 7: ["**Commercial launch – Amman core** (RO-01 accepted)"],
      12: ["Year-1 close: Amman/Irbid dense urban + Aqaba on air; Desert Highway backbone lit"], 15: ["Southern backbone ring closed (Wadi Araba – Dead Sea)"],
      18: ["Half-way: ≥ 50 % population covered"], 24: ["Year-2 close: urban layer of all major cities on air, rural programme started"], 28: ["n258 hotspot layer starts (dense urban)"],
      33: ["**Last site on air**"], 36: ["Final acceptance, as-built documentation, hand-over to operations; programme close"]}
def mdate(m): import datetime as dt; return dt.date(2027 + (m - 1) // 12, (m - 1) % 12 + 1, 1).strftime("%b %Y")
for m in range(1, 37):
    ev = list(MS.get(m, []))
    for x in RO:
        if x["m_from"] == m: ev.append(f"{x['id']} on-air window opens ({x['sites']} sites)")
        if x["m_to"] + 1 == m: ev.append(f"{x['id']} gate G3 (≥ 95 % on air)")
        if x["m_from"] + 4 == m: ev.append(f"{x['id']} cluster acceptance G4 / area launch")
        if max(1, x["m_from"] - 6) == m and m > 1: ev.append(f"{x['id']} nominal release, surveys and acquisition start")
        if x["m_from"] - 3 == m: ev.append(f"{x['id']} gate G1 design freeze, material call-off")
    rows += f"| M{m} | {mdate(m)} | {'; '.join(ev) if ev else '–'} |\n"
act = "| Rollout | Activity | Start | End |\n|---|---|---|---|\n" + "".join(f"| {r['rollout']} | {r['activity']} | M{r['start_month']} {r['start']} | M{r['end_month']} {r['end']} |\n" for r in sched)
w("01_Programme_Schedule.md", f"""
# 01 – Programme Schedule (36 months, 10 rollouts)
{gantt}

## Month-by-month milestones
{rows}
## S-curve (cumulative sites on air at end of each window)
| Rollout | End of window | Cumulative sites | % of programme | Cum. population covered |
|---|---|---|---|---|
{''.join(f"| {x['id']} | {x['window'].split(' – ')[1]} | {f(x['cum_sites'])} | {100 * x['cum_sites'] / S['sites_total']:.0f} % | {x['cum_pop_pct']} % |" + chr(10) for x in RO)}
## Activity schedule per rollout
{act}
The colour Gantt is in `Jordan_5G_Deployment_Plan.xlsx` (sheet “Schedule (Gantt)”).
""")

# ------------------------------------------------------------------ 02 transport & core
w("02_Transport_and_Core_Deployment.md", f"""
# 02 – Transport and Core Deployment Plan

## 1. 5G core
| Phase | Months | Scope |
|---|---|---|
| C0 | M1–M2 | DC1 (Amman West) and DC2 (Amman East) facility readiness, cloud platform, IP fabric, security zones |
| C1 | M2–M4 | 5GC control plane (AMF, SMF, AUSF, UDM/UDR, PCF, NRF, NSSF, SCP, CHF), UPF pool 1, IMS/VoNR, OSS, lawful intercept; interconnect and roaming tests; **first call M4** |
| C2 | M6–M9 | Geo-redundancy failover tests DC1↔DC2; Amman Centre and Zarqa edge UPF + CDN (with RO-02) |
| C3 | M8–M12 | Irbid regional DC: edge UPF/MEC, UDR replica (with RO-02/03); Aqaba regional DC and international gateway (with RO-03) |
| C4 | M13–M30 | UPF capacity steps following traffic: +400 Gbps per 600 accepted city sites; slice catalogue (eMBB-1G GFBR, FWA, enterprise); NEF exposure |
| C5 | M31–M36 | Final dimensioning to ≈ {f(S['bh_total_gbps'])} Gbps busy hour (N+1), DR drill, hand-over |

## 2. Backbone and metro core (must be lit before the dependent rollout opens)
| Rollout | Routes lit | Route km |
|---|---|---|
{''.join(f"| {x['id']} | {'; '.join(x['bb_routes']) if x['bb_routes'] else '–'} | {x['bb_km']} |" + chr(10) for x in RO)}
Sequence logic: metro core (RO-01) → northern ring Amman–Zarqa–Mafraq–Irbid–Jerash (RO-02) → Desert Highway to Aqaba incl. cable-landing access (RO-03) → Wadi Araba–Dead Sea closes the southern national ring (RO-04) → King’s Highway and Salt (RO-05) → Jordan Valley, Ajloun (RO-06) → cross-links and Azraq (RO-07) → eastern desert and Wadi Rum (RO-08). First light may use leased/swapped dark fiber; DWDM/OTN nodes at every PoP; ring protection verified (< 50 ms) before the rollout gate G2.

## 3. Hubs, aggregation and access rings
| Rollout | Hubs commissioned | Hub routers | Access-ring km | Aggregation km | Spur km | Microwave hops | Pooled DUs (C-RAN) | Site DUs (D-RAN) |
|---|---|---|---|---|---|---|---|---|
{''.join(f"| {x['id']} | {x['hubs']} | {x['hub_routers']} | {x['access_km']} | {x['agg_km']} | {x['spur_km']} | {x['mw']} | {x['du_cran']} | {x['du_dran']} |" + chr(10) for x in RO)}| **Total** | {tot('hubs')} | {tot('hub_routers')} | {f(tot('access_km'))} | {tot('agg_km')} | {tot('spur_km')} | {tot('mw')} | {tot('du_cran')} | {f(tot('du_dran'))} |

Build order inside a rollout: (1) hub room (power 2N, cooling, GNSS, racks) → (2) aggregation ring to PoP, routers, PTP grandmaster/boundary-clock chain verified (±1.5 µs; ±130 ns inside C-RAN cluster) → (3) access rings, both directions spliced and OTDR-tested before radio integration → (4) DU pool commissioning → (5) sites. A ring is accepted only when closed: single-homed sites are not counted as on-air for gate G3.

Fiber acceptance: OTDR both directions 1310/1550 nm, splice ≤ 0.1 dB, span loss within budget for 25GE-LR / eCPRI (≤ 10 km fronthaul), as-built GIS route uploaded.
""")

# ------------------------------------------------------------------ 03 site implementation standard
w("03_Site_Implementation_Standard.md", """
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
""")

# ------------------------------------------------------------------ 04 indoor
vt = ""
for x in RO:
    for v in x["venues"]: vt += f"| {x['id']} | {x['window']} | {v[0]} | {v[1]} | {v[2]} | {v[3]} |\n"
w("04_Indoor_Deployment_Plan.md", f"""
# 04 – Indoor Deployment Plan
{S['indoor']['venues']} venues · {f(S['indoor']['prru'])} n78 pRRUs · {S['indoor']['mmw']} n258 heads. A venue is scheduled one rollout after the macro cluster around it (earliest RO-02) so neighbours, handover and leakage control can be tuned against a live outdoor layer.

| Rollout | Venues | pRRU | n258 heads |
|---|---|---|---|
{''.join(f"| {x['id']} | {len(x['venues'])} | {x['prru']} | {x['vmmw']} |" + chr(10) for x in RO)}
## Venue schedule
| Rollout | Window | Venue | Type | n78 pRRU | n258 heads |
|---|---|---|---|---|---|
{vt}
## Per-venue process (14–18 weeks)
1. Access agreement with the owner (commercial model: neutral-host ready, operator-funded) – 4–6 weeks, started at T−6.
2. Walk survey, floor plans, 3-D indoor prediction, pRRU/RHUB positions, cable routes; owner design approval – 3 weeks.
3. Installation out of trading hours: CAT6A/hybrid fiber, RHUBs in IDF rooms, DU in MDF, dual diverse fiber to hub – 4–6 weeks.
4. Commissioning, walk test: ≥ 95 % of public area ≥ 1 Gbps, SS-RSRP ≥ −95 dBm, leakage outside ≤ −105 dBm at 10 m or 10 dB below macro, lifts and car parks VoNR continuity – 1–2 weeks.
5. Hand-over with as-built drawings and owner O&M contact sheet.
Phase 2 (after RO-10, outside this plan’s BoQ): every building > 10,000 m² or > 8 floors identified from the building-height layer.
""")

# ------------------------------------------------------------------ 05 resources & procurement
rt = "| Rollout | Sites | Acquisition agents | Civil crews | Urban fiber crews | Backbone crews | Install crews | SSV teams | Optimisation teams |\n|---|---|---|---|---|---|---|---|---|\n"
for x in RO:
    r = x["res"]; rt += f"| {x['id']} | {x['sites']} | {r['acq']} | {r['civil']} | {r['fiber']} | {r['bb']} | {r['install']} | {r['ssv']} | {r['opt']} |\n"
boq = list(csv.reader(open(os.path.join(DEP, "rollout_boq.csv"), encoding="utf-8")))
bt = "| " + " | ".join(boq[0]) + " |\n|" + "---|" * len(boq[0]) + "\n" + "".join("| " + " | ".join(r) + " |\n" for r in boq[1:])
w("05_Resource_and_Procurement_Plan.md", f"""
# 05 – Resource and Procurement Plan

## 1. Field resources per rollout
{rt}
Productivity norms: acquisition agent 12 sites / 3 months; civil crew 2 rooftops, 1 monopole or 0.7 tower per month; urban fiber crew 4 route-km/month (micro-trench / existing duct); backbone crew 25 km/month (plough / duct along highways); install crew 7 sites/month; SSV team 60 sites/month; one optimisation team per 150 sites. Three to four rollouts overlap, so **programme peak ≈ 1.6 × the single-rollout peak** for acquisition and civil, 1.2 × for install. Minimum three civil and two fiber contractors to avoid single-supplier dependency; regional sub-contractors for Irbid, Aqaba and the south.

## 2. Bill of quantities by rollout
{bt}
## 3. Lead times and call-off calendar
| Item | Lead time | Order rule |
|---|---|---|
| 64T64R AAU, RRUs, DU/BBU | 16–20 weeks | frame order M1; firm call-off per rollout at gate G1 (T−3) with 10 % buffer; RO-01…RO-03 called off together at M1 |
| Passive antennas, RET, jumpers | 10–12 weeks | same as radio |
| Routers, DWDM/OTN | 16–24 weeks | backbone nodes ordered one rollout earlier than radio |
| Fiber cable (48/96-core), ducts | 8–12 weeks | annual volume order, monthly deliveries |
| Monopoles / towers (local steel) | 8–10 weeks | rolling 3-month forecast to two local fabricators |
| Rectifiers, Li-ion batteries, solar hybrid | 12–16 weeks | with radio |
| pRRU / RHUB / mmWave heads | 16 weeks | per venue design approval |
| Core / cloud hardware | 12–16 weeks | M1 (C1), then per capacity step |

## 4. Logistics
Central warehouse Amman (Sahab / Al-Muwaqqar industrial area) from M2; regional cross-docks Irbid (RO-02) and Aqaba (RO-03, also port of entry with ASEZA customs regime). Kitting per site (one pallet set per site, barcoded to the site ID in `rollout_sites.csv`); reverse logistics for packaging and faulty units; 2 % spares pool growing with the installed base.

## 5. People and competence
PMO ≈ 45 staff at peak. Vendor training academy in M1–M3: 5G SA commissioning, massive-MIMO beam configuration, eCPRI/PTP, work-at-height. Local content target ≥ 70 % of field hours.
""")

# ------------------------------------------------------------------ 06 risk register
w("06_Risk_Register.md", f"""
# 06 – Risk Register
P = probability, I = impact (1 low – 5 high).

| # | Risk | P | I | Rollouts | Mitigation | Owner |
|---|---|---|---|---|---|---|
| 1 | Less than 300 MHz of n78 awarded | 3 | 5 | all | Design fallback: 200 MHz gives ≈ 78 % of bins ≥ 1 Gbps – bring the n258 layer forward from RO-09 to RO-03 in dense urban, enable DL CoMP in C-RAN clusters; adjust commercial promise by area | Regulatory / CTO |
| 2 | Site acquisition slower than 3 months (rooftop owners, municipality permits) | 4 | 4 | RO-01…RO-06 | Sharing frameworks first, 2 candidates per nominal, GAM/ASEZA fast-track MoU, standard lease and rent card, acquisition starts T−6 | Acquisition |
| 3 | Hilltop/rooftop structural limits for 64T64R + passive antenna (≈ 75 kg per sector) | 3 | 3 | city rollouts | Structural screening in TSSR, lightweight poles, split to two roofs, 32T32R variant where loading fails | Civil |
| 4 | Fiber right-of-way and street-works permits delay rings | 4 | 4 | all city rollouts | Use existing ducts / lease dark fiber first, micro-trenching approval, ring may open on E-band protection for ≤ 60 days | Transport |
| 5 | Backbone route not lit before dependent rollout | 3 | 4 | RO-02…RO-05, RO-08 | Leased capacity as first light; backbone ordered one rollout ahead; gate G2 checks | Transport |
| 6 | Supply-chain delay of AAUs / routers | 3 | 4 | all | Frame agreement with delivery SLA and penalties, three rollouts of buffer stock in year 1, dual-source routers | Procurement |
| 7 | Grid connection lead time; rural sites off-grid | 3 | 3 | RO-04…RO-09 | Utility framework, temporary generator ≤ 60 days, solar-hybrid standard design for rural/highway | Civil |
| 8 | Cross-border interference / coordination ({S['border_sectors']} sectors) and TDD frame misalignment with neighbours | 3 | 3 | RO-03…RO-06 (Aqaba, Jordan Valley, Ramtha) | Early TRC coordination, +2° tilt and power limits already in design, common DDDSU frame, monitoring probes | Regulatory / RF |
| 9 | 1 Gbps cluster acceptance fails (model vs reality in hilly, stone-built Amman) | 3 | 4 | RO-01…RO-03 | CW calibration campaign in M1–M3, RO-01 used as pilot with 3-week optimisation buffer, infill budget 3 % of sites | RF |
| 10 | Device ecosystem: few UEs support 3CC n78 CA | 3 | 4 | launch | CPE-first launch (FWA), device certification programme with OEMs, 2CC fallback marketed by area | Marketing |
| 11 | Core readiness slips (M4 first call) | 2 | 5 | RO-01 | Vendor-hosted staging core from M2, phased NF activation, parallel DC2 build | Core |
| 12 | HSE incident at height or in street works | 2 | 5 | all | Certification, permit-to-work, audits 10 % of sites weekly, stop-work authority | HSE |
| 13 | Community / EMF objections | 3 | 2 | city rollouts | Public EMF measurements portal, camouflage catalogue, municipality engagement | Corporate affairs |
| 14 | Resource peak (≈ {peak['install']} install + {peak['civil']} civil crews) not available locally | 3 | 3 | RO-04…RO-08 | Training academy M1–M3, regional contractors, levelled quotas (≤ 770 sites per rollout) | PMO |
| 15 | Currency / budget overrun from survey-driven scope change (±10 % sites) | 3 | 3 | all | Re-baseline at each G1, contingency 8 %, change control board | PMO / Finance |
| 16 | Indoor venue owners delay access | 3 | 2 | RO-02…RO-10 | Start agreements at T−6, neutral-host offer, substitute venues from phase-2 list | Indoor |
""")

# ------------------------------------------------------------------ RO work packages
for x in RO:
    c, r = x["cls"], x["res"]
    a = [q for q in sched if q["rollout"] == x["id"]]
    prereq = []
    if x["r"] == 1: prereq += ["Spectrum licence and type approval", "DC1/DC2 core ready, first call (M4)", "Amman metro core ring lit", "Site-sharing and dark-fiber frameworks signed", "CW model-calibration campaign complete"]
    else: prereq += [f"{RO[x['r'] - 2]['id']} gate G2 passed (teams and process release)"]
    if x["bb_routes"]: prereq.append("Backbone lit in this rollout before G2: " + "; ".join(x["bb_routes"]))
    need = sorted({q for y in RO[:x["r"] - 1] for q in y["bb_routes"]})
    if need: prereq.append("Backbone already in service from earlier rollouts: " + "; ".join(n.split(" (")[0] for n in need[:8]) + (" …" if len(need) > 8 else ""))
    if border.get(x["id"]): prereq.append(f"Cross-border coordination filed for {border[x['id']]} flagged sectors in this rollout")
    notes = []
    if c.get("DU", 0) > 50: notes.append("Dense-urban rooftops: structural screening and owner negotiations dominate; C-RAN fronthaul ≤ 10 km to the DU hotel must be verified per site.")
    if x["rooftop"] > x["sites"] * 0.5: notes.append("More than half the sites are rooftops – prioritise existing shared rooftops; antenna must clear local roofs by 8 m (heights in `rollout_sites.csv`).")
    if c.get("R", 0) + c.get("HW", 0) > 50: notes.append("Rural/highway towers: 45 m lattice, solar-hybrid power where off-grid, backbone add/drop or microwave per `backhaul` column; security fencing standard.")
    if any("Aqaba" in n for n, _ in x["clusters"][:5]): notes.append("Aqaba: ASEZA permitting and customs regime; sectors facing Eilat/Taba carry +2° tilt and coordination limits.")
    if any(n in ("Dead Sea", "Wadi Musa / Petra") for n, _ in x["clusters"]): notes.append("Tourism zones (Dead Sea / Petra): camouflage structures, heritage-authority approval (PDTRA for Petra), work outside peak season where possible.")
    if x["n258"]: notes.append(f"Includes {x['n258']} n258 street small cells for dense-urban hotspots (municipal street-furniture agreement required).")
    if x["r"] == 1: notes.append("Pilot rollout: 3-week extra optimisation buffer; acceptance results recalibrate the prediction model for all later rollouts.")
    if x["r"] == 10: notes.append("Final rollout: network-wide parameter audit, neighbour clean-up, as-built documentation and O&M hand-over run in parallel (M34–M36).")
    w(f"{x['id']}_Work_Package.md", f"""
# {x['id']} – Work Package
**On-air window: {x['window']} (M{x['m_from']}–M{x['m_to']}) · {x['sites']} sites · {x['sectors']} sectors · {x['hubs']} hubs · {x['access_km'] + x['agg_km'] + x['spur_km']} km access/aggregation fiber · {x['bb_km']} km backbone · {len(x['venues'])} indoor venues**

After this rollout: {f(x['cum_sites'])} sites on air ({100 * x['cum_sites'] / S['sites_total']:.0f} % of programme), ≈ {x['cum_pop_pct']} % of population covered, {f(x['cum_1g_km2'])} km² of 1 Gbps footprint. Site list: filter `rollout = {x['id']}` in `rollout_sites.csv` / workbook sheet “Sites”; on the map choose “Rollout phase” and move the slider to {x['r']}.

## 1. Scope
| Class | Sites | | Site type | Sites |
|---|---|---|---|---|
| Dense urban | {c.get('DU', 0)} | | Rooftop | {x['rooftop']} |
| Urban | {c.get('U', 0)} | | Monopole / greenfield | {x['mono']} |
| Suburban | {c.get('SU', 0)} | | Lattice tower | {x['tower']} |
| Rural | {c.get('R', 0)} | | | |
| Highway | {c.get('HW', 0)} | | **Total** | **{x['sites']}** |

**Areas:** {', '.join(f'{n} ({k})' for n, k in x['clusters'])}.
**Governorates:** {', '.join(f'{n} {k}' for n, k in x['gov'])}.

## 2. Work packages (build units)
| Unit | Type | Cluster / route | Sites |
|---|---|---|---|
{''.join(f"| {u[0]} | {u[1]} | {u[2]} | {u[3]} |" + chr(10) for u in x['units'])}
## 3. Bill of quantities
| Item | Qty | | Item | Qty |
|---|---|---|---|---|
| n78 64T64R AAU | {x['aau64']} | | Hubs / DU hotels | {x['hubs']} |
| n78 8T8R (rural) | {x['aau8']} | | Hub aggregation routers | {x['hub_routers']} |
| Passive 2L4H antenna + RET | {x['passive']} | | Cell-site routers 25GE | {x['csr']} |
| n28 RRU | {x['rru_low']} | | Access-ring fiber km | {x['access_km']} |
| n1/n3 RRU | {x['rru_mid']} | | Aggregation fiber km | {x['agg_km']} |
| Pooled DU (C-RAN, 0.75 per site) | {x['du_cran']} | | Backbone add/drop spur km | {x['spur_km']} |
| Site DU (D-RAN) | {x['du_dran']} | | Backbone / metro core km lit | {x['bb_km']} |
| Fronthaul gateways (C-RAN) | {x['fhgw']} | | | |
| n258 street cells | {x['n258']} | | Microwave hops | {x['mw']} |
| Indoor pRRU / n258 heads | {x['prru']} / {x['vmmw']} | | Power systems (rectifier + battery) | {x['sites']} |

## 4. Prerequisites (entry criteria)
{''.join('- ' + p + chr(10) for p in prereq)}
## 5. Schedule
| Activity | Start | End |
|---|---|---|
{''.join(f"| {q['activity']} | M{q['start_month']} · {q['start']} | M{q['end_month']} · {q['end']} |" + chr(10) for q in a)}
Required run-rate: ≈ {x['rate']} sites on air per month; ≈ {math.ceil(r['fib_km'] / 3)} km of access/aggregation fiber per month.

## 6. Resources
{r['acq']} acquisition agents · {r['civil']} civil crews · {r['fiber']} urban fiber crews · {r['bb']} backbone crews · {r['install']} radio install crews · {r['ssv']} SSV teams · {r['opt']} optimisation teams.

## 7. Indoor venues in this rollout
{('| Venue | Type | pRRU | n258 |' + chr(10) + '|---|---|---|---|' + chr(10) + ''.join(f'| {v[0]} | {v[1]} | {v[2]} | {v[3]} |' + chr(10) for v in x['venues'])) if x['venues'] else 'None.'}

## 8. Exit criteria
- G3: ≥ 95 % of sites on air, all access rings closed, no open critical alarms.
- G4: every cluster passes the acceptance KPIs of `03_Site_Implementation_Standard.md` §6 (≥ 95 % of bins ≥ 1 Gbps in DU/U, ≥ 93 % SU; rural/highway route KPIs).
- G5: as-built pack, asset register, spares and O&M hand-over signed; lessons-learned fed to {('RO-%02d' % (x['r'] + 1)) if x['r'] < 10 else 'operations'}.

## 9. Rollout-specific notes
{''.join('- ' + n + chr(10) for n in notes) if notes else '- Standard process applies.'}
""")
