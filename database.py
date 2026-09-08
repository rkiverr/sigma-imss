"""
Capa de persistencia: base de datos relacional normalizada (SQLite para el
prototipo; el motor puede sustituirse por PostgreSQL/MySQL sin cambiar la
lógica de negocio, ya que solo se usa SQL estándar).

Tablas: patron, usuario, trabajador, movimiento, bitacora
"""
import sqlite3
from datetime import datetime

DB_PATH = "prueba_concepto.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS patron (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registro_patronal TEXT NOT NULL,
        razon_social TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura'))
    );

    CREATE TABLE IF NOT EXISTS trabajador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS movimiento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trabajador_id INTEGER NOT NULL,
        patron_id INTEGER NOT NULL,
        tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('08','02')),
        fecha_movimiento TEXT NOT NULL,
        tipo_trabajador TEXT,
        tipo_salario TEXT,
        tipo_jornada TEXT,
        sdi TEXT,
        causa_baja TEXT,
        estado TEXT NOT NULL CHECK (estado IN ('Válido','Rechazado','Exportado')),
        exportado INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (trabajador_id) REFERENCES trabajador(id),
        FOREIGN KEY (patron_id) REFERENCES patron(id)
    );

    CREATE TABLE IF NOT EXISTS bitacora (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        movimiento_id INTEGER,
        accion TEXT NOT NULL,
        detalle TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id),
        FOREIGN KEY (movimiento_id) REFERENCES movimiento(id)
    );
    """)

    # Datos semilla mínimos para poder correr la prueba de concepto
    cur.execute("SELECT COUNT(*) FROM patron")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO patron (registro_patronal, razon_social) VALUES (?, ?)",
            ("A1234567890", "Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V."),
        )

    cur.execute("SELECT COUNT(*) FROM usuario")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO usuario (nombre, rol) VALUES (?, ?)",
            [("admin.rrhh", "administrador"), ("captura.obra1", "captura")],
        )

    conn.commit()
    conn.close()


def registrar_bitacora(conn, usuario_id, movimiento_id, accion, detalle=""):
    conn.execute(
        "INSERT INTO bitacora (usuario_id, movimiento_id, accion, detalle, timestamp) VALUES (?, ?, ?, ?, ?)",
        (usuario_id, movimiento_id, accion, detalle, datetime.now().isoformat(timespec="seconds")),
    )


def obtener_o_crear_trabajador(conn, nombre_completo, curp, nss, rfc):
    row = conn.execute("SELECT id FROM trabajador WHERE curp = ?", (curp,)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO trabajador (nombre_completo, curp, nss, rfc) VALUES (?, ?, ?, ?)",
        (nombre_completo, curp, nss, rfc),
    )
    return cur.lastrowid
