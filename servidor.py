"""
Arranque del sistema en modo producción.

El servidor de desarrollo de Flask (app.run) está pensado para programar: con
debug=True publica una consola de depuración y el detalle técnico de cada error
a cualquiera que alcance el puerto. En la oficina el sistema se usa desde la red
local, así que aquí se sirve con waitress, un servidor WSGI de producción que
funciona en Windows sin compilar nada.

Al arrancar, primero revisa que el puerto esté libre: en Windows un segundo
servidor puede escuchar en el mismo puerto sin ningún error y las peticiones se
reparten entre los dos, así que si ya hay alguien escuchando se detiene con un
mensaje. Después respalda la base (antes de cualquier migración) y deja un hilo
que respalda cada SIGMA_RESPALDO_HORAS horas (sigma/respaldo.py).

Uso (desde la raíz del repositorio):
    python servidor.py

Para programar está el servidor de desarrollo: python -m sigma

Variables de entorno:
    SIGMA_HOST     interfaz donde escucha (por defecto 0.0.0.0: toda la red local)
    SIGMA_PUERTO   puerto (por defecto 5050)
    SIGMA_HILOS    peticiones que se atienden a la vez (por defecto 8)
    SECRET_KEY     clave fija de sesión; sin ella se crea y reutiliza .clave_sesion
    (las de respaldo, sesión y tamaño de petición están en el README)
"""
import os
import socket
import sys
from datetime import date

from waitress import serve

from sigma import respaldo
from sigma.app import app
from sigma.database import descripcion_backend, init_db
from sigma.validaciones import aviso_montos_sin_cargar


def puerto_ocupado(host, puerto):
    """True si ya hay un programa escuchando en ese puerto (por ejemplo, otra copia de Sigma)."""
    destino = "127.0.0.1" if host in ("", "0.0.0.0") else host
    try:
        with socket.create_connection((destino, puerto), timeout=1):
            return True
    except OSError:
        return False


def main():
    host = os.environ.get("SIGMA_HOST", "0.0.0.0")
    puerto = int(os.environ.get("SIGMA_PUERTO", "5050"))
    hilos = int(os.environ.get("SIGMA_HILOS", "8"))
    if puerto_ocupado(host, puerto):
        print(f"[sigma] Error: el puerto {puerto} ya está en uso. Lo más probable es que Sigma ya esté "
              f"corriendo en esta PC; ciérrelo antes de arrancar otra copia o elija otro puerto con "
              f"SIGMA_PUERTO.", flush=True)
        sys.exit(1)
    try:
        ruta = respaldo.respaldar()
        if ruta:
            print(f"[sigma] Respaldo al arrancar: {ruta}", flush=True)
    except Exception as error:  # un respaldo fallido no impide atender
        print(f"[sigma] Aviso: no se pudo respaldar la base al arrancar: {error}", flush=True)
    init_db()
    respaldo.iniciar_automatico()
    print(f"[sigma] Motor de datos: {descripcion_backend()}", flush=True)
    aviso = aviso_montos_sin_cargar(date.today().year)
    if aviso:
        print(f"[sigma] Aviso: {aviso}", flush=True)
    print(f"[sigma] Servidor de producción (waitress, {hilos} hilos) en http://{host}:{puerto}",
          flush=True)
    # ident oculta la versión del servidor en la cabecera Server.
    serve(app, host=host, port=puerto, threads=hilos, ident="Sigma")


if __name__ == "__main__":
    main()
