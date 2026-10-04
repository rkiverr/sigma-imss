"""
Arranque del sistema en modo producción.

El servidor de desarrollo de Flask (app.run) está pensado para programar: con
debug=True publica una consola de depuración y el detalle técnico de cada error
a cualquiera que alcance el puerto. En la oficina el sistema se usa desde la red
local, así que aquí se sirve con waitress, un servidor WSGI de producción que
funciona en Windows sin compilar nada.

Uso:
    python servidor.py

Variables de entorno:
    SIGMA_HOST     interfaz donde escucha (por defecto 0.0.0.0: toda la red local)
    SIGMA_PUERTO   puerto (por defecto 5050)
    SIGMA_HILOS    peticiones que se atienden a la vez (por defecto 8)
    SECRET_KEY     clave fija de sesión; sin ella se genera una por arranque
"""
import os

from waitress import serve

from app import app
from database import descripcion_backend, init_db


def main():
    host = os.environ.get("SIGMA_HOST", "0.0.0.0")
    puerto = int(os.environ.get("SIGMA_PUERTO", "5050"))
    hilos = int(os.environ.get("SIGMA_HILOS", "8"))
    init_db()
    print(f"[sigma] Motor de datos: {descripcion_backend()}", flush=True)
    print(f"[sigma] Servidor de producción (waitress, {hilos} hilos) en http://{host}:{puerto}",
          flush=True)
    # ident oculta la versión del servidor en la cabecera Server.
    serve(app, host=host, port=puerto, threads=hilos, ident="Sigma")


if __name__ == "__main__":
    main()
