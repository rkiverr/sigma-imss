"""
Servidor de desarrollo de Sigma, solo para programar.

Uso (desde la raíz del repositorio):
    python -m sigma

En la oficina se arranca con servidor.py (waitress). El modo debug publica una
consola de depuración y el detalle de los errores, por eso solo se activa a
petición expresa (SIGMA_DEBUG=1) y, salvo que se indique otra cosa, escuchando
únicamente en este equipo.
"""
import os

from .app import app
from .database import descripcion_backend, init_db

depurar = os.environ.get("SIGMA_DEBUG") == "1"
host = os.environ.get("SIGMA_HOST", "127.0.0.1")
puerto = int(os.environ.get("SIGMA_PUERTO", "5050"))
init_db()
print(f"[sigma] Motor de datos: {descripcion_backend()}")
print(f"[sigma] Servidor de DESARROLLO en http://{host}:{puerto} "
      f"(debug {'activo' if depurar else 'apagado'}). Para la oficina usa: python servidor.py")
app.run(debug=depurar, host=host, port=puerto)
