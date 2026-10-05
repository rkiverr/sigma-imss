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
Rama `mejora/estructura-de-carpetas`, **PR #2** (`github.com/rkiverr/sigma-imss/pull/2`), con tres commits:
`3269ff1` (la reorganización), `ac56fc1` (quita un import sin uso y registra la verificación) y `51a45ec` (el
método de verificación en el wiki). Se integró a `main` con el merge `fb3a4a8` (§5). Se usó `git mv`
para conservar el historial de cada archivo:

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

### Verificación contra `main` (pedida por Pedro después del PR)
El método completo, con los scripts, quedó en [[verificar-un-cambio-contra-main]].
Las dos versiones, con el mismo arnés, una tras otra:

| Prueba | `main` | Rama |
|---|---|---|
| Criterios CA5-1 a CA5-9 (arnés del E5 completo) | 9/9 | 9/9 |
| CA5-10 (arnés del E3) | 8/8 | 8/8 |
| Diferencias en resultados funcionales (cada caso de B, carreras, seguridad, contraste, volumen, caída) | — | **0** |
| p95 de captura con 20 usuarios (solo referencia) | 175.2 ms | 145.8 ms |

- **Lado a lado:** las dos versiones con waitress, cada una sobre una copia de `sigma_imss.db`, con las mismas 18
  peticiones. En la primera corrida, las dos de `/api/validar` se mandaron como formulario y solo compararon el caso
  sin datos (esa ruta recibe JSON); se repitió con JSON y siguieron saliendo idénticas (pantalla, filtros, CSS, JS, 404, detalle, validación en vivo, captura con errores, captura válida,
  duplicado, CSRF, exportar, descargar, `/console`). **18/18 respuestas idénticas**, una vez normalizados el
  nonce, las horas y el `ETag` (waitress lo calcula con la fecha del archivo). El lote IDSE salió igual y en
  `exportaciones/` junto a `servidor.py`.
- **Git:** plantillas, CSS, JS y `plazo.py` se movieron sin cambiar un byte (similitud 100 %). En `app.py`,
  `validaciones.py`, `database.py` y `exportar_idse.py` solo cambiaron imports, rutas y comentarios, y
  `__main__.py` tiene exactamente el arranque que estaba al final de `app.py`.
- **Navegador (Chrome headless):** la página se dibuja completa en los dos temas con los datos reales, `app.js`
  corre (cambia el `title` del botón de tema) y la consola no tiene errores ni bloqueos de la CSP.
- **Corrección:** quedaba `init_db` importado en `app.py` sin usarse (solo lo usaba el arranque que pasó a
  `__main__.py`). Se quitó.
- En el bloque 3 del E3 cambia entre corridas qué capturista recibe el id 3 y cuál el 4. Es propio de la prueba,
  que lanza los dos hilos a la vez; con `main` también varía (6 corridas: 3 y 3).

### Después de la verificación
- Pedro preguntó si, al aceptar el PR, la computadora de su compañero se reorganiza sola. Respuesta: GitHub sí;
  cada copia local necesita `git switch main` y `git pull` ([[preguntas-frecuentes]]).
- Se levantó Sigma con `python servidor.py` sobre la base real para que Pedro la viera, y se detuvo a petición suya.
- La extensión de Chrome no estaba conectada; la revisión visual se hizo con Chrome headless.

## 4. Hallazgos
- **Windows no dejó renombrar `static/`** con `git mv` ("Permission denied"): VS Code tenía la carpeta abierta. Se
  movieron los dos archivos uno por uno. `templates/` sí se pudo mover entera.
- **El p95 de captura con 20 usuarios varía entre corridas.** Con la nueva estructura dio 190.8 y 218.4 ms. Para
  descartar la reorganización, el bloque D se corrió contra el código de `main` en la misma sesión: 182.6 ms. Es la
  máquina, no el código; los 120.0 ms del informe son de otra corrida. Nota agregada en [[resultados-de-pruebas]].
- El reporte del E3 ahora dice `Archivo generado: pruebas\resultados\lote_idse_prueba.txt` en lugar de
  `lote_idse_prueba.txt`. La copia de `raw/resultados/` no se toca, porque es de antes.

## 5. Integración a `main`
Pedro decidió no esperar la revisión: pidió integrar todo a `main` y quitar el PR. Se hizo el merge `fb3a4a8`
(`--no-ff`, como el del E5), con una comprobación rápida sobre `main` integrado: compila, E3 con 8/8 y el servidor
responde. Después se pusieron al día `CLAUDE.md`, el `README.md`, este wiki y `raw/historial/git-log.md`, y se
subió `main`. GitHub no deja borrar un PR: el #2 quedó cerrado como integrado.

## 6. Pendientes
- Avisarle a Gael que la reorganización ya está en `main`, igual que con el E5.
- Al integrarlo, en cada copia local:
  - El desarrollo se arranca con `python -m sigma`.
  - Los reportes viejos sueltos en la raíz (`resultados_*`) ya no están en `.gitignore`, así que conviene
    borrarlos.
- ~~Decidir si se borra la rama~~: Pedro dejó la decisión al agente. Se borró en GitHub y en local, porque ya
  estaba integrada, ningún informe la cita y la página del PR #2 conserva los commits. También se borraron los
  reportes de las verificaciones en `pruebas/resultados/`; sus cifras están en esta página.

Ver también: [[cronologia]] · [[sesion-2026-10-04-entregable-5]] · [[arquitectura-general]]
