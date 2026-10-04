---
tipo: hub
tags: [decisiones, adr]
fuentes: ["CLAUDE.md", "raw/entregables/"]
actualizado: 2026-10-04
---

# Registro de decisiones (ADR)

Cada decisión de diseño con su **porqué**, para no volver a discutirla. Si algún día se cambia una, se marca
como `estado: reemplazada` y se crea la nueva; nunca se borra.

| ADR | Decisión | Desde | Estado |
|---|---|---|---|
| [[adr-001-cliente-servidor-con-sgbd-relacional]] | Cliente-servidor con SGBD relacional (Alternativa 3) | E2 | vigente |
| [[adr-002-doble-motor-de-base-de-datos]] | PostgreSQL como objetivo y SQLite como respaldo automático | E4 | vigente |
| [[adr-003-un-solo-validador]] | Un solo validador para el navegador y el servidor | E4 | vigente |
| [[adr-004-errores-y-avisos-son-distintos]] | Errores bloquean; avisos no | E4 | vigente |
| [[adr-005-422-conservando-lo-capturado]] | El formulario rechazado responde 422 con lo capturado | E4 | vigente |
| [[adr-006-frontend-sin-dependencias]] | HTML, CSS y JS propios; sin CDN ni frameworks | E4 | vigente |
| [[adr-007-marcas-de-tiempo-texto-iso]] | Marcas de tiempo como texto ISO | E4 | vigente |
| [[adr-008-sql-con-marcadores-psycopg2]] | Todo el SQL con `%s` | E4 | vigente |
| [[adr-009-servidor-de-produccion-waitress]] | waitress en producción; depuración solo a petición | E5 | vigente |
| [[adr-010-unicidad-del-movimiento-en-la-base]] | Índice UNIQUE del movimiento + 422 ante `IntegrityError` | E5 | vigente |
| [[adr-011-normalizacion-unica-y-data-longitud]] | Una sola normalización; `data-longitud` en lugar de `maxlength` | E5 | vigente |
| [[adr-012-csrf-por-origin-y-csp-con-nonce]] | CSRF por `Origin` y CSP con nonce | E5 | vigente |
| [[adr-013-reglas-de-historial]] | Validar contra el historial del trabajador | E5 | vigente |
| [[adr-014-limites-legales-del-sdi]] | SDI entre el salario mínimo y 25 UMA; el lote exporta el tope | E5 | vigente |
| [[adr-015-lazo-cerrado]] | El sistema se clasifica como lazo cerrado | 2026-09-19 | vigente |
| [[adr-016-arnes-como-caja-negra]] | El arnés del E5 prueba por HTTP sobre una copia aislada | E5 | vigente |

Ver también: [[inicio]] · [[guia-para-modificar-el-codigo]]
