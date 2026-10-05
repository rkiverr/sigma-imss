---
tipo: regla
tags: [sdi, sbc, salario-minimo, uma, lss]
fuentes: ["sigma/validaciones.py", "sigma/exportar_idse.py", "raw/normativa/lss-ley-del-seguro-social.md", "raw/normativa/racerf-reglamento-afiliacion.md", "raw/normativa/valores-oficiales-2026.md"]
actualizado: 2026-10-04
---

# Salario diario integrado (SDI) y sus límites legales

**Regla:** el salario base de cotización no puede ser **menor al salario mínimo general** ni cotizar **por
encima de 25 UMA**.

## Fundamento
- **LSS, art. 28:** los asegurados se inscriben con el salario base de cotización que perciben, con estos límites:
  - **Superior:** "el equivalente a veinticinco veces el salario mínimo general que rija en el Distrito
    Federal". Desde la reforma constitucional de desindexación (2016), esa referencia se entiende hecha a la
    **UMA**.
  - **Inferior:** "el salario mínimo general del área geográfica respectiva". Nuevo León está en la zona
    general.
- **RACERF, art. 45:** los salarios se comunican "sin exceder los límites establecidos en el artículo 28".

## Valores vigentes (`validaciones.py`)
| Año | Salario mínimo general (desde el 1 de enero) | UMA diaria (desde el 1 de febrero) | Tope = 25 UMA |
|---|---|---|---|
| 2025 | 278.80 | 113.14 | 2,828.50 |
| 2026 | **315.04** | **117.31** | **2,932.75** |

`limites_sbc(fecha)` toma el año del movimiento. En **enero** usa la UMA del año anterior; si el año no está en
la tabla, usa el más reciente. **Hay que actualizar la tabla cada año** ([[mantenimiento-anual]]).

## Cómo lo aplica Sigma
| Caso | Resultado |
|---|---|
| SDI vacío en un alta | Error |
| No numérico | Error |
| **Menor al salario mínimo** (por ejemplo, 45.05 en vez de 450.50) | **Error**: "…menor al salario mínimo general (315.04)… Revisa si se corrió el punto decimal." |
| Mayor a 10,000.00 | Error ("parece un error de captura") |
| **Mayor a 25 UMA** | **Aviso** ("…ante el IMSS se cotizará con el tope"). Se guarda el salario real, pero **el lote exporta el tope** (`exportar_idse._sdi_para_cotizar`) |

## Factor de integración
El SDI se calcula con el salario diario por el factor de integración. Con 15 días de aguinaldo, 12 de
vacaciones y 25 % de prima, el mínimo es (365 + 15 + 12 × 0.25) / 365 = **383/365 ≈ 1.0493**. El arnés lo usa
para generar SDI realistas ([[arnes-ambiente-relevante]]). Sigma **no** calcula el SDI: el capturista lo
escribe.

## Antes del E5
El límite era de 1.00 a 10,000.00, así que un 45.05 pasaba sin aviso. Fue el error **E-08**, y el de 3,500 sin
aviso el **E-09** ([[bugs-corregidos]]).

Ver también: [[reglas-de-validacion]] · [[lote-idse]] · [[adr-014-limites-legales-del-sdi]]
