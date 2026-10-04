---
tipo: entregable
tags: [trl1, problematica, variables, objetivos]
fuentes: ["raw/entregables/e1-trl1-problematica.md"]
actualizado: 2026-10-04
---

# Entregable 1 — TRL 1: problemática y variables

**Fuente cruda:** `raw/entregables/e1-trl1-problematica.md` (PDF de 13 páginas, entregado).

## Qué contiene
Secciones: descripción de la empresa, área o proceso, problemática detallada, evidencias (Figura 1: el archivo
de control de julio de 2026 con filas rojas y verdes), consecuencias, variables involucradas, requerimientos de
automatización, revisión bibliográfica y tecnológica, principios científicos, justificación, objetivos y
bibliografía.

El detalle de la problemática está en [[empresa-y-problematica]].

## Variables que definió
| Grupo | Variables |
|---|---|
| Patrón | Registro patronal (11 alfanuméricos), RFC del patrón (12–13), firma electrónica |
| Trabajador | NSS (11 dígitos), CURP (18), RFC con homoclave (13), nombre completo |
| Alta (08) | Fecha DDMMAAAA, SDI (2 decimales), tipo de trabajador (1 permanente, 2 eventual ciudad, 3 eventual construcción, 4 eventual del campo), tipo de salario (0 fijo, 1 variable, 2 mixto), tipo de jornada, crédito INFONAVIT (opcional), UMF |
| Baja (02) | Fecha (posterior o igual al alta, dentro de 5 días hábiles), causa de baja (1 a 9) |
| Control | Tipo de movimiento (08, 02, **07**), folio de envío o lote, acuse IDSE (aceptado o rechazado), código de error |

## Principios científicos que invocó
Normalización de Codd, validación algorítmica con regex, arquitectura cliente-servidor y concurrencia, control
de acceso basado en roles y no repudio, y abstracción de datos para generar el formato IDSE. Se sostuvieron en
todo el proyecto ([[arquitectura-general]]).

## Lo que quedó pendiente desde aquí
- El movimiento **07** nunca se implementó ([[hoja-de-ruta-trl6]]).
- Crédito INFONAVIT y UMF: no están en el modelo de datos.
- "Control de acceso basado en roles": los roles existen, pero falta el login.
- La autorrevisión del equipo pidió citar la Figura 1 desde el texto y llenar "Asesor interno" ("No aplica").

Siguiente: [[entregable-2-trl2]] · Hub: [[entregables-trl]]
