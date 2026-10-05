---
tipo: operacion
tags: [mantenimiento, salario-minimo, uma, dias-inhabiles, anual]
fuentes: ["sigma/validaciones.py", "sigma/plazo.py", "raw/normativa/valores-oficiales-2026.md", "raw/normativa/lft-ley-federal-del-trabajo.md"]
actualizado: 2026-10-04
---

# Mantenimiento anual (cosas que caducan)

Sigma usa datos legales que **cambian cada año**. Si no se actualizan, el sistema valida con montos viejos.
Es el riesgo R-08 de [[riesgos]].

## Calendario
| Cuándo | Qué | Dónde en el código | Fuente |
|---|---|---|---|
| **Diciembre o enero** | **Salario mínimo general** del año nuevo (zona general; Nuevo León) | `validaciones.SALARIO_MINIMO_GENERAL[año]` | CONASAMI, gob.mx/conasami |
| **Enero** (rige desde el 1 de febrero) | **UMA** del año nuevo | `validaciones.UMA_DIARIA[año]` | INEGI, inegi.org.mx/temas/uma, publicada en el DOF |
| **Enero** | **Días inhábiles del IMSS** del año (jueves y viernes santos, etc.) | `plazo.DIAS_INHABILES_ADICIONALES` (agregar objetos `date`) | Acuerdo del IMSS en el DOF |
| Cuando haya **elecciones** federales o locales | El día de la jornada electoral (LFT, art. 74, fr. IX) | `plazo.DIAS_INHABILES_ADICIONALES` | Leyes electorales |
| Cada seis años (próximo: **2030**) | Transmisión del Poder Ejecutivo: **1 de octubre** (LFT, art. 74, fr. VII) | `plazo.dias_de_descanso()` lo calcula solo (`anio % 6 == 2`; corregido en `3afbc9a`, [[bugs-corregidos]]). Si la LFT vuelve a cambiar, actualiza también `_descansos()` del arnés | LFT |

## Procedimiento
1. Agrega el año nuevo en las tablas. Por ejemplo: `SALARIO_MINIMO_GENERAL = {2025: 278.80, 2026: 315.04, 2027:
   <monto>}`.
2. Si el año no está en la tabla, `limites_sbc()` usa **el más reciente** sin avisar. Por eso hay que
   actualizarla a tiempo.
3. Guarda la fuente oficial en `Obsidian/raw/normativa/valores-oficiales-<año>.md` como archivo **nuevo**.
4. Corre las pruebas: `python pruebas/test_prueba_concepto.py` (8/8) y
   `python pruebas/prueba_ambiente_relevante.py --bloques B`.
5. Actualiza [[salario-sdi-y-limites]] y el log.

## Valores vigentes hoy
- Salario mínimo general de 2026: **$315.04**.
- UMA de 2026: **$117.31** (tope de 25 UMA = **$2,932.75**).

Ver `raw/normativa/valores-oficiales-2026.md`.

Ver también: [[plazo-legal]] · [[modulo-validaciones]] · [[modulo-plazo]]
