---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [sql, compatibilidad, regla-de-oro]
fuentes: ["sigma/database.py"]
actualizado: 2026-10-04
---

# ADR-008: Todo el SQL con marcadores `%s`

**Decisión.** Toda consulta de la aplicación usa marcadores **`%s`**, el estilo de psycopg2. Para SQLite,
`_CursorSQLite` los traduce a `?` con una expresión regular.

**Por qué.** Así la capa de negocio escribe **un solo SQL** para los dos motores
([[adr-002-doble-motor-de-base-de-datos]]).

**Regla de oro.** Si agregas SQL nuevo, **escríbelo con `%s`, nunca con `?`**. El traductor solo va en un
sentido: `?` rompería PostgreSQL.

**Además:**
- **Nunca** armes SQL concatenando datos del usuario. Siempre van como parámetros; así se evita la inyección SQL
  ([[seguridad-web]]).
- No uses `%` literal en el SQL, porque psycopg2 lo interpreta. Si hace falta, escríbelo como `%%`.

Ver: [[guia-para-modificar-el-codigo]] · [[decisiones]]
