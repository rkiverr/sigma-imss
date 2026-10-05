---
tipo: concepto
tags: [postgresql, sqlite, persistencia, portabilidad]
fuentes: ["sigma/database.py", "README.md"]
actualizado: 2026-10-04
---

# Doble motor de base de datos: PostgreSQL y SQLite

**PostgreSQL** es el motor objetivo (Alternativa 3 del E2). **SQLite** es el respaldo automático cuando no hay
servidor PostgreSQL. Decisión completa en [[adr-002-doble-motor-de-base-de-datos]].

## Cómo funciona sin duplicar lógica
- Toda la aplicación escribe **SQL estándar con marcadores `%s`**, el estilo de psycopg2.
- Para SQLite, `_ConexionSQLite` y `_CursorSQLite` traducen `%s` → `?` al vuelo.
- Solo el **DDL** está duplicado (`_DDL_POSTGRES` / `_DDL_SQLITE`), porque `SERIAL` y `AUTOINCREMENT` no son
  intercambiables.
- `RETURNING id` funciona en los dos: SQLite lo soporta desde la versión 3.35.
- Las marcas de tiempo son texto ISO, que funciona en `TIMESTAMP` y en `TEXT`
  ([[adr-007-marcas-de-tiempo-texto-iso]]).
- El orden por fecha real usa `substr(...) || substr(...)`, que existe en ambos.

## Cuál se usa
La selección se hace una vez por proceso ([[modulo-database]]):
`SIGMA_DB=sqlite` → SQLite; si psycopg2 se conecta a PostgreSQL → PostgreSQL; en cualquier otro caso → SQLite
con un aviso. La insignia de la barra muestra el motor activo.

En la laptop de Pedro (Python 3.14) **siempre es SQLite**, porque `requirements.txt` solo instala
psycopg2-binary en Python < 3.13. Para usar PostgreSQL ahí habría que instalar psycopg (v3) o un psycopg2
compatible.

## Diferencias que importan
| | SQLite | PostgreSQL |
|---|---|---|
| Escrituras simultáneas | **Una a la vez**; las demás esperan hasta `timeout=10` s | Concurrentes por filas |
| Lo que se midió | Con 20 usuarios sin pausa, una captura tardó hasta **6.0 s** (p95: 120 ms) | No se midió (no está instalado) |
| Datos compartidos | El archivo es local de cada persona | Un servidor para toda la oficina |
| WAL | `PRAGMA journal_mode = WAL`: se puede leer mientras otro escribe | Nativo |

Por eso el plan para TRL 6 es **migrar a PostgreSQL** en el servidor de la oficina ([[hoja-de-ruta-trl6]]).

## Para PostgreSQL
```powershell
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py
```
Antes hay que crear la base vacía con `createdb sigma_imss`. Las tablas se crean solas.

Ver también: [[modelo-de-datos]] · [[configuracion]] · [[problemas-frecuentes]]
