---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [validacion, api, consistencia]
fuentes: ["app.py", "validaciones.py", "static/js/app.js"]
actualizado: 2026-10-04
---

# ADR-003: Un solo validador para el navegador y el servidor

**Contexto.** La interfaz necesita retroalimentación inmediata mientras el usuario escribe.

**Decisión.** El navegador **no tiene su propia copia de las reglas**. Envía el formulario a
`POST /api/validar`, que ejecuta **la misma** `validaciones.validar_campos()` que usa `POST /capturar`. Desde el
E5, también comparten la normalización ([[adr-011-normalizacion-unica-y-data-longitud]]).

**Por qué.** Si hubiera dos copias, se desincronizarían en cuanto alguien cambiara una. Así es imposible que la
ayuda visual diga una cosa y el servidor haga otra. La validación del cliente es **ayuda visual**; la que manda
es la del servidor.

**Consecuencias.**
- Cada campo que se valida en vivo cuesta una petición HTTP (unos 8 ms de p95 en el E5).
- Las reglas que necesitan la base (conflictos, duplicados, historial) **no** se ven en vivo, solo al guardar.
- `validar_movimiento()` conserva su firma `(bool, list[str])` porque la usa `test_prueba_concepto.py`.

Ver: [[modulo-validaciones]] · [[decisiones]]
