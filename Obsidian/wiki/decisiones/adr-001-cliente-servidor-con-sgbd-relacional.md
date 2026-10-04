---
tipo: decision
estado: vigente
fecha: 2026-09 (Entregable 2)
tags: [arquitectura, cliente-servidor, sgbd]
fuentes: ["raw/entregables/e2-trl2-alternativas-y-arquitectura.md"]
actualizado: 2026-10-04
---

# ADR-001: Cliente-servidor con SGBD relacional (Alternativa 3)

**Contexto.** El proceso vive en un Excel que usa una sola persona, sin auditoría y con el estado marcado por
colores ([[empresa-y-problematica]]).

**Decisión.** Un sistema centralizado **cliente-servidor**, con un **SGBD relacional** normalizado y una
interfaz web a la que entran varios usuarios.

**Por qué.**
- El motor de la base resuelve la **concurrencia** con bloqueos.
- La **normalización** (Codd) evita duplicar datos del trabajador.
- La interfaz web puede usar **texto en lugar de colores** (WCAG).
- La bitácora con usuario y hora da **trazabilidad**.

**Alternativas descartadas.**
- **Macros VBA en Excel:** no resuelven la concurrencia ni la auditoría.
- **Aplicación de escritorio con base local:** una sola persona a la vez; los residentes no tienen acceso.

**Consecuencias.** Requiere un servidor, aunque sea una PC de la oficina, y más desarrollo. Todas las demás
decisiones parten de esta. Los informes la citan como "Alternativa 3 del Entregable 2".

Ver: [[entregable-2-trl2]] · [[arquitectura-general]] · [[decisiones]]
