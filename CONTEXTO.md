# Proyecto: Flujogramas CR 3148 Hospital Carlos Cornejo Rosello Vizcardo – Azángaro (COSAPI)

Lee este archivo primero. Resume lo hecho en una conversación previa en claude.ai (17-nov-2026).

## Objetivo
Tener todos los flujogramas de gestión documental/ingeniería (hechos en draw.io) en **un solo HTML de acceso inmediato** para obra, publicado en SharePoint, y después construir aplicaciones sobre ellos. El usuario trabaja en obra (Oficina Técnica); idioma: español.

## Estado actual
- `fuentes/*.drawio`: 8 flujogramas originales (revA 2026). Son la fuente de verdad.
- `construir.py`: genera `salida/Flujogramas_01_AZANGARO.html` (pestañas por grupo, zoom, impresión; incluye el visor de draw.io `vendor/viewer-static.min.js`, de github.com/jgraph/drawio, así que funciona sin internet). Ejecutar: `python3 construir.py`.
- `referencia_pdf/`: PDF de los 4 primeros flujogramas (solo referencia).
- Verificado con Playwright sin red: renderiza bien. Limitación: rombos de decisión tipo `mxgraph.flowchart.decision` se ven cuadrados offline (falta la plantilla de forma); no cambia el contenido.

## Pendientes / problemas conocidos
1. `Cambios.drawio` y `Actualizar_modelo_BIM.drawio` son **idénticos (mismo md5)** y muestran el Fiel Sketch. Hay que obtener los flujogramas reales.
2. En SharePoint (`02_Fuentes`) hay más .drawio que no se han recibido: Drywall 2, FieldSketch, FS Llata 01/02, FS Planos THSSB, Org OT Contingencia, y otros. Agregarlos a `fuentes/` y a `ITEMS` en `construir.py`.
3. SharePoint descarga los .html en vez de abrirlos en el navegador: para ver en línea usar PDF o una página de SharePoint con visor de archivos; el HTML es para descargar/uso local.

## Decisiones tomadas
- Estructura de carpetas en SharePoint (propuesta aceptada de hecho): `01 Flujogramas/` con `01_Vigente`, `02_Fuentes` (.drawio), `03_Historial` (revisiones anteriores). Los PDF revA se subieron por error a `03_Historial`; deben ir a `01_Vigente`.
- Ciclo: Elaborar (draw.io) → Revisar (OT + Gerencia) → Publicar (SharePoint) → Usar en obra (enlace/QR/Teams) → Mejorar (revB, revC…).
- Roles (a confirmar): OT elabora; Gerencia aprueba; Cont. Documentario publica y controla log; Obra consulta y reporta cambios.
- Tablero (whiteboard) con este ciclo: https://claude.ai/artifact/U1pJAqhhw3KgHzQ84g5nq4

## Ideas para siguientes aplicaciones (por prioridad sugerida)
1. Mapa clicable: `Mapa_Diseno_Hospitales` como portada que abre cada flujograma (falta definir qué proceso del mapa corresponde a cada flujograma).
2. Ficha por proceso (responsable, entradas, salidas, formato, plazo) junto a cada flujograma.
3. Buscador de texto dentro de los flujogramas (los .drawio son XML: se puede indexar el atributo `value` de cada celda).
4. Control de versión visible (revisión, fecha, aprobador) y paquete PDF imprimible.
5. Página SharePoint con visor + QR; PWA instalable en celular.
6. Automatización con Power Automate (log de cartas/RFI, formulario de RFI, indicadores) — requiere TI de COSAPI.

## Notas de contexto del usuario
- Cuenta de Claude asociada a un correo corporativo compartido; el usuario está regularizando accesos con TI. No guardar credenciales en archivos.
- No tengo acceso a su SharePoint desde Claude; los archivos se pasan por descarga manual.
