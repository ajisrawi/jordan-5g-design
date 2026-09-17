#!/usr/bin/env python3
"""Builds PDFs (design report with map figures; combined deployment plan) via Markdown -> HTML -> headless Chrome."""
import os, re, subprocess, glob, markdown
from PIL import Image
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
A = os.path.join(ROOT, "report_assets")
CSS = """@page{size:A4;margin:16mm 14mm 16mm 14mm}
body{font:10pt/1.45 'Segoe UI',Calibri,Arial,sans-serif;color:#1a2430}
h1{font-size:21pt;color:#0b3a5e;border-bottom:3px solid #0b84c6;padding-bottom:6px;margin:0 0 10px}
h2{font-size:14pt;color:#0b3a5e;margin:20px 0 6px;border-bottom:1px solid #c9d6e2;padding-bottom:3px;page-break-after:avoid}
h3{font-size:11.5pt;color:#0b5a8e;margin:14px 0 4px;page-break-after:avoid}
table{border-collapse:collapse;width:100%;margin:6px 0 12px;font-size:8.3pt}
th{background:#0b3a5e;color:#fff;text-align:left;padding:4px 5px}td{border:1px solid #c9d6e2;padding:3px 5px;vertical-align:top}
tr:nth-child(even) td{background:#f3f7fb}tr{page-break-inside:avoid}
code{background:#eef3f8;padding:1px 4px;border-radius:3px;font-size:8.6pt}pre{background:#eef3f8;padding:8px;font-size:8pt;white-space:pre-wrap}
figure{margin:10px 0 14px;page-break-inside:avoid;text-align:center}figure img{width:100%;border:1px solid #9fb0c0}
figcaption{font-size:8.5pt;color:#455;margin-top:3px}hr{border:0;border-top:1px solid #c9d6e2;margin:14px 0}
.cover{font-size:10pt;color:#455;margin-bottom:12px}.doc{page-break-before:always}"""
def fig(name, cap):
    src = os.path.join(A, name + ".png"); jpg = os.path.join(A, name + ".jpg")
    if os.path.exists(src):
        im = Image.open(src).convert("RGB"); im.thumbnail((1500, 1500)); im.save(jpg, quality=82)
    return f'\n\n<figure><img src="file:///{jpg.replace(os.sep, "/")}"><figcaption>{cap}</figcaption></figure>\n\n'
def to_pdf(md_text, out, title):
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    h = os.path.join(A, os.path.basename(out) + ".html")
    open(h, "w", encoding="utf-8").write(f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{html}</body></html>")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", "file:///" + h.replace(os.sep, "/")], check=True, capture_output=True)
    print("wrote", out, os.path.getsize(out) // 1024, "KB")

# ---- design report
t = open(os.path.join(ROOT, "5G_Jordan_Design_Report.md"), encoding="utf-8").read()
ins = [("### What “1 Gbps guaranteed", fig("fig1_national", "Figure 1 – National design on satellite imagery: service-class zones, sites, DWDM backbone, core data centres / PoPs and indoor venues.")),
       ("## 3. Frequency plan", fig("fig2_amman_1gbps", "Figure 2 – Amman: terrain-aware single-user DL prediction (n78 300 MHz + FDD CA, 10 % neighbour load). Green ≥ 1 Gbps, amber 0.7–1 Gbps, red < 0.7 Gbps; wadis and cell corners stand out.")),
       ("## 5. Link budgets", fig("fig3_sectors", "Figure 3 – Amman core at street level: 375 m grid moved onto local high points, three sectors at 30° / 150° / 270°; squares are indoor venues.")),
       ("## 7. Transport, fiber and core", fig("fig5_n28", "Figure 4 – n28 (700 MHz) national coverage layer with DEM diffraction: populated west, highway and desert corridors.")),
       ("## 8. Indoor coverage", fig("fig4_fiber", "Figure 5 – Amman transport: C-RAN access rings (green), D-RAN rings (blue), 100GE aggregation rings (yellow), hubs, metro core (white) and backbone (magenta)."))]
for key, f_ in ins:
    assert key in t, key; t = t.replace(key, f_ + key, 1)
ro = open(os.path.join(ROOT, "deployment", "00_Master_Deployment_Plan.md"), encoding="utf-8").read()
tab = ro[ro.index("## 2. The ten rollouts"):ro.index("## 3. Timeline")].replace("## 2. The ten rollouts", "## 11. Deployment summary – 10 rollouts over 36 months")
t = t.replace("*Data credits:", tab + fig("fig6_rollout", "Figure 6 – Amman–Zarqa rollout sequence: inside-out from the dense-urban core (RO-01) to the suburban ring (RO-09/10). Full plan in the deployment/ folder.") + "*Data credits:")
to_pdf(t, os.path.join(ROOT, "5G_Jordan_Design_Report.pdf"), "Jordan 5G SA – Nominal Design Report")

# ---- deployment plan (all documents in one PDF)
parts = []
for fpath in sorted(glob.glob(os.path.join(ROOT, "deployment", "0*.md"))) + sorted(glob.glob(os.path.join(ROOT, "deployment", "RO-*.md"))):
    d = open(fpath, encoding="utf-8").read()
    d = re.sub(r"```mermaid.*?```", "*(Gantt chart: see workbook `Jordan_5G_Deployment_Plan.xlsx`, sheet “Schedule (Gantt)”, and the activity table in document 01.)*", d, flags=re.S)
    parts.append(('<div class="doc"></div>\n\n' if parts else "") + d)
parts.insert(1, fig("fig6_rollout", "Rollout sequence, Amman–Zarqa metro: colour = rollout in which the hub cluster goes on air."))
to_pdf("\n\n".join(parts), os.path.join(ROOT, "deployment", "Jordan_5G_Deployment_Plan.pdf"), "Jordan 5G SA – Deployment Plan")

# ---- low-level design (RAN, core, transport)
parts = []
for fpath in sorted(glob.glob(os.path.join(ROOT, "lld", "LLD-*.md"))):
    parts.append(('<div class="doc"></div>\n\n' if parts else "") + open(fpath, encoding="utf-8").read())
if parts: to_pdf("\n\n".join(parts), os.path.join(ROOT, "lld", "Jordan_5G_Low_Level_Design.pdf"), "Jordan 5G SA – Low-Level Design")
