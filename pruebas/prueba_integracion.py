"""
Arnés de pruebas del Entregable 6 (TRL 6): integración y demostración del sistema.

El arnés del Entregable 5 (prueba_ambiente_relevante.py) somete al sistema a las
condiciones de la empresa. Este arnés demuestra el SISTEMA COMPLETO integrado:
el servidor de producción corre como proceso independiente sobre una copia
aislada, y un "equipo de captura" entra por la IP de la red local, inicia
sesión y recorre el ciclo de una semana de operación.

Bloques:
  F - Escenario funcional: inicio de sesión, captura, rechazo y corrección,
      historial, plazo, roles, exportación por tipo, descarga y bitácora.
  L - Conformidad del lote con la estructura oficial del IMSS (168 posiciones,
      un archivo por tipo, cada campo en su posición).
  S - Seguridad: autenticación, bloqueo, roles, cookie, métodos HTTP, rutas,
      tamaño de petición y tráfico en la red.
  R - Respaldo y restauración: pérdida simulada de la base y recuperación.
  C - Comunicación entre equipos: tamaño y tiempo de cada enlace, por la IP de
      la red local y por el propio equipo.

Uso (desde la raíz del repositorio; los reportes quedan en pruebas/resultados/):
    python pruebas/prueba_integracion.py
    python pruebas/prueba_integracion.py --bloques F,L --capturas   (guarda el HTML de las pantallas)
"""
import argparse
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.parse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prueba_ambiente_relevante as par  # noqa: E402  (Servidor, Cliente y plantilla sintética)

RAIZ = par.RAIZ
SALIDA = os.path.join(RAIZ, "pruebas", "resultados")
CAPTURAS = os.path.join(SALIDA, "integracion")
RESULTADOS = {}
REPORTE = []
GUARDAR_HTML = False
ADMIN, CAPTURA = "1", "2"


def log(linea=""):
    print(linea, flush=True)
    REPORTE.append(linea)


def entorno_de(srv):
    """Variables con las que corre la copia aislada (para usar la consola de Sigma sobre ella)."""
    return dict(os.environ, SIGMA_DB="sqlite", SQLITE_PATH=srv.base, PYTHONIOENCODING="utf-8")


def consola(srv, *argumentos):
    return subprocess.run([sys.executable, "-m", *argumentos], cwd=srv.dir, env=entorno_de(srv),
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


def guardar_html(srv, nombre, texto):
    """HTML de una pantalla, listo para fotografiarlo con un navegador sin cabeza."""
    if not GUARDAR_HTML:
        return
    os.makedirs(CAPTURAS, exist_ok=True)
    base = f'<base href="http://{par.ip_lan()}:{srv.puerto}/">'
    texto = texto.replace("<head>", "<head>" + base, 1)
    texto = re.sub(r"<html([^>]*)>", r'<html\1 data-tema="claro">', texto, count=1)
    with open(os.path.join(CAPTURAS, nombre), "w", encoding="utf-8") as f:
        f.write(texto)


def con_sesion(cliente, r):
    """Página que sigue a una redirección, con la cookie que dejó la respuesta."""
    return cliente.pedir("GET", r.ubicacion or "/", cabeceras={"Cookie": par._galleta(r) or ""})


# ==========================================================================
# Bloque F — Escenario funcional por la red local
# ==========================================================================
def bloque_f(modo):
    log("=" * 78)
    log("BLOQUE F — ESCENARIO FUNCIONAL (una semana de operación por la red local)")
    log("=" * 78)
    casos = []
    ip = par.ip_lan()
    plantilla = par.Plantilla(20261007)

    def caso(clave, descripcion, requisito, esperado, obtenido, ok, ms, **extra):
        casos.append({"clave": clave, "descripcion": descripcion, "requisito": requisito,
                      "esperado": esperado, "obtenido": obtenido, "ok": bool(ok), "ms": round(ms, 1), **extra})
        log(f"  {clave} {'OK   ' if ok else 'FALLA'} {ms:7.1f} ms  {descripcion} -> {obtenido}")

    with par.Servidor(modo) as srv:
        anonimo = par.Cliente(srv.puerto, host=ip, sesion=False)
        cli = par.Cliente(srv.puerto, host=ip, usuario_id=CAPTURA, sesion=False)
        cli.sesion = False
        d2, d1, d0 = par.dia_habil_atras(2), par.dia_habil_atras(1), par.dia_habil_atras(0)
        t1, t2, t3, t4, t5, t6, t7 = (plantilla.trabajador() for _ in range(7))

        r = anonimo.pedir("GET", "/")
        caso("PF-01", "Abrir Sigma desde una PC de captura sin haber iniciado sesión", "OE3",
             "Redirige al inicio de sesión", f"HTTP {r.estado} → {r.ubicacion}",
             r.estado == 302 and (r.ubicacion or "").endswith("/login"), r.segundos * 1000)
        pagina_login = anonimo.pedir("GET", "/login")
        guardar_html(srv, "snap_login.html", pagina_login.texto)

        malo = urllib.parse.urlencode({"usuario": "captura.obra1", "contrasena": "equivocada"}).encode()
        r = cli.pedir("POST", "/login", malo, {"Content-Type": "application/x-www-form-urlencoded",
                                                "Origin": cli.origen})
        caso("PF-02", "Iniciar sesión con una contraseña equivocada", "OE3",
             "401 con mensaje genérico", f"HTTP {r.estado} · {'genérico' if 'incorrectos' in r.texto else '?'}",
             r.estado == 401 and "Usuario o contraseña incorrectos" in r.texto, r.segundos * 1000)

        cli.sesion = True
        r = cli.iniciar_sesion(CAPTURA)
        caso("PF-03", "Iniciar sesión como capturista (captura.obra1)", "OE3", "302 a la pantalla principal",
             f"HTTP {r.estado} → {r.ubicacion}", r.estado == 302, r.segundos * 1000)

        malo = par.alta(t1, d2, CAPTURA)
        malo["rfc"] = "XAXX010101AB1"
        r = cli.validar(malo)
        j = r.json()
        caso("PF-04", "Validación en vivo de un RFC que no corresponde a la CURP", "OE1",
             "JSON con error en el campo rfc", f"HTTP {r.estado} · errores={sorted(j.get('errores', {}))}",
             r.estado == 200 and "rfc" in j.get("errores", {}), r.segundos * 1000)

        r = cli.formulario("/capturar", par.alta(t1, d2, CAPTURA))
        pag = con_sesion(cli, r)
        cat, msg = par.leer_notificacion(pag.texto)
        caso("PF-05", "Alta válida con nombre separado y UMF", "R1, OE4",
             "Guardada; mensaje con la fecha límite del plazo", f"HTTP {r.estado} · {cat}: {msg[:70]}…",
             r.estado == 302 and cat == "success" and "a más tardar" in msg, r.segundos * 1000)
        guardar_html(srv, "snap_exito.html", pag.texto)

        datos = par.alta(t2, d1, CAPTURA)
        datos["nss"] = datos["nss"][:10]
        datos["rfc"] = datos["rfc"][:4] + "991231" + datos["rfc"][10:]
        r = cli.formulario("/capturar", datos)
        errores = par.leer_errores(r.texto)
        conserva = t2["curp"] in r.texto and t2["apellido_paterno"] in r.texto
        caso("PF-06", "Alta con NSS incompleto y RFC incoherente", "OE1",
             "422 con un mensaje por campo; los datos no se borran",
             f"HTTP {r.estado} · {len(errores)} errores · conserva datos={conserva}",
             r.estado == 422 and len(errores) == 2 and conserva, r.segundos * 1000, errores=errores)
        guardar_html(srv, "snap_rechazo.html", r.texto)

        r = cli.formulario("/capturar", par.alta(t2, d1, CAPTURA))
        caso("PF-07", "El capturista corrige y reenvía el mismo movimiento", "OE1", "Guardado al segundo intento",
             f"HTTP {r.estado}", r.estado == 302, r.segundos * 1000)

        r = cli.formulario("/capturar", par.alta(t1, d0, CAPTURA))
        errores = par.leer_errores(r.texto)
        caso("PF-08", "Segunda alta de un trabajador que sigue vigente", "R1", "422: ya tiene un alta vigente",
             f"HTTP {r.estado}", r.estado == 422 and any("alta vigente" in e for e in errores), r.segundos * 1000)

        r = cli.formulario("/capturar", par.baja(t1, d1, "1", CAPTURA))
        caso("PF-09", "Baja por término de contrato", "R1", "Guardada", f"HTTP {r.estado}",
             r.estado == 302, r.segundos * 1000)

        r = cli.formulario("/capturar", par.baja(t1, d0, "2", CAPTURA))
        errores = par.leer_errores(r.texto)
        caso("PF-10", "Baja de un trabajador ya dado de baja", "R1", "422: no tiene alta vigente",
             f"HTTP {r.estado}", r.estado == 422 and any("dado de baja" in e for e in errores), r.segundos * 1000)

        r = cli.formulario("/capturar", par.alta(t1, d0, CAPTURA))
        caso("PF-11", "Reingreso del mismo trabajador a otra obra", "R1", "Guardado como alta 08",
             f"HTTP {r.estado}", r.estado == 302, r.segundos * 1000)

        r = cli.formulario("/capturar", par.alta(t3, par.dia_habil_atras(9), CAPTURA))
        pag = con_sesion(cli, r)
        cat, msg = par.leer_notificacion(pag.texto)
        caso("PF-12", "Alta con 9 días hábiles de retraso", "OE4", "Guardada con aviso de plazo vencido",
             f"HTTP {r.estado} · {cat}", r.estado == 302 and cat == "warning" and "venció" in msg, r.segundos * 1000)
        guardar_html(srv, "snap_aviso.html", pag.texto)

        datos = dict(par.alta(t4, d1, CAPTURA), sdi="31.50")
        r = cli.formulario("/capturar", datos)
        errores = par.leer_errores(r.texto)
        caso("PF-13", "Alta con salario de 31.50 (punto corrido)", "OE1", "422: menor al salario mínimo",
             f"HTTP {r.estado}", r.estado == 422 and any("mínimo" in e for e in errores), r.segundos * 1000)

        datos = {k: v for k, v in par.alta(t4, d1, CAPTURA).items() if k != "umf"}
        r = cli.formulario("/capturar", datos)
        errores = par.leer_errores(r.texto)
        caso("PF-14", "Alta sin unidad de medicina familiar", "OE2", "422: la UMF es obligatoria en un alta",
             f"HTTP {r.estado}", r.estado == 422 and any("medicina familiar" in e for e in errores),
             r.segundos * 1000)

        invertido = dict(par.alta(t5, d1, CAPTURA), apellido_paterno=t5["apellido_materno"],
                         apellido_materno=t5["apellido_paterno"])
        j = cli.validar(invertido).json()
        aviso = j.get("avisos", {}).get("curp", "")
        caso("PF-15", "Apellidos capturados al revés", "OE1", "Aviso: las iniciales de la CURP no corresponden",
             f"válido={j.get('valido')} · aviso={'sí' if 'iniciales' in aviso else 'no'}",
             j.get("valido") and "iniciales" in aviso, 0.0)

        for t in (t4, t5, t6, t7):
            cli.formulario("/capturar", par.alta(t, d1, CAPTURA))

        r = cli.formulario("/exportar", {})
        caso("PF-16", "La capturista intenta generar el lote", "OE3", "403: solo administración",
             f"HTTP {r.estado}", r.estado == 403, r.segundos * 1000)

        cli.pedir("POST", "/logout", b"", {"Origin": cli.origen,
                                           "Content-Type": "application/x-www-form-urlencoded"})
        cli._usuario_en_sesion = None
        cli.cookie = None
        cli.iniciar_sesion(ADMIN)
        guardar_html(srv, "snap_tablero_previo.html", cli.pedir("GET", "/").texto)
        r = cli.formulario("/exportar", {"usuario_id": ADMIN})
        pag = con_sesion(cli, r)
        cat, msg = par.leer_notificacion(pag.texto)
        archivos = re.findall(r"(lote_idse_(?:altas|bajas)_\d+_\d+\.txt)", msg)
        n_lote = int(re.search(r"con (\d+) movimiento", msg).group(1)) if "movimiento" in msg else 0
        caso("PF-17", "Administración genera el lote con los pendientes", "OE2",
             "Un archivo de altas y otro de bajas", f"HTTP {r.estado} · {n_lote} movimientos · {len(archivos)} archivos",
             r.estado == 302 and cat == "success" and len(archivos) == 2, r.segundos * 1000,
             n_lote=n_lote, archivos=archivos)
        guardar_html(srv, "snap_exportado.html", pag.texto)

        lotes = {}
        for tipo in ("altas", "bajas"):
            r = cli.pedir("GET", f"/descargar-lote?tipo={tipo}")
            lotes[tipo] = r.cuerpo
        tamanos = {tipo: sorted({len(x) for x in contenido.split(b"\r\n")[:-1]}) for tipo, contenido in lotes.items()}
        registros = sum(len(c.split(b"\r\n")) - 1 for c in lotes.values())
        caso("PF-18", "Descargar los dos archivos desde la PC de captura", "OE2",
             "Registros de 168 posiciones, uno por movimiento",
             f"{registros} registros · longitudes {tamanos}",
             registros == n_lote and all(t == [168] for t in tamanos.values()), r.segundos * 1000)
        os.makedirs(CAPTURAS, exist_ok=True)
        for tipo, contenido in lotes.items():
            with open(os.path.join(CAPTURAS, f"lote_{tipo}.txt"), "wb") as f:
                f.write(contenido)

        r = cli.pedir("GET", "/?q=" + t2["nss"])
        r2 = cli.pedir("GET", "/?estado=Exportado")
        caso("PF-19", "Buscar por NSS y filtrar por estado Exportado", "R1", "Encuentra al trabajador",
             f"encontrado={t2['curp'] in r.texto} · filas Exportado={r2.texto.count('>Exportado<')}",
             t2["curp"] in r.texto and r2.estado == 200, (r.segundos + r2.segundos) * 1000)

        folio = int(re.findall(r'data-movimiento="(\d+)"', r2.texto)[-1])
        r = cli.pedir("GET", f"/api/movimiento/{folio}")
        historial = r.json().get("historial", [])
        acciones = [h["accion"] for h in historial]
        caso("PF-20", "Detalle de un movimiento exportado con su historial", "R3",
             "Captura y exportación, con usuario y hora", f"{acciones}",
             "Movimiento capturado" in acciones and "Incluido en lote IDSE" in acciones, r.segundos * 1000,
             historial=historial)

        r = cli.formulario("/exportar", {"usuario_id": ADMIN})
        cat, msg = par.leer_notificacion(con_sesion(cli, r).texto)
        caso("PF-21", "Generar un lote cuando no hay pendientes", "OE2", "Mensaje claro, sin lote vacío",
             f"{cat}: {msg}", cat == "error" and "No hay" in msg, r.segundos * 1000)

        conexion = srv.bd()
        filas = conexion.execute("""SELECT u.nombre, b.accion, COUNT(*) FROM bitacora b
                                    JOIN usuario u ON u.id = b.usuario_id GROUP BY 1, 2 ORDER BY 1, 2""").fetchall()
        sin_usuario = conexion.execute("SELECT COUNT(*) FROM bitacora WHERE usuario_id IS NULL").fetchone()[0]
        atribucion = conexion.execute(
            """SELECT u.nombre FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
               WHERE b.accion = 'Movimiento capturado' GROUP BY 1""").fetchall()
        conexion.close()
        caso("PF-22", "Bitácora en la base: autoría comprobada por la sesión", "R3, OE3",
             "Cada captura a nombre de quien inició sesión", f"capturó: {[a[0] for a in atribucion]} · sin usuario={sin_usuario}",
             sin_usuario == 0 and [a[0] for a in atribucion] == ["captura.obra1"], 0.0,
             bitacora=[list(f) for f in filas])

        vieja = cli.cookie
        r = cli.pedir("POST", "/logout", b"", {"Origin": cli.origen, "Content-Type": "application/x-www-form-urlencoded"})
        # Se reutiliza la cookie que tenía la sesión: ya no debe servir.
        r2 = par.Cliente(srv.puerto, host=ip, sesion=False).pedir("GET", "/", cabeceras={"Cookie": vieja})
        caso("PF-23", "Cerrar sesión y volver con la cookie anterior", "OE3",
             "La cookie anterior ya no sirve", f"HTTP {r.estado} → {r.ubicacion} · con la cookie anterior: "
             f"HTTP {r2.estado} → {r2.ubicacion}", r.estado == 302 and r2.estado == 302, r.segundos * 1000)
        excepciones = srv.excepciones()

    correctos = sum(c["ok"] for c in casos)
    log(f"  {correctos} de {len(casos)} casos correctos · excepciones en el servidor: {excepciones}")
    log("")
    RESULTADOS["F"] = {"casos": casos, "correctos": correctos, "total": len(casos), "excepciones_servidor": excepciones}


# ==========================================================================
# Bloque L — Conformidad del lote con la estructura oficial del IMSS
# ==========================================================================
def _campo(linea, inicio, longitud):
    return linea[inicio - 1:inicio - 1 + longitud]


def bloque_l(modo):
    log("=" * 78)
    log("BLOQUE L — CONFORMIDAD DEL LOTE CON LA ESTRUCTURA OFICIAL DEL IMSS")
    log("=" * 78)
    sys.path.insert(0, par.CODIGO)
    from sigma.exportar_idse import ESTRUCTURA  # noqa: E402
    from sigma.validaciones import limites_sbc  # noqa: E402
    plantilla = par.Plantilla(77)
    with par.Servidor(modo) as srv:
        cli = par.Cliente(srv.puerto, usuario_id=CAPTURA)
        enviados = {}
        for i in range(30):
            t = plantilla.trabajador()
            r = cli.formulario("/capturar", par.alta(t, par.dia_habil_atras(2), CAPTURA))
            if r.estado == 302:
                enviados[t["curp"]] = t
        for t in list(enviados.values())[:12]:
            cli.formulario("/capturar", par.baja(t, par.dia_habil_atras(1), "2", CAPTURA))
        antes = len(srv.lotes())
        cli.formulario("/exportar", {"usuario_id": ADMIN})
        lotes = []
        for ruta in srv.lotes()[antes:]:          # se leen antes de que se borre la copia aislada
            with open(ruta, "rb") as f:
                lotes.append((ruta, f.read()))
        conexion = srv.bd()
        filas = {(f["curp"], f["tipo_movimiento"]): dict(f) for f in conexion.execute(
            """SELECT t.curp, t.nss, t.id AS trabajador_id, m.tipo_movimiento, m.fecha_movimiento, m.sdi,
                      m.tipo_jornada, m.umf, m.causa_baja FROM movimiento m
               JOIN trabajador t ON t.id = m.trabajador_id""")}
        conexion.close()
    revisiones = {"registros": 0, "longitud_168": 0, "identificador_9": 0, "tipo_correcto": 0,
                  "nss": 0, "fecha": 0, "salario": 0, "jornada_oficial": 0, "umf": 0, "curp": 0,
                  "causa": 0, "crlf": 0, "cp1252": 0, "archivos": len(lotes)}
    por_archivo = []
    for ruta, crudo in lotes:
        tipo_archivo = "08" if "_altas_" in ruta else "02"
        revisiones["crlf"] += int(crudo.endswith(b"\r\n") and b"\n" not in crudo.replace(b"\r\n", b""))
        try:
            texto = crudo.decode("cp1252")
            revisiones["cp1252"] += 1
        except UnicodeDecodeError:
            texto = crudo.decode("latin-1")
        lineas = texto.split("\r\n")[:-1]
        por_archivo.append({"archivo": os.path.basename(ruta), "tipo": tipo_archivo, "registros": len(lineas)})
        for linea in lineas:
            revisiones["registros"] += 1
            revisiones["longitud_168"] += int(len(linea) == 168)
            revisiones["identificador_9"] += int(linea[167:168] == "9")
            tipo = _campo(linea, 132, 2)
            revisiones["tipo_correcto"] += int(tipo == tipo_archivo)
            curp = _campo(linea, 150, 18) if tipo == "08" else None
            nss = _campo(linea, 12, 10) + _campo(linea, 22, 1)
            fila = next((f for (c, tm), f in filas.items() if f["nss"] == nss and tm == tipo), None)
            if fila is None:
                continue
            revisiones["nss"] += 1
            revisiones["fecha"] += int(_campo(linea, 119, 8) == fila["fecha_movimiento"])
            if tipo == "08":
                tope = limites_sbc(fila["fecha_movimiento"])[1]
                esperado = f"{round(min(float(fila['sdi']), tope) * 100):06d}"
                revisiones["salario"] += int(_campo(linea, 104, 6) == esperado)
                revisiones["jornada_oficial"] += int(_campo(linea, 118, 1) == fila["tipo_jornada"] == "0")
                revisiones["umf"] += int(_campo(linea, 127, 3) == fila["umf"])
                revisiones["curp"] += int(curp == fila["curp"])
            else:
                revisiones["causa"] += int(_campo(linea, 149, 1) == fila["causa_baja"]
                                           and _campo(linea, 150, 18) == " " * 18
                                           and _campo(linea, 104, 15) == "0" * 15)
    altas = sum(1 for a in por_archivo if a["tipo"] == "08" for _ in range(a["registros"]))
    bajas = revisiones["registros"] - altas
    conforme = (revisiones["archivos"] == 2 and revisiones["registros"] > 0
                and all(revisiones[k] == revisiones["registros"] for k in
                        ("longitud_168", "identificador_9", "tipo_correcto", "nss", "fecha"))
                and revisiones["salario"] == revisiones["jornada_oficial"] == revisiones["umf"]
                == revisiones["curp"] == altas and revisiones["causa"] == bajas
                and revisiones["crlf"] == revisiones["cp1252"] == 2)
    log(f"  Archivos: {por_archivo}")
    log(f"  Revisiones campo por campo: {revisiones}")
    log(f"  Estructura oficial: {'CUMPLE' if conforme else 'NO CUMPLE'} ({altas} altas y {bajas} bajas)")
    log(f"  Campos por estructura: altas {len(ESTRUCTURA['08'])}, bajas {len(ESTRUCTURA['02'])}")
    log("")
    RESULTADOS["L"] = {"archivos": por_archivo, "revisiones": revisiones, "altas": altas, "bajas": bajas,
                       "conforme": conforme}


# ==========================================================================
# Bloque S — Seguridad
# ==========================================================================
def bloque_s(modo):
    log("=" * 78)
    log("BLOQUE S — SEGURIDAD DE LA VERSIÓN INTEGRADA")
    log("=" * 78)
    pruebas = []
    ip = par.ip_lan()
    plantilla = par.Plantilla(78)

    def seg(clave, prueba, resultado, seguro, nota=""):
        pruebas.append({"clave": clave, "prueba": prueba, "resultado": resultado, "seguro": bool(seguro),
                        "nota": nota})
        log(f"  [{'OK' if seguro else 'HALLAZGO'}] {clave} {prueba}: {resultado}")

    with par.Servidor(modo) as srv:
        consola(srv, "sigma.usuarios", "crear", "captura.bloqueo", "captura", "--contrasena", "bloqueo-sigma-26")
        anon = par.Cliente(srv.puerto, host=ip, sesion=False)
        r = anon.pedir("GET", "/")
        seg("S-01", "Abrir el sistema desde la red sin credenciales", f"HTTP {r.estado} → {r.ubicacion}",
            r.estado == 302 and (r.ubicacion or "").endswith("/login"))

        # La capturista manda el formulario con usuario_id=1 (admin), como lo haría alguien que
        # edita el HTML. Se envía con pedir() para que el arnés no cambie de sesión.
        cap2 = par.Cliente(srv.puerto, host=ip, usuario_id=CAPTURA)
        cap2.asegurar_sesion(CAPTURA)
        t = plantilla.trabajador()
        cuerpo = urllib.parse.urlencode(dict(par.alta(t, par.dia_habil_atras(1), CAPTURA), usuario_id=ADMIN)).encode()
        r = cap2.pedir("POST", "/capturar", cuerpo, {"Content-Type": "application/x-www-form-urlencoded",
                                                     "Origin": cap2.origen})
        conexion = srv.bd()
        autor = conexion.execute("""SELECT u.nombre FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
                                    JOIN movimiento m ON m.id = b.movimiento_id JOIN trabajador w ON w.id = m.trabajador_id
                                    WHERE w.curp = ? AND b.accion = 'Movimiento capturado'""", (t["curp"],)).fetchone()
        conexion.close()
        seg("S-02", "Capturar con usuario_id=1 (admin) estando en sesión como capturista",
            f"HTTP {r.estado} · la bitácora registra a {autor[0] if autor else '?'}",
            autor is not None and autor[0] == "captura.obra1",
            "El usuario sale de la sesión; el campo del formulario se ignora.")

        # S-03 tráfico en claro: relevo TCP entre la PC de captura y el servidor
        capturado = []

        def relevo(puerto_escucha, listo):
            srv_sock = socket.socket()
            srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv_sock.bind(("127.0.0.1", puerto_escucha))
            srv_sock.listen(1)
            listo.set()
            c, _ = srv_sock.accept()
            d = socket.create_connection((ip, srv.puerto))
            c.settimeout(2)
            datos_c = b""
            try:
                while True:
                    trozo = c.recv(65536)
                    if not trozo:
                        break
                    datos_c += trozo
                    if b"\r\n\r\n" in datos_c:
                        cab, _, cuerpo_r = datos_c.partition(b"\r\n\r\n")
                        lon = re.search(rb"Content-Length: (\d+)", cab)
                        if lon and len(cuerpo_r) >= int(lon.group(1)):
                            break
            except socket.timeout:
                pass
            capturado.append(datos_c)
            d.sendall(datos_c)
            d.settimeout(5)
            try:
                c.sendall(d.recv(65536))
            except OSError:
                pass
            c.close()
            d.close()
            srv_sock.close()

        puerto_relevo = par._puerto_libre()
        listo = threading.Event()
        hilo = threading.Thread(target=relevo, args=(puerto_relevo, listo), daemon=True)
        hilo.start()
        listo.wait(5)
        t = plantilla.trabajador()
        datos = par.alta(t, par.dia_habil_atras(1))
        cuerpo = urllib.parse.urlencode(datos).encode()
        s = socket.create_connection(("127.0.0.1", puerto_relevo))
        s.sendall((f"POST /capturar HTTP/1.1\r\nHost: {ip}:{srv.puerto}\r\nContent-Type: "
                   f"application/x-www-form-urlencoded\r\nOrigin: http://{ip}:{srv.puerto}\r\nCookie: "
                   f"{cap2.cookie}\r\nContent-Length: {len(cuerpo)}\r\n\r\n").encode() + cuerpo)
        time.sleep(1.0)
        s.close()
        hilo.join(timeout=5)
        visto = capturado[0].decode("utf-8", "replace") if capturado else ""
        visibles = [c for c in ("curp", "nss", "rfc", "sdi") if datos[c] in urllib.parse.unquote_plus(visto)]
        if GUARDAR_HTML:
            os.makedirs(CAPTURAS, exist_ok=True)
            with open(os.path.join(CAPTURAS, "trafico_en_claro.txt"), "w", encoding="utf-8", newline="") as f:
                f.write(visto.replace(cap2.cookie or "§", "session=<cookie de sesión>"))
        seg("S-03", "Leer una captura en tránsito por la red", f"visibles en texto plano: {', '.join(visibles)}",
            not visibles, "Sin HTTPS: la sesión y los datos viajan legibles (pendiente).")

        login = cap2.pedir("POST", "/login", urllib.parse.urlencode(
            {"usuario": "captura.obra1", "contrasena": par.CONTRASENA_PRUEBA}).encode(),
            {"Content-Type": "application/x-www-form-urlencoded", "Origin": cap2.origen})
        galleta = (login.cookie or "").lower()
        banderas = {"HttpOnly": "httponly" in galleta, "SameSite=Lax": "samesite=lax" in galleta,
                    "Secure": "secure" in galleta}
        seg("S-04", "Banderas de la cookie de sesión",
            ", ".join(f"{k}={'sí' if v else 'no'}" for k, v in banderas.items()),
            banderas["HttpOnly"] and banderas["SameSite=Lax"], "Secure requiere HTTPS.")

        estados = {m: cap2.pedir(m, "/").estado for m in ("TRACE", "PUT", "DELETE")}
        estados["GET /capturar"] = cap2.pedir("GET", "/capturar").estado
        seg("S-05", "Métodos no permitidos (TRACE, PUT, DELETE y GET /capturar)", str(estados),
            all(v == 405 for v in estados.values()))

        rutas = ["/static/../../sigma_imss.db", "/static/..%2f..%2fsigma_imss.db", "/sigma_imss.db",
                 "/static/%2e%2e/app.py"]
        salidas = {ruta: cap2.pedir("GET", ruta) for ruta in rutas}
        seg("S-06", "Rutas con ../ hacia la base y el código", str({k: v.estado for k, v in salidas.items()}),
            all(v.estado == 404 and "SQLite format" not in v.texto and "def " not in v.texto
                for v in salidas.values()))

        r = cap2.pedir("GET", "/no-existe")
        seg("S-07", "Página de error sin detalle técnico",
            f"HTTP {r.estado} · server={r.cabeceras.get('server')} · CSP={'content-security-policy' in r.cabeceras}",
            r.estado == 404 and "Traceback" not in r.texto and "Werkzeug" not in r.texto)

        t = plantilla.trabajador()
        r = anon.pedir("POST", "/capturar", urllib.parse.urlencode(par.alta(t, par.dia_habil_atras(1))).encode(),
                       {"Content-Type": "application/x-www-form-urlencoded"})
        conexion = srv.bd()
        guardado = conexion.execute("SELECT COUNT(*) FROM trabajador WHERE curp = ?", (t["curp"],)).fetchone()[0]
        conexion.close()
        seg("S-08", "Captura de un programa sin sesión ni cabeceras Origin/Referer",
            f"HTTP {r.estado} → {r.ubicacion} · guardado={bool(guardado)}", r.estado == 302 and not guardado)

        grande = urllib.parse.urlencode({"nombres": "A" * 8_000_000}).encode()
        inicio = time.perf_counter()
        r = cap2.pedir("POST", "/capturar", grande, {"Content-Type": "application/x-www-form-urlencoded",
                                                     "Origin": cap2.origen})
        seg("S-09", "Formulario de 8 MB", f"HTTP {r.estado} en {round((time.perf_counter() - inicio) * 1000)} ms",
            r.estado == 413)

        abierto = True
        try:
            socket.create_connection((ip, 5432), timeout=1).close()
        except OSError:
            abierto = False
        seg("S-10", "Puerto de PostgreSQL (5432) y archivo de la base desde la red",
            f"5432 abierto={abierto} · /sigma_imss.db HTTP {salidas['/sigma_imss.db'].estado}",
            not abierto and salidas["/sigma_imss.db"].estado == 404)

        intentos = par.Cliente(srv.puerto, host=ip, sesion=False)
        mal = urllib.parse.urlencode({"usuario": "captura.bloqueo", "contrasena": "equivocada"}).encode()
        estados = [intentos.pedir("POST", "/login", mal, {"Content-Type": "application/x-www-form-urlencoded",
                                                         "Origin": intentos.origen}).estado for _ in range(5)]
        bien = urllib.parse.urlencode({"usuario": "captura.bloqueo", "contrasena": "bloqueo-sigma-26"}).encode()
        r = intentos.pedir("POST", "/login", bien, {"Content-Type": "application/x-www-form-urlencoded",
                                                    "Origin": intentos.origen})
        seg("S-11", "Cinco contraseñas equivocadas y luego la correcta",
            f"{estados} → con la correcta: HTTP {r.estado} ({'bloqueada' if 'bloquead' in r.texto else '?'})",
            r.estado == 401 and "bloquead" in r.texto)

        otra = par.Cliente(srv.puerto, host=ip, usuario_id=CAPTURA)
        otra.asegurar_sesion(CAPTURA)
        copia = otra.cookie
        otra.pedir("POST", "/logout", b"", {"Origin": otra.origen,
                                            "Content-Type": "application/x-www-form-urlencoded"})
        r = par.Cliente(srv.puerto, host=ip, sesion=False).pedir("GET", "/", cabeceras={"Cookie": copia})
        seg("S-13", "Reutilizar una cookie copiada después de cerrar sesión", f"HTTP {r.estado} → {r.ubicacion}",
            r.estado == 302 and (r.ubicacion or "").endswith("/login"),
            "El token de la sesión se borra de la base al salir.")
        cap2 = par.Cliente(srv.puerto, host=ip, usuario_id=CAPTURA)
        exp = cap2.formulario("/exportar", {})
        des = cap2.pedir("GET", "/descargar-lote?tipo=altas")
        seg("S-12", "La capturista intenta generar y descargar lotes", f"exportar HTTP {exp.estado} · descargar HTTP {des.estado}",
            exp.estado == 403 and des.estado == 403)
        excepciones = srv.excepciones()

    hallazgos = [p["clave"] for p in pruebas if not p["seguro"]]
    log(f"  Hallazgos: {len(hallazgos)} de {len(pruebas)} {hallazgos} · excepciones en el servidor: {excepciones}")
    log("")
    RESULTADOS["S"] = {"pruebas": pruebas, "hallazgos": hallazgos, "excepciones_servidor": excepciones}


# ==========================================================================
# Bloque R — Respaldo y restauración
# ==========================================================================
def bloque_r(modo):
    log("=" * 78)
    log("BLOQUE R — RESPALDO Y RESTAURACIÓN ANTE LA PÉRDIDA DE LA BASE")
    log("=" * 78)
    plantilla = par.Plantilla(79)
    srv = par.Servidor(modo)
    try:
        srv.iniciar()
        cli = par.Cliente(srv.puerto, usuario_id=CAPTURA)
        for _ in range(40):
            cli.formulario("/capturar", par.alta(plantilla.trabajador(), par.dia_habil_atras(1), CAPTURA))
        conexion = srv.bd()
        antes = {tabla: conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
                 for tabla in ("trabajador", "movimiento", "bitacora")}
        conexion.close()
        carpeta = os.path.join(srv.dir, "respaldos")
        al_arrancar = len(os.listdir(carpeta)) if os.path.isdir(carpeta) else 0
        inicio = time.perf_counter()
        hecho = consola(srv, "sigma.respaldo")
        segundos_respaldo = time.perf_counter() - inicio
        respaldo = re.search(r"Respaldo guardado en (.+)", hecho.stdout)
        ruta = respaldo.group(1).strip() if respaldo else ""
        integro = bool(ruta) and sqlite3.connect(f"file:{ruta}?mode=ro", uri=True).execute(
            "PRAGMA integrity_check").fetchone()[0] == "ok"
        # Después del respaldo se captura algo más: eso es lo que se perdería (punto de recuperación).
        for _ in range(5):
            cli.formulario("/capturar", par.alta(plantilla.trabajador(), par.dia_habil_atras(1), CAPTURA))
        srv.detener()
        for sufijo in ("", "-wal", "-shm"):
            if os.path.exists(srv.base + sufijo):
                os.remove(srv.base + sufijo)            # pérdida total del archivo de la base
        inicio = time.perf_counter()
        restaurado = consola(srv, "sigma.respaldo", "--restaurar", ruta)
        srv.iniciar()
        segundos_restauracion = time.perf_counter() - inicio
        conexion = srv.bd()
        despues = {tabla: conexion.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
                   for tabla in ("trabajador", "movimiento", "bitacora")}
        conexion.close()
        acceso = par.Cliente(srv.puerto, usuario_id=CAPTURA).pedir("GET", "/").estado
    finally:
        srv.__exit__()
    # Tras restaurar, la bitácora crece con el inicio de sesión de la verificación.
    coincide = despues["trabajador"] == antes["trabajador"] and despues["movimiento"] == antes["movimiento"]
    resumen = {"respaldos_al_arrancar": al_arrancar, "respaldo_integro": integro,
               "segundos_respaldo": round(segundos_respaldo, 2), "conteos_antes": antes,
               "conteos_despues": despues, "datos_recuperados": coincide,
               "capturas_posteriores_perdidas": 5, "segundos_restauracion": round(segundos_restauracion, 2),
               "acceso_tras_restaurar": acceso, "salida_restaurar": restaurado.stdout.strip()[:200]}
    log(f"  Respaldo al arrancar el servidor: {al_arrancar} archivo(s) · respaldo manual íntegro: {integro} "
        f"({resumen['segundos_respaldo']} s)")
    log(f"  Antes: {antes} · después de perder y restaurar: {despues} · recuperado: {coincide}")
    log(f"  Restauración y arranque: {resumen['segundos_restauracion']} s · acceso posterior: HTTP {acceso}")
    log("")
    RESULTADOS["R"] = resumen


# ==========================================================================
# Bloque C — Comunicación entre equipos
# ==========================================================================
def bloque_c(modo):
    log("=" * 78)
    log("BLOQUE C — COMUNICACIÓN ENTRE EQUIPOS (tamaños y tiempos)")
    log("=" * 78)
    ip = par.ip_lan()
    plantilla = par.Plantilla(80)
    with par.Servidor(modo) as srv:
        latencias = {}
        for nombre, host in (("localhost", "127.0.0.1"), ("red_local", ip)):
            cli = par.Cliente(srv.puerto, host=host, usuario_id=CAPTURA)
            datos = par.alta(plantilla.trabajador(), par.dia_habil_atras(1), CAPTURA)
            for _ in range(20):
                cli.pedir("GET", "/")
            t_get, t_val = [], []
            for _ in range(300):
                t_get.append(cli.pedir("GET", "/").segundos)
                t_val.append(cli.validar(datos).segundos)
            latencias[nombre] = {"tablero": par.resumen_tiempos(t_get), "validar": par.resumen_tiempos(t_val)}
        cli = par.Cliente(srv.puerto, host=ip, usuario_id=CAPTURA)
        enlaces = []

        def medir(interfaz, metodo, ruta, cuerpo=None, cabeceras=None):
            r = cli.pedir(metodo, ruta, cuerpo, cabeceras)
            enlaces.append({"interfaz": interfaz, "ruta": ruta.split("?")[0], "peticion_b": len(cuerpo or b""),
                            "respuesta_b": len(r.cuerpo), "estado": r.estado,
                            "tipo": r.cabeceras.get("content-type", ""), "ms": round(r.segundos * 1000, 1)})
            return r

        login = urllib.parse.urlencode({"usuario": "captura.obra1", "contrasena": par.CONTRASENA_PRUEBA}).encode()
        medir("Inicio de sesión", "POST", "/login", login, {"Content-Type": "application/x-www-form-urlencoded",
                                                            "Origin": cli.origen})
        medir("Pantalla principal", "GET", "/")
        medir("Hoja de estilos", "GET", "/static/css/estilos.css")
        medir("Script de la interfaz", "GET", "/static/js/app.js")
        t = plantilla.trabajador()
        datos = par.alta(t, par.dia_habil_atras(1), CAPTURA)
        medir("Validación en vivo", "POST", "/api/validar", json.dumps(datos).encode(),
              {"Content-Type": "application/json", "Origin": cli.origen})
        medir("Captura", "POST", "/capturar", urllib.parse.urlencode(datos).encode(),
              {"Content-Type": "application/x-www-form-urlencoded", "Origin": cli.origen})
        folio = re.search(r'data-movimiento="(\d+)"', cli.pedir("GET", "/").texto).group(1)
        medir("Detalle del movimiento", "GET", f"/api/movimiento/{folio}")
        admin = par.Cliente(srv.puerto, host=ip, usuario_id=ADMIN)
        admin.formulario("/exportar", {"usuario_id": ADMIN})
        r = admin.pedir("GET", "/descargar-lote?tipo=altas")
        enlaces.append({"interfaz": "Descarga del lote de altas", "ruta": "/descargar-lote", "peticion_b": 0,
                        "respuesta_b": len(r.cuerpo), "estado": r.estado,
                        "tipo": r.cabeceras.get("content-type", ""), "ms": round(r.segundos * 1000, 1)})
        # Intercambio crudo de la validación en vivo, para documentarlo
        cuerpo = json.dumps({k: datos[k] for k in ("curp", "nss", "rfc", "fecha_movimiento")}).encode()
        peticion = (f"POST /api/validar HTTP/1.1\r\nHost: {ip}:{srv.puerto}\r\nContent-Type: application/json\r\n"
                    f"Origin: http://{ip}:{srv.puerto}\r\nCookie: {cli.cookie}\r\n"
                    f"Content-Length: {len(cuerpo)}\r\nConnection: close\r\n\r\n").encode() + cuerpo
        s = socket.create_connection((ip, srv.puerto), timeout=10)
        s.sendall(peticion)
        crudo = b""
        while True:
            trozo = s.recv(65536)
            if not trozo:
                break
            crudo += trozo
        s.close()
        if GUARDAR_HTML:
            os.makedirs(CAPTURAS, exist_ok=True)
            with open(os.path.join(CAPTURAS, "intercambio_validar.txt"), "w", encoding="utf-8", newline="") as f:
                f.write((peticion.decode("utf-8") + "\r\n" + crudo.decode("utf-8", "replace"))
                        .replace(cli.cookie or "§", "session=<cookie de sesión>"))
        excepciones = srv.excepciones()
    for nombre, datos in latencias.items():
        log(f"  {nombre:<10} pantalla p95 {datos['tablero']['p95_ms']} ms · validación p95 {datos['validar']['p95_ms']} ms")
    for e in enlaces:
        log(f"  {e['interfaz']:<28} {e['ruta']:<22} {e['peticion_b']:>6} B → {e['respuesta_b']:>7} B · "
            f"HTTP {e['estado']} · {e['ms']} ms")
    log("")
    RESULTADOS["C"] = {"latencias": latencias, "enlaces": enlaces, "excepciones_servidor": excepciones}


BLOQUES = {"F": bloque_f, "L": bloque_l, "S": bloque_s, "R": bloque_r, "C": bloque_c}


def main():
    global GUARDAR_HTML
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--bloques", default="FLSRC")
    parser.add_argument("--etiqueta", default="")
    parser.add_argument("--capturas", action="store_true",
                        help="guarda el HTML de las pantallas y los intercambios en pruebas/resultados/integracion/")
    argumentos = parser.parse_args()
    GUARDAR_HTML = argumentos.capturas
    if not par.version_trl6():
        sys.exit("Este arnés requiere la versión del TRL 6 (sigma/usuarios.py).")
    sufijo = f"_{argumentos.etiqueta}" if argumentos.etiqueta else ""
    log("REPORTE DE RESULTADOS — INTEGRACIÓN Y DEMOSTRACIÓN DEL SISTEMA (ENTREGA 6 / TRL 6)")
    log("Sistema para la automatización de altas y bajas de seguro social")
    log(f"Fecha: {datetime.now():%d/%m/%Y %H:%M} · servidor de producción · Python {sys.version.split()[0]} · "
        f"IP de la red local {par.ip_lan()}")
    log("")
    RESULTADOS["meta"] = {"fecha": datetime.now().isoformat(timespec="seconds"), "python": sys.version.split()[0],
                          "ip_lan": par.ip_lan(), "etiqueta": argumentos.etiqueta}
    inicio = time.perf_counter()
    for clave in argumentos.bloques.replace(",", "").upper():
        BLOQUES[clave]("produccion")
    RESULTADOS["meta"]["duracion_total_s"] = round(time.perf_counter() - inicio, 1)
    log(f"Duración total: {RESULTADOS['meta']['duracion_total_s']} s")
    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, f"resultados_integracion{sufijo}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(REPORTE))
    with open(os.path.join(SALIDA, f"resultados_integracion{sufijo}.json"), "w", encoding="utf-8") as f:
        json.dump(RESULTADOS, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nReporte guardado en pruebas/resultados/resultados_integracion{sufijo}.txt y .json")


if __name__ == "__main__":
    main()
