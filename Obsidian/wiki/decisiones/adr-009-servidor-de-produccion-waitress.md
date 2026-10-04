---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [servidor, waitress, seguridad, despliegue]
fuentes: ["servidor.py", "app.py", "raw/resultados/e5-arnes-ambiente-relevante-antes.md"]
actualizado: 2026-10-04
---

# ADR-009: Servidor de producción waitress; depuración solo a petición

**Contexto.** Hasta el E4, se arrancaba con `python app.py`, que hacía `app.run(debug=True, host="0.0.0.0")`.
En el bloque G del E5, desde la IP de la red local:
- `/console`, la **consola de depuración de Werkzeug**, respondía **200**.
- La cabecera `Server` revelaba "Werkzeug/3.1.8 Python/3.14.3".
- Un error 500 mostraba el **detalle técnico**.

**Decisión.**
- Nuevo `servidor.py` con **waitress** (`threads=8`, `ident="Sigma"`, host y puerto por variables de entorno).
  Es lo que se usa en la oficina.
- `python app.py` queda **solo para desarrollo**: escucha en **127.0.0.1** y activa `debug` solo con
  **`SIGMA_DEBUG=1`**.

**Por qué waitress.** Es WSGI de producción, **funciona en Windows sin compilar** (gunicorn no corre en Windows)
y es puro Python.

**Resultado (E5).**
- `/console` responde 404.
- `Server: Sigma`.
- p95 de captura con 20 usuarios de 497.6 ms → **120 ms**.
- Capacidad de unas 3,800 → **unas 5,900 capturas por minuto**.

**Consecuencias.**
- Hay que instalar `waitress` (está en `requirements.txt`).
- Los cambios en `.py` ya **no se recargan solos**: hay que reiniciar el servidor.
- Conviene fijar `SECRET_KEY`.

Ver: [[modulo-servidor]] · [[seguridad-web]] · [[decisiones]]
