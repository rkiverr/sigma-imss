"""
Capa de persistencia del sistema Sigma.

Modelo relacional normalizado: patron, usuario, trabajador, movimiento, bitacora
(más migracion, que registra las conversiones de datos ya aplicadas).

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
  SQLITE_PATH    ruta del archivo .db cuando se usa SQLite (por defecto sigma_imss.db,
                 en la raíz del repositorio)
"""
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from .validaciones import iniciales_curp

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

# Raíz del repositorio (este archivo vive en sigma/). La base de trabajo queda
# ahí y no dentro del paquete, junto a exportaciones/.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Por omisión, PostgreSQL en el propio equipo. Se usa 127.0.0.1 y no "localhost"
# y se limita la espera: en Windows, sin servidor PostgreSQL, "localhost" (IPv6 e
# IPv4) tardaba 4 s en fallar en cada arranque; así tarda 1 s. Con SIGMA_DB=sqlite
# ni siquiera se intenta.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@127.0.0.1:5432/sigma_imss?client_encoding=UTF8&connect_timeout=1",
)
SQLITE_PATH = os.environ.get("SQLITE_PATH", os.path.join(RAIZ, "sigma_imss.db"))
MOTOR_FORZADO = os.environ.get("SIGMA_DB", "").strip().lower()

_BACKEND = None          # "postgres" | "sqlite"
_DETALLE_BACKEND = ""    # texto legible para mostrar en la interfaz


class ErrorBaseDeDatos(RuntimeError):
    """Error de conexión o de configuración de la base de datos."""


# Violaciones de restricciones (UNIQUE, CHECK) en cualquiera de los dos motores.
# Ocurren cuando dos capturistas guardan lo mismo al mismo tiempo: ambos pasan
# las verificaciones previas y la base es la que decide quién llegó primero.
ERRORES_DE_INTEGRIDAD = (sqlite3.IntegrityError,) + (
    (psycopg2.IntegrityError,) if psycopg2 is not None else ())


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
        razon_social TEXT NOT NULL,
        guia TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura')),
        password_hash TEXT,
        activo BOOLEAN NOT NULL DEFAULT TRUE,
        intentos_fallidos INTEGER NOT NULL DEFAULT 0,
        bloqueado_hasta TEXT,
        sesion_token TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS trabajador (
        id SERIAL PRIMARY KEY,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL,
        apellido_paterno TEXT,
        apellido_materno TEXT,
        nombres TEXT
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
        exportado BOOLEAN NOT NULL DEFAULT FALSE,
        umf TEXT
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
    """CREATE TABLE IF NOT EXISTS migracion (
        clave TEXT PRIMARY KEY,
        aplicada TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_movimiento_estado ON movimiento(estado)",
    "CREATE INDEX IF NOT EXISTS idx_bitacora_id ON bitacora(id)",
]

_DDL_SQLITE = [
    """CREATE TABLE IF NOT EXISTS patron (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registro_patronal TEXT NOT NULL,
        razon_social TEXT NOT NULL,
        guia TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura')),
        password_hash TEXT,
        activo BOOLEAN NOT NULL DEFAULT 1,
        intentos_fallidos INTEGER NOT NULL DEFAULT 0,
        bloqueado_hasta TEXT,
        sesion_token TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS trabajador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL,
        apellido_paterno TEXT,
        apellido_materno TEXT,
        nombres TEXT
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
        creado_en TEXT,
        umf TEXT
    )""",
    """CREATE TABLE IF NOT EXISTS bitacora (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL REFERENCES usuario(id),
        movimiento_id INTEGER REFERENCES movimiento(id),
        accion TEXT NOT NULL,
        detalle TEXT,
        timestamp TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS migracion (
        clave TEXT PRIMARY KEY,
        aplicada TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_movimiento_estado ON movimiento(estado)",
    "CREATE INDEX IF NOT EXISTS idx_bitacora_id ON bitacora(id)",
]

# Columnas agregadas después de la Entrega 5. Una base creada por una versión
# anterior no las tiene: init_db() las agrega sin tocar los datos.
#   (tabla, columna, tipo en SQLite, tipo en PostgreSQL)
_COLUMNAS_NUEVAS = [
    ("movimiento", "creado_en", "TEXT", "TIMESTAMP"),
    ("movimiento", "umf", "TEXT", "TEXT"),
    ("trabajador", "apellido_paterno", "TEXT", "TEXT"),
    ("trabajador", "apellido_materno", "TEXT", "TEXT"),
    ("trabajador", "nombres", "TEXT", "TEXT"),
    ("patron", "guia", "TEXT", "TEXT"),
    ("usuario", "password_hash", "TEXT", "TEXT"),
    ("usuario", "activo", "BOOLEAN NOT NULL DEFAULT 1", "BOOLEAN NOT NULL DEFAULT TRUE"),
    ("usuario", "intentos_fallidos", "INTEGER NOT NULL DEFAULT 0", "INTEGER NOT NULL DEFAULT 0"),
    ("usuario", "bloqueado_hasta", "TEXT", "TEXT"),
    ("usuario", "sesion_token", "TEXT", "TEXT"),
]

# Un mismo movimiento (trabajador, tipo y fecha) solo puede existir una vez.
# La aplicación ya lo revisa antes de insertar, pero dos capturas simultáneas
# pueden pasar esa revisión a la vez; la restricción en la base lo impide.
# Va aparte del DDL porque en una base con duplicados previos no se puede crear.
_INDICE_MOVIMIENTO_UNICO = (
    "CREATE UNIQUE INDEX IF NOT EXISTS uq_movimiento_trabajador_tipo_fecha "
    "ON movimiento(trabajador_id, tipo_movimiento, fecha_movimiento)")

PATRON_SEMILLA = ("A1234567890", "Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V.")
# Guía: número de 5 dígitos que asigna la subdelegación del IMSS al patrón. Va en
# cada registro del lote (posiciones 134-138). Antes de operar se cambia por el real.
GUIA_SEMILLA = "00000"
USUARIOS_SEMILLA = [("admin.rrhh", "administrador"), ("captura.obra1", "captura")]


def _columnas(cur, backend, tabla):
    if backend == "sqlite":
        cur.execute(f"PRAGMA table_info({tabla})")
        return {fila["name"] for fila in cur.fetchall()}
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = %s", (tabla,))
    return {fila["column_name"] for fila in cur.fetchall()}


def init_db():
    """Crea el esquema y los datos semilla, y migra bases anteriores. Es idempotente."""
    backend = _resolver_backend()
    ddl = _DDL_POSTGRES if backend == "postgres" else _DDL_SQLITE

    with conexion(commit=True) as conn:
        cur = conn.cursor()
        for sentencia in ddl:
            cur.execute(sentencia)

        # Bases creadas por versiones anteriores: se agregan las columnas nuevas.
        for tabla, columna, tipo_sqlite, tipo_postgres in _COLUMNAS_NUEVAS:
            if columna not in _columnas(cur, backend, tabla):
                tipo = tipo_sqlite if backend == "sqlite" else tipo_postgres
                cur.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")

        cur.execute("SELECT COUNT(*) AS n FROM patron")
        if cur.fetchone()["n"] == 0:
            cur.execute(
                "INSERT INTO patron (registro_patronal, razon_social, guia) VALUES (%s, %s, %s)",
                PATRON_SEMILLA + (GUIA_SEMILLA,),
            )
        cur.execute("UPDATE patron SET guia = %s WHERE guia IS NULL", (GUIA_SEMILLA,))

        cur.execute("SELECT COUNT(*) AS n FROM usuario")
        if cur.fetchone()["n"] == 0:
            cur.executemany("INSERT INTO usuario (nombre, rol) VALUES (%s, %s)", USUARIOS_SEMILLA)

        _migrar(cur)
        cur.close()

    try:
        with conexion(commit=True) as conn:
            cur = conn.cursor()
            cur.execute(_INDICE_MOVIMIENTO_UNICO)
            cur.close()
    except ERRORES_DE_INTEGRIDAD:
        print("[sigma] Aviso: la base ya contiene movimientos duplicados, así que no se creó "
              "la restricción de unicidad. Depura los duplicados y reinicia el sistema.")


# --------------------------------------------------------------------------
# Migraciones de datos (se aplican una sola vez y quedan en la tabla migracion)
# --------------------------------------------------------------------------
def _migrar(cur):
    cur.execute("SELECT clave FROM migracion")
    aplicadas = {fila["clave"] for fila in cur.fetchall()}
    for clave, funcion in _MIGRACIONES:
        if clave not in aplicadas:
            funcion(cur)
            cur.execute("INSERT INTO migracion (clave, aplicada) VALUES (%s, %s)", (clave, ahora()))


def _migrar_jornada_oficial(cur):
    """
    Hasta la Entrega 5 el catálogo de jornada era propio (1 = normal, 2 = jornada
    reducida, 3 = semana reducida, 4 = ambas). El IMSS usa 0 = normal, 1 a 5 =
    días de la semana reducida y 6 = jornada reducida.
    """
    cur.execute("UPDATE movimiento SET tipo_jornada = '6' WHERE tipo_jornada = '2'")
    cur.execute("UPDATE movimiento SET tipo_jornada = '0' WHERE tipo_jornada = '1'")
    cur.execute("SELECT id FROM movimiento WHERE tipo_jornada IN ('3', '4') ORDER BY id")
    revisar = [str(fila["id"]) for fila in cur.fetchall()]
    if revisar:
        print("[sigma] Aviso: los movimientos " + ", ".join(revisar) + " tenían semana reducida con "
              "el catálogo anterior; con el catálogo del IMSS hay que indicar cuántos días (1 a 5).")


def separar_nombre(nombre_completo, curp=""):
    """
    Divide un nombre completo en (paterno, materno, nombres). Prueba las formas
    posibles, con el nombre al final o al principio, y se queda con la que
    reproduce las iniciales de la CURP. Si ninguna coincide, toma la primera
    palabra como apellido paterno, la segunda como materno y el resto como nombre.
    """
    palabras = (nombre_completo or "").split()
    if len(palabras) < 2:
        return (palabras[0] if palabras else ""), "", ""
    candidatos = []
    n = len(palabras)
    for i in range(1, n):
        for j in range(i, n):
            pat, mat, nom = palabras[:i], palabras[i:j], palabras[j:]
            candidatos.append((" ".join(pat), " ".join(mat), " ".join(nom)))
            nom2, pat2, mat2 = palabras[:i], palabras[i:j], palabras[j:]
            if pat2:
                candidatos.append((" ".join(pat2), " ".join(mat2), " ".join(nom2)))
    clave = (curp or "")[:4].upper()
    for pat, mat, nom in candidatos:
        esperado = iniciales_curp(pat, mat, nom)
        if clave and esperado and clave in (esperado, esperado[0] + "X" + esperado[2:]):
            return pat, mat, nom
    if n == 2:
        return palabras[0], "", palabras[1]
    return palabras[0], palabras[1], " ".join(palabras[2:])


def _migrar_nombres_separados(cur):
    """El IMSS pide el nombre en tres campos; se separan los que ya estaban capturados."""
    cur.execute("SELECT id, nombre_completo, curp FROM trabajador WHERE apellido_paterno IS NULL")
    for fila in cur.fetchall():
        pat, mat, nom = separar_nombre(fila["nombre_completo"], fila["curp"])
        completo = " ".join(p for p in (pat, mat, nom) if p)
        cur.execute("UPDATE trabajador SET apellido_paterno = %s, apellido_materno = %s, nombres = %s, "
                    "nombre_completo = %s WHERE id = %s", (pat, mat, nom, completo, fila["id"]))


_MIGRACIONES = [
    ("2026-10-07-jornada-oficial", _migrar_jornada_oficial),
    ("2026-10-07-nombres-separados", _migrar_nombres_separados),
]


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


def obtener_o_crear_trabajador(conn, nombre_completo, curp, nss, rfc,
                               apellido_paterno=None, apellido_materno=None, nombres=None):
    """
    Id del expediente del trabajador (lo crea si es nuevo). Si no se reciben
    los tres campos del nombre, se obtienen separando el nombre completo.
    """
    if apellido_paterno is None and nombres is None:
        apellido_paterno, apellido_materno, nombres = separar_nombre(nombre_completo, curp)
    partes = (apellido_paterno or "", apellido_materno or "", nombres or "")
    cur = conn.cursor()
    cur.execute("SELECT id FROM trabajador WHERE curp = %s", (curp,))
    fila = cur.fetchone()
    if fila:
        # El expediente ya existe: se actualizan los datos por si cambiaron.
        cur.execute(
            "UPDATE trabajador SET nombre_completo = %s, rfc = %s, apellido_paterno = %s, "
            "apellido_materno = %s, nombres = %s WHERE id = %s",
            (nombre_completo, rfc) + partes + (fila["id"],),
        )
        cur.close()
        return fila["id"]
    cur.execute(
        "INSERT INTO trabajador (nombre_completo, curp, nss, rfc, apellido_paterno, apellido_materno, "
        "nombres) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
        (nombre_completo, curp, nss, rfc) + partes,
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
            "INSERT INTO patron (registro_patronal, razon_social, guia) VALUES (%s, %s, %s) RETURNING id",
            PATRON_SEMILLA + (GUIA_SEMILLA,),
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


# Fecha DDMMAAAA reordenada como AAAAMMDD para poder ordenar por ella en SQL.
_FECHA_ORDENABLE = ("substr(m.fecha_movimiento, 5, 4) || substr(m.fecha_movimiento, 3, 2) "
                    "|| substr(m.fecha_movimiento, 1, 2)")


def estado_afiliatorio(conn, curp):
    """
    Estado del trabajador frente al patrón según su último movimiento:
      ("SIN_REGISTRO", None)  nunca se ha capturado un movimiento suyo
      ("VIGENTE", fila)       su último movimiento es un alta
      ("NO_VIGENTE", fila)    su último movimiento es una baja
    """
    cur = conn.cursor()
    cur.execute(
        f"""SELECT m.id, m.tipo_movimiento, m.fecha_movimiento
            FROM movimiento m JOIN trabajador t ON t.id = m.trabajador_id
            WHERE t.curp = %s AND m.estado <> 'Rechazado'
            ORDER BY {_FECHA_ORDENABLE} DESC, m.id DESC
            LIMIT 1""",
        (curp,),
    )
    fila = cur.fetchone()
    cur.close()
    if fila is None:
        return "SIN_REGISTRO", None
    fila = dict(fila)
    return ("VIGENTE" if fila["tipo_movimiento"] == "08" else "NO_VIGENTE"), fila


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
