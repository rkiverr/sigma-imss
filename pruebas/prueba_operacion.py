"""
Arnés de pruebas del Entregable 9 (TRL 9): problemas encontrados durante la operación.

Cada caso reproduce un problema que apareció al operar el sistema (marcha blanca
del TRL 7 y operación de un mes del TRL 8) y comprueba que ya no ocurre. Con
--codigo se puede correr contra una versión anterior para ver el problema:
en la 509a64d los cuatro casos fallan; en la versión corregida pasan.

Casos:
  O-01 - "Último lote" ofrece un archivo de bajas de una exportación anterior.
  O-02 - Un mismo trabajador lleva alta, baja y reingreso en un solo lote.
  O-03 - Dos lotes generados en el mismo segundo: el segundo sobrescribe al primero.
  O-04 - Un segundo servidor arranca en el mismo puerto sin ningún error.

Uso (desde la raíz del repositorio; los reportes quedan en pruebas/resultados/):
    python pruebas/prueba_operacion.py
    python pruebas/prueba_operacion.py --codigo ../sigma_509a64d --etiqueta antes
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prueba_ambiente_relevante as par  # noqa: E402  (Servidor, Cliente y plantilla sintética)

SALIDA = os.path.join(par.RAIZ, "pruebas", "resultados")
RESULTADOS = {"casos": []}
REPORTE = []
ADMIN, CAPTURA = "1", "2"


def log(linea=""):
    print(linea, flush=True)
    REPORTE.append(linea)


def caso(clave, problema, esperado, obtenido, ok, **extra):
    RESULTADOS["casos"].append({"clave": clave, "problema": problema, "esperado": esperado,
                                "obtenido": obtenido, "ok": bool(ok), **extra})
    log(f"  {clave} {'OK   ' if ok else 'FALLA'}  {problema}")
    log(f"         esperado: {esperado}")
    log(f"         obtenido: {obtenido}")


def capturar(cli, datos):
    r = cli.formulario("/capturar", dict(datos, usuario_id=CAPTURA))
    if r.estado != 302:
        raise RuntimeError(f"La captura de prueba fue rechazada (HTTP {r.estado}): {par.leer_errores(r.texto)}")


def exportar(cli):
    """Genera un lote como administración y devuelve (categoría, mensaje, archivos nuevos)."""
    r = cli.formulario("/exportar", {"usuario_id": ADMIN})
    pagina = cli.pedir("GET", r.ubicacion or "/", cabeceras={"Cookie": par._galleta(r) or cli.cookie or ""})
    categoria, mensaje = par.leer_notificacion(pagina.texto)
    return categoria, mensaje, re.findall(r"(lote_idse_(?:altas|bajas)_[\d_]+\.txt)", mensaje)


def lineas_con(ruta, texto):
    with open(ruta, "rb") as f:
        return sum(1 for linea in f.read().splitlines() if texto.encode("cp1252") in linea)


def o01_lote_viejo(srv, cli, plantilla):
    t1, t2, t3 = (plantilla.trabajador() for _ in range(3))
    d3, d2, d1 = (par.dia_habil_atras(n) for n in (3, 2, 1))
    capturar(cli, par.alta(t1, d3))
    capturar(cli, par.alta(t2, d3))
    exportar(cli)                                   # lote 1: dos altas
    capturar(cli, par.baja(t1, d2))
    _, _, lote2 = exportar(cli)                     # lote 2: una baja
    capturar(cli, par.alta(t3, d1))
    _, _, lote3 = exportar(cli)                     # lote 3: solo altas
    tablero = cli.pedir("GET", "/").texto
    ofrece_bajas = "descargar-lote?tipo=bajas" in tablero
    descarga = cli.pedir("GET", "/descargar-lote?tipo=bajas")
    entrega_archivo = descarga.estado == 200
    lleva_baja_vieja = entrega_archivo and t1["nss"].encode() in descarga.cuerpo
    caso("O-01", "«Último lote» ofrece un archivo de bajas de una exportación anterior",
         "Tras un lote solo de altas, no se ofrece «Bajas (02)» y la descarga de bajas no entrega archivo",
         f"último lote {lote3} · botón «Bajas (02)» visible={ofrece_bajas} · descarga de bajas: "
         f"HTTP {descarga.estado}{' con la baja del lote anterior' if lleva_baja_vieja else ''}",
         not ofrece_bajas and not entrega_archivo,
         lote_con_bajas=lote2, ultimo_lote=lote3, boton_bajas=ofrece_bajas, descarga_bajas=descarga.estado,
         baja_vieja=lleva_baja_vieja)


def o02_mismo_trabajador(srv, cli, plantilla):
    t = plantilla.trabajador()
    capturar(cli, par.alta(t, par.dia_habil_atras(4)))
    capturar(cli, par.baja(t, par.dia_habil_atras(2)))
    capturar(cli, par.alta(t, par.dia_habil_atras(0)))       # reingreso
    secuencia = []
    for _ in range(4):
        categoria, mensaje, archivos = exportar(cli)
        if not archivos:
            break
        rutas = [os.path.join(srv.dir, "exportaciones", a) for a in archivos]
        movimientos = sum(lineas_con(ruta, t["nss"]) for ruta in rutas)
        secuencia.append({"archivos": archivos, "movimientos_del_trabajador": movimientos,
                          "en_espera": "siguiente lote" in mensaje, "categoria": categoria})
    maximo = max(s["movimientos_del_trabajador"] for s in secuencia)
    tipos = ["altas" if "_altas_" in s["archivos"][0] and len(s["archivos"]) == 1 else
             "bajas" if len(s["archivos"]) == 1 else "altas y bajas" for s in secuencia]
    caso("O-02", "Un mismo trabajador lleva alta, baja y reingreso en un solo lote",
         "A lo más un movimiento del trabajador por lote: alta, baja y reingreso salen en tres lotes seguidos",
         f"{len(secuencia)} lote(s) ({' → '.join(tipos)}) · máximo {maximo} movimiento(s) del trabajador "
         f"en un lote · aviso de espera en el primero={secuencia[0]['en_espera']}",
         maximo == 1 and len(secuencia) == 3 and tipos == ["altas", "bajas", "altas"] and secuencia[0]["en_espera"],
         secuencia=secuencia)


def _sello(nombre):
    """Fecha y hora (al segundo) que lleva el nombre de un lote."""
    return re.search(r"_(\d{8}_\d{6})", nombre).group(1)


def o03_mismo_segundo(srv, cli, plantilla):
    exportaciones, colisiones = 0, 0
    archivos_anunciados = []
    for _ in range(3):
        a, b = plantilla.trabajador(), plantilla.trabajador()
        # Se espera al inicio de un segundo para que las dos exportaciones caigan en él.
        time.sleep(1 - (time.time() % 1) + 0.02)
        capturar(cli, par.alta(a, par.dia_habil_atras(1)))
        _, _, primero = exportar(cli)
        capturar(cli, par.alta(b, par.dia_habil_atras(1)))
        _, _, segundo = exportar(cli)
        exportaciones += 2
        archivos_anunciados += primero + segundo
        if primero and segundo and _sello(primero[0]) == _sello(segundo[0]):
            colisiones += 1
    en_disco = [a for a in archivos_anunciados if os.path.isfile(os.path.join(srv.dir, "exportaciones", a))]
    distintos = len(set(archivos_anunciados))
    caso("O-03", "Dos lotes generados en el mismo segundo: el segundo sobrescribe al primero",
         "Cada exportación deja su propio archivo, aunque caiga en el mismo segundo que otra",
         f"{exportaciones} exportaciones · {colisiones} pares en el mismo segundo · {distintos} nombres "
         f"distintos · {len(set(en_disco))} archivos en disco",
         colisiones > 0 and distintos == exportaciones and len(set(en_disco)) == exportaciones,
         exportaciones=exportaciones, colisiones=colisiones, archivos=archivos_anunciados)


def o04_mismo_puerto(srv):
    entorno = dict(os.environ, SIGMA_DB="sqlite", SQLITE_PATH=srv.base, SIGMA_PUERTO=str(srv.puerto),
                   SIGMA_HOST="0.0.0.0", PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
    for variable in ("DATABASE_URL", "SIGMA_DEBUG", "SECRET_KEY"):
        entorno.pop(variable, None)
    bitacora = os.path.join(srv.dir, "segundo_servidor.log")
    with open(bitacora, "w", encoding="utf-8") as salida:
        segundo = subprocess.Popen([sys.executable, "servidor.py"], cwd=srv.dir, env=entorno,
                                   stdout=salida, stderr=subprocess.STDOUT)
    inicio = time.perf_counter()
    while segundo.poll() is None and time.perf_counter() - inicio < 8:
        time.sleep(0.1)
    sigue_vivo = segundo.poll() is None
    codigo = segundo.returncode
    if sigue_vivo:
        subprocess.run(["taskkill", "/PID", str(segundo.pid), "/T", "/F"], capture_output=True, check=False)
        segundo.wait(timeout=10)
    with open(bitacora, encoding="utf-8", errors="replace") as f:
        mensaje = f.read().strip().splitlines()
    primero_responde = par.Cliente(srv.puerto, sesion=False).pedir("GET", "/login").estado == 200
    aviso = next((m for m in mensaje if "ya está en uso" in m), "")
    caso("O-04", "Un segundo servidor arranca en el mismo puerto sin ningún error",
         "El segundo servidor se detiene con un mensaje claro y el primero sigue atendiendo",
         ("el segundo sigue corriendo después de 8 s (se detuvo a mano)" if sigue_vivo else
          f"el segundo terminó con código {codigo}: «{aviso[:90]}…»") + f" · el primero responde={primero_responde}",
         not sigue_vivo and codigo == 1 and bool(aviso) and primero_responde,
         segundo_vivo=sigue_vivo, codigo_salida=codigo, mensaje=mensaje[-3:], primero_responde=primero_responde)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--codigo", default=par.RAIZ, help="carpeta con otra versión del sistema")
    parser.add_argument("--etiqueta", default="")
    argumentos = parser.parse_args()
    par.CODIGO = os.path.abspath(argumentos.codigo)
    if not par.version_trl6():
        sys.exit("Este arnés requiere la versión del TRL 6 o posterior (sigma/usuarios.py).")
    sufijo = f"_{argumentos.etiqueta}" if argumentos.etiqueta else ""
    log("REPORTE DE RESULTADOS — PROBLEMAS ENCONTRADOS DURANTE LA OPERACIÓN (ENTREGA 9 / TRL 9)")
    log("Sistema para la automatización de altas y bajas de seguro social")
    log(f"Fecha: {datetime.now():%d/%m/%Y %H:%M} · servidor de producción · Python {sys.version.split()[0]} · "
        f"código: {par.CODIGO}")
    log("")
    RESULTADOS["meta"] = {"fecha": datetime.now().isoformat(timespec="seconds"), "python": sys.version.split()[0],
                          "codigo": par.CODIGO, "etiqueta": argumentos.etiqueta}
    inicio = time.perf_counter()
    plantilla = par.Plantilla(20261018)
    with par.Servidor("produccion") as srv:
        cli = par.Cliente(srv.puerto, host=par.ip_lan(), usuario_id=CAPTURA)
        o01_lote_viejo(srv, cli, plantilla)
        o02_mismo_trabajador(srv, cli, plantilla)
        o03_mismo_segundo(srv, cli, plantilla)
        o04_mismo_puerto(srv)
        RESULTADOS["excepciones_servidor"] = srv.excepciones()
    correctos = sum(c["ok"] for c in RESULTADOS["casos"])
    RESULTADOS["correctos"], RESULTADOS["total"] = correctos, len(RESULTADOS["casos"])
    RESULTADOS["meta"]["duracion_total_s"] = round(time.perf_counter() - inicio, 1)
    log("")
    log(f"  {correctos} de {len(RESULTADOS['casos'])} casos correctos · excepciones en el servidor: "
        f"{RESULTADOS['excepciones_servidor']}")
    log(f"Duración total: {RESULTADOS['meta']['duracion_total_s']} s")
    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, f"resultados_operacion{sufijo}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(REPORTE))
    with open(os.path.join(SALIDA, f"resultados_operacion{sufijo}.json"), "w", encoding="utf-8") as f:
        json.dump(RESULTADOS, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nReporte guardado en pruebas/resultados/resultados_operacion{sufijo}.txt y .json")


if __name__ == "__main__":
    main()
