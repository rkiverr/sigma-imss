---
tipo: modulo
tags: [pruebas, arnes, trl5, carga, seguridad, accesibilidad]
fuentes: ["prueba_ambiente_relevante.py", "raw/resultados/e5-arnes-ambiente-relevante-antes.md", "raw/resultados/e5-arnes-ambiente-relevante-despues.md"]
actualizado: 2026-10-04
---

# `prueba_ambiente_relevante.py` — arnés del Entregable 5

Tiene 1,382 líneas. Prueba **el sistema completo** en condiciones semejantes a las de la empresa
([[entregable-5-trl5]]). Usa solo la biblioteca estándar.

```bash
python prueba_ambiente_relevante.py                         # todo, con waitress (~3 min)
python prueba_ambiente_relevante.py --bloques B,C,G         # solo algunos bloques
python prueba_ambiente_relevante.py --servidor desarrollo   # con el servidor de Flask
python prueba_ambiente_relevante.py --codigo <carpeta> --servidor desarrollo --etiqueta antes
```
Genera `resultados_ambiente_relevante[_etiqueta].txt` y `.json` (en `.gitignore`).

## Principios ([[adr-016-arnes-como-caja-negra]])
- **Caja negra por HTTP**: levanta el servidor como proceso independiente y lo usa como lo haría el navegador.
- **Copia aislada por bloque**:
  - La clase `Servidor` copia el código a un directorio temporal (`sigma_trl5_*`) con su propia
    `sigma_ambiente.db` y un puerto libre.
  - Por eso **nunca toca** `sigma_imss.db` ni `exportaciones/`.
  - Al terminar, borra la copia.
- **Emula al navegador**: `leer_atributos()` lee `maxlength` y `data-longitud` de la página servida, y
  `emular_navegador()` aplica primero el recorte del navegador y después las máscaras de `app.js`.
- **Conexiones persistentes** (keep-alive) y `SO_LINGER 0` al cerrar. Así se mide al servidor y no el
  agotamiento de puertos del cliente (WinError 10048).
- **`--codigo`** permite correr una versión vieja del sistema. La del E4 se extrajo con `git archive 4c79ce4`.

## Plantilla sintética (`Plantilla`)
- Nombres mexicanos con acentos y ñ; partículas como "De la Rosa".
- **CURP con las reglas de RENAPO**: vocal interna, consonantes internas, Ñ→X, José/María, entidad y
  **dígito verificador**.
- RFC coherente con la CURP.
- **NSS con dígito de Luhn**, únicos.
- Tipo 3 (eventual de la construcción) en el 60 % de los casos.
- SDI por puesto (ayudante, oficial o supervisor) × el factor de integración 383/365.
- Las fechas son relativas a hoy: `dia_habil_atras(n)`.

## Bloques
| Bloque | Prueba | Mide |
|---|---|---|
| A | Mes simulado: 60 altas de arranque, 30 bajas y 25 altas de rotación, 20 bajas de cierre y 5 reingresos, con 3 capturistas y exportación por etapa | Fallas, lotes, bitácora y atribución por usuario, latencias |
| B | 19 categorías × 8 casos: 3 de "formato válido" (deben aceptarse) y 16 de error (deben bloquearse o avisarse); 60 controles limpios; coherencia sin JavaScript | Bloqueado, avisado o no detectado; falsos positivos |
| C | 25 pares de alta nueva simultánea, 25 de reingreso simultáneo y 10 de doble envío a 40 ms | Duplicados en la base, errores 5xx |
| D | 1, 3, 5, 10 y 20 usuarios sin pausa, 15 s por nivel | Peticiones por segundo, capturas por minuto, p50/p95/máximo, errores, memoria |
| E | Base precargada con 1,000, 5,000 y 10,000 movimientos | Tablero, búsqueda, detalle, captura, exportación de 510, tamaño de la base |
| F | Caída abrupta (`taskkill /T /F`) con 5 capturistas activos | Capturas confirmadas perdidas, integridad, asientos huérfanos, arranque |
| G | 8 pruebas de red y seguridad: servidor, `/console`, folio enorme, CSRF, inyección SQL, XSS, cabeceras, acceso por IP de la LAN | Hallazgos |
| H | Contraste WCAG de 14 pares de color de `estilos.css` | Pares bajo 4.5:1 |

## Trampas al mantenerlo
- Si cambias las máscaras o las longitudes de la interfaz, **actualiza `emular_navegador()`**.
- Tiene su **propia copia** del calendario de días hábiles (`_descansos`), con el mismo bug que `plazo.py`
  ([[bugs-conocidos]]).
- El `python.exe` del entorno virtual es un **lanzador** que crea al intérprete como proceso hijo. Por eso
  `memoria_mb()` busca a los hijos con PowerShell y `detener()` mata el árbol de procesos.
- Las carreras (bloque C) son probabilísticas: con el código viejo salen de 2 a 5 duplicados según la corrida.

Ver también: [[resultados-de-pruebas]] · [[estrategia-de-pruebas]] · [[arnes-prueba-de-concepto]]
