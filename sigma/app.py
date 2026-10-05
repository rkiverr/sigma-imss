"""
Sistema Sigma — prototipo validado en ambiente relevante (Entrega 5, TRL 5).

Interfaz cliente (aplicación web) + lógica de servidor (validación,
persistencia y exportación) para el sistema de altas y bajas IMSS/IDSE.

Arquitectura cliente-servidor (paquete sigma/):
    templates/ + static/   capa de presentación
    app.py                 controlador HTTP y reglas de flujo
    validaciones.py        validación algorítmica
    plazo.py               plazo legal de cinco días hábiles
    database.py            persistencia relacional (PostgreSQL o SQLite)
    exportar_idse.py       abstracción de datos hacia el formato IDSE
    __main__.py            servidor de desarrollo (python -m sigma)
    ../servidor.py         arranque en modo producción (waitress)
"""
import os
import secrets
from datetime import datetime
from urllib.parse import urlparse

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, send_file, url_for)

from . import exportar_idse, plazo
from .database import (ERRORES_DE_INTEGRIDAD, ErrorBaseDeDatos, conexion,
                       conflicto_de_identidad, descripcion_backend,
                       estadisticas, estado_afiliatorio, init_db,
                       movimiento_duplicado, obtener_o_crear_trabajador,
                       obtener_patron_id, registrar_bitacora)
from .validaciones import (CAUSAS_BAJA, ORDEN_CAMPOS, TIPO_ALTA, TIPO_BAJA,
                           TIPOS_JORNADA, TIPOS_SALARIO, TIPOS_TRABAJADOR,
                           normalizar_datos, validar_campos)

app = Flask(__name__)
# En producción debe fijarse con la variable de entorno; en desarrollo se
# genera una clave efímera para no dejar un secreto fijo en el repositorio.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

MOVIMIENTOS_POR_PAGINA = 25

# Folio más grande que cabe en un INTEGER de PostgreSQL; uno mayor no puede
# existir y, sin esta revisión, hacía fallar la consulta con error 500.
FOLIO_MAXIMO = 2 ** 31 - 1

ETIQUETAS_TIPO = {TIPO_ALTA: "Alta / Reingreso", TIPO_BAJA: "Baja"}

CAMPOS_FORMULARIO = [
    "nombre_completo", "curp", "nss", "rfc", "tipo_movimiento", "fecha_movimiento",
    "tipo_trabajador", "tipo_salario", "tipo_jornada", "sdi", "causa_baja",
]

CATALOGOS = {
    "tipo_trabajador": TIPOS_TRABAJADOR,
    "tipo_salario": TIPOS_SALARIO,
    "tipo_jornada": TIPOS_JORNADA,
    "causa_baja": CAUSAS_BAJA,
}


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


def _usuario_valido(conn, valor):
    """
    Convierte el usuario recibido del formulario a un id existente.
    Devuelve None si el valor es inválido, en lugar de reventar con ValueError.
    """
    try:
        usuario_id = int(valor)
    except (TypeError, ValueError):
        return None
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuario WHERE id = %s", (usuario_id,))
    fila = cur.fetchone()
    cur.close()
    return fila["id"] if fila else None


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
                  m.tipo_trabajador, m.tipo_salario, m.tipo_jornada
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
    cur.execute("SELECT id, nombre, rol FROM usuario ORDER BY id")
    usuarios = [dict(fila) for fila in cur.fetchall()]

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
        "usuarios": usuarios,
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
        "lote_disponible": exportar_idse.ultimo_lote() is not None,
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

    # Un formulario solo se acepta si lo envió una página de Sigma. Los
    # navegadores ponen el sitio de origen en Origin (o en Referer); si otro
    # sitio intenta enviar una captura a nombre del usuario (CSRF), no coincide.
    if request.method == "POST":
        origen = request.headers.get("Origin") or request.headers.get("Referer")
        if origen and urlparse(origen).netloc != request.host:
            abort(403)


@app.context_processor
def variables_de_plantilla():
    return {"csp_nonce": getattr(g, "csp_nonce", "")}


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

    with conexion(commit=True) as conn:
        usuario_id = _usuario_valido(conn, request.form.get("usuario_id"))
        if usuario_id is None:
            errores["usuario_id"] = "Selecciona un usuario válido para atribuir la captura."

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
            if usuario_id is not None:
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
        conn, datos["nombre_completo"], datos["curp"], datos["nss"], datos["rfc"])

    cur = conn.cursor()
    cur.execute(
        """INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento,
               tipo_trabajador, tipo_salario, tipo_jornada, sdi, causa_baja, estado,
               exportado, creado_en)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Válido', FALSE, %s)
           RETURNING id""",
        (trabajador_id, patron_id, datos["tipo_movimiento"], datos["fecha_movimiento"],
         datos["tipo_trabajador"], datos["tipo_salario"], datos["tipo_jornada"],
         datos["sdi"], datos["causa_baja"],
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
def exportar():
    with conexion(commit=True) as conn:
        usuario_id = _usuario_valido(conn, request.form.get("usuario_id"))
        if usuario_id is None:
            flash("Selecciona un usuario válido antes de generar el lote.", "error")
            return redirect(url_for("index"))

        cur = conn.cursor()
        cur.execute(
            """SELECT m.id AS movimiento_id, p.registro_patronal, m.tipo_movimiento,
                      t.curp, t.nss, t.rfc, m.fecha_movimiento, m.tipo_trabajador,
                      m.tipo_salario, m.tipo_jornada, m.sdi, m.causa_baja
               FROM movimiento m
               JOIN trabajador t ON t.id = m.trabajador_id
               JOIN patron p ON p.id = m.patron_id
               WHERE m.estado = 'Válido' AND m.exportado = FALSE
               ORDER BY m.id"""
        )
        registros = [dict(fila) for fila in cur.fetchall()]

        if not registros:
            cur.close()
            flash("No hay movimientos válidos pendientes de exportar.", "error")
            return redirect(url_for("index"))

        ruta = exportar_idse.exportar_lote(registros)

        cur.executemany(
            "UPDATE movimiento SET exportado = TRUE, estado = 'Exportado' WHERE id = %s",
            [(registro["movimiento_id"],) for registro in registros],
        )
        cur.close()
        registrar_bitacora(conn, usuario_id, None, "Exportación de lote IDSE",
                           f"{len(registros)} movimiento(s) en {os.path.basename(ruta)}")

    flash(f"Lote IDSE generado con {len(registros)} movimiento(s): {os.path.basename(ruta)}", "success")
    return redirect(url_for("index"))


@app.route("/descargar-lote")
def descargar_lote():
    ruta = exportar_idse.ultimo_lote()
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
            """SELECT m.id, t.nombre_completo, t.curp, t.nss, t.rfc, p.registro_patronal,
                      p.razon_social, m.tipo_movimiento, m.fecha_movimiento, m.estado,
                      m.tipo_trabajador, m.tipo_salario, m.tipo_jornada, m.sdi,
                      m.causa_baja, m.creado_en
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
@app.errorhandler(404)
def error_404(_error):
    return render_template("error.html", codigo=404, titulo="Página no encontrada",
                           detalle="La dirección solicitada no existe en el sistema."), 404


@app.errorhandler(403)
def error_403(_error):
    return render_template("error.html", codigo=403, titulo="Solicitud rechazada",
                           detalle="La captura no se envió desde una página de Sigma, así que no "
                                   "se guardó. Vuelve al inicio y captura desde el formulario."), 403


@app.errorhandler(ErrorBaseDeDatos)
def error_base_de_datos(error):
    return render_template("error.html", codigo=503, titulo="Base de datos no disponible",
                           detalle=str(error)), 503


@app.errorhandler(Exception)
def error_no_controlado(error):
    if isinstance(error, ErrorBaseDeDatos):
        return error_base_de_datos(error)
    codigo = getattr(error, "code", 500)
    if codigo == 404:
        return error_404(error)
    if codigo == 403:
        return error_403(error)
    app.logger.exception("Error no controlado")
    return render_template(
        "error.html", codigo=500, titulo="Ocurrió un error en el servidor",
        detalle=str(error) if app.debug else
        "El movimiento no se guardó. Revisa la consola del servidor para el detalle técnico."), 500
