---
tipo: bug
estado: abierto
tags: [bugs, pendientes, limitaciones]
fuentes: ["sigma/plazo.py", "raw/normativa/lft-ley-federal-del-trabajo.md", "raw/entregables/e5-trl5-ambiente-relevante.md", "pruebas/prueba_integracion.py"]
actualizado: 2026-10-07
---

# Bugs y limitaciones conocidos (abiertos)

No hay bugs abiertos. Los encontrados en el E6 se corrigieron en la rama local `trl6/correcciones`
([[bugs-corregidos]]).

## Limitaciones declaradas
| Clave | Limitación | Página |
|---|---|---|
| P-11 (E-18) | Sin HTTPS: la sesión, la contraseña y los datos viajan en claro por la red local (S-03 del [[arnes-integracion]]) | [[seguridad-web]] |
| P-14 (E-16) | Sin PostgreSQL instalado: con 20 usuarios sin pausa, SQLite serializa las escrituras y la captura más lenta llega a segundos | [[doble-motor-de-base-de-datos]] |
| — | El lote sigue la estructura publicada, pero la codificación, el CRLF y la Ñ se confirman con un lote de prueba en el IDSE | [[lote-idse]] |
| — | Inicio de sesión: si una PC cierra sesión, las demás que usan la misma cuenta también salen (el token es por usuario) | [[modulo-usuarios]] |

## Otras limitaciones
| Limitación | Página |
|---|---|
| Del dígito verificador de RENAPO, algunos cambios de letra no se detectan (4 de 8); el aviso de iniciales solo cubre las 4 primeras letras | [[curp]] |
| Las jornadas electorales (LFT, art. 74, fr. IX) no se calculan: se cargan a mano en `DIAS_INHABILES_ADICIONALES` | [[mantenimiento-anual]] |
| El movimiento 07 no está implementado | [[catalogos-idse]] |
| La interfaz solo usa el primer patrón | [[hoja-de-ruta-trl6]] |
| El estado `'Rechazado'` no se escribe nunca (espera la lectura del acuse) | [[modelo-de-datos]] |
| El respaldo de PostgreSQL (`pg_dump`) no se ha probado: no hay PostgreSQL en el equipo de pruebas | [[modulo-respaldo]] |

Ver también: [[bugs-corregidos]] · [[hoja-de-ruta-trl6]]
