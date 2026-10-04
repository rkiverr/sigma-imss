---
tipo: historial
tags: [cronologia, git, ramas, entregables]
fuentes: ["raw/historial/git-log.md", "raw/entregables/"]
actualizado: 2026-10-04
---

# Cronología del proyecto

Todos los hechos con fecha, en orden. Los hashes salen de `raw/historial/git-log.md`.

| Fecha | Hecho | Quién | Referencia |
|---|---|---|---|
| ago 2026 | **Entregable 1 (TRL 1)**: problemática, variables del IMSS y objetivos | Equipo 4 | [[entregable-1-trl1]] |
| ago–sep 2026 | **Entregable 2 (TRL 2)**: 3 alternativas; se elige cliente-servidor + SGBD relacional | Equipo 4 | [[entregable-2-trl2]] · [[adr-001-cliente-servidor-con-sgbd-relacional]] |
| 2026-09-07 | `827835e` "first commit" (repo vacío con README) | Gael | — |
| 2026-09-08 | `e591752` Prototipo inicial: validación, base de datos y exportación IDSE (TRL 3) | Gael | [[arnes-prueba-de-concepto]] |
| 2026-09-09 | `7c1bc27` y `ccdfe48`: configuración de PostgreSQL y `client_encoding` por el `UnicodeDecodeError` | Gael | [[problemas-frecuentes]] |
| sep 2026 | **Entregable 3 (TRL 3)**: prueba de concepto, 8/8 casos | Equipo 4 | [[entregable-3-trl3]] |
| 2026-09-10 | `4c79ce4` Rediseño de la interfaz y refuerzo de validación y persistencia, en la rama `mejora/interfaz-y-validaciones`; se abre el **PR #1** | Pedro con Claude | [[sesion-2026-09-10-rediseno-y-entregable-4]] |
| 2026-09-11 | `9533587` Merge del PR #1 a `main` | Gael (rkiverr) | — |
| ~2026-09-15 | **Entregable 4 (TRL 4)**: prototipo integrado; 20 pruebas; 9 defectos corregidos | Pedro con Claude | [[entregable-4-trl4]] |
| 2026-09-19 | Pedro decide que Sigma se clasifica como **lazo cerrado** | Pedro | [[adr-015-lazo-cerrado]] |
| 2026-10-03 | Pedro confirma que el código vigente es `Desktop\sigma-imss` y que el PR #1 ya está fusionado | Pedro | [[equipo-y-contexto-academico]] |
| 2026-10-04 | `26befae` y `321d660`: arnés de ambiente relevante; línea base del código del E4: **6/10** | Pedro con Claude | [[arnes-ambiente-relevante]] |
| 2026-10-04 | `cb3f643`, `76d101b` y `cf3989b`: los 15 ajustes del E5 | Pedro con Claude | [[bugs-corregidos]] |
| 2026-10-04 | `0049036` y `b46ad50`: documentación y resultados en `CLAUDE.md`; corrida final: **10/10** | Pedro con Claude | [[resultados-de-pruebas]] |
| 2026-10-04 | **Entregable 5 (TRL 5)** redactado: 27 páginas, en Word y PDF | Pedro con Claude | [[entregable-5-trl5]] |
| 2026-10-04 | `cffd375` Merge de `trl5/ambiente-relevante` a `main`, **sin PR** (Pedro lo pidió así); push de `main` y de la rama | Pedro con Claude | [[sesion-2026-10-04-entregable-5]] |
| 2026-10-04 | `438b7e6` y `c29ad8f`: `CLAUDE.md` e `instrucciones/Instrucciones.md` al día con el E5 | Pedro con Claude | — |
| 2026-10-04 | `3afbc9a`: el feriado de transmisión del Ejecutivo pasa al 1 de octubre (LFT reformada en 2024; BUG-01) | Pedro con Claude | [[bugs-corregidos]] |
| 2026-10-04 | Se agrega este segundo cerebro (`Obsidian/`) con los punteros en `CLAUDE.md` y `README.md`; push a `main` | Pedro con Claude | [[inicio]] |
| (pendiente) | TRL 6: demostración en ambiente real | — | [[hoja-de-ruta-trl6]] |

## Ramas
| Rama | Punta | Estado |
|---|---|---|
| `main` | El commit que agrega `Obsidian/` (después de `3afbc9a`) | **Vigente.** Incluye todo: E5, corrección del calendario y este wiki |
| `mejora/interfaz-y-validaciones` | `4c79ce4` | Histórica (E4). Ya fusionada por el PR #1 |
| `trl5/ambiente-relevante` | `b46ad50` | Histórica (E5). Ya fusionada; se conserva porque el informe del E5 la cita por nombre |

Si cambian las ramas, regenera `raw/historial/git-log.md` y actualiza esta tabla y [[inicio]].

Ver también: [[trayectoria-trl]] · [[entregables-trl]]
