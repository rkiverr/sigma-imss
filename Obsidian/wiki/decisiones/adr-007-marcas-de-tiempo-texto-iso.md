---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [fechas, sqlite, python]
fuentes: ["database.py", "app.py"]
actualizado: 2026-10-04
---

# ADR-007: Marcas de tiempo como texto ISO

**Decisión.** `bitacora.timestamp` y `movimiento.creado_en` se guardan como **texto ISO**
(`AAAA-MM-DD HH:MM:SS`), generado por `database.ahora()` o por `datetime.now().isoformat(sep=" ",
timespec="seconds")`, **no** como objetos `datetime`.

**Por qué.** Python 3.12+ **deprecó los adaptadores de fecha** de sqlite3. Una cadena ISO funciona igual en una
columna `TIMESTAMP` de PostgreSQL y en una `TEXT` de SQLite.

**Consecuencias.** Al leer, el filtro de plantilla `momento` acepta los dos tipos: `datetime` desde PostgreSQL y
texto desde SQLite.

Ver: [[modulo-database]] · [[decisiones]]
