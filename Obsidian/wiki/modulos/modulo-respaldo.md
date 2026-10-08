---
tipo: modulo
tags: [respaldo, restauracion, base-de-datos, operacion]
fuentes: ["sigma/respaldo.py", "servidor.py"]
actualizado: 2026-10-07
---

# `sigma/respaldo.py` — respaldo y restauración de la base

Nació en el TRL 6 ([[adr-020-respaldo-automatico]]).

## Variables
`SIGMA_RESPALDOS` (carpeta, por omisión `respaldos/`), `SIGMA_RESPALDO_HORAS` (24) y `SIGMA_RESPALDOS_CONSERVAR`
(30). Ver [[configuracion]].

## Funciones
| Función | Qué hace |
|---|---|
| `respaldar()` | Elige según el motor activo |
| `respaldar_sqlite(origen=None)` | `sqlite3.backup` → `journal_mode = DELETE` → `integrity_check`; descarta la copia si falla; rota |
| `respaldar_postgres()` | `pg_dump --format=custom` si existe (no probado: no hay PostgreSQL en el equipo de pruebas) |
| `verificar(ruta)` | `integrity_check` en modo de solo lectura |
| `restaurar(archivo)` | Verifica el respaldo, guarda `antes_de_restaurar_…db`, borra `-wal`/`-shm` y copia |
| `iniciar_automatico()` | Hilo `respaldo-automatico` cada `HORAS` |
| `main()` | Consola: sin argumentos respalda; `--listar`; `--restaurar ARCHIVO` |

## Trampas
- Sin `journal_mode = DELETE`, verificar la copia creaba `-wal` y `-shm` junto a ella (se vio en el arnés: 3
  archivos por respaldo).
- Restaurar con el servidor encendido no es seguro: se hace detenido.

## Pruebas
[[arnes-integracion]], bloque R: 40 capturas → respaldo → 5 capturas más → se borra la base → restaurar →
conteos idénticos al respaldo y acceso normal.

Ver también: [[modulo-servidor]] · [[como-arrancar]] · [[riesgos]]
