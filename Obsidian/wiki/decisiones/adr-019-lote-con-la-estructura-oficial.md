---
tipo: decision
estado: vigente
fecha: 2026-10-07 (Entregable 6)
tags: [idse, lote, layout, catalogos, nombre, umf]
fuentes: ["sigma/exportar_idse.py", "sigma/validaciones.py", "sigma/database.py"]
actualizado: 2026-10-07
---

# ADR-019: El lote sigue la estructura oficial del IMSS (168 posiciones, un archivo por tipo)

**Contexto.** Hasta el E5 el lote era una representación con campos separados por `|`, en UTF-8, sin el nombre
del trabajador y con altas y bajas en el mismo archivo (riesgo R-01, el #1 del proyecto). En el E6 se obtuvo el
documento del IMSS "Estructura de Movimientos afiliatorios"
(`https://www.imss.gob.mx/sites/all/statics/sua/dispmag/EstructuraMovimientosAfiliatorios.pdf`) y la comparación
dio 7 de 18 aspectos compatibles. Además, el catálogo de jornada de Sigma usaba 1 para la jornada normal, que el
IMSS lee como "un día a la semana" (el E1 ya decía 0 = normal).

**Decisión.**
- `exportar_idse.ESTRUCTURA` transcribe el documento campo por campo (posición, longitud y tipo A/N/AN) para
  altas o reingresos (08) y bajas (02). `generar_linea_idse()` afirma 168 posiciones.
- Un archivo por tipo: `lote_idse_altas_…txt` y `lote_idse_bajas_…txt`.
- La captura separa **apellido paterno, materno (opcional) y nombre(s)**, de 27 posiciones cada uno, y pide la
  **UMF** en el alta. `nombre_completo` se conserva como dato derivado.
- La **guía** es un dato del patrón (`patron.guia`, semilla `00000`); la **clave del trabajador** es su id.
- Catálogo de jornada oficial: 0 = normal, 1–5 = días de la semana reducida, 6 = jornada reducida.
- Salario en 6 dígitos con 2 decimales implícitos, topado a 25 UMA; en la baja, 15 ceros, la causa en la 149 y la
  CURP en blanco.
- Codificación Windows-1252 (un byte por carácter, para que los 168 caracteres sean 168 bytes) y CRLF.

**Por qué.** Un carácter de desfase rechaza el lote entero. Tener la estructura como tabla de datos permite
corregir una posición sin tocar la lógica (lo que proponía la versión alterna del E3).

**Consecuencias.**
- Las bases anteriores se migran: nombres separados y jornada `1→0`, `2→6` ([[adr-021-migraciones-de-datos-unicas]]).
- Los movimientos viejos sin UMF ni apellidos no se exportan y la interfaz lo avisa.
- **Por confirmar con un lote de prueba en el IDSE:** la codificación, el CRLF y la Ñ (el documento no lo dice), y
  que el salario lleve 2 decimales implícitos.

**Alternativas descartadas.** Seguir con el formato delimitado (no lo acepta el IDSE). Derivar los apellidos del
nombre completo al exportar: falla con apellidos compuestos ("Díaz de León").

Ver también: [[lote-idse]] · [[catalogos-idse]] · [[modulo-exportar-idse]] · [[decisiones]]
