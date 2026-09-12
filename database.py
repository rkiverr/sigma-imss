"""
Capa de persistencia del sistema Sigma.

Modelo relacional normalizado: patron, usuario, trabajador, movimiento, bitacora.

Soporta dos motores sin cambiar la lógica de negocio, porque toda la capa
superior usa únicamente SQL estándar:

  * PostgreSQL  — motor objetivo del proyecto (Alternativa 3 de la Entrega 2).
                  Se usa siempre que haya un servidor accesible y psycopg2
                  instalado.
  * SQLite      — respaldo automático. Permite ejecutar y demostrar el
                  prototipo en cualquier equipo sin instalar un servidor.

Selección del motor:
  DATABASE_URL   postgresql://usuario:password@host:5432/sigma_imss
  SIGMA_DB       "postgres" o "sqlite" para forzar uno de los dos.
  SQLITE_PATH    ruta del archivo .db cuando se usa SQLite (por defecto sigma_imss.db)
"""
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime

# En Windows con configuración regional en español, libpq (la librería detrás
# de psycopg2) traduce sus mensajes de error usando una codificación distinta a
# UTF-8. Eso hace que psycopg2 truene con UnicodeDecodeError al LEER el mensaje
# de error, ocultando el error real. Forzamos mensajes ASCII para poder verlo.
os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"
os.environ.setdefault("PGCLIENTENCODING", "UTF8")

try:
    import psycopg2
    import psycopg2.extras
except ImportError:  # el prototipo sigue siendo funcional sobre SQLite
    psycopg2 = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/sigma_imss?client_encoding=UTF8",
)
SQLITE_PATH = os.environ.get("SQLITE_PATH", os.path.join(BASE_DIR, "sigma_imss.db"))
MOTOR_FORZADO = os.environ.get("SIGMA_DB", "").strip().lower()

_BACKEND = None          # "postgres" | "sqlite"
_DETALLE_BACKEND = ""    # texto legible para mostrar en la interfaz


class ErrorBaseDeDatos(RuntimeError):
    """Error de conexión o de configuración de la base de datos."""


# --------------------------------------------------------------------------
# Adaptadores de SQLite para que acepte el mismo SQL que PostgreSQL
# --------------------------------------------------------------------------
_PLACEHOLDER = re.compile(r"%s")


def _traducir(sql):
    """Convierte los marcadores %s de psycopg2 al ? que espera sqlite3."""
    return _PLACEHOLDER.sub("?", sql)


class _CursorSQLite:
    """Cursor de sqlite3 que entiende los marcadores de psycopg2."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, params=()):
        return self._cursor.execute(_traducir(sql), params)

    def executemany(self, sql, seq):
        return self._cursor.executemany(_traducir(sql), seq)

    def __getattr__(self, nombre):
        return getattr(self._cursor, nombre)

    def __iter__(self):
        return iter(self._cursor)


class _ConexionSQLite:
    """Conexión de sqlite3 que devuelve cursores compatibles."""

    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return _CursorSQLite(self._conn.cursor())

    def __getattr__(self, nombre):
        return getattr(self._conn, nombre)


# --------------------------------------------------------------------------
# Selección y apertura de conexiones
# --------------------------------------------------------------------------
def _abrir_postgres():
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


def _abrir_sqlite():
    conn = sqlite3.connect(SQLITE_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")  # permite lecturas durante escrituras
    return _ConexionSQLite(conn)


def _resolver_backend():
    """Decide una sola vez qué motor se va a usar durante la ejecución."""
    global _BACKEND, _DETALLE_BACKEND
    if _BACKEND:
        return _BACKEND

    if MOTOR_FORZADO == "sqlite":
        _BACKEND, _DETALLE_BACKEND = "sqlite", "SQLite - " + os.path.basename(SQLITE_PATH)
        return _BACKEND

    if psycopg2 is not None:
        try:
            _abrir_postgres().close()
            host = re.sub(r"^.*@", "", DATABASE_URL.split("?")[0])
            _BACKEND, _DETALLE_BACKEND = "postgres", "PostgreSQL - " + host
            return _BACKEND
        except Exception as exc:
            if MOTOR_FORZADO == "postgres":
                raise ErrorBaseDeDatos(
                    "No fue posible conectar con PostgreSQL usando DATABASE_URL.\n" + str(exc)
                ) from exc
            texto = str(exc).strip()
            motivo = texto.splitlines()[0] if texto else "servidor no disponible"
    elif MOTOR_FORZADO == "postgres":
        raise ErrorBaseDeDatos(
            "SIGMA_DB=postgres pero psycopg2 no está instalado (pip install psycopg2-binary)."
        )
    else:
        motivo = "psycopg2 no está instalado"

    _BACKEND = "sqlite"
    _DETALLE_BACKEND = "SQLite - " + os.path.basename(SQLITE_PATH)
    print("[sigma] PostgreSQL no disponible (" + motivo + "). Usando SQLite: " + SQLITE_PATH)
    return _BACKEND


def get_conn():
    """Devuelve una conexión nueva al motor activo."""
    if _resolver_backend() == "postgres":
        return _abrir_postgres()
    return _abrir_sqlite()


@contextmanager
def conexion(commit=False):
    """
    Context manager que garantiza commit/rollback y cierre de la conexión
    incluso si la vista lanza una excepción.
    """
    conn = get_conn()
    try:
        yield conn
        if commit:
            conn.commit()
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass


def backend_actual():
    _resolver_backend()
    return _BACKEND


def descripcion_backend():
    """Texto corto del motor activo, para mostrarlo en la interfaz."""
    _resolver_backend()
    return _DETALLE_BACKEND


# --------------------------------------------------------------------------
# Esquema
# --------------------------------------------------------------------------
_DDL_POSTGRES = [
    """CREATE TABLE IF NOT EXISTS patron (
        id SERIAL PRIMARY KEY,
        registro_patronal TEXT NOT NULL,
        razon_social TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura'))
    )""",
    """CREATE TABLE IF NOT EXISTS trabajador (
        id SERIAL PRIMARY KEY,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS movimiento (
        id SERIAL PRIMARY KEY,
        trabajador_id INTEGER NOT NULL REFERENCES trabajador(id),
        patron_id INTEGER NOT NULL REFERENCES patron(id),
        tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('08','02')),
        fecha_movimiento TEXT NOT NULL,
        tipo_trabajador TEXT,
        tipo_salario TEXT,
        tipo_jornada TEXT,
        sdi TEXT,
        causa_baja TEXT,
        estado TEXT NOT NULL CHECK (estado IN ('Válido','Rechazado','Exportado')),
        exportado BOOLEAN NOT NULL DEFAULT FALSE
    )""",
    """CREATE TABLE IF NOT EXISTS bitacora (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER NOT NULL REFERENCES usuario(id),
        movimiento_id INTEGER REFERENCES movimiento(id),
        accion TEXT NOT NULL,
        detalle TEXT,
        timestamp TIMESTAMP NOT NULL
    )""",
    "ALTER TABLE movimiento ADD COLUMN IF NOT EXISTS creado_en TIMESTAMP",
    "CREATE INDEX IF NOT EXISTS idx_movimiento_estado ON movimiento(estado)",
    "CREATE INDEX IF NOT EXISTS idx_bitacora_id ON bitacora(id)",
]

_DDL_SQLITE = [
    """CREATE TABLE IF NOT EXISTS patron (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registro_patronal TEXT NOT NULL,
        razon_social TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura'))
    )""",
    """CREATE TABLE IF NOT EXISTS trabajador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS movimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trabajador_id INTEGER NOT NULL REFERENCES trabajador(id),
        patron_id INTEGER NOT NULL REFERENCES patron(id),
        tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('08','02')),
        fecha_movimiento TEXT NOT NULL,
        tipo_trabajador TEXT,
        tipo_salario TEXT,
        tipo_jornada TEXT,
        sdi TEXT,
        causa_baja TEXT,
        estado TEXT NOT NULL CHECK (estado IN ('Válido','Rechazado','Exportado')),
        exportado BOOLEAN NOT NULL DEFAULT FALSE,
        creado_en TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS bitacora (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL REFERENCES usuario(id),
        movimiento_id INTEGER REFERENCES movimiento(id),
        accion TEXT NOT NULL,
        detalle TEXT,
        timestamp TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_movimiento_estado ON movimiento(estado)",
    "CREATE INDEX IF NOT EXISTS idx_bitacora_id ON bitacora(id)",
]

PATRON_SEMILLA = ("A1234567890", "Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V.")
USUARIOS_SEMILLA = [("admin.rrhh", "administrador"), ("captura.obra1", "captura")]


def init_db():
    """Crea el esquema y los datos semilla. Es idempotente."""
    backend = _resolver_backend()
    ddl = _DDL_POSTGRES if backend == "postgres" else _DDL_SQLITE

    with conexion(commit=True) as conn:
        cur = conn.cursor()
        for sentencia in ddl:
            cur.execute(sentencia)

        # Migración de bases creadas por versiones anteriores del prototipo.
        if backend == "sqlite":
            cur.execute("PRAGMA table_info(movimiento)")
            columnas = {fila["name"] for fila in cur.fetchall()}
            if "creado_en" not in columnas:
                cur.execute("ALTER TABLE movimiento ADD COLUMN creado_en TEXT")

        cur.execute("SELECT COUNT(*) AS n FROM patron")
        if cur.fetchone()["n"] == 0:
            cur.execute(
                "INSERT INTO patron (registro_patronal, razon_social) VALUES (%s, %s)",
                PATRON_SEMILLA,
            )

        cur.execute("SELECT COUNT(*) AS n FROM usuario")
        if cur.fetchone()["n"] == 0:
            cur.executemany("INSERT INTO usuario (nombre, rol) VALUES (%s, %s)", USUARIOS_SEMILLA)
        cur.close()


# --------------------------------------------------------------------------
# Operaciones de dominio
# --------------------------------------------------------------------------
def ahora():
    """Marca de tiempo ISO, compatible con TIMESTAMP de PostgreSQL y TEXT de SQLite."""
    return datetime.now().isoformat(sep=" ", timespec="seconds")


def registrar_bitacora(conn, usuario_id, movimiento_id, accion, detalle=""):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bitacora (usuario_id, movimiento_id, accion, detalle, timestamp)"
        " VALUES (%s, %s, %s, %s, %s)",
        (usuario_id, movimiento_id, accion, detalle, ahora()),
    )
    cur.close()


def obtener_o_crear_trabajador(conn, nombre_completo, curp, nss, rfc):
    cur = conn.cursor()
    cur.execute("SELECT id FROM trabajador WHERE curp = %s", (curp,))
    fila = cur.fetchone()
    if fila:
        # El expediente ya existe: se actualizan los datos por si cambiaron.
        cur.execute(
            "UPDATE trabajador SET nombre_completo = %s, rfc = %s WHERE id = %s",
            (nombre_completo, rfc, fila["id"]),
        )
        cur.close()
        return fila["id"]
    cur.execute(
        "INSERT INTO trabajador (nombre_completo, curp, nss, rfc) VALUES (%s, %s, %s, %s) RETURNING id",
        (nombre_completo, curp, nss, rfc),
    )
    nuevo = cur.fetchone()["id"]
    cur.close()
    return nuevo


def obtener_patron_id(conn):
    """Id del patrón activo. Lo crea si la tabla está vacía."""
    cur = conn.cursor()
    cur.execute("SELECT id FROM patron ORDER BY id LIMIT 1")
    fila = cur.fetchone()
    if fila is None:
        cur.execute(
            "INSERT INTO patron (registro_patronal, razon_social) VALUES (%s, %s) RETURNING id",
            PATRON_SEMILLA,
        )
        fila = cur.fetchone()
    cur.close()
    return fila["id"]


def conflicto_de_identidad(conn, curp, nss):
    """
    Detecta choques con expedientes ya registrados ANTES de intentar el INSERT,
    para devolver un mensaje entendible en lugar de un error de integridad.
    Devuelve (campo, mensaje) o None.
    """
    cur = conn.cursor()
    cur.execute("SELECT nombre_completo, nss FROM trabajador WHERE curp = %s", (curp,))
    por_curp = cur.fetchone()
    if por_curp and por_curp["nss"] != nss:
        cur.close()
        return ("nss", "La CURP ya está registrada a nombre de " + por_curp["nombre_completo"]
                + " con el NSS " + por_curp["nss"] + ". Verifica el NSS capturado.")

    cur.execute("SELECT nombre_completo, curp FROM trabajador WHERE nss = %s", (nss,))
    por_nss = cur.fetchone()
    cur.close()
    if por_nss and por_nss["curp"] != curp:
        return ("nss", "El NSS ya pertenece a " + por_nss["nombre_completo"]
                + " (CURP " + por_nss["curp"] + "). Un NSS no puede repetirse entre trabajadores.")
    return None


def movimiento_duplicado(conn, curp, tipo_movimiento, fecha_movimiento):
    """Devuelve el id del movimiento idéntico ya registrado, o None."""
    cur = conn.cursor()
    cur.execute(
        """SELECT m.id FROM movimiento m
           JOIN trabajador t ON t.id = m.trabajador_id
           WHERE t.curp = %s AND m.tipo_movimiento = %s AND m.fecha_movimiento = %s
           LIMIT 1""",
        (curp, tipo_movimiento, fecha_movimiento),
    )
    fila = cur.fetchone()
    cur.close()
    return fila["id"] if fila else None


def estadisticas(conn):
    """Contadores para el tablero de la interfaz."""
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN estado = 'Válido'    THEN 1 ELSE 0 END) AS pendientes,
               SUM(CASE WHEN estado = 'Exportado' THEN 1 ELSE 0 END) AS exportados,
               SUM(CASE WHEN tipo_movimiento = '08' THEN 1 ELSE 0 END) AS altas,
               SUM(CASE WHEN tipo_movimiento = '02' THEN 1 ELSE 0 END) AS bajas
        FROM movimiento
    """)
    fila = dict(cur.fetchone())
    cur.execute("SELECT COUNT(*) AS n FROM bitacora WHERE accion LIKE %s", ("%rechazado%",))
    fila["rechazos"] = cur.fetchone()["n"] or 0
    cur.close()
    return {clave: (valor or 0) for clave, valor in fila.items()}
