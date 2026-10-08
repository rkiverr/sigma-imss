"""
Sistema Sigma — sistema integrado y demostrado en ambiente relevante (Entrega 6, TRL 6).

Interfaz cliente (aplicación web) + lógica de servidor (validación,
persistencia y exportación) para el sistema de altas y bajas IMSS/IDSE.

Arquitectura cliente-servidor (paquete sigma/):
    templates/ + static/   capa de presentación
    app.py                 controlador HTTP, sesión y reglas de flujo
    validaciones.py        validación algorítmica
    plazo.py               plazo legal de cinco días hábiles
    database.py            persistencia relacional (PostgreSQL o SQLite)
    exportar_idse.py       lote IDSE con la estructura oficial de 168 posiciones
    usuarios.py            contraseñas, inicio de sesión y consola de usuarios
    respaldo.py            respaldo y restauración de la base
    __main__.py            servidor de desarrollo (python -m sigma)
    ../servidor.py         arranque en modo producción (waitress)
"""
import os
import secrets
from datetime import date, datetime, timedelta
from functools import wraps
from urllib.parse import urlparse

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, send_file, session, url_for)
from werkzeug.exceptions import Forbidden, HTTPException

from . import exportar_idse, plazo, usuarios
from .database import (ERRORES_DE_INTEGRIDAD, RAIZ, ErrorBaseDeDatos, conexion,
                       conflicto_de_identidad, descripcion_backend,
                       estadisticas, estado_afiliatorio,
                       movimiento_duplicado, obtener_o_crear_trabajador,
                       obtener_patron_id, registrar_bitacora)
from .validaciones import (CAUSAS_BAJA, ORDEN_CAMPOS, TIPO_ALTA, TIPO_BAJA,
                           TIPOS_JORNADA, TIPOS_SALARIO, TIPOS_TRABAJADOR,
                           aviso_montos_sin_cargar, normalizar_datos, validar_campos)


def _clave_de_sesion():
    """
    Clave con la que se firma la cookie de sesión. Si no viene en SECRET_KEY,
    se genera una vez y se guarda en .clave_sesion (fuera de Git), para que
    reiniciar el servidor no cierre las sesiones ni pierda los mensajes.
    """
    if os.environ.get("SECRET_KEY"):
        return os.environ["SECRET_KEY"]
    ruta = os.path.join(RAIZ, ".clave_sesion")
    try:
        with open(ruta, encoding="utf-8") as archivo:
            clave = archivo.read().strip()
        if clave:
            return clave
    except OSError:
        pass
    clave = secrets.token_hex(32)
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(clave)
    except OSError:
        pass  # sin permiso de escritura: la clave vive mientras dure el proceso
    return clave


app = Flask(__name__)
app.secret_key = _clave_de_sesion()
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=float(os.environ.get("SIGMA_SESION_HORAS", "10"))),
    # Un formulario de captura pesa menos de 1 KB; el límite evita que una sola
    # petición enorme ocupe al servidor.
    MAX_CONTENT_LENGTH=int(os.environ.get("SIGMA_MAX_PETICION_KB", "1024")) * 1024,
)

MOVIMIENTOS_POR_PAGINA = 25

# Folio más grande que cabe en un INTEGER de PostgreSQL; uno mayor no puede
# existir y, sin esta revisión, hacía fallar la consulta con error 500.
FOLIO_MAXIMO = 2 ** 31 - 1

ETIQUETAS_TIPO = {TIPO_ALTA: "Alta / Reingreso", TIPO_BAJA: "Baja"}

CAMPOS_FORMULARIO = [
    "apellido_paterno", "apellido_materno", "nombres", "curp", "nss", "rfc", "tipo_movimiento",
    "fecha_movimiento", "tipo_trabajador", "tipo_salario", "tipo_jornada", "sdi", "umf", "causa_baja",
]

CATALOGOS = {
    "tipo_trabajador": TIPOS_TRABAJADOR,
    "tipo_salario": TIPOS_SALARIO,
    "tipo_jornada": TIPOS_JORNADA,
    "causa_baja": CAUSAS_BAJA,
}

# Rutas que se pueden abrir sin haber iniciado sesión.
RUTAS_PUBLICAS = {"login", "static"}


# --------------------------------------------------------------------------
# Filtros de plantilla
# --------------------------------------------------------------------------
@app.template_filter("fecha_idse")
def filtro_fecha_idse(valor):
    """DDMMAAAA -> DD/MM/AAAA para lectura humana."""
    texto = str(valor or "")
    if len(texto) == 8 and texto.isdigit():
        return f"{texto[0:2]}/{texto[2:4]}/{texto[4:8]}"
    return texto or "—"


@app.template_filter("momento")
def filtro_momento(valor):
    """Formatea una marca de tiempo venga como datetime (PostgreSQL) o texto (SQLite)."""
    if valor is None:
        return "—"
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M:%S")
    texto = str(valor)
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(texto, formato).strftime("%d/%m/%Y %H:%M:%S")
        except ValueError:
            continue
    return texto


@app.template_filter("etiqueta_tipo")
def filtro_etiqueta_tipo(valor):
    return ETIQUETAS_TIPO.get(str(valor), str(valor or "—"))


# --------------------------------------------------------------------------
# Lectura de datos para la pantalla principal
# --------------------------------------------------------------------------
def _leer_formulario():
    """Extrae y normaliza los campos capturados en el formulario."""
    return normalizar_datos({campo: request.form.get(campo) for campo in CAMPOS_FORMULARIO})


def _legible(ddmmaaaa):
    return f"{ddmmaaaa[0:2]}/{ddmmaaaa[2:4]}/{ddmmaaaa[4:8]}"


def _validar_historial(conn, datos):
    """
    Reglas que dependen del historial afiliatorio del trabajador. Atienden el
    problema descrito en la Entrega 1: el archivo de control no distinguía a un
    trabajador que solo cambió de obra de uno que salió de la empresa, lo que
    producía altas duplicadas y bajas de personas ya dadas de baja.
    Devuelve (errores, avisos).
    """
    estado, ultimo = estado_afiliatorio(conn, datos["curp"])
    fecha = datetime.strptime(datos["fecha_movimiento"], "%d%m%Y").date()
    previa = (datetime.strptime(ultimo["fecha_movimiento"], "%d%m%Y").date()
              if ultimo else None)

    if datos["tipo_movimiento"] == TIPO_ALTA:
        if estado == "VIGENTE":
            return {"tipo_movimiento": (
                f"El trabajador ya tiene un alta vigente desde el "
                f"{_legible(ultimo['fecha_movimiento'])} (folio #{ultimo['id']}). Si solo cambió "
                "de obra no necesita un alta nueva; si salió de la empresa, registra primero "
                "la baja.")}, {}
        if estado == "NO_VIGENTE" and fecha < previa:
            return {"fecha_movimiento": (
                f"El reingreso no puede ser anterior a la baja del "
                f"{_legible(ultimo['fecha_movimiento'])} (folio #{ultimo['id']}).")}, {}
        return {}, {}

    if estado == "SIN_REGISTRO":
        return {}, {"tipo_movimiento": (
            "Sigma no tiene registrada un alta de este trabajador. Verifica que esté dado de "
            "alta ante el IMSS antes de presentar la baja.")}
    if estado == "NO_VIGENTE":
        return {"tipo_movimiento": (
            f"El trabajador ya fue dado de baja el {_legible(ultimo['fecha_movimiento'])} "
            f"(folio #{ultimo['id']}); no tiene un alta vigente que cerrar.")}, {}
    if fecha < previa:
        return {"fecha_movimiento": (
            f"La fecha de baja ({_legible(datos['fecha_movimiento'])}) es anterior a la del alta "
            f"vigente ({_legible(ultimo['fecha_movimiento'])}).")}, {}
    return {}, {}


def _consultar_movimientos(conn, filtros):
    """Lista de movimientos aplicando los filtros de la interfaz, ya paginada."""
    condiciones = []
    parametros = []

    if filtros["q"]:
        patron = f"%{filtros['q'].upper()}%"
        condiciones.append("(UPPER(t.nombre_completo) LIKE %s OR UPPER(t.curp) LIKE %s OR t.nss LIKE %s)")
        parametros += [patron, patron, patron]
    if filtros["estado"]:
        condiciones.append("m.estado = %s")
        parametros.append(filtros["estado"])
    if filtros["tipo"]:
        condiciones.append("m.tipo_movimiento = %s")
        parametros.append(filtros["tipo"])

    where = (" WHERE " + " AND ".join(condiciones)) if condiciones else ""

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS n FROM movimiento m JOIN trabajador t ON t.id = m.trabajador_id" + where,
                tuple(parametros))
    total = cur.fetchone()["n"]

    pagina = max(1, filtros["pagina"])
    offset = (pagina - 1) * MOVIMIENTOS_POR_PAGINA
    cur.execute(
        """SELECT m.id, t.nombre_completo, t.curp, t.nss, t.rfc, m.tipo_movimiento,
                  m.fecha_movimiento, m.estado, m.sdi, m.causa_baja, m.creado_en,
                  m.tipo_trabajador, m.tipo_salario, m.tipo_jornada, m.umf
           FROM movimiento m JOIN trabajador t ON t.id = m.trabajador_id"""
        + where + " ORDER BY m.id DESC LIMIT %s OFFSET %s",
        tuple(parametros) + (MOVIMIENTOS_POR_PAGINA, offset),
    )
    movimientos = [dict(fila) for fila in cur.fetchall()]
    cur.close()

    paginas = max(1, -(-total // MOVIMIENTOS_POR_PAGINA))  # división hacia arriba
    return movimientos, total, min(pagina, paginas), paginas


def _contexto(conn, filtros, form=None, errores=None, avisos=None):
    """Arma todo lo que necesita la plantilla principal."""
    movimientos, total, pagina, paginas = _consultar_movimientos(conn, filtros)

    cur = conn.cursor()
    cur.execute(
        """SELECT b.timestamp, u.nombre AS usuario, b.accion, b.detalle, b.movimiento_id
           FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
           ORDER BY b.id DESC LIMIT 15"""
    )
    bitacora = [dict(fila) for fila in cur.fetchall()]

    cur.execute("SELECT registro_patronal, razon_social FROM patron ORDER BY id LIMIT 1")
    fila = cur.fetchone()
    patron = dict(fila) if fila else {"registro_patronal": "—", "razon_social": "—"}
    cur.close()

    filtros_activos = bool(filtros["q"] or filtros["estado"] or filtros["tipo"])

    return {
        "movimientos": movimientos,
        "total_movimientos": total,
        "pagina": pagina,
        "paginas": paginas,
        "bitacora": bitacora,
        "patron": patron,
        "stats": estadisticas(conn),
        "filtros": filtros,
        "filtros_activos": filtros_activos,
        "form": form or {},
        "errores": errores or {},
        "avisos": avisos or {},
        "catalogos": CATALOGOS,
        "orden_campos": ORDEN_CAMPOS,
        "motor": descripcion_backend(),
        "es_admin": g.usuario["rol"] == "administrador",
        "lote_altas": exportar_idse.ultimo_lote("altas") is not None,
        "lote_bajas": exportar_idse.ultimo_lote("bajas") is not None,
        "aviso_montos": aviso_montos_sin_cargar(date.today().year),
    }


def _filtros_de_peticion():
    try:
        pagina = int(request.args.get("pagina", 1))
    except ValueError:
        pagina = 1
    estado = request.args.get("estado", "").strip()
    tipo = request.args.get("tipo", "").strip()
    return {
        "q": request.args.get("q", "").strip(),
        "estado": estado if estado in ("Válido", "Exportado", "Rechazado") else "",
        "tipo": tipo if tipo in (TIPO_ALTA, TIPO_BAJA) else "",
        "pagina": max(1, pagina),
    }


# --------------------------------------------------------------------------
# Seguridad de cada petición
# --------------------------------------------------------------------------
@app.before_request
def preparar_peticion():
    # Nonce de un solo uso para el único script en línea (el del tema), de modo
    # que la política de contenido pueda prohibir cualquier otro.
    g.csp_nonce = secrets.token_urlsafe(16)
    g.usuario = None

    # Un formulario solo se acepta si lo envió una página de Sigma. Los
    # navegadores ponen el sitio de origen en Origin (o en Referer); si otro
    # sitio intenta enviar una captura a nombre del usuario (CSRF), no coincide.
    if request.method == "POST":
        origen = request.headers.get("Origin") or request.headers.get("Referer")
        if origen and urlparse(origen).netloc != request.host:
            abort(403)

    # Las direcciones que no existen responden 404 aunque no haya sesión.
    if request.endpoint is None or request.endpoint == "static":
        return None

    usuario_id = session.get("usuario_id")
    if usuario_id:
        with conexion() as conn:
            usuario = usuarios.por_id(conn, usuario_id)
        # La cookie solo vale si su token coincide con el de la base (ver usuarios.abrir_sesion).
        if (usuario and usuario["activo"] and usuario["sesion_token"]
                and secrets.compare_digest(session.get("token") or "", usuario["sesion_token"])):
            g.usuario = usuario
        else:
            session.clear()

    if g.usuario is None and request.endpoint not in RUTAS_PUBLICAS:
        if request.path.startswith("/api/"):
            return jsonify({"error": "La sesión terminó. Vuelve a iniciar sesión."}), 401
        return redirect(url_for("login"))
    return None


def requiere_rol(rol):
    """Restringe una vista a un rol; los demás reciben 403 con la explicación."""
    def decorador(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            if g.usuario is None or g.usuario["rol"] != rol:
                abort(403, "Solo el personal de administración puede generar y descargar lotes IDSE.")
            return vista(*args, **kwargs)
        return envoltura
    return decorador


@app.context_processor
def variables_de_plantilla():
    return {"csp_nonce": getattr(g, "csp_nonce", ""), "usuario_actual": getattr(g, "usuario", None)}


@app.after_request
def cabeceras_de_seguridad(respuesta):
    nonce = getattr(g, "csp_nonce", "")
    respuesta.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "form-action 'self'; frame-ancestors 'none'; base-uri 'self'")
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Referrer-Policy"] = "same-origin"
    return respuesta


# --------------------------------------------------------------------------
# Sesión
# --------------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario is not None:
        return redirect(url_for("index"))
    nombre = ""
    error = None
    estado = 200
    if request.method == "POST":
        nombre = (request.form.get("usuario") or "").strip()
        with conexion(commit=True) as conn:
            usuario, error = usuarios.autenticar(conn, nombre, request.form.get("contrasena") or "")
            token = usuarios.abrir_sesion(conn, usuario) if usuario else None
        if usuario:
            # Una sesión nueva en cada inicio evita reutilizar una cookie anterior.
            session.clear()
            session.permanent = True
            session["usuario_id"] = usuario["id"]
            session["token"] = token
            return redirect(url_for("index"))
        estado = 401
    with conexion() as conn:
        sin_contrasenas = not usuarios.hay_contrasenas(conn)
    return render_template("login.html", error=error, nombre=nombre,
                           sin_contrasenas=sin_contrasenas), estado


@app.route("/logout", methods=["POST"])
def logout():
    with conexion(commit=True) as conn:
        registrar_bitacora(conn, g.usuario["id"], None, "Cierre de sesión", "")
        # Con sesiones en cookie, borrar la cookie no basta: el token de la base
        # se elimina para que una copia de la cookie tampoco siga sirviendo.
        usuarios.cerrar_sesiones(conn, g.usuario["id"])
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("login"))


# --------------------------------------------------------------------------
# Vistas
# --------------------------------------------------------------------------
@app.route("/")
def index():
    with conexion() as conn:
        return render_template("index.html", **_contexto(conn, _filtros_de_peticion()))


@app.route("/capturar", methods=["POST"])
def capturar():
    datos = _leer_formulario()
    errores, avisos = validar_campos(datos)
    usuario_id = g.usuario["id"]

    with conexion(commit=True) as conn:
        # Reglas que dependen del estado de la base y solo tienen sentido si
        # los identificadores ya pasaron la validación de formato.
        if not errores.get("curp") and not errores.get("nss"):
            conflicto = conflicto_de_identidad(conn, datos["curp"], datos["nss"])
            if conflicto:
                errores[conflicto[0]] = conflicto[1]

        if not errores:
            duplicado = movimiento_duplicado(
                conn, datos["curp"], datos["tipo_movimiento"], datos["fecha_movimiento"])
            if duplicado:
                errores["fecha_movimiento"] = (
                    f"Este movimiento ya fue capturado (folio #{duplicado}): mismo trabajador, "
                    "mismo tipo y misma fecha.")

        if not errores:
            errores_historial, avisos_historial = _validar_historial(conn, datos)
            errores.update(errores_historial)
            avisos.update(avisos_historial)

        movimiento_id = None
        if not errores:
            try:
                movimiento_id = _guardar_movimiento(conn, datos, usuario_id)
            except ERRORES_DE_INTEGRIDAD:
                # Otro capturista guardó lo mismo un instante antes: ambos
                # pasaron las revisiones previas y la base de datos decidió.
                conn.rollback()
                errores["movimiento"] = (
                    "Otro usuario acaba de registrar este mismo movimiento (o al mismo "
                    "trabajador con esta CURP o NSS). Revisa la tabla de movimientos antes de "
                    "volver a capturarlo.")

        if errores:
            registrar_bitacora(conn, usuario_id, None, "Intento de captura rechazado",
                               " | ".join(errores.values()))
            filtros = _filtros_de_peticion()
            contexto = _contexto(conn, filtros, form=datos, errores=errores, avisos=avisos)
            return render_template("index.html", **contexto), 422

    limite = plazo.fecha_limite(datos["fecha_movimiento"]).strftime("%d/%m/%Y")
    mensaje = f"Movimiento #{movimiento_id} validado y guardado correctamente."
    if avisos:
        mensaje += " Avisos: " + " ".join(avisos.values())
        flash(mensaje, "warning")
    else:
        mensaje += f" Plazo legal: preséntalo en IDSE a más tardar el {limite}."
        flash(mensaje, "success")
    return redirect(url_for("index"))


def _guardar_movimiento(conn, datos, usuario_id):
    """Inserta trabajador (si es nuevo), movimiento y asiento de bitácora."""
    patron_id = obtener_patron_id(conn)
    trabajador_id = obtener_o_crear_trabajador(
        conn, datos["nombre_completo"], datos["curp"], datos["nss"], datos["rfc"],
        datos["apellido_paterno"], datos["apellido_materno"], datos["nombres"])

    cur = conn.cursor()
    cur.execute(
        """INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento,
               tipo_trabajador, tipo_salario, tipo_jornada, sdi, causa_baja, umf, estado,
               exportado, creado_en)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Válido', FALSE, %s)
           RETURNING id""",
        (trabajador_id, patron_id, datos["tipo_movimiento"], datos["fecha_movimiento"],
         datos["tipo_trabajador"], datos["tipo_salario"], datos["tipo_jornada"],
         datos["sdi"], datos["causa_baja"],
         datos["umf"] if datos["tipo_movimiento"] == TIPO_ALTA else "",
         datetime.now().isoformat(sep=" ", timespec="seconds")),
    )
    movimiento_id = cur.fetchone()["id"]
    cur.close()

    registrar_bitacora(
        conn, usuario_id, movimiento_id, "Movimiento capturado",
        f"{ETIQUETAS_TIPO.get(datos['tipo_movimiento'], datos['tipo_movimiento'])} "
        f"de {datos['nombre_completo']} (CURP {datos['curp']})")
    return movimiento_id


@app.route("/exportar", methods=["POST"])
@requiere_rol("administrador")
def exportar():
    usuario_id = g.usuario["id"]
    with conexion(commit=True) as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT m.id AS movimiento_id, p.registro_patronal, p.guia, m.tipo_movimiento,
                      t.id AS trabajador_id, t.curp, t.nss, t.rfc, t.apellido_paterno,
                      t.apellido_materno, t.nombres, m.fecha_movimiento, m.tipo_trabajador,
                      m.tipo_salario, m.tipo_jornada, m.sdi, m.causa_baja, m.umf
               FROM movimiento m
               JOIN trabajador t ON t.id = m.trabajador_id
               JOIN patron p ON p.id = m.patron_id
               WHERE m.estado = 'Válido' AND m.exportado = FALSE
               ORDER BY m.id"""
        )
        pendientes = [dict(fila) for fila in cur.fetchall()]
        # Movimientos de bases anteriores al TRL 6 que no traen apellidos o UMF:
        # no se pueden escribir en la estructura oficial y se quedan pendientes.
        incompletos = [r for r in pendientes if exportar_idse.faltantes(r)]
        registros = [r for r in pendientes if not exportar_idse.faltantes(r)]

        if not registros:
            cur.close()
            if incompletos:
                flash(_mensaje_incompletos(incompletos), "error")
            else:
                flash("No hay movimientos válidos pendientes de exportar.", "error")
            return redirect(url_for("index"))

        rutas = exportar_idse.exportar_lote(registros)
        cur.executemany(
            "UPDATE movimiento SET exportado = TRUE, estado = 'Exportado' WHERE id = %s",
            [(registro["movimiento_id"],) for registro in registros],
        )
        cur.close()
        archivos = {tipo: os.path.basename(ruta) for tipo, ruta in rutas.items()}
        for registro in registros:
            registrar_bitacora(conn, usuario_id, registro["movimiento_id"], "Incluido en lote IDSE",
                               archivos[registro["tipo_movimiento"]])
        resumen = "; ".join(
            f"{sum(1 for r in registros if r['tipo_movimiento'] == tipo)} "
            f"{exportar_idse.NOMBRES_TIPO[tipo]} en {archivo}" for tipo, archivo in archivos.items())
        registrar_bitacora(conn, usuario_id, None, "Exportación de lote IDSE",
                           f"{len(registros)} movimiento(s): {resumen}")

    mensaje = f"Lote IDSE generado con {len(registros)} movimiento(s): {resumen}."
    if incompletos:
        flash(mensaje + " " + _mensaje_incompletos(incompletos), "warning")
    else:
        flash(mensaje, "success")
    return redirect(url_for("index"))


def _mensaje_incompletos(incompletos):
    folios = ", ".join(f"#{r['movimiento_id']}" for r in incompletos)
    return (f"No se exportaron {len(incompletos)} movimiento(s) capturados antes del TRL 6 ({folios}) "
            "porque les faltan apellidos separados o la UMF que pide el IMSS.")


@app.route("/descargar-lote")
@requiere_rol("administrador")
def descargar_lote():
    tipo = request.args.get("tipo")
    ruta = exportar_idse.ultimo_lote(tipo if tipo in ("altas", "bajas") else None)
    if not ruta or not os.path.isfile(ruta):
        flash("Todavía no se ha generado ningún lote IDSE para descargar.", "error")
        return redirect(url_for("index"))
    return send_file(ruta, as_attachment=True, mimetype="text/plain")


# --------------------------------------------------------------------------
# API usada por la interfaz (validación en vivo y detalle de movimientos)
# --------------------------------------------------------------------------
@app.route("/api/validar", methods=["POST"])
def api_validar():
    """
    Ejecuta EL MISMO validador que usa el servidor al guardar, de modo que la
    retroalimentación inmediata del formulario no pueda desviarse de la regla
    real. La validación del cliente es una ayuda visual, no una defensa.
    """
    datos = request.get_json(silent=True) or {}
    limpio = normalizar_datos({campo: datos.get(campo) for campo in CAMPOS_FORMULARIO})
    errores, avisos = validar_campos(limpio)
    return jsonify({"valido": not errores, "errores": errores, "avisos": avisos})


@app.route("/api/movimiento/<int:movimiento_id>")
def api_movimiento(movimiento_id):
    if movimiento_id > FOLIO_MAXIMO:
        return jsonify({"error": "El movimiento solicitado no existe."}), 404
    with conexion() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT m.id, t.nombre_completo, t.apellido_paterno, t.apellido_materno, t.nombres,
                      t.curp, t.nss, t.rfc, p.registro_patronal, p.razon_social,
                      m.tipo_movimiento, m.fecha_movimiento, m.estado, m.tipo_trabajador,
                      m.tipo_salario, m.tipo_jornada, m.sdi, m.causa_baja, m.umf, m.creado_en
               FROM movimiento m
               JOIN trabajador t ON t.id = m.trabajador_id
               JOIN patron p ON p.id = m.patron_id
               WHERE m.id = %s""",
            (movimiento_id,),
        )
        fila = cur.fetchone()

        cur.execute(
            """SELECT b.timestamp, u.nombre AS usuario, b.accion, b.detalle
               FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
               WHERE b.movimiento_id = %s ORDER BY b.id""",
            (movimiento_id,),
        )
        historial = [dict(registro) for registro in cur.fetchall()]
        cur.close()

    if fila is None:
        return jsonify({"error": "El movimiento solicitado no existe."}), 404

    movimiento = dict(fila)
    movimiento["tipo_etiqueta"] = ETIQUETAS_TIPO.get(movimiento["tipo_movimiento"], "")
    movimiento["fecha_legible"] = filtro_fecha_idse(movimiento["fecha_movimiento"])
    movimiento["creado_en"] = filtro_momento(movimiento["creado_en"])
    for campo, catalogo in CATALOGOS.items():
        movimiento[campo + "_etiqueta"] = catalogo.get(str(movimiento.get(campo) or ""), "")
    movimiento["historial"] = [
        {**registro, "timestamp": filtro_momento(registro["timestamp"])} for registro in historial
    ]
    return jsonify(movimiento)


# --------------------------------------------------------------------------
# Manejo de errores
# --------------------------------------------------------------------------
MENSAJES_HTTP = {
    400: ("Solicitud no válida", "El navegador envió datos que Sigma no pudo leer. Vuelve al inicio "
                                 "e inténtalo de nuevo."),
    405: ("Esta dirección no se abre así", "Las capturas y los lotes se envían con los botones de la "
                                           "pantalla principal; abrir esta dirección directamente no "
                                           "guarda ni cambia nada."),
    413: ("La solicitud es demasiado grande", "Sigma acepta envíos de hasta "
                                              f"{app.config['MAX_CONTENT_LENGTH'] // 1024} KB. Un "
                                              "formulario de captura normal pesa menos de 1 KB."),
}


@app.errorhandler(404)
def error_404(_error):
    return render_template("error.html", codigo=404, titulo="Página no encontrada",
                           detalle="La dirección solicitada no existe en el sistema."), 404


@app.errorhandler(403)
def error_403(error):
    descripcion = getattr(error, "description", "")
    if descripcion and descripcion != Forbidden.description:
        return render_template("error.html", codigo=403, titulo="Acceso restringido",
                               detalle=descripcion), 403
    return render_template("error.html", codigo=403, titulo="Solicitud rechazada",
                           detalle="La captura no se envió desde una página de Sigma, así que no "
                                   "se guardó. Vuelve al inicio y captura desde el formulario."), 403


@app.errorhandler(ErrorBaseDeDatos)
def error_base_de_datos(error):
    return render_template("error.html", codigo=503, titulo="Base de datos no disponible",
                           detalle=str(error)), 503


def error_http(error):
    """Cualquier otro error HTTP (405, 413, 400…) conserva su código y su explicación."""
    codigo = error.code or 500
    titulo, detalle = MENSAJES_HTTP.get(codigo, (error.name, "La solicitud no se pudo atender."))
    if request.path.startswith("/api/"):
        return jsonify({"error": titulo}), codigo
    return render_template("error.html", codigo=codigo, titulo=titulo, detalle=detalle), codigo


@app.errorhandler(Exception)
def error_no_controlado(error):
    if isinstance(error, ErrorBaseDeDatos):
        return error_base_de_datos(error)
    if isinstance(error, HTTPException):
        if error.code == 404:
            return error_404(error)
        if error.code == 403:
            return error_403(error)
        return error_http(error)
    app.logger.exception("Error no controlado")
    return render_template(
        "error.html", codigo=500, titulo="Ocurrió un error en el servidor",
        detalle=str(error) if app.debug else
        "El movimiento no se guardó. Revisa la consola del servidor para el detalle técnico."), 500
