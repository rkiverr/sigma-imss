---
tipo: historial
tags: [sesion, entregable-5, trl5, merge, segundo-cerebro]
fuentes: ["raw/historial/git-log.md", "raw/entregables/e5-trl5-ambiente-relevante.md", "raw/resultados/"]
actualizado: 2026-10-04
---

# Sesión del 4 de oct de 2026: Entregable 5, integración a main y segundo cerebro

Trabajo de Pedro con Claude Code.

## 1. Lo que pidió Pedro
- **El documento:** el Entregable 5, "TRL 5: Validación en ambiente relevante", con la rúbrica de 12 puntos
  (`raw/entregables/e5-rubrica-del-maestro.md`), en Word y PDF, con el mismo formato que los anteriores.
- **Permiso para correr el proyecto:** autorizó correrlo para sacar capturas.

Sus respuestas a las preguntas de arranque:
- Los ajustes van en una **rama nueva**.
- Las cifras de la empresa se manejan como **supuestos declarados**.
- El **arnés queda en el repo**.

## 2. Línea base (código del E4)
- Se escribió [[arnes-ambiente-relevante]] (`26befae`) y se corrió contra el código del E4 con `--codigo`.
- Resultado: **6 de 10** criterios. Aparecieron 20 errores (E-01…E-20).
- Tropiezos del arnés, ya resueltos en `321d660`:
  - **`WinError 10048`:** se agotaban los puertos del cliente. Se resolvió con conexiones persistentes y
    `SO_LINGER 0`.
  - **Memoria de 4 MB:** era la del lanzador del venv. Ahora se mide el proceso hijo y el árbol se mata con
    `taskkill /T /F`.
  - **Regex de `tasklist`:** esperaba `K"`, pero Windows imprime `KB"`.
  - **NSS repetidos:** la plantilla sintética generaba colisiones. Se agregó un conjunto de NSS usados.
  - **Carreras no reproducibles:** ahora los dos clientes abren la conexión antes de la barrera.
  - **`shutil.ignore_patterns` como atributo de clase:** daba `TypeError`. Se envolvió en `staticmethod`.

## 3. Ajustes (rama `trl5/ambiente-relevante`)
- **`cb3f643`:** plazo legal, límites del SDI, dígito de la CURP, nombre sin dígitos y normalización única.
- **`76d101b`:** waitress, reglas de historial, índice UNIQUE, CSRF, CSP y folio fuera de rango.
- **`cf3989b`:** `data-longitud`, contraste AA y pie TRL 5.
- **`0049036` y `b46ad50`:** documentación y resultados en `CLAUDE.md`.

Detalle de cada uno en [[bugs-corregidos]]. Las decisiones van de [[adr-009-servidor-de-produccion-waitress]] a
[[adr-014-limites-legales-del-sdi]], más [[adr-016-arnes-como-caja-negra]].

Corrida final: **10 de 10** ([[resultados-de-pruebas]]).

## 4. El documento
- **Tamaño:** 27 páginas, 11 figuras y 11 tablas. Se guardó como `Entregable 5 — TRL 5.docx` y `.pdf` en la
  carpeta de la materia.
- **Método completo:** [[como-se-hizo-el-entregable-5]].
- **Tropiezos:**
  - **Huecos de paginación por diagramas altos:** se rediseñaron en horizontal. Subir el tamaño de fuente lo
    empeoraba. Se agregó un detector de huecos con pymupdf.
  - **Capturas en tema oscuro:** Chrome headless tomaba el tema oscuro de Windows. Se inyecta
    `data-tema="claro"`.
  - **Autor ajeno:** la plantilla heredada traía "BRENDA JANETT ALONSO GUTIERREZ" en los metadatos. Se cambió a
    "Equipo 4".

## 5. Integración y publicación
- **Merge:** Pedro pidió "súbelo al main de una". Se hizo el merge `--no-ff` `cffd375`, sin PR, después de
  verificar `py_compile`, el arnés del E3 (8/8) y los bloques B, C y G.
- **Push:** se empujaron `main` y `trl5/ambiente-relevante`. La rama se conserva porque el informe la cita.
- **Documentación al día:**
  - `438b7e6`: `CLAUDE.md` del repo, con la sección "Ramas".
  - `c29ad8f`: `instrucciones/Instrucciones.md`.
- **Explicación:** Pedro pidió que se le explicaran las mejoras. Hay que **responderle siempre en español**.

## 6. Segundo cerebro
- **Lo que pidió:** crear `Obsidian/` con el patrón LLM Wiki, solo archivos `.md` y solo contenido del proyecto.
  "Primero hazlo en mi computadora y luego lo subimos al git": primero se hizo local y después Pedro dijo
  "haz todo eso y súbelo".
- **Fuentes crudas:** se extrajeron con scripts en el scratchpad:
  - Entregables E1–E5: docx → md, quitando los espacios de ancho cero (U+200B) que dejan los PDF.
  - Normativa: de los PDF oficiales.
  - `git log`.
  - Salidas de los arneses.
- **Hallazgo al extraer la LFT:** BUG-01. El feriado de transmisión del Ejecutivo debe ser el 1 de octubre, no
  el 1 de diciembre. Pedro autorizó la corrección y se hizo en `3afbc9a` ([[bugs-corregidos]]). Se verificó con
  el arnés del E3 (8/8) y los bloques B, C y G (96.9 %, 0 duplicados, 0 hallazgos).
- **Publicación:**
  - Un commit agrega `Obsidian/` junto con el puntero en `CLAUDE.md` y `README.md`.
  - `.gitignore` excluye `Obsidian/.obsidian/` y `Obsidian/.trash/`, que es la configuración personal de
    Obsidian.
  - Todo se empujó a `main`.

## Pendientes que deja
- Que Pedro revise el E5 y lo suba a la plataforma.
- Avisar a Gael que los cambios entraron directo a `main`, sin PR.
- Todo lo de TRL 6 ([[hoja-de-ruta-trl6]]).

Ver también: [[cronologia]] · [[entregable-5-trl5]]
