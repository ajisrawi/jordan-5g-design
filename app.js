/* Jordan 5G SA nominal design viewer. Data: data/design.js (window.DESIGN), data/rasters.js (window.RASTERS). */
(function () {
  const D = window.DESIGN, RS = window.RASTERS || [], RO = window.ROLLOUT || null;
  const ro = { on: false, upto: 10 };
  const CK = Object.keys(D.classes);                       // DU, U, SU, R, HW
  const CCOL = { DU: '#f43f5e', U: '#f59e0b', SU: '#22d3ee', R: '#a3e635', HW: '#c084fc' };
  const $ = (s) => document.querySelector(s);
  const fmt = (n) => (n == null ? '–' : Number(n).toLocaleString('en-US'));

  /* ------------------------------------------------------------------ map + base layers */
  const map = L.map('map', { preferCanvas: true, zoomControl: true }).setView([31.2, 36.5], 8);
  const esri = (p) => `https://server.arcgisonline.com/ArcGIS/rest/services/${p}/MapServer/tile/{z}/{y}/{x}`;
  const sat = L.tileLayer(esri('World_Imagery'), { maxZoom: 19, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics' }).addTo(map);
  const lbl = L.layerGroup([L.tileLayer(esri('Reference/World_Transportation'), { maxZoom: 19, opacity: .8 }),
                            L.tileLayer(esri('Reference/World_Boundaries_and_Places'), { maxZoom: 19 })]).addTo(map);
  const base = { 'Satellite (Esri World Imagery)': sat,
    'Terrain (OpenTopoMap)': L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', { maxZoom: 17, attribution: '© OpenTopoMap, SRTM' }),
    'Streets (OpenStreetMap)': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' }) };
  L.control.scale({ imperial: false }).addTo(map);
  ['zones', 'bldg', 'cov', 'fiber', 'sectors', 'sites', 'top'].forEach((n, i) => { map.createPane(n).style.zIndex = 410 + i * 10; });
  const canvasFor = (pane) => L.canvas({ pane, padding: .3 });
  const rSites = canvasFor('sites'), rSec = canvasFor('sectors'), rFib = canvasFor('fiber'), rZone = canvasFor('zones');

  /* ------------------------------------------------------------------ overlays */
  const LY = {};
  LY.gov = L.geoJSON(D.adm1, { pane: 'zones', renderer: rZone, interactive: false, style: { color: '#fff', weight: 1.2, fill: false, dashArray: '4 4', opacity: .7 } });
  LY.zones = L.layerGroup(D.zones.map(z => L.polygon(z.ring, { pane: 'zones', renderer: rZone, color: CCOL[z.cls], weight: 1.5, fillOpacity: .07 })
    .bindTooltip(`${z.name} – ${D.classes[z.cls].name}`, { sticky: true })));
  LY.bldg = L.imageOverlay('data/bldg_height.png', D.bldg.bounds, { pane: 'bldg', opacity: .75 });

  // sites
  const sitePopup = (s) => {
    const c = CK[s[3]], k = D.classes[c];
    const rows = s[12].map((e, i) => `<tr><td>${s[0]}-${i + 1}</td><td>${e[0]}°</td><td>${e[1]}°</td><td>${c === 'R' || c === 'HW' ? '–' : e[2] + '°'}</td><td>${e[3]}°</td><td>${e[4]}°</td><td>${e[5]}</td><td>${e[8] > 0 ? '+' : ''}${e[8]} m${e[6] ? ' ⚠' : ''}</td></tr>`).join('');
    return `<h3>${s[0]} ${s[11] ? '<span class="pill">HUB</span>' : ''}</h3>
      <div class="note">${k.name} · ${s[4]} · ${s[5]} governorate</div>
      <table><tr><td>Position</td><td>${s[1].toFixed(5)}, ${s[2].toFixed(5)}</td></tr>
      <tr><td>Ground elevation (DEM)</td><td>${s[7]} m AMSL</td></tr>
      <tr><td>Local building height (GHSL, 250 m)</td><td>mean ${s[13]} m · max ${s[14]} m</td></tr>
      <tr><td>Site type / antenna height</td><td>${s[15]} · <b>${s[6]} m AGL</b></td></tr>
      <tr><td>Configuration</td><td style="text-align:left">${k.config}</td></tr>
      <tr><td>Backhaul</td><td>${s[10]}</td></tr><tr><td>Hub / ring</td><td>${s[8] || '–'} / ${s[9] || '–'}</td></tr></table>
      <table><tr><th>Cell</th><th>Az</th><th>M-tilt</th><th>n78 dig.</th><th>RET mid</th><th>RET low</th><th>PCI</th><th>Δterrain</th></tr>${rows}</table>
      <div class="note">Δterrain = site ground − mean ground of sector footprint. ⚠ = boresight crosses a border/sea within 2 km: cross-border coordination, +2° tilt applied.</div>`;
  };
  LY.sites = L.layerGroup(); LY.sectors = L.layerGroup();
  const drawSites = () => {
    LY.sites.clearLayers(); LY.sectors.clearLayers();
    const z = map.getZoom(), b = map.getBounds().pad(.1), showSec = z >= 13 && map.hasLayer(LY.sectors);
    const rad = z < 9 ? 1.5 : z < 11 ? 2.2 : z < 13 ? 3.2 : 5;
    for (const s of D.sites) {
      if (z >= 10 && !b.contains([s[1], s[2]])) continue;
      const c = CK[s[3]], rr = RO ? RO.site[s[0]] : 0;
      if (ro.on && rr > ro.upto) continue;
      if (map.hasLayer(LY.sites))
        L.circleMarker([s[1], s[2]], { renderer: rSites, pane: 'sites', radius: s[11] ? rad + 2 : rad, color: s[11] ? '#fff' : '#111', weight: s[11] ? 1.5 : .6, fillColor: ro.on ? RO.colors[rr - 1] : CCOL[c], fillOpacity: .95 })
          .bindPopup(() => sitePopup(s) + (RO ? `<div class="note">Deployment: <b>RO-${String(rr).padStart(2, '0')}</b> · on air ${RO.meta[rr - 1].window}</div>` : ''), { maxWidth: 460 }).addTo(LY.sites);
      if (showSec) {
        const R = Math.min(D.classes[c].range * .55, 1.2), kx = 111.32 * Math.cos(s[1] * Math.PI / 180);
        for (const e of s[12]) {
          const pts = [[s[1], s[2]]];
          for (let a = e[0] - 32; a <= e[0] + 32; a += 8) pts.push([s[1] + R * Math.cos(a * Math.PI / 180) / 110.574, s[2] + R * Math.sin(a * Math.PI / 180) / kx]);
          L.polygon(pts, { renderer: rSec, pane: 'sectors', color: e[6] ? '#ff0' : CCOL[c], weight: 1, fillOpacity: .28, interactive: false }).addTo(LY.sectors);
        }
      }
    }
  };
  map.on('moveend zoomend', drawSites);

  // transport
  const line = (path, o, tip) => { const l = L.polyline(path, Object.assign({ renderer: rFib, pane: 'fiber' }, o)); if (tip) l.bindTooltip(tip, { sticky: true }); return l; };
  LY.backbone = L.layerGroup(D.backbone.map(b => line(b.path, { color: b.tier === 'national' ? '#ff2d95' : '#ff9ecb', weight: b.tier === 'national' ? 4 : 2.5, opacity: .95 },
    `${b.name}<br>${b.tier === 'national' ? 'National DWDM ring, N×400G' : 'Regional DWDM / 100GE spur'} · ≈${b.km} km`)));
  LY.metro = L.layerGroup([line(D.metro_core.path, { color: '#fff', weight: 4, dashArray: '2 7' }, `${D.metro_core.name}<br>N×400GE · ≈${D.metro_core.km} km`)]
    .concat(D.metro_spurs.map(p => line(p, { color: '#fff', weight: 2.5, dashArray: '2 7' }))));
  LY.agg = L.layerGroup(D.grings.map(r => line(r[2], { color: '#fde047', weight: 2.5, opacity: .9 }, `${r[0]} · aggregation ring 100GE · ${r[1]} km`)));
  LY.access = L.layerGroup(D.arings.map(r => line(r[3], { color: r[2] ? '#4ade80' : '#60a5fa', weight: 1.4, opacity: .85 },
    `${r[0]} · ${r[2] ? 'C-RAN access ring (eCPRI fronthaul + 25GE)' : 'D-RAN access ring 10/25GE'} · ${r[1]} km`)));
  LY.mw = L.layerGroup(D.mw.map(p => line(p, { color: '#e879f9', weight: 1.2, dashArray: '4 5' }, 'Microwave backhaul hop')));
  LY.hubs = L.layerGroup(D.hubs.map(h => L.circleMarker([h[1], h[2]], { pane: 'top', radius: 6, color: '#111', weight: 1, fillColor: '#fde047', fillOpacity: 1 })
    .bindPopup(`<h3>${h[0]}</h3>${h[3]}<br>${h[4]} sites homed · parent PoP ${h[5] || '–'}`)));
  const popIcon = (role) => L.divIcon({ className: '', iconSize: [18, 18], html: `<div style="width:18px;height:18px;transform:rotate(45deg);border:2px solid #111;background:${role === 'core' ? '#ef4444' : role === 'edge' ? '#fb923c' : '#fff'}"></div>` });
  LY.pops = L.layerGroup(D.pops.map(p => L.marker([p.lat, p.lon], { pane: 'top', icon: popIcon(p.role) }).bindPopup(`<h3>${p.id}</h3>${p.name}<br>Role: ${p.role}`)));
  const vIcon = L.divIcon({ className: '', iconSize: [16, 16], html: '<div style="width:16px;height:16px;border-radius:4px;border:2px solid #fff;background:#7c3aed"></div>' });
  const vMarkers = {};
  LY.venues = L.layerGroup(D.venues.map(v => (vMarkers[v.name] = L.marker([v.lat, v.lon], { pane: 'top', icon: vIcon }).bindPopup(
    `<h3>${v.name}</h3><div class="note">${v.type} · served area ≈ ${fmt(v.area)} m²${v.rooms ? ' · ' + v.rooms + ' rooms' : ''} (estimate – confirm by survey)</div>
     <table><tr><td>n78 4T4R pRRU (3×100 MHz)</td><td>${v.prru}</td></tr><tr><td>RHUB / PoE++ aggregation</td><td>${v.rhub}</td></tr>
     <tr><td>n258 mmWave heads (800 MHz)</td><td>${v.mmw}</td></tr><tr><td>In-building DU/BBU</td><td>${v.bbu}</td></tr><tr><td>Fiber backhaul</td><td>${v.backhaul}</td></tr></table>`))));

  /* ------------------------------------------------------------------ coverage rasters (terrain-aware, recoloured live) */
  const F = D.rfc, R78 = D.radio.n78_64T;
  const seLUT = new Float32Array(600);                     // SINR -15 … +45 dB in 0.1 dB steps
  for (let i = 0; i < 600; i++) { const s = -15 + i * .1; let b = 0;
    for (let r = 1; r <= 4; r++) { const x = Math.pow(10, (s - 10 * Math.log10(r) - F.pen[r]) / 10); b = Math.max(b, r * Math.min(F.cap, F.impl * Math.log2(1 + x))); } seLUT[i] = b; }
  const se = (s) => seLUT[Math.max(0, Math.min(599, Math.round((s + 15) * 10)))];
  const tp = (sinr, bw) => se(sinr) * F.re100 * (bw / 100) * F.tdd_dl * (1 - F.oh) / 1e6 + se(sinr - 5) * (3.5 * 52 * 12 * 14000) * (1 - F.oh) / 1e6;
  const SCALES = {
    rsrp: { title: 'SS-RSRP (dBm)', stops: [[-80, '#006837'], [-90, '#31a354'], [-100, '#addd8e'], [-110, '#fed976'], [-118, '#fd8d3c'], [-999, '#bd0026']] },
    sinr: { title: 'DL SINR (dB)', stops: [[25, '#08519c'], [20, '#3182bd'], [15, '#31a354'], [10, '#addd8e'], [5, '#fed976'], [0, '#fd8d3c'], [-999, '#bd0026']] },
    tp: { title: 'Single-user DL throughput (Mbps)', stops: [[2000, '#54278f'], [1500, '#08519c'], [1000, '#31a354'], [750, '#d9f0a3'], [500, '#fed976'], [250, '#fd8d3c'], [-1, '#bd0026']] },
    gbps: { title: '1 Gbps target', stops: [[1000, '#22c55e'], [700, '#fbbf24'], [-1, '#ef4444']] },
    n28: { title: 'n28 (700 MHz) SS-RSRP (dBm)', stops: [[-90, '#006837'], [-100, '#31a354'], [-110, '#addd8e'], [-118, '#fed976'], [-124, '#fd8d3c'], [-999, '#bd0026']] } };
  const hex = (h) => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  Object.values(SCALES).forEach(s => s.stops.forEach(t => t.push(hex(t[1]))));
  const cov = { mode: 'gbps', bw: 300, load: 10, pen: 0, opacity: .6, ready: false, overlays: [], stats: null };
  const merc = (la) => Math.log(Math.tan(Math.PI / 4 + la * Math.PI / 360));
  const loadRasters = () => Promise.all(RS.map(r => new Promise(res => { const im = new Image(); im.onload = () => {
    const c = document.createElement('canvas'); c.width = im.width; c.height = im.height; const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(im, 0, 0);
    r.w = im.width; r.h = im.height; r.px = x.getImageData(0, 0, im.width, im.height).data; r.canvas = c; res(); }; im.src = r.png; })));
  const valueAt = (r, i, mode) => {                        // i = pixel byte offset
    const p = r.px, shift = (r.layer === 'n78' ? 10 * Math.log10(300 / cov.bw) : 0) - cov.pen;
    const S = p[i] / 2 - 150 + shift, I = p[i + 1] / 2 - 150 + shift;
    if (mode === 'rsrp' || mode === 'n28') return p[i] / 2 - 150 - cov.pen - (r.layer === 'n78' ? 4 : 0);   // SSB beam is 4 dB below the traffic beam
    const nse = r.layer === 'n78' ? -174 + 10 * Math.log10(30e3) + F.ue_nf : -174 + 10 * Math.log10(15e3) + F.ue_nf;
    const sinr = S - 10 * Math.log10(Math.pow(10, (I - (r.layer === 'n78' ? R78.bf_iso : 0)) / 10) * cov.load / 100 + Math.pow(10, nse / 10));
    return mode === 'sinr' ? sinr : tp(sinr, cov.bw);
  };
  const renderCov = () => {
    cov.overlays.forEach(o => map.removeLayer(o)); cov.overlays = [];
    if (!cov.ready || !map.hasLayer(LY.cov)) { legend.update(); return; }
    $('#busy').style.display = 'block';
    setTimeout(() => {
      const sc = SCALES[cov.mode], st = { 1: [0, 0], 2: [0, 0], 3: [0, 0] };
      for (const r of RS) {
        const isN28 = r.layer === 'n28';
        if ((cov.mode === 'n28') !== isN28) continue;
        const out = document.createElement('canvas'); out.width = r.w; out.height = r.h; const ctx = out.getContext('2d'), img = ctx.createImageData(r.w, r.h), o = img.data, p = r.px;
        for (let i = 0; i < p.length; i += 4) {
          if (!p[i + 3]) continue;
          const v = valueAt(r, i, cov.mode);
          let col = sc.stops[sc.stops.length - 1][2]; for (const t of sc.stops) if (v >= t[0]) { col = t[2]; break; }
          o[i] = col[0]; o[i + 1] = col[1]; o[i + 2] = col[2]; o[i + 3] = 255;
          if (!isN28 && p[i + 2]) { const t = valueAt(r, i, 'tp'); st[p[i + 2]][0]++; if (t >= 1000) st[p[i + 2]][1]++; }
        }
        ctx.putImageData(img, 0, 0);
        cov.overlays.push(L.imageOverlay(out.toDataURL(), r.bounds, { pane: 'cov', opacity: cov.opacity }).addTo(map));
      }
      cov.stats = st; legend.update(); updateCovStats(); $('#busy').style.display = 'none';
    }, 20);
  };
  LY.cov = L.layerGroup(); // logical toggle only
  map.on('click', (e) => {
    if (!cov.ready || !map.hasLayer(LY.cov)) return;
    for (const r of RS) { const [[s, w], [n, ea]] = r.bounds; if (e.latlng.lat < s || e.latlng.lat > n || e.latlng.lng < w || e.latlng.lng > ea) continue;
      if ((cov.mode === 'n28') !== (r.layer === 'n28')) continue;
      const col = Math.floor((e.latlng.lng - w) / (ea - w) * r.w), row = Math.floor((merc(n) - merc(e.latlng.lat)) / (merc(n) - merc(s)) * r.h), i = (row * r.w + col) * 4;
      if (!r.px[i + 3]) continue;
      const rs = valueAt(r, i, 'rsrp'), si = valueAt(r, i, 'sinr'), t = valueAt(r, i, 'tp');
      L.popup({ pane: 'popupPane' }).setLatLng(e.latlng).setContent(`<h3>Prediction at point</h3><table><tr><td>Layer</td><td>${r.layer === 'n78' ? 'n78 ' + cov.bw + ' MHz + FDD CA' : 'n28 10 MHz'}</td></tr>
        <tr><td>SS-RSRP</td><td>${rs.toFixed(1)} dBm</td></tr><tr><td>SINR @ ${cov.load}% neighbour load</td><td>${si.toFixed(1)} dB</td></tr>
        ${r.layer === 'n78' ? `<tr><td>Single-user DL throughput</td><td><b>${Math.round(t)} Mbps</b></td></tr>` : ''}</table>
        <div class="note">Median prediction, UMa/RMa + DEM knife-edge diffraction; ${cov.pen ? cov.pen + ' dB building loss' : 'outdoor'}.</div>`).openOn(map); return; }
  });
  const legend = L.control({ position: 'bottomright' });
  legend.onAdd = function () { this.div = L.DomUtil.create('div', 'legend'); this.update(); return this.div; };
  legend.update = function () { if (!this.div) return; let h = '';
    if (map.hasLayer(LY.cov)) { const sc = SCALES[cov.mode]; h += `<b>${sc.title}</b><br>` + sc.stops.map((t, i) => `<i style="background:${t[1]}"></i>${i === sc.stops.length - 1 ? '&lt; ' + sc.stops[i - 1][0] : '≥ ' + t[0]}`).join('<br>') + '<hr style="border-color:#2b3c4f">'; }
    if (map.hasLayer(LY.bldg)) h += '<b>Building height (m)</b><br>' + D.bldg.ramp.map(r => `<i style="background:rgb(${r[1].join(',')})"></i>≥ ${r[0]}`).join('<br>') + '<hr style="border-color:#2b3c4f">';
    if (ro.on) h += '<b>Rollout (on-air window)</b><br>' + RO.meta.map((m, i) => `<i style="background:${RO.colors[i]};border-radius:50%;width:10px;opacity:${i < ro.upto ? 1 : .25}"></i>${m.id} · ${m.window}`).join('<br>');
    else h += '<b>Sites</b><br>' + CK.map(c => `<i style="background:${CCOL[c]};border-radius:50%;width:10px"></i>${D.classes[c].name}`).join('<br>');
    this.div.innerHTML = h; };
  legend.addTo(map);

  /* ------------------------------------------------------------------ side panel */
  const TABS = [['layers', 'Map'], ['summary', 'Summary'], ['radio', 'Radio plan'], ['budget', 'Budget & 1 Gbps'], ['transport', 'Fiber & core'], ['indoor', 'Indoor'], ['rollout', 'Rollout']];
  $('#tabs').innerHTML = TABS.map(([k, n], i) => `<button data-t="${k}" class="${i ? '' : 'on'}">${n}</button>`).join('');
  $('#t-layers').classList.add('on');
  $('#tabs').onclick = (e) => { const t = e.target.dataset.t; if (!t) return; document.querySelectorAll('#tabs button').forEach(b => b.classList.toggle('on', b.dataset.t === t));
    document.querySelectorAll('.tab').forEach(s => s.classList.toggle('on', s.id === 't-' + t)); };

  const LAYERS = [['cov', 'Coverage prediction (terrain-aware)', '#22c55e', true], ['sites', 'Sites', '#f59e0b', true], ['sectors', 'Sector azimuths (zoom ≥ 13)', '#f59e0b', true],
    ['zones', 'Service-class zones', '#22d3ee', false], ['bldg', 'Building heights (GHSL 100 m)', '#f03b20', false], ['gov', 'Governorates', '#fff', true],
    ['backbone', 'National / regional DWDM backbone', '#ff2d95', true], ['metro', 'Amman metro core ring', '#fff', true], ['agg', 'Aggregation rings (100GE)', '#fde047', false],
    ['access', 'Access rings (C-RAN green / D-RAN blue)', '#4ade80', false], ['mw', 'Microwave hops', '#e879f9', false], ['hubs', 'C-RAN / pre-agg hubs', '#fde047', false],
    ['pops', 'Core DCs & PoPs', '#ef4444', true], ['venues', 'Indoor venues (malls, hotels, …)', '#7c3aed', true]];
  $('#t-layers').innerHTML = `<h2>Base map</h2><select id="base">${Object.keys(base).map(n => `<option>${n}</option>`).join('')}</select>
    <label class="row"><input type="checkbox" id="lbl" checked> Place names & roads overlay</label>
    <h2>Layers</h2>${LAYERS.map(([k, n, c, on]) => `<label class="row"><input type="checkbox" data-l="${k}" ${on ? 'checked' : ''}><span class="sw" style="background:${c}"></span>${n}</label>`).join('')}
    <h2>Coverage prediction</h2>
    <div class="ctl"><span>Map</span><select id="c-mode"><option value="gbps">1 Gbps compliance (single-user DL)</option><option value="tp">DL throughput</option><option value="sinr">SINR</option><option value="rsrp">n78 SS-RSRP</option><option value="n28">n28 700 MHz national coverage</option></select></div>
    <div class="ctl"><span>n78 bandwidth (carrier aggregation)</span><select id="c-bw"><option value="100">100 MHz (1 CC)</option><option value="200">200 MHz (2 CC)</option><option value="300" selected>300 MHz (3 CC) – design baseline</option></select></div>
    <div class="ctl"><span>Neighbour-cell load <b id="c-load-v">10 %</b></span><input type="range" id="c-load" min="5" max="100" step="5" value="10"></div>
    <div class="ctl"><span>User environment</span><select id="c-pen"><option value="0">Outdoor</option><option value="13">In-car / light indoor (13 dB)</option><option value="25">Deep indoor, stone façade (25 dB)</option></select></div>
    <div class="ctl"><span>Opacity</span><input type="range" id="c-op" min="20" max="100" step="5" value="60"></div>
    <div id="c-stats" class="note"></div>
    <p class="note">Click the map for RSRP / SINR / throughput at a point. Click a site for antenna height, azimuth, tilt and PCI. Prediction = 3GPP 38.901 median path loss + knife-edge diffraction on the Copernicus 90 m DEM, real antenna heights above GHSL rooftops, sector patterns and tilts. Nominal-planning accuracy – calibrate with CW drive tests before build.</p>`;
  const updateCovStats = () => { const st = cov.stats; if (!st || cov.mode === 'n28') { $('#c-stats').innerHTML = ''; return; }
    const nm = { 1: 'Dense urban', 2: 'Urban', 3: 'Suburban' };
    $('#c-stats').innerHTML = `<table><tr><th>Area ≥ 1 Gbps</th><th>${cov.bw} MHz · ${cov.load}% load</th></tr>` + [1, 2, 3].map(k => { const v = st[k][0] ? 100 * st[k][1] / st[k][0] : 0;
      return `<tr><td>${nm[k]}</td><td class="${v >= 95 ? 'ok' : v >= 80 ? 'warn' : 'bad'}"><b>${v.toFixed(1)} %</b></td></tr>`; }).join('') + '</table>'; };
  $('#base').onchange = (e) => { Object.values(base).forEach(l => map.removeLayer(l)); base[e.target.value].addTo(map).bringToBack(); };
  $('#lbl').onchange = (e) => e.target.checked ? lbl.addTo(map) : map.removeLayer(lbl);
  document.querySelectorAll('[data-l]').forEach(cb => { const apply = () => { const l = LY[cb.dataset.l]; cb.checked ? l.addTo(map) : map.removeLayer(l);
      if (cb.dataset.l === 'cov') renderCov(); else if (['sites', 'sectors'].includes(cb.dataset.l)) drawSites(); legend.update(); }; cb.onchange = apply; if (cb.checked) LY[cb.dataset.l].addTo(map); });
  $('#c-mode').onchange = (e) => { cov.mode = e.target.value; renderCov(); };
  $('#c-bw').onchange = (e) => { cov.bw = +e.target.value; renderCov(); };
  $('#c-pen').onchange = (e) => { cov.pen = +e.target.value; renderCov(); };
  $('#c-load').oninput = (e) => { $('#c-load-v').textContent = e.target.value + ' %'; };
  $('#c-load').onchange = (e) => { cov.load = +e.target.value; renderCov(); };
  $('#c-op').oninput = (e) => { cov.opacity = e.target.value / 100; cov.overlays.forEach(o => o.setOpacity(cov.opacity)); };

  /* ---- Summary */
  const S = D.summary;
  $('#t-summary').innerHTML = `<div class="kpis">
    <div class="kpi"><b>${fmt(S.sites_total)}</b><span>macro sites · ${fmt(S.sectors_total)} sectors</span></div>
    <div class="kpi"><b>${fmt(S.geo_1g_km2)} km²</b><span>1 Gbps service footprint</span></div>
    <div class="kpi"><b>${(100 * S.pop_in_zones / S.pop_total).toFixed(0)} %</b><span>population inside designed zones (${(S.pop_in_zones / 1e6).toFixed(1)} M)</span></div>
    <div class="kpi"><b>${fmt(S.access_fiber_km + S.agg_fiber_km + S.backbone_km + S.metro_core_km + S.spur_km)} km</b><span>fiber route (access + agg + backbone)</span></div>
    <div class="kpi"><b>${fmt(S.subs_total / 1e6)} M</b><span>design subscribers · ${fmt(S.bh_total_gbps)} Gbps busy hour</span></div>
    <div class="kpi"><b>${fmt(S.indoor.prru)}</b><span>indoor pRRUs in ${S.indoor.venues} venues · ${S.indoor.mmw} mmWave heads</span></div></div>
    <h2>Sites by service class</h2><table><tr><th>Class</th><th>ISD</th><th>Cell range</th><th>Sites</th><th>Mean ant. height</th></tr>
    ${CK.map(c => `<tr><td><span class="sw" style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${CCOL[c]}"></span> ${D.classes[c].name}</td><td>${D.classes[c].isd * 1000} m</td><td>${Math.round(D.classes[c].range * 1000)} m</td><td>${fmt(S.by_class[c])}</td><td>${S.bldg.by_class[c] ? S.bldg.by_class[c].mean_ant + ' m' : D.classes[c].h + ' m'}</td></tr>`).join('')}</table>
    <h2>Terrain & buildings used</h2>
    <p class="note">• Copernicus GLO-90 DEM: ${fmt(S.terrain.moved)} nominals moved onto the local high point inside their search ring (mean gain ${S.terrain.mean_gain_m} m); per-sector tilt from site-to-footprint terrain delta; knife-edge diffraction in every prediction.<br>
    • GHSL building heights: ${fmt(S.bldg.rooftop)} rooftop sites with antenna ≥ local max roof + 8 m; ${fmt(S.bldg.greenfield)} monopoles; ${fmt(S.bldg.towers)} rural towers; ${fmt(S.bldg.pruned)} nominals removed because their whole cell has no buildings.<br>
    • ${S.border_sectors} sectors flagged for cross-border coordination.</p>
    <h2>Sites by governorate</h2><table><tr><th>Governorate</th>${CK.map(c => `<th>${c}</th>`).join('')}<th>Total</th></tr>
    ${Object.entries(S.by_governorate).sort((a, b) => Object.values(b[1]).reduce((x, y) => x + y, 0) - Object.values(a[1]).reduce((x, y) => x + y, 0)).map(([g, v]) => `<tr><td>${g}</td>${CK.map(c => `<td>${v[c] || ''}</td>`).join('')}<td><b>${Object.values(v).reduce((x, y) => x + y, 0)}</b></td></tr>`).join('')}</table>
    <h2>Capacity (busy hour)</h2><table><tr><th>Class</th><th>Subs / sector</th><th>Offered Mbps</th><th>Load 100</th><th>200</th><th>300 MHz</th></tr>
    ${D.capacity.map(r => `<tr><td>${D.classes[r.cls].name}</td><td>${r.subs_per_sector}</td><td>${r.offered_mbps}</td><td>${r.load_100}%</td><td>${r.load_200}%</td><td><b>${r.load_300}%</b></td></tr>`).join('')}</table>
    <p class="note">Assumptions: ${S.assumptions.SUB_PEN * 100}% of population on this network, ${S.assumptions.GB_MONTH} GB/sub/month, ${S.assumptions.BH_SHARE * 100}% of daily traffic in the busy hour (${S.bh_mbps_per_sub} Mbps/sub), mean cell spectral efficiency ${S.assumptions.CELL_SE} b/s/Hz (64T64R MU-MIMO).</p>
    <p class="note">Full tables: <code>output/sites.csv</code>, <code>output/sectors.csv</code>, <code>output/fiber_rings.csv</code>, <code>output/hubs.csv</code>, <code>output/indoor_venues.csv</code>. Report: <code>5G_Jordan_Design_Report.md</code>.</p>`;

  /* ---- Radio plan */
  $('#t-radio').innerHTML = `<h2>Frequency plan</h2><table><tr><th>Band</th><th>Spectrum</th><th>Role</th></tr>
    <tr><td>n28 700 MHz FDD</td><td>2×10 MHz</td><td style="text-align:left">National coverage, deep indoor, VoNR, UL anchor. Every site.</td></tr>
    <tr><td>n3 1800 MHz FDD</td><td>2×20 MHz</td><td style="text-align:left">PCell / UL carrier for n78 CA; capacity in rural.</td></tr>
    <tr><td>n1 2100 MHz FDD</td><td>2×15 MHz</td><td style="text-align:left">Extra FDD capacity in DU / U / rural.</td></tr>
    <tr><td><b>n78 3.4–3.7 GHz TDD</b></td><td><b>3×100 MHz</b></td><td style="text-align:left"><b>1 Gbps layer.</b> 64T64R, reuse-1, DDDSU, 3CC DL CA + FDD PCell.</td></tr>
    <tr><td>n258 26 GHz TDD</td><td>800 MHz</td><td style="text-align:left">Hotspots, venues, FWA: multi-Gbps, relieves n78.</td></tr></table>
    <p class="note">Spectrum holdings are a design assumption – to be secured with TRC. With only 100 MHz of n78 the 1 Gbps target is not achievable (see Budget tab); 200 MHz reaches ≈ 77 % of locations.</p>
    <h2>Antenna system per sector</h2><table><tr><th>Class</th><th>Sectors</th><th style="text-align:left">Antenna line-up</th></tr>
    <tr><td>DU / U / SU</td><td>3</td><td style="text-align:left">① n78 64T64R AAU (192 AE, 320 W, 400 MHz IBW, 24 dBi traffic beam, H-scan ±60°, V-HPBW 6°, digital tilt −2…+9°). ② Passive 2L4H multiband antenna 2.0 m (2×698–960 + 4×1695–2690 MHz, 15.5 / 17.5 dBi, independent RET 2–12°) fed by n28 2T4R + n1/n3 4T4R RRUs.</td></tr>
    <tr><td>DU hotspots</td><td>+2–4</td><td style="text-align:left">n258 street-level radios on lamp posts, 8–10 m, 120–150 m spacing.</td></tr>
    <tr><td>Rural</td><td>3</td><td style="text-align:left">Passive 2L4H 2.6 m antenna (n28 4T4R, n1/n3 4T4R) + n78 8T8R on 45 m lattice tower.</td></tr>
    <tr><td>Highway</td><td>2</td><td style="text-align:left">Two sectors along the road bearing, n28 + n3 4T4R, 45 m tower, 7 km spacing.</td></tr></table>
    <h2>Azimuth rule</h2><p class="note">Hexagonal 3GPP lattice, boresights <b>30° / 150° / 270°</b> so each sector points at a neighbour site’s back-to-back null (ISD = 1.5 × cell range). Highway sites follow the road bearing. Rural/highway sectors pointing across a border or the sea are removed; city sectors within 2 km of a border get +2° tilt and are listed for coordination (Aqaba–Eilat/Taba, Jordan Valley, Ramtha–Daraa).</p>
    <h2>Tilt rule (per sector, terrain-aware)</h2><p class="note">total tilt = atan((h<sub>ant</sub> + z<sub>site</sub> − z̄<sub>footprint</sub> − 1.5) / cell range) + V-HPBW/2, clamped 2–14°. z from the DEM (mean of 9 footprint points at 0.5–1.0 R, ±30°). n78 uses digital tilt up to 9°, remainder is mechanical (shared with the passive antenna, whose RETs are set separately for mid and low band). Every value is in <code>output/sectors.csv</code> and in the site pop-ups.</p>
    <h2>Antenna height rule (buildings)</h2><p class="note">h<sub>ant</sub> = max(class default, max GHSL building height within 250 m + 8 m), cap 60 m. Rooftop where local buildings ≥ 9 m, else monopole. Mean result: DU ${S.bldg.by_class.DU.mean_ant} m (max ${S.bldg.by_class.DU.max_ant} m), U ${S.bldg.by_class.U.mean_ant} m, SU ${S.bldg.by_class.SU.mean_ant} m.</p>
    <h2>Cell parameters</h2><p class="note">PCI: 336 groups × 3, greedy reuse distance ≥ 6 × ISD, mod-3 separated inside a site (collision/confusion-free in plan). SSB: 8 beams n78 (Case C, 30 kHz), SSB in carrier 1; TDD pattern DDDSU (S 10:2:2), GPS/PTP phase-aligned nationally and with neighbouring-country 3.5 GHz networks. PRACH format B4 (city) / format 0 (rural, 15 km). TAC per hub cluster.</p>`;

  /* ---- Budget & compliance */
  const lb = D.link_budget;
  const compTable = (env) => `<table><tr><th>${env}</th><th>Load</th><th>100 MHz</th><th>200 MHz</th><th>300 MHz</th></tr>` + Object.entries(D.compliance).map(([k, v]) =>
    [10, 20, 30, 50].map((l, i) => `<tr><td>${i ? '' : k}</td><td>${l}%</td>${[100, 200, 300].map(b => { const x = v[`${env}|${l}|${b}`]; return `<td class="${x.pct_1g >= 95 ? 'ok' : x.pct_1g >= 75 ? 'warn' : 'bad'}">${x.pct_1g}%<br><span class="note">p5 ${x.p5}</span></td>`; }).join('')}</tr>`).join('')).join('') + '</table>';
  $('#t-budget').innerHTML = `<h2>How 1 Gbps per user is delivered</h2>
    <p class="note">One user alone in a cell gets the whole carrier. Throughput = bandwidth × TDD-DL share (74%) × (1 − 14% overhead) × rank-adaptive spectral efficiency (≤ 4 layers, 256-QAM). 1 Gbps therefore needs SINR ≈ <b>${lb.find(r => r.layer.startsWith('n78 300')).sinr_req} dB with 300 MHz</b>, ${lb.find(r => r.layer.startsWith('n78 200')).sinr_req} dB with 200 MHz, ${lb.find(r => r.layer.startsWith('n78 100')).sinr_req} dB with 100 MHz. The grid is interference-limited, so the guarantee is a function of <i>bandwidth</i> and <i>neighbour load</i>, not of transmit power.</p>
    <h2>Area ≥ 1 Gbps – terrain-aware, all designed zones</h2>${compTable('outdoor')}${compTable('light indoor / in-car')}${compTable('deep indoor')}
    <p class="note">% of 50 m pixels with single-user DL ≥ 1 Gbps (n78 + 35 MHz FDD CA); p5 = 5th-percentile Mbps. Busy-hour load with 300 MHz is ${D.capacity[0].load_300}% (DU), ${D.capacity[1].load_300}% (U), ${D.capacity[2].load_300}% (SU) → design operating point ≈ the 10% rows. Expansion trigger: sector PRB utilisation &gt; 20% in busy hour → add n258 / split.</p>
    <h2>Link budgets</h2><table><tr><th>Link</th><th>Class</th><th>EIRP/SC</th><th>SINR req</th><th>Pen.</th><th>MAPL</th><th>Range</th><th>Design</th></tr>
    ${lb.map(r => r.feasible === false ? `<tr><td>${r.layer}</td><td>${r.cls}</td><td colspan="6" class="bad">not achievable</td></tr>` : `<tr><td>${r.layer}</td><td>${r.cls}</td><td>${r.eirp_sc}</td><td>${r.sinr_req}</td><td>${r.pen}</td><td>${r.mapl}</td><td class="${r.range_m >= r.design_range_m ? 'ok' : 'bad'}">${r.range_m} m</td><td>${r.design_range_m} m</td></tr>`).join('')}</table>
    <p class="note">Per-subcarrier budget: UE NF 7 dB, interference margin 3 dB, shadow margin 6.8 dB (95% area, σ 6 dB; SU 4 dB), 38.901 UMa-NLOS / RMa-NLOS. Where the n78 uplink falls short, the UE transmits on the n3/n1 FDD PCell (UL/DL decoupling through FDD-TDD CA).</p>`;

  /* ---- Transport */
  $('#t-transport').innerHTML = `<div class="kpis"><div class="kpi"><b>${fmt(S.access_fiber_km)} km</b><span>${S.access_rings} access rings</span></div><div class="kpi"><b>${fmt(S.agg_fiber_km)} km</b><span>${S.agg_rings} aggregation rings</span></div>
    <div class="kpi"><b>${fmt(S.backbone_km)} km</b><span>DWDM backbone routes</span></div><div class="kpi"><b>${S.hubs}</b><span>C-RAN / pre-agg hubs</span></div>
    <div class="kpi"><b>${fmt(S.fiber_sites)}</b><span>sites on fiber (${(100 * S.fiber_sites / S.sites_total).toFixed(0)}%)</span></div><div class="kpi"><b>${S.mw_links}</b><span>microwave-fed rural sites</span></div></div>
    <h2>Architecture</h2><table><tr><th>Tier</th><th style="text-align:left">Design</th></tr>
    <tr><td>Fronthaul</td><td style="text-align:left">DU/U: C-RAN. AAU ↔ DU hotel on eCPRI 7-2x, 3×25GE per n78 AAU, dark fiber ≤ 10 km (≤ 75 µs one-way), 12-core drop per site.</td></tr>
    <tr><td>Access ring</td><td style="text-align:left">≤ 8 sites/ring, dual-homed to hub; D-RAN sites 25GE (peak sector 5.2 Gbps @ 300 MHz + mean of others ≈ 8 Gbps/site). 48-core cable.</td></tr>
    <tr><td>Aggregation</td><td style="text-align:left">Hubs (≈ 40 sites each) on 100GE rings of ≤ 5 hubs to a PoP; SRv6 / EVPN, FlexE hard slices (eMBB, FWA, enterprise, O&M).</td></tr>
    <tr><td>Metro core</td><td style="text-align:left">Amman ring DC1–North–Zarqa–DC2–South, N×400GE, Centre PoP dual-homed.</td></tr>
    <tr><td>Backbone</td><td style="text-align:left">National DWDM ring Amman–Desert Hwy–Aqaba–Wadi Araba/Dead Sea–Amman plus northern ring Amman–Zarqa–Mafraq–Irbid–Jerash–Amman; regional spurs. 96-core + OTN, N×400G.</td></tr>
    <tr><td>Sync</td><td style="text-align:left">GNSS + ePRTC at DCs/PoPs, PTP G.8275.1 full on-path, SyncE; ±1.5 µs TDD, ±130 ns inside C-RAN clusters (CA / CoMP).</td></tr>
    <tr><td>Rural</td><td style="text-align:left">Backbone add/drop where a route is within 2 km; otherwise E-band 10G (≤ 6 km) or 6–18 GHz XPIC.</td></tr></table>
    <h2>5G core (SA, cloud-native)</h2><table><tr><th>Site</th><th style="text-align:left">Functions</th></tr>${D.pops.filter(p => p.role !== 'agg').map(p => `<tr><td>${p.id}</td><td style="text-align:left">${p.name}</td></tr>`).join('')}</table>
    <p class="note">Control plane (AMF, SMF, AUSF, UDM/UDR, PCF, NRF, NSSF, NEF, SCP, CHF, IMS for VoNR) active-active in DC1/DC2, subscriber data replica in Irbid. User plane distributed: UPF pools sized for ${fmt(S.bh_total_gbps)} Gbps busy hour with N+1 (≈ 55% Amman DCs, 15% Amman Centre/Zarqa edge, 15% Irbid, 8% Aqaba, rest regional), CDN caches + MEC at edge PoPs, international transit via Aqaba cable landing and northern terrestrial routes.</p>`;

  /* ---- Indoor */
  $('#t-indoor').innerHTML = `<h2>Solution standard</h2><table><tr><th>Venue type</th><th style="text-align:left">Design</th></tr>
    <tr><td>Malls, airports, convention</td><td style="text-align:left">Digital indoor system: n78 4T4R pRRU (3×100 MHz, 4×250 mW) every 20–25 m in open areas (≈ 550–600 m² each) on CAT6A/hybrid-fiber from RHUBs; n258 mmWave heads in atria, food courts, gates, halls; n28/n3 via the same pRRU (multi-band) for VoNR.</td></tr>
    <tr><td>Hotels</td><td style="text-align:left">One pRRU per ≈ 5 rooms in corridors (stone/concrete partitions), dedicated units in ballrooms, lobby, pool; lift shafts with directional pRRU.</td></tr>
    <tr><td>Hospitals, campuses</td><td style="text-align:left">pRRU per ≈ 650 m², EMC-reviewed power in clinical zones; outdoor campus by macro + pole small cells.</td></tr>
    <tr><td>Stadium</td><td style="text-align:left">n258 + n78 narrow-beam bowl sectors under the roof, ≈ 1 sector / 700 seats; concourse pRRUs.</td></tr></table>
    <p class="note">Indoor budget: 24 dBm/port, 38.901 InH-NLOS 76 dB @ 15 m → RSRP ≈ −85 dBm, SINR &gt; 25 dB, rank 4 → 1.5–3 Gbps per user. Indoor cells use dedicated PCIs, lower SSB power at entrances and a 3 dB handover offset towards the macro to stop leakage.</p>
    <h2>Venues (${D.venues.length})</h2><table><tr><th>Venue</th><th>pRRU</th><th>mmW</th><th>Backhaul</th></tr>
    ${D.venues.map(v => `<tr><td><a class="venue-link" data-v="${v.name}">${v.name}</a><br><span class="note">${v.type}</span></td><td>${v.prru}</td><td>${v.mmw}</td><td>${v.backhaul}</td></tr>`).join('')}</table>
    <p class="note">Coordinates and floor areas are approximate – to be confirmed by site survey. Every building &gt; 10,000 m² or &gt; 8 floors found in the GHSL layer should be added to the indoor programme in phase 2.</p>`;
  $('#t-indoor').onclick = (e) => { const n = e.target.dataset.v; if (!n) return; const m = vMarkers[n]; if (!map.hasLayer(LY.venues)) LY.venues.addTo(map); map.setView(m.getLatLng(), 17); m.openPopup(); };

  if (RO) {
    $('#t-rollout').innerHTML = `<h2>Deployment: 10 rollouts / 36 months</h2>
      <label class="row"><input type="checkbox" id="ro-on"> Colour sites by rollout phase</label>
      <div class="ctl"><span>Show build up to <b id="ro-v">RO-10</b></span><input type="range" id="ro-s" min="1" max="10" step="1" value="10"></div>
      <div id="ro-k" class="kpis"></div>
      <table><tr><th>Rollout</th><th>On air</th><th>Sites</th><th>Cum.</th><th>Pop.</th><th>1G km²</th></tr>
      ${RO.meta.map((m, i) => `<tr><td><span class="sw" style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${RO.colors[i]}"></span> ${m.id}</td><td>${m.window}</td><td>${m.sites}</td><td>${fmt(m.cum_sites)}</td><td>${m.cum_pop}%</td><td>${fmt(m.cum_1g)}</td></tr><tr><td colspan="6" class="note" style="text-align:left">${m.top}</td></tr>`).join('')}</table>
      <p class="note">Build unit = hub cluster (DU hotel + its access rings). Backbone routes are lit before the dependent rollout. Documents: <code>deployment/00_Master_Deployment_Plan.md</code>, work packages <code>RO-01…RO-10</code>, workbook <code>Jordan_5G_Deployment_Plan.xlsx</code>.</p>`;
    const roK = () => { const m = RO.meta[ro.upto - 1]; $('#ro-k').innerHTML = `<div class="kpi"><b>${fmt(m.cum_sites)}</b><span>sites on air after ${m.id}</span></div><div class="kpi"><b>${m.cum_pop} %</b><span>population covered · ${fmt(m.cum_1g)} km² at 1 Gbps</span></div>`; };
    $('#ro-on').onchange = (e) => { ro.on = e.target.checked; drawSites(); legend.update(); };
    $('#ro-s').oninput = (e) => { ro.upto = +e.target.value; $('#ro-v').textContent = RO.meta[ro.upto - 1].id + ' · ' + RO.meta[ro.upto - 1].window; roK(); if (!ro.on) { ro.on = true; $('#ro-on').checked = true; } drawSites(); legend.update(); };
    roK();
  }
  // URL parameters: ?v=lat,lon,zoom  &side=0 (hide panel)  &ro=N (rollout view up to N)  &mode=gbps|tp|sinr|rsrp|n28  &layers=access,agg,...
  const Q = new URLSearchParams(location.search);
  if (Q.get('side') === '0') { $('#side').style.display = 'none'; map.invalidateSize(); }
  if (Q.get('v')) { const v = Q.get('v').split(',').map(Number); map.setView([v[0], v[1]], v[2] || 12); }
  if (Q.get('mode')) { cov.mode = Q.get('mode'); $('#c-mode').value = cov.mode; }
  if (Q.get('cov') === '0') { document.querySelector('[data-l=cov]').checked = false; map.removeLayer(LY.cov); }
  (Q.get('layers') || '').split(',').filter(Boolean).forEach(k => { const cb = document.querySelector(`[data-l=${k}]`); if (cb && !cb.checked) { cb.checked = true; LY[k].addTo(map); } });
  if (RO && Q.get('ro')) { ro.on = true; ro.upto = +Q.get('ro'); $('#ro-on').checked = true; $('#ro-s').value = ro.upto; legend.update(); }
  drawSites();
  loadRasters().then(() => { cov.ready = true; renderCov(); });
  window.__map = map;
})();
