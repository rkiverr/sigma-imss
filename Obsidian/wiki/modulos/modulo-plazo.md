---
tipo: modulo
tags: [plazo, dias-habiles, lss, lft]
fuentes: ["sigma/plazo.py", "raw/normativa/lss-ley-del-seguro-social.md", "raw/normativa/lft-ley-federal-del-trabajo.md"]
actualizado: 2026-10-04
---

# `sigma/plazo.py` — plazo legal de cinco días hábiles

Tiene 101 líneas y es nuevo en el E5. Calcula si un movimiento está **en plazo, por vencer o vencido** según el
art. 15, fr. I, de la LSS. La regla de negocio completa está en [[plazo-legal]]. La lógica se portó de la versión
alterna del E3 (`imss_poc/plazo.py`).

## Constantes
- `UMBRAL_DIAS_HABILES = 5`.
- `DIAS_INHABILES_ADICIONALES = set()`: fechas `date` que el IMSS publica en el DOF cada año (por ejemplo, jueves
  y viernes santos) y los días de jornada electoral (LFT, art. 74, fr. IX). **Se llena a mano**
  ([[mantenimiento-anual]]).

## Funciones
| Función | Qué hace |
|---|---|
| `_enesimo_lunes(anio, mes, n)` | El n-ésimo lunes de un mes, para los feriados móviles |
| `dias_de_descanso(anio)` | Días de descanso obligatorio del art. 74 de la LFT, calculados por año |
| `es_dia_habil(dia)` | No es sábado, domingo, día de descanso ni día adicional |
| `fecha_limite(fecha)` | Cuenta 5 días hábiles **a partir del día siguiente** al movimiento |
| `dias_habiles_transcurridos(fecha, hoy)` | Días hábiles desde el día siguiente hasta hoy (inclusive) |
| `evaluar(fecha, hoy)` | `{"estado", "dias_habiles_transcurridos", "dias_habiles_restantes", "fecha_limite"}` |

`evaluar()` asigna el estado así:
- **VENCIDO** si transcurrieron más de 5 días hábiles.
- **POR_VENCER** si transcurrieron 4 o 5: es el último día hábil o el anterior.
- **EN_PLAZO** en los demás casos. Una fecha futura cuenta 0 días.

## Quién lo usa
- `validaciones.verificar_plazo()` convierte VENCIDO o POR_VENCER en un **aviso**.
- `app.capturar()` pone la `fecha_limite` en el mensaje de éxito.
- `prueba_ambiente_relevante.py` tiene **su propia copia** del calendario (`_descansos`, `dia_habil_atras`) para
  generar fechas de prueba.

## Transmisión del Poder Ejecutivo (corregido el 2026-10-04)
`dias_de_descanso()` agrega el **1 de octubre** cuando `anio % 6 == 2` (2024, 2030…), como dice la LFT reformada
en el DOF del 30-09-2024 (art. 74, fr. VII). Antes usaba el 1 de diciembre con `anio % 6 == 0` (BUG-01, commit
`3afbc9a`, [[bugs-corregidos]]). Las jornadas electorales (fr. IX) no se calculan: van en
`DIAS_INHABILES_ADICIONALES`.

## Trampas
- El conteo empieza **el día siguiente** al movimiento; el día del movimiento no cuenta.
- El arnés tiene una **copia** del calendario (`_descansos()`): si cambias `dias_de_descanso()`, cambia también
  la copia.
- Si cambias el umbral o el calendario, revisa los avisos que espera el bloque B del arnés (categoría B15).

Ver también: [[plazo-legal]] · [[modulo-validaciones]]
