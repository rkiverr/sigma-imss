"""
Usuarios de Sigma: contraseñas, inicio de sesión y administración desde la consola.

Hasta la Entrega 5 el usuario que capturaba se elegía de una lista, así que la
bitácora documentaba la autoría pero no la demostraba. Desde el TRL 6 cada
persona entra con su contraseña y la bitácora toma el usuario de la sesión.

  * Las contraseñas se guardan con hash (werkzeug.security, que ya viene con Flask).
  * Tras INTENTOS_MAXIMOS intentos fallidos, la cuenta se bloquea MINUTOS_BLOQUEO minutos.
  * Roles: "captura" captura y consulta; "administrador" además genera y descarga lotes.
  * La sesión lleva un token que también vive en la base: cerrar sesión, cambiar la
    contraseña o desactivar al usuario lo borra, y las cookies anteriores dejan de servir.

Uso (desde la raíz del repositorio):
    python -m sigma.usuarios listar
    python -m sigma.usuarios contrasena admin.rrhh          (pide la contraseña dos veces)
    python -m sigma.usuarios crear captura.obra2 captura
    python -m sigma.usuarios desactivar captura.obra2
    python -m sigma.usuarios activar captura.obra2
    python -m sigma.usuarios desbloquear admin.rrhh
"""
import argparse
import getpass
import secrets
import sys
from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from .database import conexion, init_db, registrar_bitacora

ROLES = ("administrador", "captura")
INTENTOS_MAXIMOS = 5
MINUTOS_BLOQUEO = 15
LONGITUD_MINIMA = 8
MENSAJE_GENERICO = "Usuario o contraseña incorrectos."

# Hash de referencia: si el usuario no existe se compara contra él, para que la
# respuesta tarde lo mismo y no delate qué nombres de usuario son válidos.
_HASH_DE_RELLENO = generate_password_hash("sigma-relleno-sin-uso")


def buscar(conn, nombre):
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE nombre = %s", ((nombre or "").strip(),))
    fila = cur.fetchone()
    cur.close()
    return dict(fila) if fila else None


def por_id(conn, usuario_id):
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, rol, activo, sesion_token FROM usuario WHERE id = %s", (usuario_id,))
    fila = cur.fetchone()
    cur.close()
    return dict(fila) if fila else None


def fijar_contrasena(conn, nombre, contrasena):
    if len(contrasena or "") < LONGITUD_MINIMA:
        raise ValueError(f"La contraseña debe tener al menos {LONGITUD_MINIMA} caracteres.")
    cur = conn.cursor()
    cur.execute("UPDATE usuario SET password_hash = %s, intentos_fallidos = 0, bloqueado_hasta = NULL, "
                "sesion_token = NULL WHERE nombre = %s", (generate_password_hash(contrasena), nombre))
    cambiados = cur.rowcount
    cur.close()
    if not cambiados:
        raise ValueError(f"No existe el usuario {nombre}.")


def _bloqueado(usuario, ahora):
    texto = usuario.get("bloqueado_hasta")
    if not texto:
        return None
    hasta = datetime.fromisoformat(str(texto))
    return hasta if hasta > ahora else None


def autenticar(conn, nombre, contrasena):
    """
    Devuelve (usuario, None) si las credenciales son correctas, o (None, mensaje).
    Cuenta los intentos fallidos y bloquea la cuenta al llegar al máximo.
    """
    usuario = buscar(conn, nombre)
    ahora = datetime.now()
    if usuario is None or not usuario.get("password_hash") or not usuario.get("activo"):
        check_password_hash(_HASH_DE_RELLENO, contrasena or "")
        return None, MENSAJE_GENERICO
    hasta = _bloqueado(usuario, ahora)
    if hasta:
        return None, (f"La cuenta está bloqueada por {INTENTOS_MAXIMOS} intentos fallidos; "
                      f"vuelve a intentarlo después de las {hasta:%H:%M}.")
    cur = conn.cursor()
    if check_password_hash(usuario["password_hash"], contrasena or ""):
        cur.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id = %s",
                    (usuario["id"],))
        cur.close()
        registrar_bitacora(conn, usuario["id"], None, "Inicio de sesión", "")
        return usuario, None
    intentos = (usuario.get("intentos_fallidos") or 0) + 1
    if intentos >= INTENTOS_MAXIMOS:
        hasta = ahora + timedelta(minutes=MINUTOS_BLOQUEO)
        cur.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = %s WHERE id = %s",
                    (hasta.isoformat(sep=" ", timespec="seconds"), usuario["id"]))
        cur.close()
        registrar_bitacora(conn, usuario["id"], None, "Cuenta bloqueada",
                           f"{INTENTOS_MAXIMOS} intentos fallidos; bloqueada hasta las {hasta:%H:%M}")
        return None, (f"La cuenta quedó bloqueada {MINUTOS_BLOQUEO} minutos por "
                      f"{INTENTOS_MAXIMOS} intentos fallidos.")
    cur.execute("UPDATE usuario SET intentos_fallidos = %s WHERE id = %s", (intentos, usuario["id"]))
    cur.close()
    registrar_bitacora(conn, usuario["id"], None, "Inicio de sesión fallido",
                       f"intento {intentos} de {INTENTOS_MAXIMOS}")
    return None, MENSAJE_GENERICO


def abrir_sesion(conn, usuario):
    """
    Token de sesión del usuario. Varias PC pueden usar la misma cuenta a la vez,
    así que se reutiliza el vigente; solo se crea uno si no hay.
    """
    if usuario.get("sesion_token"):
        return usuario["sesion_token"]
    token = secrets.token_hex(16)
    cur = conn.cursor()
    cur.execute("UPDATE usuario SET sesion_token = %s WHERE id = %s", (token, usuario["id"]))
    cur.close()
    return token


def cerrar_sesiones(conn, usuario_id):
    """Invalida todas las sesiones abiertas del usuario (cookies copiadas incluidas)."""
    cur = conn.cursor()
    cur.execute("UPDATE usuario SET sesion_token = NULL WHERE id = %s", (usuario_id,))
    cur.close()


def hay_contrasenas(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS n FROM usuario WHERE password_hash IS NOT NULL AND activo")
    n = cur.fetchone()["n"]
    cur.close()
    return n > 0


# --------------------------------------------------------------------------
# Consola
# --------------------------------------------------------------------------
def _pedir_contrasena(argumentos):
    if argumentos.contrasena:
        return argumentos.contrasena
    primera = getpass.getpass("Contraseña nueva: ")
    if getpass.getpass("Repite la contraseña: ") != primera:
        raise ValueError("Las contraseñas no coinciden.")
    return primera


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m sigma.usuarios",
                                     description="Administra los usuarios de Sigma.")
    sub = parser.add_subparsers(dest="accion", required=True)
    sub.add_parser("listar", help="muestra los usuarios, su rol y su estado")
    crear = sub.add_parser("crear", help="crea un usuario y le asigna contraseña")
    crear.add_argument("nombre")
    crear.add_argument("rol", choices=ROLES)
    crear.add_argument("--contrasena", help="para scripts; si se omite, se pide en la consola")
    cambiar = sub.add_parser("contrasena", help="asigna o cambia la contraseña de un usuario")
    cambiar.add_argument("nombre")
    cambiar.add_argument("--contrasena", help="para scripts; si se omite, se pide en la consola")
    for accion in ("activar", "desactivar", "desbloquear"):
        sub.add_parser(accion).add_argument("nombre")
    argumentos = parser.parse_args(argv)

    init_db()
    try:
        with conexion(commit=True) as conn:
            if argumentos.accion == "listar":
                cur = conn.cursor()
                cur.execute("SELECT nombre, rol, activo, password_hash, bloqueado_hasta FROM usuario "
                            "ORDER BY id")
                for fila in cur.fetchall():
                    estado = "activo" if fila["activo"] else "desactivado"
                    if not fila["password_hash"]:
                        estado += " · sin contraseña"
                    if fila["bloqueado_hasta"]:
                        estado += f" · bloqueado hasta {fila['bloqueado_hasta']}"
                    print(f"{fila['nombre']:<20} {fila['rol']:<14} {estado}")
                cur.close()
            elif argumentos.accion == "crear":
                if buscar(conn, argumentos.nombre):
                    raise ValueError(f"El usuario {argumentos.nombre} ya existe.")
                contrasena = _pedir_contrasena(argumentos)
                cur = conn.cursor()
                cur.execute("INSERT INTO usuario (nombre, rol) VALUES (%s, %s)",
                            (argumentos.nombre, argumentos.rol))
                cur.close()
                fijar_contrasena(conn, argumentos.nombre, contrasena)
                print(f"Usuario {argumentos.nombre} ({argumentos.rol}) creado.")
            elif argumentos.accion == "contrasena":
                fijar_contrasena(conn, argumentos.nombre, _pedir_contrasena(argumentos))
                print(f"Contraseña de {argumentos.nombre} actualizada.")
            else:
                if not buscar(conn, argumentos.nombre):
                    raise ValueError(f"No existe el usuario {argumentos.nombre}.")
                cur = conn.cursor()
                if argumentos.accion == "desbloquear":
                    cur.execute("UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = NULL "
                                "WHERE nombre = %s", (argumentos.nombre,))
                else:
                    cur.execute("UPDATE usuario SET activo = %s, sesion_token = NULL WHERE nombre = %s",
                                (argumentos.accion == "activar", argumentos.nombre))
                cur.close()
                print(f"Usuario {argumentos.nombre}: {argumentos.accion} listo.")
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
