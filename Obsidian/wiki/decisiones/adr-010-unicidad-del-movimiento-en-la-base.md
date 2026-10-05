---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [concurrencia, integridad, unique, carreras]
fuentes: ["sigma/database.py", "sigma/app.py", "raw/resultados/e5-arnes-ambiente-relevante-antes.md"]
actualizado: 2026-10-04
---

# ADR-010: La unicidad del movimiento la garantiza la base de datos

**Contexto.** `movimiento_duplicado()` revisa antes de insertar, pero **dos capturistas que guardan lo mismo al
mismo tiempo** pasan los dos la revisión antes de que cualquiera escriba. Es una condición de carrera. En el
bloque C del E5, con el código del E4:
- **5 de 25 reingresos quedaron duplicados** en la base.
- **7 de 25 altas de trabajadores nuevos** terminaron en **error 500**: `IntegrityError` por la CURP o el NSS
  únicos.

**Decisión.**
1. Índice **`UNIQUE (trabajador_id, tipo_movimiento, fecha_movimiento)`** (`uq_movimiento_trabajador_tipo_fecha`),
   creado aparte en `init_db()`. Si la base ya trae duplicados, solo avisa.
2. En `capturar()`, `_guardar_movimiento()` va dentro de `try/except ERRORES_DE_INTEGRIDAD`. Si falla, hace
   `conn.rollback()` y responde con un error claro (422): "Otro usuario acaba de registrar este mismo
   movimiento…".

**Por qué.** Es la lección del E3: **la concurrencia la resuelve el motor de la base**, no la aplicación.
Revisar antes da buenos mensajes, y la restricción da la garantía.

**Resultado (E5).** 60 pares simultáneos: **0 duplicados y 0 errores 500.**

**Consecuencias.** `ERRORES_DE_INTEGRIDAD` cubre sqlite3 y psycopg2. El rollback deshace también el UPDATE del
trabajador que hace `obtener_o_crear_trabajador`.

Ver: [[modelo-de-datos]] · [[flujo-de-captura]] · [[decisiones]]
