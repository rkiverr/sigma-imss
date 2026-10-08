---
tipo: decision
estado: vigente
fecha: 2026-10-07 (Entregable 6)
tags: [base-de-datos, migracion, compatibilidad]
fuentes: ["sigma/database.py"]
actualizado: 2026-10-07
---

# ADR-021: Columnas nuevas y migraciones de datos que se aplican una sola vez

**Contexto.** El TRL 6 agregó columnas (apellidos, UMF, guía, contraseñas, token) y cambió el significado de un
catálogo (jornada). Una base creada por una versión anterior, como la del escritorio de Pedro, debía seguir
funcionando sin borrarla.

**Decisión.**
- `init_db()` agrega las columnas que falten (`_COLUMNAS_NUEVAS`, en los dos motores) sin tocar los datos.
- `_MIGRACIONES` es una lista de `(clave, función)`; cada una se aplica **una sola vez** y queda en la tabla
  `migracion`. Hoy hay dos: `2026-10-07-jornada-oficial` (`1→0`, `2→6`; avisa de los `3`/`4`, que en el catálogo
  oficial necesitan el número de días) y `2026-10-07-nombres-separados`.
- `separar_nombre()` prueba todas las divisiones del nombre completo (con el nombre al final o al principio) y se
  queda con la que reproduce las iniciales de la CURP; si ninguna, primera palabra = paterno, segunda = materno.
  Con la base del escritorio separó bien "Garza **Díaz de León** Emilio".
- `servidor.py` respalda antes de migrar ([[adr-020-respaldo-automatico]]).

**Consecuencias.** Una migración nueva lleva una clave nueva; nunca se modifica una ya aplicada. Las bases nuevas
registran las migraciones al crearse, sin hacer nada.

Ver también: [[modulo-database]] · [[modelo-de-datos]] · [[decisiones]]
