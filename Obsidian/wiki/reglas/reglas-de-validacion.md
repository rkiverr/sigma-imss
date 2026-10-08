---
tipo: regla
tags: [validacion, errores, avisos, catalogo-de-reglas]
fuentes: ["sigma/validaciones.py", "sigma/app.py", "sigma/database.py"]
actualizado: 2026-10-07
---

# Catálogo completo de reglas de validación

Son todas las reglas que aplica Sigma antes de guardar un movimiento, en el orden en que se evalúan.
- **Error:** bloquea; el servidor responde 422.
- **Aviso:** guarda, pero muestra la advertencia.

Ver [[errores-vs-avisos]].

## A. Reglas del formulario aislado
Viven en `validaciones.validar_campos()` y también corren en `/api/validar`.

| # | Campo | Regla | Tipo | Mensaje (resumen) |
|---|---|---|---|---|
| 1 | Nombre | Obligatorio | Error | "El nombre completo del trabajador es obligatorio." |
| 2 | Nombre | Mínimo 5 caracteres | Error | "…parece incompleto (mínimo 5 caracteres)." |
| 3 | Nombre | Solo letras (con acentos y ñ), espacio, `.`, `-` y `'` (E5) | Error | "…revisa si se tecleó un número o un símbolo (por ejemplo, un cero en lugar de la letra O)." |
| 4 | CURP | Obligatoria, 18 caracteres y `CURP_REGEX` | Error | "La CURP debe tener 18 caracteres; se capturaron N." / "Formato de CURP inválido…" |
| 5 | CURP | La fecha AAMMDD que trae dentro debe existir | Error | "La fecha de nacimiento contenida en la CURP no existe en el calendario." |
| 6 | NSS | Obligatorio, solo dígitos, exactamente 11 | Error | "El NSS debe tener exactamente 11 dígitos; se capturaron N." |
| 7 | RFC | Obligatorio y `RFC_REGEX` (12 o 13) | Error | "Formato de RFC inválido…" |
| 8 | RFC | Coherente con la CURP: las 4 letras (si el RFC tiene 13) y la fecha | Error | "Las primeras 4 letras del RFC no coinciden…" / "La fecha de nacimiento del RFC no coincide…" |
| 9 | Fecha | Obligatoria, DDMMAAAA y real (descarta el 31 de febrero) | Error | "Formato de fecha inválido…" / "La combinación de día, mes y año no existe…" |
| 10 | Tipo | Solo 08 o 02 | Error | "El tipo de movimiento debe ser 08 (Alta o Reingreso) o 02 (Baja)." |
| 11 | SDI | Obligatorio en un alta; numérico | Error | "…es obligatorio en un alta." / "…debe ser un número (por ejemplo 450.50)." |
| 12 | SDI | **No menor al salario mínimo general** vigente en la fecha (E5) | Error | "El salario diario integrado (45.05) es menor al salario mínimo general (315.04)… Revisa si se corrió el punto decimal." |
| 13 | SDI | No mayor a 10,000.00 | Error | "…parece un error de captura: revisa el punto decimal." |
| 14 | Tipo de trabajador, de salario y de jornada | Obligatorios en un alta y del catálogo | Error | "Falta capturar el tipo de …: es un dato obligatorio para este tipo de movimiento." / "…no está en el catálogo del IDSE." |
| 15 | Causa de baja | Obligatoria en una baja y del catálogo | Error | "Falta capturar la causa de baja…" |
| 16 | Causa de baja | **No** debe venir en un alta | Error | "Un alta (08) no debe llevar causa de baja." |
| 17 | CURP | Dígito verificador de RENAPO (E5) | **Aviso** | "El dígito verificador de la CURP no coincide (se esperaba N)…" ([[curp]]) |
| 18 | NSS | Dígito verificador de Luhn | **Aviso** | "El dígito verificador del NSS no coincide (se esperaba N)…" ([[nss]]) |
| 19 | SDI | Mayor al tope de 25 UMA (E5) | **Aviso** | "…rebasa el tope de 25 UMA (2,932.75); ante el IMSS se cotizará con el tope (art. 28 LSS)." |
| 20 | Fecha | Más de 1 año al futuro o más de 5 de antigüedad | **Aviso** | "La fecha está a más de un año en el futuro…" |
| 21 | Fecha | **Plazo de 5 días hábiles** vencido o en su último día (E5). Si aplica el aviso 20, no se da este | **Aviso** | "El plazo legal de 5 días hábiles venció el DD/MM/AAAA (art. 15, fr. I, LSS)…" ([[plazo-legal]]) |

## B. Reglas que consultan la base
Viven en `app.capturar()` y **no** corren en `/api/validar`.

| # | Regla | Tipo | Dónde |
|---|---|---|---|
| 22 | El usuario que captura debe existir | Error | `_usuario_valido()` |
| 23 | La CURP ya registrada con **otro NSS**, o el NSS de **otra persona** | Error | `conflicto_de_identidad()` |
| 24 | El **mismo movimiento** (trabajador, tipo y fecha) ya capturado; da el folio | Error | `movimiento_duplicado()` |
| 25 | **Alta** de alguien con **alta vigente** (E5) | Error | `_validar_historial()` ([[historial-afiliatorio]]) |
| 26 | **Reingreso** con fecha anterior a su última baja (E5) | Error | ídem |
| 27 | **Baja** de alguien ya dado de baja (E5) | Error | ídem |
| 28 | **Baja** con fecha anterior a su alta vigente (E5) | Error | ídem |
| 29 | **Baja** de alguien **sin historial** en Sigma (E5) | **Aviso** | ídem |
| 30 | Otro capturista guardó lo mismo un instante antes (`IntegrityError`) (E5) | Error | `capturar()` + índice único |

## C. Otras reglas de la petición
- POST con `Origin`/`Referer` de otro sitio → **403** ([[seguridad-web]]).

## Cobertura medida (E5)
Con 128 errores inyectados en 16 categorías: **88 bloqueados, 36 avisados y 4 no detectados** (96.9 %), con 0
falsos positivos en 60 capturas limpias. Los 4 no detectados son CURP con una consonante cambiada, un límite del
algoritmo de RENAPO ([[resultados-de-pruebas]]).


## Reglas nuevas del TRL 6 (2026-10-07)
| Regla | Tipo | Dónde |
|---|---|---|
| Apellido paterno y nombre(s) obligatorios; materno opcional; 27 caracteres como máximo cada uno | error | `validar_nombre()` |
| UMF de 1 a 3 dígitos (no 000), obligatoria en el alta | error | `validar_umf()` |
| Jornada del catálogo oficial (0–6) | error | `validar_catalogo(TIPOS_JORNADA)` |
| Iniciales de la CURP contra el nombre capturado | aviso | `verificar_iniciales_curp()` |
| Año sin montos legales cargados | aviso | `aviso_montos_sin_cargar()` |

Ver también: [[modulo-validaciones]] · [[flujo-de-captura]] · [[catalogos-idse]] · [[salario-sdi-y-limites]]
