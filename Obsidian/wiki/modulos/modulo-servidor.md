---
tipo: modulo
tags: [servidor, waitress, produccion, despliegue]
fuentes: ["servidor.py", "sigma/app.py"]
actualizado: 2026-10-18
---

# `servidor.py` — arranque en producción (waitress)

Tiene 40 líneas y es nuevo en el E5. **Así se arranca Sigma en la oficina:**

```bash
python servidor.py
```

Se queda en la raíz del repositorio, fuera del paquete, e importa la aplicación con
`from sigma.app import app` ([[adr-017-paquete-sigma-y-carpeta-de-pruebas]]). Hace cuatro cosas:
1. Lee `SIGMA_HOST` (por defecto `0.0.0.0`, es decir, toda la red local), `SIGMA_PUERTO` (5050) y `SIGMA_HILOS`
   (8).
2. Llama a `init_db()`.
3. Imprime el motor de datos y la dirección.
4. Llama a `waitress.serve(app, host, port, threads, ident="Sigma")`. Con `ident="Sigma"`, la cabecera
   `Server` dice "Sigma" y no revela versiones.

Salida esperada:
```text
[sigma] Motor de datos: SQLite - sigma_imss.db
[sigma] Servidor de producción (waitress, 8 hilos) en http://0.0.0.0:5050
```

## Por qué existe
Antes la oficina usaba `python app.py`, que levantaba el servidor de **desarrollo** de Flask con `debug=True` en
`0.0.0.0`. Eso publicaba en la red local la **consola de depuración de Werkzeug** (`/console`) y el detalle
técnico de cada error 500. Se detectó en el bloque G del E5. Decisión completa en
[[adr-009-servidor-de-produccion-waitress]].

## Requisitos
- `pip install -r requirements.txt` (incluye `waitress>=3.0`).
- La primera vez, Windows puede preguntar si permite el acceso a Python: hay que aceptar **solo redes
  privadas**.
- Conviene fijar `SECRET_KEY` para que las sesiones sobrevivan a un reinicio ([[configuracion]]).

## Medido en el E5 (waitress con 8 hilos)
- **0 errores** con 20 usuarios sin pausa.
- p95 de captura de **120 ms**, contra 497.6 ms del servidor de Flask.
- **Unas 5,900 capturas por minuto.**
- Arranque en unos 0.6 s.
- Memoria de unos 45–68 MB.

Detalle en [[resultados-de-pruebas]].


## Cambios del TRL 6 (2026-10-07)
`main()` respalda la base **antes** de `init_db()` (y antes de cualquier migración), arranca el hilo de respaldo
periódico y avisa si faltan los montos legales del año ([[modulo-respaldo]], [[adr-020-respaldo-automatico]]).

## Cambios del TRL 9 (2026-10-18)
Antes de todo, `main()` llama a `puerto_ocupado(host, puerto)`: intenta conectarse al puerto (a `127.0.0.1` si
escucha en `0.0.0.0`). Si alguien responde, imprime `[sigma] Error: el puerto 5050 ya está en uso…` y sale con
código 1, **sin respaldar ni migrar**. Motivo: en Windows, waitress dejaba arrancar un segundo servidor en el
mismo puerto sin error y las peticiones se repartían entre los dos (H-01 de la marcha blanca del TRL 7).
Lo prueba O-04 del [[arnes-operacion]].

Ver también: [[como-arrancar]] · [[modulo-app]] · [[arquitectura-general]]
