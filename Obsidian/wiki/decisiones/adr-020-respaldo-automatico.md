---
tipo: decision
estado: vigente
fecha: 2026-10-07 (Entregable 6)
tags: [respaldo, base-de-datos, operacion, riesgos]
fuentes: ["sigma/respaldo.py", "servidor.py"]
actualizado: 2026-10-07
---

# ADR-020: Respaldo automático al arrancar y cada 24 horas

**Contexto.** La base era un solo archivo en una PC y nadie lo copiaba (E-19, R-02). La LSS (art. 15, fr. II)
pide conservar los registros cinco años.

**Decisión.**
- `servidor.py` llama a `respaldo.respaldar()` **antes** de `init_db()` (así una migración nunca toca datos sin
  copia) y deja un hilo que respalda cada `SIGMA_RESPALDO_HORAS` (24).
- SQLite: API `backup` de sqlite3 (copia consistente aunque haya capturas en curso) → `journal_mode = DELETE`
  para que el respaldo sea un solo archivo → `PRAGMA integrity_check`. Se conservan
  `SIGMA_RESPALDOS_CONSERVAR` (30).
- PostgreSQL: `pg_dump --format=custom` si está instalado (no se pudo probar: no hay PostgreSQL en el equipo).
- `python -m sigma.respaldo --restaurar ARCHIVO` (con el servidor detenido) guarda antes una copia de la base
  actual.
- La carpeta es `SIGMA_RESPALDOS` (por omisión `respaldos/`, en `.gitignore`); en la oficina conviene otro disco.

**Por qué.** Copiar el archivo `.db` con el servidor encendido puede dejar una copia inconsistente (WAL); la API
de respaldo no. Hacerlo dentro del servidor evita depender del Programador de tareas.

**Consecuencias.** El arranque tarda lo que tarda copiar la base (0.1 s con 40 movimientos). Prueba en
[[arnes-integracion]] (bloque R): se pierde la base, se restaura el respaldo y los conteos coinciden.

Ver también: [[modulo-respaldo]] · [[riesgos]] · [[decisiones]]
