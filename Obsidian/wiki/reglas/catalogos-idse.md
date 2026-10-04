---
tipo: regla
tags: [catalogos, idse, tipo-trabajador, causa-baja]
fuentes: ["validaciones.py", "raw/entregables/e1-trl1-problematica.md"]
actualizado: 2026-10-04
---

# Catálogos del IDSE

Están en `validaciones.py`. Son la **misma fuente** para validar y para armar los desplegables: `app.py` los pasa
como `CATALOGOS`. El usuario elige la clave y se guarda solo la clave.

## Tipo de movimiento
| Clave | Significado |
|---|---|
| **08** | Alta o reingreso |
| **02** | Baja |
| 07 | Modificación de salario. Está en el E1, pero **no está implementado** ([[hoja-de-ruta-trl6]]) |

## Tipo de trabajador (`TIPOS_TRABAJADOR`), obligatorio en un alta
| Clave | Significado |
|---|---|
| 1 | Trabajador permanente |
| 2 | Trabajador eventual |
| 3 | Eventual de la construcción. Es lo más común en la empresa |
| 4 | Eventual del campo |

## Tipo de salario (`TIPOS_SALARIO`), obligatorio en un alta
| Clave | Significado |
|---|---|
| 0 | Fijo |
| 1 | Variable |
| 2 | Mixto |

## Tipo de jornada (`TIPOS_JORNADA`), obligatorio en un alta
| Clave | Significado |
|---|---|
| 1 | Jornada normal (semana completa) |
| 2 | Jornada reducida |
| 3 | Semana reducida |
| 4 | Jornada y semana reducidas |

## Causa de baja (`CAUSAS_BAJA`), obligatoria en una baja y prohibida en un alta
| Clave | Significado |
|---|---|
| 1 | Término de contrato |
| 2 | Separación voluntaria |
| 3 | Abandono de empleo |
| 4 | Defunción |
| 5 | Clausura |
| 6 | Otra |
| 7 | Ausentismo |
| 8 | Rescisión de contrato |
| 9 | Jubilación |
| A | Pensión |

## ⚠ Diferencias con el Entregable 1
- El E1 listó el tipo de trabajador "2 = Eventual ciudad" y el tipo de jornada "0 = Normal / 1 a 6 =
  reducidas". El código usa las claves de arriba.
- El E1 tiene "9 = Jubilación / Pensión"; el código las separa en 9 y A.

**Antes de operar en serio, hay que confirmar los catálogos contra el instructivo oficial del IDSE**, el mismo
que hace falta para el layout ([[lote-idse]]).

## Historia
En el E3, la causa de baja era texto libre. En el E4 se volvió catálogo, y por eso se actualizaron los casos C2
y C5 del arnés ([[arnes-prueba-de-concepto]]).

Ver también: [[reglas-de-validacion]] · [[glosario]]
