---
tipo: bug
estado: abierto
tags: [bugs, pendientes, limitaciones]
fuentes: ["sigma/plazo.py", "raw/normativa/lft-ley-federal-del-trabajo.md", "raw/entregables/e5-trl5-ambiente-relevante.md"]
actualizado: 2026-10-04
---

# Bugs y limitaciones conocidos (abiertos)

Hoy no hay bugs abiertos. BUG-01, el feriado de transmisión del Ejecutivo, se corrigió el 2026-10-04 en el
commit `3afbc9a` ([[bugs-corregidos]]).

## Limitaciones declaradas en el E5 (planeadas para TRL 6)
| Clave | Limitación | Página |
|---|---|---|
| E-16 | Con 20 usuarios sin pausa, una captura llegó a 6.0 s (SQLite serializa las escrituras) | [[doble-motor-de-base-de-datos]] |
| E-17 | No hay autenticación: el usuario se elige de una lista | [[seguridad-web]] |
| E-18 | El tráfico en la LAN va sin cifrar (HTTP) | [[seguridad-web]] |
| E-19 | No hay respaldo automático de la base | [[riesgos]] |
| E-20 | El layout del lote IDSE no está confirmado contra el instructivo oficial (riesgo #1) | [[lote-idse]] |

## Otras limitaciones
| Limitación | Página |
|---|---|
| Del dígito verificador de RENAPO, algunos cambios de letra no se detectan (4 de 8) | [[curp]] |
| Las jornadas electorales (LFT, art. 74, fr. IX) no se calculan: se cargan a mano en `DIAS_INHABILES_ADICIONALES` | [[mantenimiento-anual]] |
| El movimiento 07 no está implementado | [[catalogos-idse]] |
| La interfaz solo usa el primer patrón | [[hoja-de-ruta-trl6]] |
| El estado `'Rechazado'` no se escribe nunca (espera la lectura del acuse) | [[modelo-de-datos]] |
| El punto verde de la insignia del motor es decorativo: no monitorea nada | [[preguntas-frecuentes]] |

Ver también: [[bugs-corregidos]] · [[hoja-de-ruta-trl6]]
