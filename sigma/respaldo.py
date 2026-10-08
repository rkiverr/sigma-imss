"""
Respaldo y restauración de la base de datos de Sigma.

Hasta la Entrega 5 la base era un solo archivo en una PC y nadie lo copiaba.
Desde el TRL 6, servidor.py respalda al arrancar (antes de migrar la base) y
después cada SIGMA_RESPALDO_HORAS horas. También se puede respaldar a mano.

  * SQLite: copia en caliente con la API de respaldo de sqlite3 (consistente
    aunque haya capturas en curso), verificada con PRAGMA integrity_check.
  * PostgreSQL: pg_dump, si las herramientas de PostgreSQL están instaladas.
  * Se conservan los SIGMA_RESPALDOS_CONSERVAR respaldos más recientes.

Variables de entorno:
    SIGMA_RESPALDOS            carpeta destino (por omisión respaldos/ en la raíz;
                               conviene que sea otro disco o una carpeta compartida)
    SIGMA_RESPALDO_HORAS       cada cuántas horas respalda servidor.py (24)
    SIGMA_RESPALDOS_CONSERVAR  cuántos respaldos se guardan (30)

Uso (desde la raíz del repositorio):
    python -m sigma.respaldo                       respalda ahora
    python -m sigma.respaldo --listar              muestra los respaldos
    python -m sigma.respaldo --restaurar ARCHIVO   restaura (con el servidor detenido)
"""
import argparse
import glob
import os
import shutil
import sqlite3
import subprocess
import sys
import threading
from datetime import datetime

from . import database

CARPETA = os.environ.get("SIGMA_RESPALDOS", os.path.join(database.RAIZ, "respaldos"))
CONSERVAR = int(os.environ.get("SIGMA_RESPALDOS_CONSERVAR", "30"))
HORAS = float(os.environ.get("SIGMA_RESPALDO_HORAS", "24"))
_CANDADO = threading.Lock()


def _marca():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _rotar(patron):
    respaldos = sorted(glob.glob(os.path.join(CARPETA, patron)))
    for viejo in respaldos[:-CONSERVAR] if CONSERVAR > 0 else []:
        os.remove(viejo)


def verificar(ruta):
    """True si el archivo es una base SQLite íntegra."""
    conexion = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    try:
        return conexion.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        conexion.close()


def respaldar_sqlite(origen=None):
    """Copia la base SQLite a la carpeta de respaldos y devuelve la ruta del respaldo."""
    origen = origen or database.SQLITE_PATH
    if not os.path.isfile(origen):
        return None
    os.makedirs(CARPETA, exist_ok=True)
    destino = os.path.join(CARPETA, f"sigma_imss_{_marca()}.db")
    with _CANDADO:
        fuente = sqlite3.connect(origen, timeout=30)
        copia = sqlite3.connect(destino)
        try:
            fuente.backup(copia)
            # La base de trabajo usa WAL; el respaldo queda como un solo archivo autocontenido.
            copia.execute("PRAGMA journal_mode = DELETE")
        finally:
            copia.close()
            fuente.close()
    if not verificar(destino):
        os.remove(destino)
        raise RuntimeError("El respaldo no pasó la verificación de integridad y se descartó.")
    _rotar("sigma_imss_*.db")
    return destino


def respaldar_postgres():
    """Respaldo con pg_dump (formato personalizado). Devuelve la ruta o None si no hay pg_dump."""
    pg_dump = shutil.which("pg_dump")
    if pg_dump is None:
        print("[sigma] Aviso: no se encontró pg_dump; instala las herramientas de PostgreSQL "
              "para respaldar la base.", flush=True)
        return None
    os.makedirs(CARPETA, exist_ok=True)
    destino = os.path.join(CARPETA, f"sigma_imss_{_marca()}.dump")
    subprocess.run([pg_dump, "--format=custom", "--file", destino, database.DATABASE_URL], check=True)
    _rotar("sigma_imss_*.dump")
    return destino


def respaldar():
    """Respalda la base del motor activo. Devuelve la ruta del respaldo o None."""
    if database.backend_actual() == "postgres":
        return respaldar_postgres()
    return respaldar_sqlite()


def restaurar(archivo):
    """
    Reemplaza la base SQLite por un respaldo. Antes guarda una copia de la base
    actual, por si hubiera que deshacer. Se hace con el servidor detenido.
    """
    if not verificar(archivo):
        raise RuntimeError("El archivo no es un respaldo íntegro de Sigma.")
    destino = database.SQLITE_PATH
    if os.path.isfile(destino):
        os.makedirs(CARPETA, exist_ok=True)
        shutil.copy2(destino, os.path.join(CARPETA, f"antes_de_restaurar_{_marca()}.db"))
    for sufijo in ("-wal", "-shm"):
        if os.path.isfile(destino + sufijo):
            os.remove(destino + sufijo)
    shutil.copy2(archivo, destino)
    return destino


def iniciar_automatico():
    """Hilo que respalda cada HORAS horas mientras el servidor esté en marcha."""
    def ciclo():
        espera = threading.Event()
        while not espera.wait(HORAS * 3600):
            try:
                ruta = respaldar()
                if ruta:
                    print(f"[sigma] Respaldo automático: {ruta}", flush=True)
            except Exception as error:  # el servidor sigue aunque falle un respaldo
                print(f"[sigma] Aviso: falló el respaldo automático: {error}", flush=True)

    if HORAS > 0:
        threading.Thread(target=ciclo, name="respaldo-automatico", daemon=True).start()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m sigma.respaldo",
                                     description="Respalda o restaura la base de datos de Sigma.")
    grupo = parser.add_mutually_exclusive_group()
    grupo.add_argument("--restaurar", metavar="ARCHIVO", help="restaura la base desde un respaldo")
    grupo.add_argument("--listar", action="store_true", help="muestra los respaldos guardados")
    argumentos = parser.parse_args(argv)
    try:
        if argumentos.listar:
            for ruta in sorted(glob.glob(os.path.join(CARPETA, "sigma_imss_*"))):
                print(f"{os.path.basename(ruta)}  {os.path.getsize(ruta) / 1024:,.0f} KB")
        elif argumentos.restaurar:
            print(f"Base restaurada en {restaurar(argumentos.restaurar)}")
        else:
            ruta = respaldar()
            print(f"Respaldo guardado en {ruta}" if ruta else "No había base que respaldar.")
    except (RuntimeError, OSError, sqlite3.Error, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
