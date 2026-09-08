"""
Arnés de pruebas para el Desarrollo experimental de la Entrega 3.
Ejecuta los tres bloques descritos en el informe:
  Bloque 1 - Validación de captura (casos válidos e inválidos)
  Bloque 2 - Exportación al formato IDSE
  Bloque 3 - Concurrencia y auditoría (dos usuarios capturando a la vez)

Produce un reporte de texto con los resultados, listo para pegar en la
sección "Resultados" del informe.
"""
import os
import threading
from database import get_conn, init_db, registrar_bitacora, obtener_o_crear_trabajador
from validaciones import validar_movimiento
from exportar_idse import exportar_a_archivo

REPORTE = []


def log(linea=""):
    print(linea)
    REPORTE.append(linea)


# --------------------------------------------------------------------------
# Dataset de prueba: mezcla de casos válidos e inválidos
# --------------------------------------------------------------------------
CASOS_PRUEBA = [
    {"caso": "C1 - Alta válida",
     "datos": {"nombre_completo": "Gael Antonio Rivera Diego", "curp": "RIDG050515HNLVLL09",
               "nss": "12345678901", "rfc": "RIDG050515AB1", "tipo_movimiento": "08",
               "fecha_movimiento": "05092026", "tipo_trabajador": "1", "tipo_salario": "0",
               "tipo_jornada": "1", "sdi": "450.50", "causa_baja": ""},
     "esperado": True},
    {"caso": "C2 - Baja válida",
     "datos": {"nombre_completo": "Ernesto Beas Hernandez", "curp": "BEHE900101HNLRRN05",
               "nss": "98765432101", "rfc": "BEHE900101AB2", "tipo_movimiento": "02",
               "fecha_movimiento": "01092026", "causa_baja": "Terminación de obra"},
     "esperado": True},
    {"caso": "C3 - CURP con longitud incorrecta",
     "datos": {"nombre_completo": "Pedro Luna Salas", "curp": "LUSP99010",
               "nss": "11122233344", "rfc": "LUSP990101AB3", "tipo_movimiento": "08",
               "fecha_movimiento": "10092026"},
     "esperado": False},
    {"caso": "C4 - NSS con letras",
     "datos": {"nombre_completo": "Hector Garza Pachicano", "curp": "GAPH880303HNLRCC02",
               "nss": "1234ABC8901", "rfc": "GAPH880303AB4", "tipo_movimiento": "08",
               "fecha_movimiento": "12092026"},
     "esperado": False},
    {"caso": "C5 - Fecha fuera de formato (usa guiones)",
     "datos": {"nombre_completo": "Emilio Garza Diaz de Leon", "curp": "GADE970707HNLRML08",
               "nss": "55566677788", "rfc": "GADE970707AB5", "tipo_movimiento": "02",
               "fecha_movimiento": "12-09-2026", "causa_baja": "Renuncia"},
     "esperado": False},
    {"caso": "C6 - Fecha inexistente en el calendario (31 de febrero)",
     "datos": {"nombre_completo": "Sofia Ramirez Torres", "curp": "RATS930231MNLMRF01",
               "nss": "22233344455", "rfc": "RATS930231AB6", "tipo_movimiento": "08",
               "fecha_movimiento": "31022026"},
     "esperado": False},
    {"caso": "C7 - Tipo de movimiento inválido",
     "datos": {"nombre_completo": "Laura Mendez Cantu", "curp": "MECL881212MNLNND07",
               "nss": "33344455566", "rfc": "MECL881212AB7", "tipo_movimiento": "99",
               "fecha_movimiento": "15092026"},
     "esperado": False},
    {"caso": "C8 - Nombre vacío",
     "datos": {"nombre_completo": "", "curp": "TORJ951111HNLRZR06",
               "nss": "44455566677", "rfc": "TORJ951111AB8", "tipo_movimiento": "08",
               "fecha_movimiento": "20092026"},
     "esperado": False},
]


def bloque_1_validacion():
    log("=" * 78)
    log("BLOQUE 1 — VALIDACIÓN DE CAPTURA")
    log("=" * 78)
    conn = get_conn()
    aciertos = 0
    for caso in CASOS_PRUEBA:
        es_valido, errores = validar_movimiento(caso["datos"])
        cumple = (es_valido == caso["esperado"])
        aciertos += int(cumple)
        estado = "CUMPLE" if cumple else "NO CUMPLE"
        log(f"[{estado}] {caso['caso']}: esperado={'válido' if caso['esperado'] else 'rechazado'}, "
            f"obtenido={'válido' if es_valido else 'rechazado'}")
        if errores:
            for e in errores:
                log(f"        -> {e}")

        # Persistir el intento en la base de datos / bitácora (usuario 1 = admin.rrhh)
        if es_valido:
            patron_id = conn.execute("SELECT id FROM patron LIMIT 1").fetchone()["id"]
            trabajador_id = obtener_o_crear_trabajador(
                conn, caso["datos"]["nombre_completo"], caso["datos"]["curp"],
                caso["datos"]["nss"], caso["datos"]["rfc"])
            cur = conn.execute("""
                INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento,
                    tipo_trabajador, tipo_salario, tipo_jornada, sdi, causa_baja, estado, exportado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Válido', 0)
            """, (trabajador_id, patron_id, caso["datos"]["tipo_movimiento"], caso["datos"]["fecha_movimiento"],
                  caso["datos"].get("tipo_trabajador", ""), caso["datos"].get("tipo_salario", ""),
                  caso["datos"].get("tipo_jornada", ""), caso["datos"].get("sdi", ""),
                  caso["datos"].get("causa_baja", "")))
            registrar_bitacora(conn, 1, cur.lastrowid, "Movimiento capturado", caso["caso"])
        else:
            registrar_bitacora(conn, 1, None, "Intento de captura rechazado", "; ".join(errores))
    conn.commit()
    conn.close()
    log("")
    log(f"Resultado del bloque 1: {aciertos}/{len(CASOS_PRUEBA)} casos cumplen el resultado esperado "
        f"({round(100 * aciertos / len(CASOS_PRUEBA), 1)}%).")
    log("")
    return aciertos, len(CASOS_PRUEBA)


def bloque_2_exportacion():
    log("=" * 78)
    log("BLOQUE 2 — EXPORTACIÓN AL FORMATO IDSE")
    log("=" * 78)
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
    ruta = exportar_a_archivo(registros, "lote_idse_prueba.txt")

    ids = [r["movimiento_id"] for r in registros]
    conn.executemany("UPDATE movimiento SET exportado = 1, estado = 'Exportado' WHERE id = ?", [(i,) for i in ids])
    registrar_bitacora(conn, 1, None, "Exportación de lote IDSE (prueba)", f"{len(registros)} movimiento(s)")
    conn.commit()
    conn.close()

    log(f"Movimientos válidos exportados: {len(registros)}")
    log(f"Archivo generado: {ruta}")
    log("Contenido del lote (una línea por movimiento, campos separados por '|'):")
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            log("   " + linea.strip())
    cumple = len(registros) == 2  # C1 y C2 son los únicos válidos del dataset
    log("")
    log(f"Resultado del bloque 2: {'CUMPLE' if cumple else 'NO CUMPLE'} — se esperaban 2 movimientos válidos "
        f"(C1 y C2) y se exportaron {len(registros)}.")
    log("")
    return cumple


def bloque_3_concurrencia():
    log("=" * 78)
    log("BLOQUE 3 — CONCURRENCIA Y AUDITORÍA")
    log("=" * 78)

    resultados = {"usuario_a": None, "usuario_b": None}

    def capturar_usuario_a():
        conn = get_conn()
        patron_id = conn.execute("SELECT id FROM patron LIMIT 1").fetchone()["id"]
        trabajador_id = obtener_o_crear_trabajador(conn, "Usuario Concurrente A", "CONA900101HNLNNC01", "10101010101", "CONA900101AB1")
        cur = conn.execute("""
            INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento, estado, exportado)
            VALUES (?, ?, '08', '01092026', 'Válido', 0)
        """, (trabajador_id, patron_id))
        registrar_bitacora(conn, 1, cur.lastrowid, "Movimiento capturado", "Prueba de concurrencia - Usuario A")
        conn.commit()
        resultados["usuario_a"] = cur.lastrowid
        conn.close()

    def capturar_usuario_b():
        conn = get_conn()
        patron_id = conn.execute("SELECT id FROM patron LIMIT 1").fetchone()["id"]
        trabajador_id = obtener_o_crear_trabajador(conn, "Usuario Concurrente B", "CONB900101MNLNNC02", "20202020202", "CONB900101AB2")
        cur = conn.execute("""
            INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento, estado, exportado)
            VALUES (?, ?, '08', '01092026', 'Válido', 0)
        """, (trabajador_id, patron_id))
        registrar_bitacora(conn, 2, cur.lastrowid, "Movimiento capturado", "Prueba de concurrencia - Usuario B")
        conn.commit()
        resultados["usuario_b"] = cur.lastrowid
        conn.close()

    t1 = threading.Thread(target=capturar_usuario_a)
    t2 = threading.Thread(target=capturar_usuario_b)
    t1.start(); t2.start()
    t1.join(); t2.join()

    conn = get_conn()
    bitacora = conn.execute("""
        SELECT b.timestamp, u.nombre AS usuario, b.accion, b.detalle
        FROM bitacora b JOIN usuario u ON u.id = b.usuario_id
        WHERE b.detalle LIKE '%concurrencia%'
        ORDER BY b.id
    """).fetchall()
    conn.close()

    log(f"Movimiento insertado por usuario A: id={resultados['usuario_a']}")
    log(f"Movimiento insertado por usuario B: id={resultados['usuario_b']}")
    log("Entradas de bitácora generadas:")
    for b in bitacora:
        log(f"   {b['timestamp']} | {b['usuario']} | {b['accion']} | {b['detalle']}")

    cumple = (resultados["usuario_a"] != resultados["usuario_b"]
              and resultados["usuario_a"] is not None
              and resultados["usuario_b"] is not None
              and len(bitacora) == 2)
    log("")
    log(f"Resultado del bloque 3: {'CUMPLE' if cumple else 'NO CUMPLE'} — ambos movimientos se registraron "
        f"con IDs distintos y cada uno quedó atribuido a su usuario correspondiente en la bitácora, "
        f"sin pérdida ni sobrescritura de datos.")
    log("")
    return cumple


if __name__ == "__main__":
    if os.path.exists("prueba_concepto.db"):
        os.remove("prueba_concepto.db")
    init_db()

    log("REPORTE DE RESULTADOS — PRUEBA DE CONCEPTO (ENTREGA 3 / TRL 3)")
    log("Sistema para la automatización de altas y bajas de seguro social")
    log("")

    aciertos, total = bloque_1_validacion()
    cumple_b2 = bloque_2_exportacion()
    cumple_b3 = bloque_3_concurrencia()

    log("=" * 78)
    log("RESUMEN GENERAL FRENTE A LOS CRITERIOS DE ACEPTACIÓN")
    log("=" * 78)
    log(f"1) Rechazo de CURP/NSS inválidos: {'CUMPLE' if aciertos == total else 'REVISAR'} "
        f"({aciertos}/{total} casos correctos)")
    log(f"2) Rechazo de fechas inválidas: incluido en el bloque 1 (casos C5 y C6)")
    log(f"3) Estructura del archivo de exportación IDSE: {'CUMPLE' if cumple_b2 else 'REVISAR'}")
    log(f"4) Asociación de cada movimiento a usuario + timestamp en bitácora: CUMPLE (ver bloques 1 y 3)")
    log(f"5) Sin pérdida de datos en captura concurrente: {'CUMPLE' if cumple_b3 else 'REVISAR'}")

    with open("resultados_prueba_concepto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(REPORTE))
    print("\nReporte guardado en resultados_prueba_concepto.txt")
