---
tipo: historial
tags: [sesion, estructura, carpetas, paquete, pruebas]
fuentes: ["sigma/", "pruebas/", "servidor.py", ".gitignore", "README.md", "CLAUDE.md"]
actualizado: 2026-10-04
---

# Sesión del 4 de oct de 2026: reorganización del repositorio en carpetas

Trabajo de Pedro con Claude Code.

## 1. Lo que pidió Pedro
"Organiza mejor los archivos y las carpetas." Se le ofrecieron dos opciones: una ligera (mover solo los arneses) y
el paquete `sigma/`. Preguntó si se recomendaba estructurar las carpetas; se le recomendó el paquete y se hizo así,
en una rama nueva con PR, sin tocar `main`, para que el equipo decida si se integra.

## 2. Lo que se hizo
Rama `mejora/estructura-de-carpetas`. Con `git mv` para conservar el historial de cada archivo:

| Antes | Ahora |
|---|---|
| `app.py`, `validaciones.py`, `plazo.py`, `database.py`, `exportar_idse.py` | `sigma/` |
| `templates/`, `static/` | `sigma/templates/`, `sigma/static/` |
| bloque `if __name__ == "__main__"` de `app.py` | `sigma/__main__.py` (`python -m sigma`) |
| `test_prueba_concepto.py`, `prueba_ambiente_relevante.py` | `pruebas/` |
| `sigma_pruebas.db`, `lote_idse_prueba.txt`, `resultados_*` (sueltos) | `pruebas/resultados/` (en `.gitignore`) |
| `servidor.py`, `sigma_imss.db`, `exportaciones/` | **sin cambio**, en la raíz |

Cambios de código, todos mecánicos:
- Imports relativos dentro de `sigma/`. `servidor.py` importa `from sigma.app import app`.
- `database.RAIZ` (antes `BASE_DIR`) y `exportar_idse.DIRECTORIO_SALIDA` suben un nivel para que la base y los
  lotes sigan en la raíz.
- Arnés del E3: agrega la raíz a `sys.path` y escribe todo en `pruebas/resultados/`.
- Arnés del E5: `RAIZ` es la raíz del repo, los reportes van a `pruebas/resultados/`, ya no copia `pruebas/` ni
  `Obsidian/` al directorio temporal, y `codigo_en_paquete()` permite seguir usando `--codigo` con versiones de
  la estructura anterior.
- Documentación: `README.md` (árbol nuevo), `CLAUDE.md` del repo, las tres guías de `instrucciones/` y este wiki
  ([[log]]).

La decisión completa, con alternativas, está en [[adr-017-paquete-sigma-y-carpeta-de-pruebas]].

## 3. Verificación
- **Arnés del E3:** 8/8, los tres bloques CUMPLE.
- **`python -m sigma`:** página, CSS, JS y 404 responden bien.
- **Arnés del E5 completo** (waitress, nueva estructura, 141 s): 140/140 en el mes simulado; 96.9 % de detección
  (4 no detectados, los mismos CURP de siempre); 0 rechazos indebidos; 0 falsos positivos; 60 pares de carreras sin
  duplicados ni 5xx; 0 capturas perdidas tras la caída; 8/8 en seguridad; contraste AA en todos los pares.
  Coincide con [[resultados-de-pruebas]].
- **`--codigo` con la estructura anterior** (copia de `main`): funciona con `--servidor desarrollo` (bloques G y H)
  y con `produccion` (G). En modo desarrollo, el arnés del paquete también arranca bien.

## 4. Hallazgos
- **Windows no dejó renombrar `static/`** con `git mv` ("Permission denied"): VS Code tenía la carpeta abierta. Se
  movieron los dos archivos uno por uno. `templates/` sí se pudo mover entera.
- **El p95 de captura con 20 usuarios varía entre corridas.** Con la nueva estructura dio 190.8 y 218.4 ms. Para
  descartar la reorganización, el bloque D se corrió contra el código de `main` en la misma sesión: 182.6 ms. Es la
  máquina, no el código; los 120.0 ms del informe son de otra corrida. Nota agregada en [[resultados-de-pruebas]].
- El reporte del E3 ahora dice `Archivo generado: pruebas\resultados\lote_idse_prueba.txt` en lugar de
  `lote_idse_prueba.txt`. La copia de `raw/resultados/` no se toca, porque es de antes.

## 5. Pendientes
- Que el equipo revise el PR y decida si se integra.
- Al integrarlo, en cada copia local:
  - El desarrollo se arranca con `python -m sigma`.
  - Los reportes viejos sueltos en la raíz (`resultados_*`) ya no están en `.gitignore`, así que conviene
    borrarlos.
- Regenerar `raw/historial/git-log.md` y actualizar [[cronologia]] e [[inicio]] cuando se integre.

Ver también: [[cronologia]] · [[sesion-2026-10-04-entregable-5]] · [[arquitectura-general]]
