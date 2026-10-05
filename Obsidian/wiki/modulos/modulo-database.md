---
tipo: modulo
tags: [database, persistencia, sqlite, postgresql, transacciones]
fuentes: ["sigma/database.py"]
actualizado: 2026-10-04
---

# `sigma/database.py` — persistencia y selección de motor

Tiene 482 líneas. Implementa el modelo relacional ([[modelo-de-datos]]) sobre **PostgreSQL o SQLite**, con la
misma lógica para ambos ([[doble-motor-de-base-de-datos]]).

## Configuración (variables de entorno, se leen **al importar**)
| Variable | Por defecto | Para qué |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/sigma_imss?client_encoding=UTF8` | Conexión a PostgreSQL |
| `SIGMA_DB` | vacío | `sqlite` o `postgres` para forzar el motor |
| `SQLITE_PATH` | `sigma_imss.db` en la raíz del repositorio (`RAIZ`, fuera de `sigma/`) | Archivo de SQLite |

Al importarse, fuerza `LC_ALL=C` y `LANG=C` (y `PGCLIENTENCODING=UTF8`). Así, en Windows en español, `psycopg2`
no truena con `UnicodeDecodeError` al leer los mensajes de error de `libpq` ([[problemas-frecuentes]]).

## Selección del motor (`_resolver_backend`)
Se decide **una sola vez** por proceso:
1. Con `SIGMA_DB=sqlite`, usa SQLite.
2. Si hay `psycopg2` y PostgreSQL responde, usa PostgreSQL.
3. En cualquier otro caso usa SQLite, e imprime `[sigma] PostgreSQL no disponible (…). Usando SQLite: …`.
4. Con `SIGMA_DB=postgres` y sin servidor, lanza `ErrorBaseDeDatos`, que el navegador ve como un 503.

`descripcion_backend()` devuelve el texto que muestra la insignia de la barra (por ejemplo,
"SQLite - sigma_imss.db").

## Piezas clave
- **`_ConexionSQLite` y `_CursorSQLite`**: envoltorios que traducen `%s` → `?` (`_traducir`). Por eso **todo el
  SQL de la aplicación usa `%s`** ([[adr-008-sql-con-marcadores-psycopg2]]).
- `_abrir_sqlite()`: `timeout=10`, `row_factory=sqlite3.Row`, `PRAGMA foreign_keys = ON` y
  `PRAGMA journal_mode = WAL` (permite leer mientras alguien escribe).
- **`conexion(commit=False)`**: *context manager* que confirma si `commit=True`, revierte si hubo excepción y
  **siempre** cierra.
- `get_conn()`: conexión nueva al motor activo. La usa el arnés del E3.
- **`ERRORES_DE_INTEGRIDAD`**: `(sqlite3.IntegrityError, psycopg2.IntegrityError)`. `app.py` lo atrapa en las
  carreras.
- `ErrorBaseDeDatos`: error de conexión o de configuración.

## Esquema e inicialización
- `_DDL_POSTGRES` y `_DDL_SQLITE`: es lo único duplicado, porque `SERIAL` y `AUTOINCREMENT` no son
  intercambiables.
- **`init_db()`** es idempotente:
  1. Crea las tablas e índices.
  2. Migra `creado_en` en SQLite viejas.
  3. Siembra el patrón y los usuarios.
  4. En un bloque aparte, crea `_INDICE_MOVIMIENTO_UNICO` (`uq_movimiento_trabajador_tipo_fecha`). Si la base ya
     tiene duplicados, solo imprime un aviso ([[adr-010-unicidad-del-movimiento-en-la-base]]).
- `PATRON_SEMILLA = ("A1234567890", "Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V.")`. Es un dato
  **inventado**.
- `USUARIOS_SEMILLA = [("admin.rrhh","administrador"), ("captura.obra1","captura")]`.

## Operaciones de dominio
| Función | Qué hace |
|---|---|
| `ahora()` | Marca de tiempo ISO en texto ([[adr-007-marcas-de-tiempo-texto-iso]]) |
| `registrar_bitacora(conn, usuario_id, movimiento_id, accion, detalle)` | INSERT en la bitácora |
| `obtener_o_crear_trabajador(conn, nombre, curp, nss, rfc)` | Busca por CURP. Si existe, **actualiza nombre y RFC**; si no, lo crea |
| `obtener_patron_id(conn)` | Id del primer patrón; lo crea si la tabla está vacía (bug corregido en el E4) |
| `conflicto_de_identidad(conn, curp, nss)` | `("nss", mensaje)` si la CURP ya tiene otro NSS o si el NSS es de otra persona; si no, `None` |
| `movimiento_duplicado(conn, curp, tipo, fecha)` | Id del movimiento idéntico o `None` |
| **`estado_afiliatorio(conn, curp)`** | `("SIN_REGISTRO", None)`, `("VIGENTE", fila)` o `("NO_VIGENTE", fila)` según el último movimiento **por fecha real** (`_FECHA_ORDENABLE` reordena DDMMAAAA a AAAAMMDD); excluye los `'Rechazado'` ([[historial-afiliatorio]]) |
| `estadisticas(conn)` | Contadores del tablero: total, pendientes, exportados, altas, bajas y rechazos (los toma de la bitácora) |
| `backend_actual()`, `descripcion_backend()` | Motor activo |

## Trampas
- **SQL nuevo con `%s`.** El traductor solo va en un sentido.
- Las marcas de tiempo se guardan como **texto ISO**, no como `datetime`: Python 3.12+ deprecó los adaptadores
  de sqlite3.
- El arnés del E3 fija `SQLITE_PATH` **antes** de importar este módulo, porque la configuración se lee al
  importarlo.
- `sigma_imss.db` es **local** de cada persona; está en `.gitignore`.

Ver también: [[modelo-de-datos]] · [[doble-motor-de-base-de-datos]] · [[modulo-app]]
