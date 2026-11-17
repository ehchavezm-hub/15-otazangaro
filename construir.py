"""
Genera salida/Flujogramas_01_AZANGARO.html
Diseño v2: Figtree · NASA palette · minimal · infografías animadas
python3 construir.py
"""
import html, json, pathlib

AQUI = pathlib.Path(__file__).parent

ITEMS = [
    ("RFI_Supervision.drawio",           "RFI",        "RFI – Supervisión",          "Requerimiento de Información (RFI) – Supervisión",        ""),
    ("RFI_Subcontratista.drawio",        "RFI",        "RFI – Subcontratista",        "Requerimiento de Información (RFI) – Subcontratista",     ""),
    ("Cartas_Cliente_Supervision.drawio","Cartas",     "Cartas – Cliente / Sup.",     "Cartas enviadas y recibidas – Cliente / Supervisión",     ""),
    ("Cartas_Subcontratista.drawio",     "Cartas",     "Cartas – Subcontratista",     "Cartas enviadas y recibidas – Subcontratista",            ""),
    ("Compatibilizacion.drawio",         "Ingeniería", "Compatibilización",           "Compatibilización",                                      ""),
    ("Actualizar_modelo_BIM.drawio",     "Ingeniería", "Actualizar modelo BIM",       "Actualizar modelo BIM",                                  "Idéntico a «Cambios»: muestra el flujograma de Fiel Sketch. Falta el flujograma real."),
    ("Cambios.drawio",                   "Ingeniería", "Cambios",                     "Cambios",                                                "Idéntico a «Actualizar modelo BIM»: muestra el flujograma de Fiel Sketch. Falta el flujograma real."),
    ("Mapa_Diseno_Hospitales.drawio",    "Mapa",       "Mapa Diseño de Hospitales",   "Diseño de Hospitales – Macroprocesos y procesos",         ""),
]

# ── Groups ────────────────────────────────────────────────────────────────────
groups_order, groups_map = [], {}
for i, (_, g, tab, titulo, aviso) in enumerate(ITEMS):
    if g not in groups_map:
        groups_order.append(g)
        groups_map[g] = []
    groups_map[g].append((i, tab))

# ── Viewer ────────────────────────────────────────────────────────────────────
viewer_js = (AQUI / "vendor/viewer-static.min.js").read_text(encoding="utf-8", errors="replace").replace("</script", "<\\/script").replace('�', '\\uFFFD')

# ── Nav + Panels ──────────────────────────────────────────────────────────────
nav_html = panels_html = ""
cur_g = None
for i, (arch, g, tab, titulo, aviso) in enumerate(ITEMS):
    if g != cur_g:
        nav_html += f'<div class="gh">{g}</div>'
        cur_g = g
    act = " on" if i == 0 else ""
    nav_html += (
        f'<button class="tab{act}" data-i="{i}" data-g="{g}">'
        f'{tab}{"&thinsp;⚠" if aviso else ""}</button>'
    )
    xml = (AQUI / "fuentes" / arch).read_text(encoding="utf-8", errors="replace").replace('�', '')
    cfg = html.escape(json.dumps({
        "highlight": "#1A6FFF", "nav": False, "resize": True,
        "toolbar": "zoom layers", "xml": xml, "fit": True
    }, ensure_ascii=False), quote=True)
    warn = f'<div class="warn"><span class="wi">⚠</span>{aviso}</div>' if aviso else ""
    panels_html += (
        f'<section class="panel{act}" id="p{i}">'
        f'<div class="ph"><span class="bc">{g}</span><h2>{titulo}</h2></div>'
        f'{warn}'
        f'<div class="box"><div class="mxgraph" id="g{i}" data-mxgraph="{cfg}" style="width:100%"></div></div>'
        f'</section>'
    )

# ── Sidebar process-tree SVG (animated) ───────────────────────────────────────
N    = len(groups_order)
GAP  = 46
Y0   = 20
SVH  = Y0 + (N - 1) * GAP + Y0
SL   = (N - 1) * GAP   # spine length

svg_parts = [
    f'<svg class="ptree" viewBox="0 0 190 {SVH}" width="190" height="{SVH}"'
    f' fill="none" xmlns="http://www.w3.org/2000/svg">',
    # Spine line
    f'<line class="spine" x1="11" y1="{Y0}" x2="11" y2="{Y0 + SL}"'
    f' stroke="rgba(255,255,255,0.14)" stroke-width="0.75"'
    f' stroke-dasharray="{SL}" stroke-dashoffset="{SL}"/>',
]
for gi, gname in enumerate(groups_order):
    y   = Y0 + gi * GAP
    nd  = 0.28 + gi * 0.14   # staggered delay
    cnt = len(groups_map[gname])
    svg_parts.append(
        f'<g class="gn" data-g="{gname}" style="animation-delay:{nd:.2f}s">'
        # Horizontal tick
        f'<line x1="15" y1="{y}" x2="27" y2="{y}"'
        f' stroke="rgba(26,111,255,0.55)" stroke-width="0.75"'
        f' stroke-dasharray="12" stroke-dashoffset="12"/>'
        # Diamond node (rotated rect)
        f'<rect x="6" y="{y - 5}" width="10" height="10"'
        f' fill="rgba(26,111,255,0.08)" stroke="rgba(26,111,255,0.5)" stroke-width="0.75"'
        f' transform="rotate(45 11 {y})"/>'
        # Label
        f'<text x="31" y="{y + 4}" fill="rgba(255,255,255,0.65)"'
        f' font-size="11" font-family="Figtree,system-ui,sans-serif">{gname}</text>'
        # Count pill
        f'<text x="188" y="{y + 4}" fill="rgba(255,255,255,0.22)"'
        f' font-size="10" font-family="Figtree,system-ui,sans-serif"'
        f' text-anchor="end">{cnt}</text>'
        f'</g>'
    )
svg_parts.append('</svg>')
tree_svg = "".join(svg_parts)

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600&display=swap');

/* ── Tokens: NASA palette ── */
:root {
  --nav-bg    : #08142A;
  --nav-line  : rgba(255,255,255,0.065);
  --nav-muted : rgba(255,255,255,0.25);
  --nav-fg    : rgba(255,255,255,0.68);

  --bg        : #EFF3FA;
  --bg-panel  : #FFFFFF;
  --bg-warn   : rgba(245,166,35,0.07);

  --fg        : #0C1428;
  --fg-2      : #3D516B;
  --fg-3      : #8294B4;

  --blue      : #1A6FFF;
  --blue-soft : rgba(26,111,255,0.09);
  --gold      : #F5A623;
  --red       : #E8321A;
  --red-soft  : rgba(232,50,26,0.07);

  --line      : rgba(12,20,40,0.07);
  --shadow    : 0 1px 4px rgba(12,20,40,0.07), 0 0 0 0.5px rgba(12,20,40,0.05);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg        : #0C1428;
    --bg-panel  : #101D30;
    --bg-warn   : rgba(245,166,35,0.06);
    --fg        : #CBD6EC;
    --fg-2      : #5A6E8C;
    --fg-3      : #334059;
    --line      : rgba(255,255,255,0.055);
    --shadow    : 0 1px 6px rgba(0,0,0,0.3), 0 0 0 0.5px rgba(0,0,0,0.2);
    --blue-soft : rgba(26,111,255,0.14);
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg        : #0C1428;
  --bg-panel  : #101D30;
  --bg-warn   : rgba(245,166,35,0.06);
  --fg        : #CBD6EC;
  --fg-2      : #5A6E8C;
  --fg-3      : #334059;
  --line      : rgba(255,255,255,0.055);
  --shadow    : 0 1px 6px rgba(0,0,0,0.3), 0 0 0 0.5px rgba(0,0,0,0.2);
  --blue-soft : rgba(26,111,255,0.14);
  color-scheme: dark;
}

/* ── Reset ── */
*, *::before, *::after { box-sizing: border-box }

body {
  margin: 0;
  font-family: 'Figtree', 'Inter', 'Segoe UI', system-ui, sans-serif;
  font-size: 13.5px;
  line-height: 1.5;
  background: var(--bg);
  color: var(--fg);
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ── NAV ───────────────────────────────────────────────────────── */
nav {
  width: 224px;
  flex: none;
  background: var(--nav-bg);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

/* Decorative bottom-right triangle on nav */
nav::after {
  content: '';
  position: absolute;
  bottom: 0; right: 0;
  border-bottom: 48px solid rgba(26,111,255,0.07);
  border-left: 48px solid transparent;
  pointer-events: none;
}

/* ── NAV TOP ── */
.nt {
  flex: none;
  padding: 20px 18px 16px;
  border-bottom: 0.5px solid var(--nav-line);
}
.nt-id {
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.28);
  margin-bottom: 3px;
}
.nt-title {
  font-size: 12.5px;
  font-weight: 500;
  color: rgba(255,255,255,0.82);
  line-height: 1.3;
}

/* ── PROCESS TREE ── */
.ntree {
  flex: none;
  padding: 15px 17px 12px;
  border-bottom: 0.5px solid var(--nav-line);
}
.ntree-label {
  font-size: 8.5px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.2);
  margin-bottom: 10px;
}
.ptree { display: block; overflow: visible }

/* Spine animation */
.spine { animation: draw-spine 1.1s cubic-bezier(.4,0,.2,1) .05s both }
@keyframes draw-spine { to { stroke-dashoffset: 0 } }

/* Node entry */
.gn {
  opacity: 0;
  animation: gn-in .35s ease both;
}
@keyframes gn-in {
  from { opacity: 0; transform: translateX(-5px) }
  to   { opacity: 1; transform: translateX(0) }
}
/* Tick line inside node */
.gn line { animation: tick-in .28s ease .08s both }
@keyframes tick-in { to { stroke-dashoffset: 0 } }

/* ── NAV TABS ── */
.ntabs {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 6px 0 20px;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.08) transparent;
}
.gh {
  font-size: 8.5px;
  font-weight: 600;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: var(--gold);
  opacity: 0.75;
  padding: 14px 18px 4px;
  line-height: 1;
}
.tab {
  display: block;
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  color: var(--nav-fg);
  font-family: inherit;
  font-size: 12.5px;
  line-height: 1.35;
  padding: 7px 18px 7px 22px;
  cursor: pointer;
  position: relative;
  transition: color .15s, background .15s;
}
/* Active bar — grows from center */
.tab::before {
  content: '';
  position: absolute;
  left: 0; top: 50%;
  transform: translateY(-50%) scaleY(0);
  transform-origin: center;
  width: 2px;
  height: 55%;
  background: var(--blue);
  border-radius: 0 1px 1px 0;
  transition: transform .22s cubic-bezier(.4,0,.2,1);
}
.tab:hover {
  background: rgba(255,255,255,0.038);
  color: rgba(255,255,255,0.88);
}
.tab.on {
  background: rgba(26,111,255,0.12);
  color: #fff;
  font-weight: 500;
}
.tab.on::before { transform: translateY(-50%) scaleY(1) }

/* ── MAIN ──────────────────────────────────────────────────────── */
main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
  background: var(--bg);
}

/* ── PANEL ──────────────────────────────────────────────────────── */
.panel { display: none; flex-direction: column; flex: 1; overflow: hidden; min-height: 0 }
.panel.on {
  display: flex;
  animation: panel-in .22s cubic-bezier(.4,0,.2,1) both;
}
@keyframes panel-in {
  from { opacity: 0; transform: translateX(7px) }
  to   { opacity: 1; transform: translateX(0) }
}

/* Panel header */
.ph {
  flex: none;
  padding: 15px 20px 12px;
  background: var(--bg-panel);
  border-bottom: 0.5px solid var(--line);
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}
/* Corner triangle — upper right */
.ph::after {
  content: '';
  position: absolute;
  right: 0; top: 0;
  border-top: 38px solid var(--blue);
  border-left: 38px solid transparent;
  opacity: 0.09;
  pointer-events: none;
}
/* Animated blue underline */
.ph::before {
  content: '';
  position: absolute;
  left: 0; bottom: 0;
  height: 0.75px; width: 100%;
  background: linear-gradient(90deg, var(--blue) 0%, transparent 55%);
  transform: scaleX(0);
  transform-origin: left;
  animation: line-in .55s cubic-bezier(.4,0,.2,1) .05s both;
}
@keyframes line-in { to { transform: scaleX(1) } }

.bc {
  display: block;
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--blue);
  opacity: 0.7;
  margin-bottom: 2px;
}
.ph h2 {
  margin: 0;
  font-size: 17px;
  font-weight: 300;
  color: var(--fg);
  letter-spacing: -0.015em;
  line-height: 1.25;
  text-wrap: balance;
}

/* Warning band */
.warn {
  flex: none;
  display: flex;
  align-items: flex-start;
  gap: 9px;
  background: var(--bg-warn);
  border-left: 1.5px solid var(--gold);
  padding: 9px 18px;
  font-size: 12px;
  color: var(--fg-2);
  line-height: 1.45;
}
.wi { flex: none; opacity: .65 }

/* Diagram box */
.box {
  flex: 1;
  overflow: auto;
  background: var(--bg-panel);
  padding: 8px;
  min-height: 0;
}

/* ── RESPONSIVE ─────────────────────────────────────────────────── */
@media (max-width: 700px) {
  body  { flex-direction: column; height: auto; overflow: auto }
  nav   { width: 100%; flex-direction: row; flex-wrap: wrap; padding: 10px 12px 0 }
  nav::after { display: none }
  .nt   { width: 100%; border-bottom: none; padding: 0 0 8px }
  .ntree { display: none }
  .ntabs { width: 100%; padding: 0 0 10px; display: flex; flex-wrap: wrap; gap: 4px }
  .gh   { display: none }
  .tab  { width: auto; flex: none; padding: 5px 10px; border-radius: 4px; font-size: 11.5px }
  .tab.on { background: rgba(26,111,255,0.28) }
  .tab::before { display: none }
  main  { overflow: visible }
  .panel.on { display: flex; min-height: 80vh }
}

@media print {
  nav { display: none }
  .panel { display: none !important }
  .panel.on { display: flex !important }
  body { display: flex; height: auto; overflow: visible }
  .box { overflow: visible }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    transition-duration: .01ms !important;
  }
}
"""

# ── JS ────────────────────────────────────────────────────────────────────────
JS_APP = """
var rendered = {};

function show(i) {
  var btn = document.querySelector('.tab[data-i="' + i + '"]');
  if (!btn) return;
  var g = btn.dataset.g;

  // Tabs
  document.querySelectorAll('.tab').forEach(function(b) {
    b.classList.toggle('on', +b.dataset.i === i);
  });

  // Panels
  document.querySelectorAll('.panel').forEach(function(p, k) {
    p.classList.toggle('on', k === i);
  });

  // Highlight active group in process tree
  document.querySelectorAll('.gn').forEach(function(n) {
    n.style.opacity = (n.dataset.g === g) ? '1' : '0.38';
  });

  // Lazy-render draw.io
  if (!rendered[i]) {
    rendered[i] = 1;
    GraphViewer.createViewerForElement(document.getElementById('g' + i));
  }
}

document.querySelectorAll('.tab').forEach(function(b) {
  b.onclick = function() { show(+b.dataset.i); };
});

show(0);
"""

# ── Assemble HTML ─────────────────────────────────────────────────────────────
pagina = (
    '<!DOCTYPE html>'
    '<html lang="es">'
    '<head>'
    '<meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>Flujogramas – 01 AZANGARO</title>'
    f'<style>{CSS}</style>'
    '</head>'
    '<body>'
    '<nav>'
    '<div class="nt">'
    '<div class="nt-id">CR 3148 · Hospital Azángaro</div>'
    '<div class="nt-title">Flujogramas de Gestión</div>'
    '</div>'
    '<div class="ntree">'
    '<div class="ntree-label">Procesos</div>'
    f'{tree_svg}'
    '</div>'
    f'<div class="ntabs">{nav_html}</div>'
    '</nav>'
    f'<main>{panels_html}</main>'
    f'<script>{viewer_js}</script>'
    f'<script>{JS_APP}</script>'
    '</body>'
    '</html>'
)

(AQUI / "salida").mkdir(exist_ok=True)
out = AQUI / "salida/Flujogramas_01_AZANGARO.html"
out.write_text(pagina, encoding="utf-8")
print(f"OK  {len(pagina)//1024} KB  →  {out}")
