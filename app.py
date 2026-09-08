"""
Prototipo de prueba de concepto — Entrega 3.
Interfaz cliente (formulario web) + lógica de servidor (validación,
persistencia y exportación) para el sistema de altas/bajas IMSS/IDSE.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from database import get_conn, init_db, registrar_bitacora, obtener_o_crear_trabajador
from validaciones import validar_movimiento
from exportar_idse import exportar_a_archivo

app = Flask(__name__)
app.secret_key = "prueba-concepto-trl3"


@app.route("/")
def index():
    conn = get_conn()
    movimientos = conn.execute("""
        SELECT m.id, t.nombre_completo, t.curp, m.tipo_movimiento, m.fecha_movimiento, m.estado
        FROM movimiento m JOIN trabajador t ON t.id = m.trabajador_id
        ORDER BY m.id DESC
    """).fetchall()
    usuarios = conn.execute("SELECT id, nombre, rol FROM usuario").fetchall()
    bitacora = conn.execute("""
        SELECT b.timestamp, u.nombre AS usuario, b.accion, b.detalle
        FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
        ORDER BY b.id DESC LIMIT 15
    """).fetchall()
    conn.close()
    return render_template("index.html", movimientos=movimientos, usuarios=usuarios, bitacora=bitacora)


@app.route("/capturar", methods=["POST"])
def capturar():
    datos = {
        "nombre_completo": request.form.get("nombre_completo", "").strip(),
        "curp": request.form.get("curp", "").strip().upper(),
        "nss": request.form.get("nss", "").strip(),
        "rfc": request.form.get("rfc", "").strip().upper(),
        "tipo_movimiento": request.form.get("tipo_movimiento", "").strip(),
        "fecha_movimiento": request.form.get("fecha_movimiento", "").strip(),
        "tipo_trabajador": request.form.get("tipo_trabajador", "").strip(),
        "tipo_salario": request.form.get("tipo_salario", "").strip(),
        "tipo_jornada": request.form.get("tipo_jornada", "").strip(),
        "sdi": request.form.get("sdi", "").strip(),
        "causa_baja": request.form.get("causa_baja", "").strip(),
    }
    usuario_id = int(request.form.get("usuario_id"))

    es_valido, errores = validar_movimiento(datos)

    conn = get_conn()
    if not es_valido:
        registrar_bitacora(conn, usuario_id, None, "Intento de captura rechazado", "; ".join(errores))
        conn.commit()
        conn.close()
        flash("Movimiento RECHAZADO: " + " | ".join(errores), "error")
        return redirect(url_for("index"))

    patron_id = conn.execute("SELECT id FROM patron LIMIT 1").fetchone()["id"]
    trabajador_id = obtener_o_crear_trabajador(conn, datos["nombre_completo"], datos["curp"], datos["nss"], datos["rfc"])

    cur = conn.execute("""
        INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento,
            tipo_trabajador, tipo_salario, tipo_jornada, sdi, causa_baja, estado, exportado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Válido', 0)
    """, (trabajador_id, patron_id, datos["tipo_movimiento"], datos["fecha_movimiento"],
          datos["tipo_trabajador"], datos["tipo_salario"], datos["tipo_jornada"],
          datos["sdi"], datos["causa_baja"]))
    movimiento_id = cur.lastrowid

    registrar_bitacora(conn, usuario_id, movimiento_id, "Movimiento capturado", f"Tipo {datos['tipo_movimiento']} - CURP {datos['curp']}")
    conn.commit()
    conn.close()
    flash("Movimiento capturado y validado correctamente.", "success")
    return redirect(url_for("index"))


@app.route("/exportar", methods=["POST"])
def exportar():
    usuario_id = int(request.form.get("usuario_id"))
    conn = get_conn()
    rows = conn.execute("""
        SELECT m.id AS movimiento_id, p.registro_patronal, m.tipo_movimiento, t.curp, t.nss, t.rfc,
               m.fecha_movimiento, m.tipo_trabajador, m.tipo_salario, m.tipo_jornada, m.sdi, m.causa_baja
        FROM movimiento m
        JOIN trabajador t ON t.id = m.trabajador_id
        JOIN patron p ON p.id = m.patron_id
        WHERE m.estado = 'Válido' AND m.exportado = 0
    """).fetchall()
    registros = [dict(r) for r in rows]

    if not registros:
        flash("No hay movimientos válidos pendientes de exportar.", "error")
        conn.close()
        return redirect(url_for("index"))

    ruta = exportar_a_archivo(registros, "lote_idse.txt")

    ids = [r["movimiento_id"] for r in registros]
    conn.executemany("UPDATE movimiento SET exportado = 1, estado = 'Exportado' WHERE id = ?", [(i,) for i in ids])
    registrar_bitacora(conn, usuario_id, None, "Exportación de lote IDSE", f"{len(registros)} movimiento(s) exportado(s)")
    conn.commit()
    conn.close()
    flash(f"Lote IDSE generado con {len(registros)} movimiento(s): {ruta}", "success")
    return redirect(url_for("index"))


@app.route("/descargar-lote")
def descargar_lote():
    return send_file("lote_idse.txt", as_attachment=True)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5050)
