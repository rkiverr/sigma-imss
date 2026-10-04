---
tipo: operacion
tags: [configuracion, variables-de-entorno]
fuentes: ["servidor.py", "app.py", "database.py", "README.md"]
actualizado: 2026-10-04
---

# Configuración (variables de entorno)

| Variable | Dónde se lee | Por defecto | Para qué |
|---|---|---|---|
| `SIGMA_HOST` | `servidor.py`, `app.py` | `0.0.0.0` en servidor.py · `127.0.0.1` en app.py | Interfaz de escucha |
| `SIGMA_PUERTO` | `servidor.py`, `app.py` | `5050` | Puerto |
| `SIGMA_HILOS` | `servidor.py` | `8` | Peticiones simultáneas de waitress |
| `SIGMA_DEBUG` | `app.py` | (apagado) | `1` = depuración en `python app.py` |
| `SECRET_KEY` | `app.py` | Aleatoria en cada arranque | Firma de sesiones y *flash*. **Fíjala en la oficina** para que un reinicio no invalide sesiones |
| `DATABASE_URL` | `database.py` | `postgresql://postgres:postgres@localhost:5432/sigma_imss?client_encoding=UTF8` | PostgreSQL |
| `SIGMA_DB` | `database.py` | (automático) | `sqlite` o `postgres` para forzar el motor |
| `SQLITE_PATH` | `database.py` | `sigma_imss.db` junto al código | Archivo SQLite |

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

Ver también: [[como-arrancar]] · [[doble-motor-de-base-de-datos]]
