---
tipo: operacion
tags: [configuracion, variables-de-entorno]
fuentes: ["servidor.py", "sigma/app.py", "sigma/database.py", "README.md"]
actualizado: 2026-10-07
---

# Configuración (variables de entorno)

| Variable | Dónde se lee | Por defecto | Para qué |
|---|---|---|---|
| `SIGMA_HOST` | `servidor.py`, `sigma/__main__.py` | `0.0.0.0` en servidor.py · `127.0.0.1` con `python -m sigma` | Interfaz de escucha |
| `SIGMA_PUERTO` | `servidor.py`, `sigma/__main__.py` | `5050` | Puerto |
| `SIGMA_HILOS` | `servidor.py` | `8` | Peticiones simultáneas de waitress |
| `SIGMA_DEBUG` | `sigma/__main__.py` | (apagado) | `1` = depuración en `python -m sigma` |
| `SECRET_KEY` | `app.py` | Aleatoria en cada arranque | Firma de sesiones y *flash*. **Fíjala en la oficina** para que un reinicio no invalide sesiones |
| `DATABASE_URL` | `database.py` | `postgresql://postgres:postgres@localhost:5432/sigma_imss?client_encoding=UTF8` | PostgreSQL |
| `SIGMA_DB` | `database.py` | (automático) | `sqlite` o `postgres` para forzar el motor |
| `SQLITE_PATH` | `database.py` | `sigma_imss.db` en la raíz del repositorio (fuera de `sigma/`) | Archivo SQLite |

**Importante:** `database.py` lee su configuración **al importarse**. Para cambiarla, fíjala antes de arrancar,
o antes del `import` si es en un script (así lo hace el arnés del E3).

## Ejemplos (PowerShell)
```powershell
# Usar PostgreSQL
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py

# Otro puerto y una clave fija
$env:SIGMA_PUERTO = "8080"; $env:SECRET_KEY = "<cadena larga aleatoria>"
python servidor.py
```

## Datos que no son variables, pero hay que cambiar antes de operar en serio
- **Registro patronal real:** `PATRON_SEMILLA` en `database.py`. Después hay que borrar la base para que se
  vuelva a sembrar.
- **Usuarios reales:** `USUARIOS_SEMILLA`. Mientras no haya login, solo firman la bitácora.
- **Montos legales del año:** `validaciones.py` ([[mantenimiento-anual]]).


## Variables nuevas del TRL 6 (2026-10-07)
| Variable | Dónde se lee | Por defecto | Para qué |
|---|---|---|---|
| `SIGMA_SESION_HORAS` | `app.py` | `10` | Duración de la sesión |
| `SIGMA_MAX_PETICION_KB` | `app.py` | `1024` | Tamaño máximo de una petición (413 si se pasa) |
| `SIGMA_RESPALDOS` | `respaldo.py` | `respaldos/` en la raíz | Carpeta de respaldos (mejor otro disco) |
| `SIGMA_RESPALDO_HORAS` | `respaldo.py` | `24` | Cada cuántas horas respalda `servidor.py` |
| `SIGMA_RESPALDOS_CONSERVAR` | `respaldo.py` | `30` | Cuántos respaldos se guardan |

Cambios:
- `SECRET_KEY`: si falta, se crea y reutiliza `.clave_sesion` (ya no cambia en cada arranque).
- `DATABASE_URL` por omisión: `127.0.0.1` con `connect_timeout=1`. Sin PostgreSQL, el intento tarda 1 s (con
  `localhost` tardaba 4 s). `SIGMA_DB=sqlite` lo evita.
- Datos que se cambian antes de operar: `PATRON_SEMILLA` y `GUIA_SEMILLA` (`database.py`) y las contraseñas
  (`python -m sigma.usuarios`).

Ver también: [[como-arrancar]] · [[doble-motor-de-base-de-datos]]
