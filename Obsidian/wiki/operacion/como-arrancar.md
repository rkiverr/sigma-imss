---
tipo: operacion
tags: [arranque, comandos, instalacion]
fuentes: ["README.md", "instrucciones/Ejecutar.md", "instrucciones/README.md", "servidor.py"]
actualizado: 2026-10-04
---

# Cómo arrancar Sigma

## Primera vez
```bash
cd C:\Users\Pedro\Desktop\sigma-imss
pip install -r requirements.txt        # Flask y waitress (psycopg2 solo con Python < 3.13)
```

## En la oficina (producción)
```bash
python servidor.py
```
Abre <http://localhost:5050>. Desde otra PC de la red, usa `http://<IP del servidor>:5050`; la de la laptop de
Pedro fue `192.168.0.8` en las pruebas. La primera vez, Windows puede pedir permiso para Python: hay que aceptar
**solo redes privadas**. **Deja la terminal abierta**; se detiene con `Ctrl + C`.

## Para programar (desarrollo)
```bash
python app.py                  # solo en 127.0.0.1, sin depuración
$env:SIGMA_DEBUG = "1"; python app.py   # con depuración y recarga (PowerShell)
```
Nunca uses esto en la oficina ([[adr-009-servidor-de-produccion-waitress]]).

## Pruebas
```bash
python test_prueba_concepto.py          # E3, regresión: debe dar 8/8 (~2 s)
python prueba_ambiente_relevante.py     # E5, todo (~3 min)
python prueba_ambiente_relevante.py --bloques B,C,G   # rápido: errores, carreras y seguridad
```
Ver [[estrategia-de-pruebas]].

## Empezar de cero
1. Detén el servidor.
2. Borra `sigma_imss.db` y, si quieres, la carpeta `exportaciones/`.
3. Vuelve a arrancar: las tablas, el patrón semilla y los usuarios se crean solos.

## Dónde queda cada cosa
| Archivo o carpeta | Qué es | ¿En Git? |
|---|---|---|
| `sigma_imss.db` (+ `-wal`, `-shm`) | Base SQLite de trabajo | No (`.gitignore`) |
| `exportaciones/lote_idse_*.txt` | Lotes generados | No |
| `sigma_pruebas.db`, `resultados_*` | Salidas de los arneses | No |
| `Obsidian/` | Este segundo cerebro | Sí (pendiente de subir) |

Ver también: [[configuracion]] · [[problemas-frecuentes]] · [[modulo-servidor]]
