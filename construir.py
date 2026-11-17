"""Genera salida/Flujogramas_01_AZANGARO.html a partir de fuentes/*.drawio.
Uso:  python3 construir.py
El HTML resultante es autosuficiente (lleva el visor de draw.io incluido, funciona sin internet).
Para agregar un flujograma: copiar el .drawio a fuentes/ y añadir una fila a ITEMS.
"""
import html, json, pathlib
AQUI = pathlib.Path(__file__).parent
# (archivo, grupo del menú, nombre de pestaña, título, aviso opcional)
ITEMS = [
 ("RFI_Supervision.drawio","RFI","RFI – Supervisión","Requerimiento de Información (RFI) – Supervisión",""),
 ("RFI_Subcontratista.drawio","RFI","RFI – Subcontratista","Requerimiento de Información (RFI) – Subcontratista",""),
 ("Cartas_Cliente_Supervision.drawio","Cartas","Cartas – Cliente/Supervisión","Cartas enviadas y recibidas – Cliente / Supervisión",""),
 ("Cartas_Subcontratista.drawio","Cartas","Cartas – Subcontratista","Cartas enviadas y recibidas – Subcontratista",""),
 ("Compatibilizacion.drawio","Ingeniería","Compatibilización","Compatibilización",""),
 ("Actualizar_modelo_BIM.drawio","Ingeniería","Actualizar modelo BIM","Actualizar modelo BIM","Idéntico a «Cambios»: muestra el flujograma de Fiel Sketch. Falta el flujograma real."),
 ("Cambios.drawio","Ingeniería","Cambios","Cambios","Idéntico a «Actualizar modelo BIM»: muestra el flujograma de Fiel Sketch. Falta el flujograma real."),
 ("Mapa_Diseno_Hospitales.drawio","Mapa","Mapa Diseño de Hospitales","Diseño de Hospitales – Macroprocesos y procesos",""),
]
viewer = (AQUI/"vendor/viewer-static.min.js").read_text(encoding="utf-8").replace("</script","<\\/script")
btns, panels, cur = "", "", None
for i,(arch,g,tab,titulo,aviso) in enumerate(ITEMS):
    xml = (AQUI/"fuentes"/arch).read_text(encoding="utf-8")
    cfg = html.escape(json.dumps({"highlight":"#0000ff","nav":False,"resize":True,"toolbar":"zoom layers","xml":xml,"fit":True},ensure_ascii=False),quote=True)
    if g!=cur: btns+=f'<div class="grp">{g}</div>'; cur=g
    btns+=f'<button class="tab{" on" if i==0 else ""}" data-i="{i}">{tab}{" ⚠" if aviso else ""}</button>'
    w = f'<div class="warn">⚠ {aviso}</div>' if aviso else ""
    panels+=f'<section class="panel{" on" if i==0 else ""}" id="p{i}"><h2>{titulo}</h2>{w}<div class="box"><div class="mxgraph" id="g{i}" data-mxgraph="{cfg}" style="width:100%"></div></div></section>'
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,Segoe UI,Arial,sans-serif;background:#eceff3;color:#1f2933;display:flex;height:100vh}
nav{width:230px;flex:none;background:#1f2d3d;color:#fff;overflow:auto;padding:12px}nav h1{font-size:15px;margin:0 0 10px}
.grp{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#f2b705;margin:14px 0 4px}
.tab{display:block;width:100%;text-align:left;border:0;background:#2b3e54;color:#fff;padding:8px 10px;margin:3px 0;border-radius:6px;cursor:pointer;font-size:13px}
.tab.on{background:#f2b705;color:#1f2d3d;font-weight:600}main{flex:1;overflow:auto;padding:14px}.panel{display:none}.panel.on{display:block}h2{font-size:16px;margin:0 0 8px}
.warn{background:#fff3cd;border:1px solid #f2b705;border-radius:6px;padding:8px 10px;font-size:13px;margin-bottom:8px}
.box{background:#fff;border-radius:8px;box-shadow:0 1px 6px #0003;padding:6px;overflow:auto}
@media(max-width:700px){body{flex-direction:column;height:auto}nav{width:auto}}
@media print{nav{display:none}.panel{display:none!important}.panel.on{display:block!important}body{display:block}}"""
JS = """var done={};function show(i){document.querySelectorAll('.tab').forEach(function(b){b.classList.toggle('on',+b.dataset.i===i)});
document.querySelectorAll('.panel').forEach(function(p,k){p.classList.toggle('on',k===i)});
if(!done[i]){done[i]=1;GraphViewer.createViewerForElement(document.getElementById('g'+i));}}
document.querySelectorAll('.tab').forEach(function(b){b.onclick=function(){show(+b.dataset.i)}});show(0);"""
pagina = f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flujogramas – 01 AZANGARO</title><style>{CSS}</style></head><body><nav><h1>Flujogramas · 01 AZANGARO</h1>{btns}</nav><main>{panels}</main><script>{viewer}</script><script>{JS}</script></body></html>'
(AQUI/"salida").mkdir(exist_ok=True)
(AQUI/"salida/Flujogramas_01_AZANGARO.html").write_text(pagina,encoding="utf-8")
print("OK", len(pagina)//1024, "KB")
