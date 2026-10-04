---
tipo: entregable
tags: [trl3, prueba-de-concepto, regex, flask]
fuentes: ["raw/entregables/e3-trl3-prueba-de-concepto.md", "test_prueba_concepto.py"]
actualizado: 2026-10-04
---

# Entregable 3 — TRL 3: prueba de concepto

**Fuente cruda:** `raw/entregables/e3-trl3-prueba-de-concepto.md` (PDF de 18 páginas, entregado).
**Código:** primeros commits de Gael Rivera (`827835e`–`ccdfe48`, del 7 al 9 de sep).

## Qué se probó
El **lazo cerrado a nivel software** con un prototipo web Flask, en dos escenarios:
- **Perturbación:** datos con errores → el sistema se detiene y avisa con **texto**, no con colores.
- **Salida de control:** datos correctos → se genera la cadena de texto del IDSE.

## Criterios de aceptación (4)
1. Filtro regex funcional: NSS de 11 dígitos sin letras y CURP de 18 caracteres.
2. Validación sin colores (WCAG): mensajes explícitos en texto.
3. Abstracción y generación automática de la cadena IDSE.
4. Operación simultánea simulada (cliente-servidor).

Los cuatro **cumplieron**.

## Cómo se programó
Un módulo por bloque del diagrama del E2:
- `validaciones.py` = controlador.
- `exportar_idse.py` = actuador.
- `database.py` = persistencia: 5 tablas normalizadas, `PRAGMA foreign_keys`, `UNIQUE` en CURP y NSS, `CHECK`
  en tipo, estado y rol.
- `app.py` = servidor con 4 rutas.
- `templates/index.html` = cliente.

El **arnés** `test_prueba_concepto.py` tiene 8 casos (C1–C8) en 3 bloques: validación, exportación y
concurrencia con 2 hilos ([[arnes-prueba-de-concepto]]).

## Resultados
- 8/8 casos (100 %).
- Lote de 2 líneas con 11 campos separados por `|`.
- Dos capturas simultáneas con ids distintos y bitácora por usuario.

## Problemas que dejó (y quién los resolvió)
| Problema del E3 | Resolución |
|---|---|
| El lote usa campos delimitados, no el **ancho fijo** oficial | **Sigue abierto**: riesgo #1 ([[lote-idse]]) |
| `obtener_o_crear_trabajador()` buscaba solo por CURP → `UNIQUE constraint failed: trabajador.nss` → error 500 | E4: `conflicto_de_identidad()` ([[bugs-corregidos]]) |
| Trazabilidad sin autenticación | **Sigue abierto** ([[hoja-de-ruta-trl6]]) |
| Movimiento 07 no implementado | **Sigue abierto** |
| `causa_baja` como texto libre | E4: catálogo IDSE ([[catalogos-idse]]) |
| SDI sin validación numérica | E4: numérico; E5: límites del art. 28 de la LSS ([[salario-sdi-y-limites]]) |
| `cumplimiento_plazo` y el sensor de acuse sin programar | E5: plazo ([[plazo-legal]]); el acuse **sigue abierto** |
| Debug activo y clave de sesión fija | E4: clave efímera; E5: servidor de producción ([[adr-009-servidor-de-produccion-waitress]]) |

## Aprendizajes que dejó (siguen vigentes)
- Una regex es un filtro **necesario pero insuficiente**: el 31 de febrero pasa la regex y lo detiene `datetime`.
- Validar la **forma** y validar el **sentido** de un dato son dos operaciones distintas.
- Las restricciones de la base son una **segunda barrera**, pero hay que traducirlas a mensajes comprensibles.
- **Trazabilidad no es control de acceso.**
- **La concurrencia la resuelve el motor de base de datos**, no la aplicación (idea que el E5 llevó al índice
  único).

## Versión alterna (no entregada)
Existe otra versión del E3, más elaborada, en la carpeta `AUTO/imss_poc/` del semestre: 6 capas, con
`plazo.py`, `reglas.py` e `identificadores.py`. **No es el código del proyecto**, pero de ahí salió la lógica de
plazo y de historial que se portó en el E5 ([[modulo-plazo]], [[historial-afiliatorio]]).

Anterior: [[entregable-2-trl2]] · Siguiente: [[entregable-4-trl4]] · Hub: [[entregables-trl]]
