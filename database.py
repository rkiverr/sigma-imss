"""
Capa de persistencia: base de datos relacional normalizada en PostgreSQL.
Sustituye la versión de SQLite usada en la primera prueba de concepto,
acercando el prototipo a la Alternativa 3 descrita en la Entrega 2
(sistema cliente-servidor con SGBD relacional real).

Tablas: patron, usuario, trabajador, movimiento, bitacora

Configuración:
  Por defecto se conecta a postgresql://postgres:postgres@localhost:5432/sigma_imss
  Puede sobreescribirse con la variable de entorno DATABASE_URL, por ejemplo:
    export DATABASE_URL="postgresql://usuario:password@host:5432/basededatos"
"""
import os

# En Windows, si la configuración regional del sistema está en español,
# libpq (la librería detrás de psycopg2) traduce sus mensajes de error al
# español usando una codificación distinta a UTF-8. Eso hace que psycopg2
# truene con UnicodeDecodeError al intentar LEER el mensaje de error, en
# lugar de mostrar el error real (contraseña incorrecta, servidor caído,
# base de datos inexistente, etc.). Forzamos mensajes en inglés/ASCII para
# evitar el choque de codificación y poder ver el error verdadero.
os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"
os.environ.setdefault("PGCLIENTENCODING", "UTF8")

import psycopg2
import psycopg2.extras
from datetime import datetime

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/sigma_imss?client_encoding=UTF8"
)


def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patron (
        id SERIAL PRIMARY KEY,
        registro_patronal TEXT NOT NULL,
        razon_social TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS usuario (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL UNIQUE,
        rol TEXT NOT NULL CHECK (rol IN ('administrador', 'captura'))
    );

    CREATE TABLE IF NOT EXISTS trabajador (
        id SERIAL PRIMARY KEY,
        nombre_completo TEXT NOT NULL,
        curp TEXT NOT NULL UNIQUE,
        nss TEXT NOT NULL UNIQUE,
        rfc TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS movimiento (
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
    );

    CREATE TABLE IF NOT EXISTS bitacora (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER NOT NULL REFERENCES usuario(id),
        movimiento_id INTEGER REFERENCES movimiento(id),
        accion TEXT NOT NULL,
        detalle TEXT,
        timestamp TIMESTAMP NOT NULL
    );
    """)

    cur.execute("SELECT COUNT(*) AS n FROM patron")
    if cur.fetchone()["n"] == 0:
        cur.execute(
            "INSERT INTO patron (registro_patronal, razon_social) VALUES (%s, %s)",
            ("A1234567890", "Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V."),
        )

    cur.execute("SELECT COUNT(*) AS n FROM usuario")
    if cur.fetchone()["n"] == 0:
        cur.executemany(
            "INSERT INTO usuario (nombre, rol) VALUES (%s, %s)",
            [("admin.rrhh", "administrador"), ("captura.obra1", "captura")],
        )

    conn.commit()
    cur.close()
    conn.close()


def registrar_bitacora(conn, usuario_id, movimiento_id, accion, detalle=""):
    conn.cursor().execute(
        "INSERT INTO bitacora (usuario_id, movimiento_id, accion, detalle, timestamp) VALUES (%s, %s, %s, %s, %s)",
        (usuario_id, movimiento_id, accion, detalle, datetime.now()),
    )


def obtener_o_crear_trabajador(conn, nombre_completo, curp, nss, rfc):
    cur = conn.cursor()
    cur.execute("SELECT id FROM trabajador WHERE curp = %s", (curp,))
    row = cur.fetchone()
    if row:
        return row["id"]
    cur.execute(
        "INSERT INTO trabajador (nombre_completo, curp, nss, rfc) VALUES (%s, %s, %s, %s) RETURNING id",
        (nombre_completo, curp, nss, rfc),
    )
    return cur.fetchone()["id"]