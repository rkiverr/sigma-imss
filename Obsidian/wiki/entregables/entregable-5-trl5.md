---
tipo: entregable
tags: [trl5, ambiente-relevante, pruebas, seguridad, normativa]
fuentes: ["raw/entregables/e5-trl5-ambiente-relevante.md", "raw/entregables/e5-rubrica-del-maestro.md", "raw/resultados/"]
actualizado: 2026-10-04
---

# Entregable 5 — TRL 5: validación en ambiente relevante

**Fuentes crudas:**
- `raw/entregables/e5-trl5-ambiente-relevante.md`: el informe, 27 páginas con 11 figuras y 11 tablas.
- `raw/entregables/e5-rubrica-del-maestro.md`: la rúbrica.

**Estado:** redactado el 2026-10-04; falta subirlo a la plataforma (fecha por confirmar).
**Código:** 7 commits de la rama `trl5/ambiente-relevante`, integrados a `main` con `cffd375`.

## Lo que pedía el maestro
"El prototipo deberá comenzar a probarse considerando **condiciones semejantes a las existentes en la
empresa**". Son 12 puntos, todos cubiertos como H2 y en ese orden:
1. Ambiente real.
2. Diferencias entre laboratorio y empresa.
3. Condiciones de operación.
4. Pruebas.
5. Parámetros.
6. Resultados.
7. Errores detectados.
8. Ajustes.
9. Riesgos.
10. Seguridad.
11. Normativa.
12. Evaluación del desempeño.

## Cómo se planteó
- **Ambiente emulado, no real.** No se usaron datos reales: la LFPDPPP protege la CURP, el NSS y el salario, y
  el envío al IDSE exige la e.firma del patrón. La operación real es TRL 6–7.
- **Supuestos declarados**, porque la empresa no dio cifras:
  - 60 a 90 trabajadores en 4 a 6 obras.
  - Hasta 140 movimientos en un mes de rotación alta.
  - Picos de 20 a 30 altas al arrancar una obra.
  - Hasta 3 capturistas a la vez.
  - Mayoría de eventuales de la construcción (tipo 3).
- **Ambiente real modelado con dos lazos cerrados:**
  - Interno: segundos, validación y corrección del capturista.
  - Externo: días, acuse del IMSS.

  Ver [[sigma-como-sistema-de-control]].
- **Arnés nuevo** [[arnes-ambiente-relevante]], con bloques A–H. Se corrió **antes** (código del E4 con el
  servidor de Flask) y **después** (código ajustado con waitress).
- **10 criterios CA5-1…CA5-10.** El E4 cumplía 6 y el código ajustado cumple los 10 ([[resultados-de-pruebas]]).

## Resultados clave
| Medida | Antes (E4) | Después (E5) |
|---|---|---|
| Errores de captura detectados (128 en 16 categorías) | 50.0 % | **96.9 %** |
| Datos válidos rechazados por su formato (24) | 24 | 0 |
| Duplicados / errores 500 en 60 pares simultáneos | 5 / 7 | 0 / 0 |
| Hallazgos de seguridad (8 pruebas) | 5 | 0 |
| p95 de captura con 20 usuarios | 497.6 ms | 120.0 ms |
| Pares de color bajo 4.5:1 | 2 | 0 |

## Errores detectados y ajustes
20 errores (E-01…E-20):
- **15 corregidos** en el código ([[bugs-corregidos]]).
- **1 corregido en parte**, por el límite del dígito de RENAPO ([[curp]]).
- **4 planeados** para TRL 6: login, HTTPS, respaldo y PostgreSQL. A ellos se suma el layout del IDSE
  ([[hoja-de-ruta-trl6]]).

Las decisiones nuevas son [[adr-009-servidor-de-produccion-waitress]] a [[adr-014-limites-legales-del-sdi]] y
[[adr-016-arnes-como-caja-negra]].

## Normativa citada (verificada el 2026-10-04)
- **LSS:** art. 15, fr. I y II; art. 28; arts. 304 A, fr. II, y 304 B, fr. IV.
- **RACERF:** arts. 45, 46 y 47.
- **LFT:** art. 74.
- **LFPDPPP 2025:** arts. 14, 15, 18 y 19.
- **Estándares:** WCAG 2.1 (1.4.1 y 1.4.3), ISO/IEC 25010:2023 y OWASP Top 10:2025.

Los textos literales están en `raw/normativa/`. Ver [[plazo-legal]] y [[salario-sdi-y-limites]].

## Cómo se hizo
El método completo (python-docx, Mermaid, capturas, gráficas y Word por COM) está en
[[como-se-hizo-el-entregable-5]]. La sesión de trabajo está en [[sesion-2026-10-04-entregable-5]].

## Pendientes antes de entregarlo
- Que Pedro revise el documento y, si consigue cifras reales, sustituya los supuestos (Tablas 1 y 3).
- Subirlo a la plataforma.
- Avisar a Gael que los cambios entraron directo a `main`, sin PR.

Anterior: [[entregable-4-trl4]] · Hub: [[entregables-trl]]
