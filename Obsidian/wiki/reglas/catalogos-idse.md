---
tipo: regla
tags: [catalogos, idse, tipo-trabajador, causa-baja]
fuentes: ["sigma/validaciones.py", "raw/entregables/e1-trl1-problematica.md"]
actualizado: 2026-10-07
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

## Semana o jornada reducida (`TIPOS_JORNADA`), obligatoria en un alta
Catálogo oficial del IMSS (posición 118 del lote), vigente desde el TRL 6:

| Clave | Significado |
|---|---|
| 0 | Jornada normal |
| 1 a 5 | Semana reducida: un día … cinco días |
| 6 | Jornada reducida |

Hasta el E5 Sigma usaba un catálogo propio (1 = normal, 2 = jornada reducida, 3 = semana reducida, 4 = ambas): el
"1" que exportaba para la jornada normal el IMSS lo lee como **un día a la semana** (problema P-06 del E6). La
migración `2026-10-07-jornada-oficial` convierte `1→0` y `2→6`; los `3`/`4` necesitan el número de días y se
avisan ([[adr-021-migraciones-de-datos-unicas]]).

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

## Comparación con la estructura oficial y con el Entregable 1
- Contra el documento del IMSS "Estructura de Movimientos afiliatorios" (2026-10-07): tipo de trabajador (1–4),
  tipo de salario (0–2) y causa de baja (1–9 y A) coinciden; la jornada coincide desde el TRL 6.
- El E1 listó "2 = Eventual ciudad" (el documento oficial dice "eventual de la ciudad"), la jornada "0 = Normal /
  1 a 6 = reducidas" (era correcto) y "9 = Jubilación / Pensión" (el oficial las separa en 9 y A).

## Historia
En el E3, la causa de baja era texto libre. En el E4 se volvió catálogo, y por eso se actualizaron los casos C2
y C5 del arnés ([[arnes-prueba-de-concepto]]).

Ver también: [[reglas-de-validacion]] · [[glosario]]
