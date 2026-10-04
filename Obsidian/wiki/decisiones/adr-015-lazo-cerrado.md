---
tipo: decision
estado: vigente
fecha: 2026-09-19 (decisión de Pedro)
tags: [control, lazo-cerrado, redaccion]
fuentes: ["raw/entregables/e4-trl4-prototipo-integrado.md", "raw/entregables/e5-trl5-ambiente-relevante.md"]
actualizado: 2026-10-04
---

# ADR-015: El sistema se clasifica como lazo cerrado

**Contexto.**
- El E2 y el E3 describieron Sigma como **lazo cerrado**.
- El E4 lo reclasificó como "lazo **abierto** con retroalimentación al operador", porque el sistema no corrige
  los datos por sí mismo.

**Decisión (Pedro, 2026-09-19).** La clasificación oficial es **lazo cerrado**. Todo texto nuevo lo describe así
y el E5 ya lo hizo.

**Argumento.**
- El comparador (`validaciones.py`) **mide el error** contra la referencia (las reglas del IMSS) y lo **regresa a
  la entrada**. El operador forma parte del lazo y corrige.
- Hay un **segundo lazo**, el externo: el acuse del IMSS, que llega días después.

Ver [[sigma-como-sistema-de-control]].

**Consecuencias.** El E4 ya entregado conserva su redacción. Si el maestro pide una versión final integrada,
conviene unificarla.

Ver: [[decisiones]]
