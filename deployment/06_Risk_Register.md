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
| 8 | Cross-border interference / coordination (109 sectors) and TDD frame misalignment with neighbours | 3 | 3 | RO-03…RO-06 (Aqaba, Jordan Valley, Ramtha) | Early TRC coordination, +2° tilt and power limits already in design, common DDDSU frame, monitoring probes | Regulatory / RF |
| 9 | 1 Gbps cluster acceptance fails (model vs reality in hilly, stone-built Amman) | 3 | 4 | RO-01…RO-03 | CW calibration campaign in M1–M3, RO-01 used as pilot with 3-week optimisation buffer, infill budget 3 % of sites | RF |
| 10 | Device ecosystem: few UEs support 3CC n78 CA | 3 | 4 | launch | CPE-first launch (FWA), device certification programme with OEMs, 2CC fallback marketed by area | Marketing |
| 11 | Core readiness slips (M4 first call) | 2 | 5 | RO-01 | Vendor-hosted staging core from M2, phased NF activation, parallel DC2 build | Core |
| 12 | HSE incident at height or in street works | 2 | 5 | all | Certification, permit-to-work, audits 10 % of sites weekly, stop-work authority | HSE |
| 13 | Community / EMF objections | 3 | 2 | city rollouts | Public EMF measurements portal, camouflage catalogue, municipality engagement | Corporate affairs |
| 14 | Resource peak (≈ 37 install + 278 civil crews) not available locally | 3 | 3 | RO-04…RO-08 | Training academy M1–M3, regional contractors, levelled quotas (≤ 770 sites per rollout) | PMO |
| 15 | Currency / budget overrun from survey-driven scope change (±10 % sites) | 3 | 3 | all | Re-baseline at each G1, contingency 8 %, change control board | PMO / Finance |
| 16 | Indoor venue owners delay access | 3 | 2 | RO-02…RO-10 | Start agreements at T−6, neutral-host offer, substitute venues from phase-2 list | Indoor |
