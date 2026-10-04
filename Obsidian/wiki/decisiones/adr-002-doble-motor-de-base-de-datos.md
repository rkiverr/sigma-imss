---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [base-de-datos, postgresql, sqlite]
fuentes: ["database.py", "CLAUDE.md"]
actualizado: 2026-10-04
---

# ADR-002: PostgreSQL como objetivo, SQLite como respaldo automático

**Contexto.** El prototipo del E3 exigía PostgreSQL. En la laptop de Pedro no había PostgreSQL ni psycopg2
(el puerto 5432 estaba cerrado), así que **la aplicación no arrancaba**.

**Decisión.** `database.py` elige el motor una vez al arrancar:
1. Con `SIGMA_DB=sqlite`, usa SQLite.
2. Si PostgreSQL responde, usa PostgreSQL.
3. En cualquier otro caso, usa SQLite con un aviso.

**Por qué.** El prototipo debe poder **demostrarse en cualquier equipo** sin perder el argumento del SGBD
relacional de la Alternativa 3.

**Cómo no se duplica la lógica.** Todo el SQL usa `%s` y unos envoltorios lo traducen a `?` para SQLite. Solo
se duplica el DDL ([[adr-008-sql-con-marcadores-psycopg2]], [[doble-motor-de-base-de-datos]]).

**Consecuencias.**
- La base es **local de cada persona** (`sigma_imss.db` está en `.gitignore`).
- Para compartir datos hace falta un PostgreSQL y apuntar `DATABASE_URL` a él.
- Con mucha concurrencia, SQLite serializa las escrituras: hasta 6 s con 20 usuarios sin pausa en el E5.

**Si algún día se quiere exigir PostgreSQL**, quitar el respaldo es un cambio pequeño.

Ver: [[modulo-database]] · [[decisiones]]
