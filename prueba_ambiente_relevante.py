"""
Arnés de pruebas del Entregable 5 (TRL 5): validación en ambiente relevante.

El arnés del Entregable 3 (test_prueba_concepto.py) prueba los módulos en
laboratorio: ocho casos, un usuario y llamadas directas a las funciones. Este
arnés prueba el sistema COMPLETO en condiciones semejantes a las de la empresa:
el servidor corre como proceso independiente, los capturistas son clientes HTTP
concurrentes que se comportan como el navegador (máscaras y longitudes máximas
de la interfaz incluidas) y los datos imitan la plantilla de una contratista
eléctrica con cuadrillas que rotan entre obras.

Bloques:
  A - Mes de operación simulado: 3 capturistas, altas, bajas, reingresos y
      exportación del lote IDSE al cierre de cada etapa.
  B - Errores típicos de captura: cada intento se clasifica como bloqueado,
      avisado o no detectado; también se miden los falsos positivos.
  C - Capturas simultáneas del mismo movimiento (dos capturistas a la vez).
  D - Carga: 1, 3, 5, 10 y 20 usuarios simultáneos.
  E - Volumen: base precargada con 1 000, 5 000 y 10 000 movimientos.
  F - Recuperación: caída abrupta del servidor a media captura.
  G - Operación en red y seguridad.
  H - Accesibilidad: contraste de la paleta según WCAG 2.1.

Para no tocar la base de trabajo ni los lotes reales, cada bloque ejecuta una
COPIA AISLADA del sistema en un directorio temporal, con su propia base SQLite.

Uso:
  python prueba_ambiente_relevante.py                         # servidor de producción
  python prueba_ambiente_relevante.py --servidor desarrollo   # servidor de Flask
  python prueba_ambiente_relevante.py --bloques A,B --etiqueta prueba
  python prueba_ambiente_relevante.py --codigo ../version_e4 --servidor desarrollo --etiqueta antes
"""
import argparse
import html
import http.client
import json
import os
import random
import re
import shutil
import socket
import sqlite3
import statistics
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import urllib.parse
from datetime import date, datetime, timedelta

RAIZ = os.path.dirname(os.path.abspath(__file__))
CODIGO = RAIZ            # versión del sistema que se prueba (--codigo la cambia)
REPORTE = []
RESULTADOS = {}


def log(linea=""):
    print(linea, flush=True)
    REPORTE.append(linea)


# ==========================================================================
# Generador de una plantilla realista de trabajadores
# ==========================================================================
APELLIDOS = [
    "Garza", "Treviño", "Villarreal", "Cantú", "González", "Hernández", "Rodríguez",
    "Martínez", "López", "Sánchez", "Ramírez", "Flores", "Gómez", "Díaz", "Reyes",
    "Cruz", "Morales", "Ortiz", "Gutiérrez", "Chávez", "Ruiz", "Mendoza", "Castillo",
    "Vázquez", "Jiménez", "Salazar", "Elizondo", "Leal", "Tamez", "Peña", "Muñoz",
    "Ibáñez", "Cavazos", "De la Rosa", "Del Ángel", "Esquivel", "Quiroga", "Zambrano",
    "Barragán", "Ochoa",
]
NOMBRES_HOMBRE = [
    "Juan Carlos", "José Luis", "Miguel Ángel", "Francisco", "Alejandro", "Ricardo",
    "Óscar", "Raúl", "Martín", "Eduardo", "Sergio", "Daniel", "Jesús", "Arturo",
    "Héctor", "Roberto", "Fernando", "Iván", "Ángel", "Jorge",
]
NOMBRES_MUJER = ["Ana Karen", "María Fernanda", "Mónica", "Diana", "Laura", "Sofía",
                 "Patricia", "Rocío"]
PARTICULAS = {"DE", "LA", "DEL", "LAS", "LOS", "Y", "MC", "MAC", "VON", "VAN"}
ENTIDADES = ["NL"] * 7 + ["CL", "TS", "SP", "VZ", "ZS", "DG"]
SUBDELEGACIONES = ["19", "39", "43", "46", "47", "48", "49"]
ALFABETO_CURP = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# Factor de integración mínimo del SDI con 12 días de vacaciones, prima
# vacacional del 25 % y 15 días de aguinaldo: (365 + 15 + 12 x 0.25) / 365.
FACTOR_INTEGRACION = 383 / 365

# Supuesto declarado de salarios diarios por puesto (MXN 2026). El salario
# mínimo general de 2026 es de 315.04 pesos diarios.
PUESTOS = [("Ayudante de electricista", 330, 420, 0.45),
           ("Oficial electricista", 450, 700, 0.40),
           ("Supervisor de obra", 800, 1200, 0.15)]


def _sin_acentos(texto):
    texto = texto.upper().replace("Ñ", "X")
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")


def _palabra_clave(apellido):
    palabras = [p for p in _sin_acentos(apellido).split() if p not in PARTICULAS]
    return palabras[0] if palabras else "X"


def _nombre_clave(nombre):
    palabras = _sin_acentos(nombre).split()
    if len(palabras) > 1 and palabras[0] in ("JOSE", "MARIA", "MA", "J"):
        return palabras[1]
    return palabras[0]


def _vocal_interna(palabra):
    return next((c for c in palabra[1:] if c in "AEIOU"), "X")


def _consonante_interna(palabra):
    return next((c for c in palabra[1:] if c.isalpha() and c not in "AEIOU"), "X")


def digito_curp(base):
    """Dígito verificador de la CURP (algoritmo publicado por RENAPO)."""
    suma = sum(ALFABETO_CURP.index(c) * (18 - i) for i, c in enumerate(base[:17]))
    return (10 - suma % 10) % 10


def digito_nss(base):
    """Dígito verificador del NSS (Luhn, como en validaciones.py)."""
    suma = 0
    for indice, caracter in enumerate(base[:10]):
        digito = int(caracter)
        if indice % 2:
            digito *= 2
            if digito > 9:
                digito -= 9
        suma += digito
    return (10 - suma % 10) % 10


# --- Días hábiles: fines de semana y descansos obligatorios (art. 74 LFT) ---
def _enesimo_lunes(anio, mes, n):
    primero = date(anio, mes, 1)
    return primero + timedelta(days=(0 - primero.weekday()) % 7 + 7 * (n - 1))


def _descansos(anio):
    dias = {date(anio, 1, 1), _enesimo_lunes(anio, 2, 1), _enesimo_lunes(anio, 3, 3),
            date(anio, 5, 1), date(anio, 9, 16), _enesimo_lunes(anio, 11, 3),
            date(anio, 12, 25)}
    if anio % 6 == 0:
        dias.add(date(anio, 12, 1))
    return dias


def es_habil(dia):
    return dia.weekday() < 5 and dia not in _descansos(dia.year)


def dia_habil_atras(n, hoy=None):
    """Fecha que queda n días hábiles antes de hoy (n = 0: último día hábil)."""
    dia = hoy or date.today()
    while not es_habil(dia):
        dia -= timedelta(days=1)
    contador = 0
    while contador < n:
        dia -= timedelta(days=1)
        if es_habil(dia):
            contador += 1
    return dia


def ddmmaaaa(dia):
    return dia.strftime("%d%m%Y")


class Plantilla:
    """Genera trabajadores sintéticos con identificadores oficiales coherentes."""

    def __init__(self, semilla):
        self.azar = random.Random(semilla)
        self.candado = threading.Lock()
        self.curps = set()
        self.nss = set()
        self.consecutivo = self.azar.randint(1000, 4000)

    def trabajador(self):
        with self.candado:
            while True:
                t = self._intentar()
                if t["curp"] not in self.curps and t["nss"] not in self.nss:
                    self.curps.add(t["curp"])
                    self.nss.add(t["nss"])
                    return t

    def _intentar(self):
        az = self.azar
        mujer = az.random() < 0.12
        paterno, materno = az.choice(APELLIDOS), az.choice(APELLIDOS)
        nombre = az.choice(NOMBRES_MUJER if mujer else NOMBRES_HOMBRE)
        nacimiento = date(1966, 1, 1) + timedelta(days=az.randint(0, 14975))  # hasta 2006
        p, m, n = _palabra_clave(paterno), _palabra_clave(materno), _nombre_clave(nombre)
        iniciales = p[0] + _vocal_interna(p) + m[0] + n[0]
        base = (iniciales + nacimiento.strftime("%y%m%d") + ("M" if mujer else "H")
                + az.choice(ENTIDADES) + _consonante_interna(p) + _consonante_interna(m)
                + _consonante_interna(n) + ("A" if nacimiento.year >= 2000 else "0"))
        curp = base + str(digito_curp(base))
        homoclave = (az.choice("ABCDEFGHJKLMNPRSTUVWXYZ123456789")
                     + az.choice("ABCDEFGHJKLMNPRSTUVWXYZ123456789") + str(az.randint(0, 9)))
        rfc = curp[:10] + homoclave
        self.consecutivo += az.randint(1, 7)
        afiliacion = az.randint(max(nacimiento.year + 16, 1990), 2026) % 100
        base_nss = (az.choice(SUBDELEGACIONES) + f"{afiliacion:02d}"
                    + nacimiento.strftime("%y") + f"{self.consecutivo % 10000:04d}")
        nss = base_nss + str(digito_nss(base_nss))
        puesto = az.choices(PUESTOS, weights=[x[3] for x in PUESTOS])[0]
        salario = az.uniform(puesto[1], puesto[2])
        return {
            "nombre_completo": f"{paterno} {materno} {nombre}",
            "curp": curp, "nss": nss, "rfc": rfc,
            "tipo_trabajador": "3" if az.random() < 0.6 else "1",  # 3 = eventual de la construcción
            "tipo_salario": "0", "tipo_jornada": "1",
            "sdi": f"{salario * FACTOR_INTEGRACION:.2f}",
            "puesto": puesto[0],
        }


def alta(t, fecha, usuario_id="2"):
    """Formulario de un alta tal como lo envía el navegador (sin causa de baja)."""
    return {"nombre_completo": t["nombre_completo"], "curp": t["curp"], "nss": t["nss"],
            "rfc": t["rfc"], "tipo_movimiento": "08", "fecha_movimiento": ddmmaaaa(fecha),
            "tipo_trabajador": t["tipo_trabajador"], "tipo_salario": t["tipo_salario"],
            "tipo_jornada": t["tipo_jornada"], "sdi": t["sdi"], "usuario_id": usuario_id}


def baja(t, fecha, causa="1", usuario_id="2"):
    """Formulario de una baja: los campos de contratación van deshabilitados y no se envían."""
    return {"nombre_completo": t["nombre_completo"], "curp": t["curp"], "nss": t["nss"],
            "rfc": t["rfc"], "tipo_movimiento": "02", "fecha_movimiento": ddmmaaaa(fecha),
            "causa_baja": causa, "usuario_id": usuario_id}


# ==========================================================================
# Servidor bajo prueba (copia aislada) y cliente HTTP
# ==========================================================================
def _puerto_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def ip_lan():
    """IP de este equipo en la red local (no envía tráfico)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
        except OSError:
            return "127.0.0.1"


class Servidor:
    """Levanta una copia del sistema en un directorio temporal."""

    IGNORAR = staticmethod(shutil.ignore_patterns(".git", "*.db", "*.db-wal", "*.db-shm", "exportaciones",
                                     "__pycache__", "resultados_*", "instrucciones",
                                     "prueba_ambiente_relevante.py", "test_prueba_concepto.py"))

    def __init__(self, modo):
        self.modo = modo
        self.dir = tempfile.mkdtemp(prefix="sigma_trl5_")
        shutil.copytree(CODIGO, self.dir, ignore=self.IGNORAR, dirs_exist_ok=True)
        self.base = os.path.join(self.dir, "sigma_ambiente.db")
        self.puerto = _puerto_libre()
        self.proceso = None
        self.bitacora_servidor = os.path.join(self.dir, "servidor.log")
        self.arranques = []

    def _comando(self):
        if self.modo == "produccion":
            return [sys.executable, "servidor.py"]
        # Servidor de desarrollo de Flask tal como lo usa app.py (debug activo,
        # escuchando en todas las interfaces). Solo se apaga el recargador, que
        # es una comodidad de edición y crea un segundo proceso.
        return [sys.executable, "-c",
                "import database, app; database.init_db(); "
                f"app.app.run(host='0.0.0.0', port={self.puerto}, debug=True, use_reloader=False)"]

    def iniciar(self):
        entorno = dict(os.environ, SIGMA_DB="sqlite", SQLITE_PATH=self.base,
                       SIGMA_PUERTO=str(self.puerto), SIGMA_HOST="0.0.0.0",
                       PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
        entorno.pop("DATABASE_URL", None)
        entorno.pop("SIGMA_DEBUG", None)
        salida = open(self.bitacora_servidor, "a", encoding="utf-8")
        inicio = time.perf_counter()
        self.proceso = subprocess.Popen(self._comando(), cwd=self.dir, env=entorno,
                                        stdout=salida, stderr=subprocess.STDOUT)
        cliente = Cliente(self.puerto)
        while time.perf_counter() - inicio < 30:
            if cliente.pedir("GET", "/").estado == 200:
                self.arranques.append(time.perf_counter() - inicio)
                return self
            time.sleep(0.1)
        raise RuntimeError("El servidor no respondió en 30 s. Revisa " + self.bitacora_servidor)

    def detener(self):
        """Termina el proceso de golpe, con todo su árbol (el python.exe de un
        entorno virtual es un lanzador que crea al intérprete como hijo)."""
        if self.proceso and self.proceso.poll() is None:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(self.proceso.pid), "/T", "/F"],
                               capture_output=True, check=False)
            else:
                self.proceso.kill()
            self.proceso.wait(timeout=10)

    def memoria_mb(self):
        """Memoria de trabajo del intérprete que atiende al servidor."""
        if not self.proceso or os.name != "nt":
            return None
        pid = self.proceso.pid
        consulta = (f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid} or ParentProcessId={pid}'"
                    " | ForEach-Object { $_.WorkingSetSize }")
        salida = subprocess.run(["powershell", "-NoProfile", "-Command", consulta],
                                capture_output=True, text=True, check=False).stdout
        tamanos = [int(x) for x in salida.split() if x.isdigit()]
        return round(max(tamanos) / 1024 / 1024, 1) if tamanos else None

    def excepciones(self):
        try:
            with open(self.bitacora_servidor, encoding="utf-8", errors="replace") as f:
                return f.read().count("Traceback (most recent call last)")
        except OSError:
            return 0

    def bd(self):
        conexion = sqlite3.connect(f"file:{self.base}?mode=ro", uri=True, timeout=10)
        conexion.row_factory = sqlite3.Row
        return conexion

    def lotes(self):
        carpeta = os.path.join(self.dir, "exportaciones")
        if not os.path.isdir(carpeta):
            return []
        return sorted(os.path.join(carpeta, n) for n in os.listdir(carpeta) if n.endswith(".txt"))

    def __enter__(self):
        return self.iniciar()

    def __exit__(self, *_):
        self.detener()
        time.sleep(0.3)
        shutil.rmtree(self.dir, ignore_errors=True)


class Respuesta:
    def __init__(self, estado, cabeceras, cuerpo, segundos, cookie=None, ubicacion=None):
        self.estado, self.cabeceras, self.cuerpo = estado, cabeceras, cuerpo
        self.segundos, self.cookie, self.ubicacion = segundos, cookie, ubicacion

    @property
    def texto(self):
        return self.cuerpo.decode("utf-8", errors="replace")

    def json(self):
        try:
            return json.loads(self.texto)
        except ValueError:
            return {}


class Metricas:
    """Registro concurrente de cada petición: (ruta, estado, segundos)."""

    def __init__(self):
        self.candado = threading.Lock()
        self.registros = []
        self.tipos_error = {}

    def agregar(self, ruta, estado, segundos):
        with self.candado:
            self.registros.append((ruta, estado, segundos))

    def resumen(self, ruta=None):
        datos = [s for r, e, s in self.registros if (ruta is None or r == ruta) and e]
        return resumen_tiempos(datos)

    def errores(self):
        return sum(1 for _, e, _ in self.registros if e == 0 or e >= 500)

    def anotar_error(self, respuesta):
        with self.candado:
            clave = f"HTTP {respuesta.estado}: " + " ".join(respuesta.texto[:80].split())
            self.tipos_error[clave] = self.tipos_error.get(clave, 0) + 1


def resumen_tiempos(segundos):
    if not segundos:
        return {"n": 0}
    ms = sorted(s * 1000 for s in segundos)
    p95 = ms[min(len(ms) - 1, int(round(0.95 * (len(ms) - 1))))]
    return {"n": len(ms), "p50_ms": round(statistics.median(ms), 1), "p95_ms": round(p95, 1),
            "max_ms": round(ms[-1], 1), "media_ms": round(statistics.fmean(ms), 1)}


class Cliente:
    """
    Cliente HTTP de un capturista. Reutiliza su conexión (keep-alive) como lo
    hace un navegador y, al cerrarla, libera el puerto de inmediato; así la
    prueba mide al servidor y no el agotamiento de puertos del equipo cliente.
    """

    REINTENTABLES = (http.client.RemoteDisconnected, ConnectionResetError,
                     ConnectionAbortedError, BrokenPipeError)

    def __init__(self, puerto, host="127.0.0.1", metricas=None):
        self.puerto, self.host, self.metricas = puerto, host, metricas
        self.origen = f"http://{host}:{puerto}"
        self._conexion = None

    def _conectar(self):
        conexion = http.client.HTTPConnection(self.host, self.puerto, timeout=60)
        conexion.connect()
        conexion.sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
        return conexion

    def cerrar(self):
        if self._conexion is not None:
            try:
                self._conexion.close()
            except OSError:
                pass
            self._conexion = None

    def pedir(self, metodo, ruta, cuerpo=None, cabeceras=None, etiqueta=None):
        cabeceras = dict(cabeceras or {})
        inicio = time.perf_counter()
        respuesta = None
        for intento in range(2):
            reutilizada = self._conexion is not None
            try:
                if self._conexion is None:
                    self._conexion = self._conectar()
                self._conexion.request(metodo, ruta, body=cuerpo, headers=cabeceras)
                r = self._conexion.getresponse()
                cuerpo_r = r.read()
                respuesta = Respuesta(r.status, {k.lower(): v for k, v in r.getheaders()}, cuerpo_r,
                                      time.perf_counter() - inicio, r.getheader("Set-Cookie"),
                                      r.getheader("Location"))
                if r.will_close:
                    self.cerrar()
                break
            except self.REINTENTABLES as exc:
                # Conexión inactiva que el servidor ya cerró: el navegador
                # reintenta una vez con una conexión nueva, igual que aquí.
                self.cerrar()
                if reutilizada and intento == 0:
                    continue
                respuesta = Respuesta(0, {}, str(exc).encode(), time.perf_counter() - inicio)
                break
            except (OSError, http.client.HTTPException) as exc:
                self.cerrar()
                respuesta = Respuesta(0, {}, str(exc).encode(), time.perf_counter() - inicio)
                break
        if self.metricas is not None:
            self.metricas.agregar(etiqueta or ruta.split("?")[0], respuesta.estado, respuesta.segundos)
            if respuesta.estado == 0 or respuesta.estado >= 500:
                self.metricas.anotar_error(respuesta)
        return respuesta

    def formulario(self, ruta, datos, origen=None, cookie=None, etiqueta=None):
        cabeceras = {"Content-Type": "application/x-www-form-urlencoded",
                     "Origin": origen or self.origen, "Referer": self.origen + "/"}
        if cookie:
            cabeceras["Cookie"] = cookie
        return self.pedir("POST", ruta, urllib.parse.urlencode(datos).encode("utf-8"),
                          cabeceras, etiqueta)

    def validar(self, datos):
        return self.pedir("POST", "/api/validar", json.dumps(datos).encode("utf-8"),
                          {"Content-Type": "application/json", "Origin": self.origen})


def _galleta(respuesta):
    return respuesta.cookie.split(";")[0] if respuesta.cookie else None


def leer_notificacion(texto):
    """Categoría y texto de la notificación flotante (flash) de la página."""
    m = re.search(r'class="notificacion notificacion-(\w+)">\s*<p>(.*?)</p>', texto, re.S)
    return (m.group(1), html.unescape(m.group(2)).strip()) if m else (None, "")


def leer_errores(texto):
    bloque = re.search(r'class="resumen-errores".*?</ul>', texto, re.S)
    if not bloque:
        return []
    return [html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
            for x in re.findall(r"<li>(.*?)</li>", bloque.group(0), re.S)]


def leer_atributos(texto):
    """Longitudes máximas que la interfaz impone a los campos (maxlength y data-longitud)."""
    atributos = {}
    for campo in ("curp", "nss", "rfc", "fecha_movimiento"):
        m = re.search(r'<input[^>]*\bid="%s"[^>]*>' % campo, texto, re.S)
        etiqueta = m.group(0) if m else ""
        maximo = re.search(r'\bmaxlength="(\d+)"', etiqueta)
        longitud = re.search(r'\bdata-longitud="(\d+)"', etiqueta)
        atributos[campo] = {"maxlength": int(maximo.group(1)) if maximo else None,
                            "data-longitud": int(longitud.group(1)) if longitud else None}
    return atributos


def emular_navegador(datos, atributos):
    """
    Lo que realmente llega al servidor cuando el capturista pega o escribe el
    valor en la interfaz: primero el navegador recorta al maxlength del campo y
    después las máscaras de app.js limpian el valor (y recortan a data-longitud,
    si la plantilla la declara).
    """
    resultado = dict(datos)
    for campo in ("curp", "rfc", "nss", "fecha_movimiento"):
        if campo not in resultado:
            continue
        valor = str(resultado[campo])
        limite = atributos.get(campo, {})
        if limite.get("maxlength"):
            valor = valor[:limite["maxlength"]]
        if campo in ("nss", "fecha_movimiento"):
            valor = re.sub(r"\D", "", valor)
        else:
            valor = re.sub(r"[^A-ZÑ&0-9]", "", valor.upper())
        if limite.get("data-longitud"):
            valor = valor[:limite["data-longitud"]]
        resultado[campo] = valor
    if "nombre_completo" in resultado:
        resultado["nombre_completo"] = re.sub(r"\s+", " ", resultado["nombre_completo"]).strip()
    return resultado


def capturar(cliente, datos, validaciones=0, seguir=True):
    """
    Captura completa como la hace un capturista: validaciones en vivo al salir
    de cada campo, envío del formulario y lectura de la respuesta.
    """
    vivo = None
    for _ in range(validaciones):
        vivo = cliente.validar(datos).json()
    r = cliente.formulario("/capturar", datos, etiqueta="POST /capturar")
    resultado = {"estado": r.estado, "segundos": r.segundos, "categoria": None, "mensaje": "",
                 "errores": [], "vivo": vivo}
    if r.estado == 422:
        resultado["errores"] = leer_errores(r.texto)
    elif r.estado in (302, 303) and seguir:
        pagina = cliente.pedir("GET", "/", cabeceras={"Cookie": _galleta(r) or ""},
                               etiqueta="GET / (tras captura)")
        resultado["categoria"], resultado["mensaje"] = leer_notificacion(pagina.texto)
    return resultado


def clasificar(resultado):
    if resultado["estado"] == 422:
        return "bloqueado"
    if resultado["estado"] in (302, 303):
        return "avisado" if resultado["categoria"] == "warning" else "aceptado"
    if resultado["estado"] == 403:
        return "rechazado_403"
    return "falla"


# ==========================================================================
# Bloque A — Mes de operación simulado
# ==========================================================================
def bloque_a(modo):
    log("=" * 78)
    log("BLOQUE A — MES DE OPERACIÓN SIMULADO (3 capturistas)")
    log("=" * 78)
    plantilla = Plantilla(51)
    metricas = Metricas()
    with Servidor(modo) as srv:
        cliente_base = Cliente(srv.puerto, metricas=metricas)
        activos = [plantilla.trabajador() for _ in range(60)]
        nuevos = [plantilla.trabajador() for _ in range(25)]
        etapa_1 = [alta(t, dia_habil_atras(3)) for t in activos]
        salen = activos[:30]
        etapa_2 = ([baja(t, dia_habil_atras(2), causa=random.Random(i).choice("12"))
                    for i, t in enumerate(salen)]
                   + [alta(t, dia_habil_atras(2)) for t in nuevos])
        cierre = activos[30:50]
        reingresan = salen[:5]
        etapa_3 = ([baja(t, dia_habil_atras(1), causa="1") for t in cierre]
                   + [alta(t, dia_habil_atras(0)) for t in reingresan])
        etapas = [("Arranque de obras (altas)", etapa_1),
                  ("Rotación de cuadrillas (bajas y altas)", etapa_2),
                  ("Cierre de obra (bajas) y reingresos", etapa_3)]

        conteo = {"aceptado": 0, "avisado": 0, "bloqueado": 0, "falla": 0, "rechazado_403": 0}
        aceptados_por_usuario = []
        mensajes_rechazo = []
        exportados = 0
        inicio_total = time.perf_counter()
        candado = threading.Lock()
        for nombre, cola in etapas:
            pendientes = list(cola)
            random.Random(len(cola)).shuffle(pendientes)
            aceptados_etapa = [0]

            def capturista(usuario_id, semilla):
                azar = random.Random(semilla)
                cliente = Cliente(srv.puerto, metricas=metricas)
                while True:
                    with candado:
                        if not pendientes:
                            return
                        datos = dict(pendientes.pop(), usuario_id=usuario_id)
                    time.sleep(azar.uniform(0.05, 0.2))      # tiempo de lectura del aviso
                    r = capturar(cliente, datos, validaciones=5)
                    clase = clasificar(r)
                    with candado:
                        conteo[clase] += 1
                        if clase in ("aceptado", "avisado"):
                            aceptados_etapa[0] += 1
                            aceptados_por_usuario.append((datos["curp"], datos["tipo_movimiento"],
                                                          datos["fecha_movimiento"], usuario_id))
                        else:
                            mensajes_rechazo.append((datos["curp"], r["errores"] or r["mensaje"]))

            hilos = [threading.Thread(target=capturista, args=(u, s))
                     for u, s in (("2", 1), ("2", 2), ("1", 3))]
            inicio = time.perf_counter()
            for h in hilos:
                h.start()
            for h in hilos:
                h.join()
            duracion = time.perf_counter() - inicio
            antes = len(srv.lotes())
            r = cliente_base.formulario("/exportar", {"usuario_id": "1"}, etiqueta="POST /exportar")
            lotes = srv.lotes()
            lineas = 0
            if len(lotes) > antes:
                with open(lotes[-1], encoding="utf-8") as f:
                    lineas = sum(1 for linea in f if linea.strip())
            exportados += lineas
            log(f"  {nombre}: {len(cola)} movimientos en {duracion:.1f} s; "
                f"aceptados {aceptados_etapa[0]}; lote IDSE con {lineas} línea(s) "
                f"(HTTP {r.estado}).")
        total = time.perf_counter() - inicio_total

        conexion = srv.bd()
        cur = conexion.cursor()
        en_bd = cur.execute("SELECT COUNT(*) FROM movimiento").fetchone()[0]
        exportados_bd = cur.execute("SELECT COUNT(*) FROM movimiento WHERE estado='Exportado'").fetchone()[0]
        sin_bitacora = cur.execute(
            """SELECT COUNT(*) FROM movimiento m WHERE NOT EXISTS (
                 SELECT 1 FROM bitacora b WHERE b.movimiento_id = m.id
                 AND b.accion = 'Movimiento capturado')""").fetchone()[0]
        atribucion_erronea = 0
        for curp, tipo, fecha, usuario_id in aceptados_por_usuario:
            fila = cur.execute(
                """SELECT b.usuario_id FROM movimiento m JOIN trabajador t ON t.id = m.trabajador_id
                   JOIN bitacora b ON b.movimiento_id = m.id AND b.accion = 'Movimiento capturado'
                   WHERE t.curp = ? AND m.tipo_movimiento = ? AND m.fecha_movimiento = ?""",
                (curp, tipo, fecha)).fetchone()
            if not fila or str(fila[0]) != usuario_id:
                atribucion_erronea += 1
        conexion.close()

    movimientos = sum(len(c) for _, c in etapas)
    resumen = {
        "movimientos_enviados": movimientos, "duracion_s": round(total, 1),
        "capturas_por_minuto": round(movimientos / total * 60, 1), "clasificacion": conteo,
        "movimientos_en_bd": en_bd, "exportados_en_lotes": exportados,
        "exportados_en_bd": exportados_bd, "movimientos_sin_bitacora": sin_bitacora,
        "atribucion_erronea": atribucion_erronea, "fallas_http": metricas.errores(),
        "excepciones_servidor": srv.excepciones(),
        "latencias": {ruta: metricas.resumen(ruta) for ruta in
                      ("/api/validar", "POST /capturar", "GET / (tras captura)", "POST /exportar")},
        "rechazos_ejemplo": mensajes_rechazo[:5],
    }
    log(f"  Movimientos enviados: {movimientos} · aceptados {conteo['aceptado']} · con aviso "
        f"{conteo['avisado']} · bloqueados {conteo['bloqueado']} · fallas {conteo['falla']}")
    log(f"  En base: {en_bd} · exportados en lotes: {exportados} · sin asiento en bitácora: "
        f"{sin_bitacora} · atribución errónea: {atribucion_erronea}")
    for ruta, datos in resumen["latencias"].items():
        if datos.get("n"):
            log(f"  {ruta:<24} n={datos['n']:<5} p50={datos['p50_ms']} ms  p95={datos['p95_ms']} ms  "
                f"máx={datos['max_ms']} ms")
    if mensajes_rechazo:
        log(f"  Ejemplos de rechazo: {mensajes_rechazo[:3]}")
    log("")
    RESULTADOS["A"] = resumen


# ==========================================================================
# Bloque B — Errores típicos de captura
# ==========================================================================
def _cambiar_consonante(curp, azar):
    posicion = azar.choice([13, 14, 15])
    opciones = [c for c in "BCDFGHJKLMNPQRSTVWXYZ" if c != curp[posicion]]
    return curp[:posicion] + azar.choice(opciones) + curp[posicion + 1:]


def _transponer(nss, azar):
    while True:
        i = azar.randint(0, 8)
        a, b = nss[i], nss[i + 1]
        if a != b and {a, b} != {"0", "9"}:
            return nss[:i] + b + a + nss[i + 2:]


def _cambiar_digito(nss, azar):
    i = azar.randint(0, 9)
    return nss[:i] + azar.choice([d for d in "0123456789" if d != nss[i]]) + nss[i + 1:]


def _agrupar_nss(nss):
    return f"{nss[:2]} {nss[2:4]} {nss[4:6]} {nss[6:10]} {nss[10]}"


def _o_por_cero(curp):
    for i in range(4, 10):
        if curp[i] == "0":
            return curp[:i] + "O" + curp[i + 1:]
    return curp[:4] + "O" + curp[5:]


def _otra_fecha_rfc(t):
    rfc = t["rfc"]
    dia = int(rfc[8:10])
    nuevo = f"{(dia % 28) + 1:02d}"
    return rfc[:8] + nuevo + rfc[10:]


CATEGORIAS_B = [
    # (clave, descripción, esperado, constructor(t, azar) -> (preparación, intento))
    ("B01", "CURP y RFC en minúsculas con espacios a los lados", "aceptar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), curp=f"  {t['curp'].lower()} ",
                             rfc=f"{t['rfc'].lower()}  "))),
    ("B02", "CURP pegada con espacios internos", "aceptar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)),
                             curp=f"{t['curp'][:4]} {t['curp'][4:10]} {t['curp'][10:]}"))),
    ("B03", "NSS pegado con espacios de agrupación", "aceptar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), nss=_agrupar_nss(t["nss"])))),
    ("B04", "CURP con un carácter de menos", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), curp=t["curp"][:-1]))),
    ("B05", "Letra O en lugar de cero en la CURP", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), curp=_o_por_cero(t["curp"])))),
    ("B06", "CURP con una consonante equivocada (longitud correcta)", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), curp=_cambiar_consonante(t["curp"], az)))),
    ("B07", "NSS con dos dígitos transpuestos", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), nss=_transponer(t["nss"], az)))),
    ("B08", "NSS con un dígito equivocado", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), nss=_cambiar_digito(t["nss"], az)))),
    ("B09", "RFC con fecha distinta a la de la CURP", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), rfc=_otra_fecha_rfc(t)))),
    ("B10", "Nombre con un cero en lugar de la letra O", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)),
                             nombre_completo=t["nombre_completo"].replace("o", "0", 1)
                             if "o" in t["nombre_completo"] else t["nombre_completo"] + " 2"))),
    ("B11", "SDI con el punto decimal corrido (45.05 en vez de 450.50)", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), sdi=f"{float(t['sdi']) / 10:.2f}"))),
    ("B12", "SDI mayor al tope de 25 UMA", "detectar",
     lambda t, az: ([], dict(alta(t, dia_habil_atras(1)), sdi=f"{az.uniform(3200, 4200):.2f}"))),
    ("B13", "Alta sin condiciones de contratación", "detectar",
     lambda t, az: ([], {k: v for k, v in alta(t, dia_habil_atras(1)).items()
                         if k not in ("tipo_trabajador", "tipo_salario", "tipo_jornada")})),
    ("B14", "Baja sin causa de baja", "detectar",
     lambda t, az: ([alta(t, dia_habil_atras(3))],
                    {k: v for k, v in baja(t, dia_habil_atras(1)).items() if k != "causa_baja"})),
    ("B15", "Movimiento capturado fuera del plazo de 5 días hábiles", "detectar",
     lambda t, az: ([], alta(t, dia_habil_atras(az.randint(8, 15))))),
    ("B16", "Alta de un trabajador que ya tiene alta vigente (cambio de obra)", "detectar",
     lambda t, az: ([alta(t, dia_habil_atras(3))], alta(t, dia_habil_atras(1)))),
    ("B17", "Baja de un trabajador que ya fue dado de baja", "detectar",
     lambda t, az: ([alta(t, dia_habil_atras(4)), baja(t, dia_habil_atras(2))],
                    baja(t, dia_habil_atras(1), causa="2"))),
    ("B18", "Baja con fecha anterior a la de su alta", "detectar",
     lambda t, az: ([alta(t, dia_habil_atras(1))], baja(t, dia_habil_atras(3)))),
    ("B19", "Movimiento repetido (mismo trabajador, tipo y fecha)", "detectar",
     lambda t, az: ([alta(t, dia_habil_atras(2))], alta(t, dia_habil_atras(2)))),
]
CASOS_POR_CATEGORIA = 8
DEPENDEN_DEL_HISTORIAL = ("B14", "B16", "B17", "B18", "B19")


def bloque_b(modo):
    log("=" * 78)
    log("BLOQUE B — ERRORES TÍPICOS DE CAPTURA")
    log("=" * 78)
    plantilla = Plantilla(52)
    azar = random.Random(520)
    resultados = []
    with Servidor(modo) as srv:
        cliente = Cliente(srv.puerto)
        atributos = leer_atributos(cliente.pedir("GET", "/").texto)

        # Controles: movimientos limpios, para medir falsos positivos.
        controles = {"aceptado": 0, "avisado": 0, "bloqueado": 0, "falla": 0, "rechazado_403": 0}
        avisos_control = []
        for i in range(60):
            t = plantilla.trabajador()
            if i < 40:
                datos = alta(t, dia_habil_atras(i % 4))
            else:
                capturar(cliente, emular_navegador(alta(t, dia_habil_atras(4)), atributos))
                datos = baja(t, dia_habil_atras(i % 3), causa="2")
            r = capturar(cliente, emular_navegador(datos, atributos), validaciones=1)
            clase = clasificar(r)
            controles[clase] += 1
            if clase != "aceptado":
                avisos_control.append(r["mensaje"] or r["errores"])

        for clave, descripcion, esperado, constructor in CATEGORIAS_B:
            conteo = {"aceptado": 0, "avisado": 0, "bloqueado": 0, "falla": 0, "rechazado_403": 0}
            ejemplo = ""
            coincide_en_vivo = 0
            for _ in range(CASOS_POR_CATEGORIA):
                t = plantilla.trabajador()
                preparacion, intento = constructor(t, azar)
                for previo in preparacion:
                    capturar(cliente, emular_navegador(previo, atributos))
                enviado = emular_navegador(intento, atributos)
                r = capturar(cliente, enviado, validaciones=1)
                clase = clasificar(r)
                conteo[clase] += 1
                if r["vivo"] is not None and clave not in DEPENDEN_DEL_HISTORIAL:
                    # Coherencia: lo que la validación en vivo le dice al
                    # capturista frente a lo que decide el servidor al guardar.
                    # Las reglas de historial se excluyen: la validación en vivo
                    # revisa el formulario aislado, no la base de datos.
                    vivo_rechaza = not r["vivo"].get("valido", True)
                    coincide_en_vivo += int(vivo_rechaza == (clase == "bloqueado"))
                if not ejemplo:
                    ejemplo = "; ".join(r["errores"]) if r["errores"] else r["mensaje"]
            if esperado == "aceptar":
                correctos = conteo["aceptado"] + conteo["avisado"]
            else:
                correctos = conteo["bloqueado"] + conteo["avisado"]
            resultados.append({"clave": clave, "descripcion": descripcion, "esperado": esperado,
                               "n": CASOS_POR_CATEGORIA, **conteo, "correctos": correctos,
                               "coherencia_en_vivo": None if clave in DEPENDEN_DEL_HISTORIAL
                               else coincide_en_vivo,
                               "ejemplo": ejemplo[:300]})
            log(f"  {clave} {descripcion[:52]:<52} bloq={conteo['bloqueado']} "
                f"aviso={conteo['avisado']} acept={conteo['aceptado']} falla={conteo['falla']} "
                f"-> {'OK' if correctos == CASOS_POR_CATEGORIA else 'REVISAR'} ({correctos}/{CASOS_POR_CATEGORIA})")
            if ejemplo:
                log(f"        ejemplo: {ejemplo[:150]}")

        # Coherencia sin JavaScript: el formulario llega tal cual lo escribió el
        # usuario y la validación en vivo recibe exactamente el mismo texto.
        sin_js = []
        variantes = [("NSS con espacios de agrupación", lambda t: {"nss": _agrupar_nss(t["nss"])}),
                     ("CURP con espacios internos",
                      lambda t: {"curp": f"{t['curp'][:4]} {t['curp'][4:10]} {t['curp'][10:]}"}),
                     ("Fecha escrita con diagonales",
                      lambda t: {"fecha_movimiento": dia_habil_atras(1).strftime("%d/%m/%Y")})]
        for descripcion, cambio in variantes:
            t = plantilla.trabajador()
            datos = dict(alta(t, dia_habil_atras(1)), **cambio(t))
            vivo = cliente.validar(datos).json()
            r = capturar(cliente, datos)
            servidor_acepta = r["estado"] in (302, 303)
            sin_js.append({"variante": descripcion, "vivo_valido": bool(vivo.get("valido")),
                           "servidor_acepta": servidor_acepta,
                           "coherente": bool(vivo.get("valido")) == servidor_acepta})
            log(f"  Sin JavaScript · {descripcion}: validación en vivo "
                f"{'acepta' if vivo.get('valido') else 'rechaza'}, servidor "
                f"{'acepta' if servidor_acepta else 'rechaza'}")
        excepciones = srv.excepciones()

    detectables = [r for r in resultados if r["esperado"] == "detectar"]
    formato = [r for r in resultados if r["esperado"] == "aceptar"]
    total_det = sum(r["n"] for r in detectables)
    bloqueados = sum(r["bloqueado"] for r in detectables)
    avisados = sum(r["avisado"] for r in detectables)
    no_detectados = sum(r["aceptado"] for r in detectables)
    falsos_rechazos = sum(r["bloqueado"] for r in formato)
    resumen = {
        "categorias": resultados, "controles": controles, "avisos_en_controles": avisos_control[:5],
        "errores_inyectados": total_det, "bloqueados": bloqueados, "avisados": avisados,
        "no_detectados": no_detectados,
        "tasa_deteccion": round(100 * (bloqueados + avisados) / total_det, 1),
        "falsos_rechazos_formato": falsos_rechazos, "casos_formato": sum(r["n"] for r in formato),
        "falsos_positivos_controles": controles["bloqueado"] + controles["avisado"],
        "sin_javascript": sin_js, "excepciones_servidor": excepciones,
    }
    log("")
    log(f"  Errores inyectados: {total_det} · bloqueados {bloqueados} · avisados {avisados} · "
        f"no detectados {no_detectados} · detección {resumen['tasa_deteccion']} %")
    log(f"  Datos válidos con otro formato: {resumen['casos_formato']} · rechazados indebidamente "
        f"{falsos_rechazos}")
    log(f"  Controles limpios: {sum(controles.values())} · falsos positivos "
        f"{resumen['falsos_positivos_controles']} {avisos_control[:2] if avisos_control else ''}")
    log("")
    RESULTADOS["B"] = resumen


# ==========================================================================
# Bloque C — Capturas simultáneas del mismo movimiento
# ==========================================================================
def _par_simultaneo(puerto, datos_a, datos_b, desfase=0.0):
    barrera = threading.Barrier(2)
    salida = [None, None]

    def enviar(indice, datos, espera):
        cliente = Cliente(puerto)
        cliente._conexion = cliente._conectar()     # conexión lista: ambos envíos salen juntos
        barrera.wait()
        if espera:
            time.sleep(espera)
        salida[indice] = cliente.formulario("/capturar", datos).estado

    hilos = [threading.Thread(target=enviar, args=(0, datos_a, 0)),
             threading.Thread(target=enviar, args=(1, datos_b, desfase))]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    return salida


def bloque_c(modo):
    log("=" * 78)
    log("BLOQUE C — CAPTURAS SIMULTÁNEAS DEL MISMO MOVIMIENTO")
    log("=" * 78)
    plantilla = Plantilla(53)
    variantes = []
    with Servidor(modo) as srv:
        cliente = Cliente(srv.puerto)
        pruebas = [
            ("Trabajador nuevo: dos capturistas registran la misma alta", 25, "nuevo", 0.0),
            ("Reingreso: dos capturistas registran la misma alta de un trabajador conocido",
             25, "reingreso", 0.0),
            ("Doble envío del mismo capturista (40 ms de diferencia)", 10, "nuevo", 0.04),
        ]
        for descripcion, repeticiones, tipo, desfase in pruebas:
            conteo = {"ambos_aceptados": 0, "uno_aceptado": 0, "ninguno": 0, "con_5xx": 0}
            for _ in range(repeticiones):
                t = plantilla.trabajador()
                if tipo == "reingreso":
                    capturar(cliente, alta(t, dia_habil_atras(4)))
                    capturar(cliente, baja(t, dia_habil_atras(3)))
                datos = alta(t, dia_habil_atras(1))
                estados = _par_simultaneo(srv.puerto, dict(datos, usuario_id="1"),
                                          dict(datos, usuario_id="2"), desfase)
                aceptados = sum(1 for e in estados if e in (302, 303))
                if any(e == 0 or e >= 500 for e in estados):
                    conteo["con_5xx"] += 1
                if aceptados == 2:
                    conteo["ambos_aceptados"] += 1
                elif aceptados == 1:
                    conteo["uno_aceptado"] += 1
                else:
                    conteo["ninguno"] += 1
            variantes.append({"descripcion": descripcion, "repeticiones": repeticiones, **conteo})
            log(f"  {descripcion}: {repeticiones} pares · uno aceptado y otro rechazado "
                f"{conteo['uno_aceptado']} · ambos aceptados {conteo['ambos_aceptados']} · "
                f"pares con error 5xx {conteo['con_5xx']}")
        conexion = srv.bd()
        duplicados = conexion.execute(
            """SELECT COUNT(*) FROM (SELECT trabajador_id, tipo_movimiento, fecha_movimiento
               FROM movimiento GROUP BY 1, 2, 3 HAVING COUNT(*) > 1)""").fetchone()[0]
        conexion.close()
        excepciones = srv.excepciones()
    log(f"  Movimientos duplicados que quedaron en la base: {duplicados} · excepciones no "
        f"controladas en el servidor: {excepciones}")
    log("")
    RESULTADOS["C"] = {"variantes": variantes, "duplicados_en_bd": duplicados,
                       "excepciones_servidor": excepciones}


# ==========================================================================
# Bloque D — Carga
# ==========================================================================
NIVELES_CARGA = [1, 3, 5, 10, 20]
DURACION_NIVEL = 15


def bloque_d(modo):
    log("=" * 78)
    log(f"BLOQUE D — CARGA ({', '.join(map(str, NIVELES_CARGA))} usuarios, {DURACION_NIVEL} s por nivel)")
    log("=" * 78)
    plantilla = Plantilla(54)
    niveles = []
    with Servidor(modo) as srv:
        memoria_inicial = srv.memoria_mb()
        for usuarios in NIVELES_CARGA:
            metricas = Metricas()
            capturas = [0]
            rechazos = [0]
            candado = threading.Lock()
            limite = time.perf_counter() + DURACION_NIVEL

            def usuario(numero):
                cliente = Cliente(srv.puerto, metricas=metricas)
                while time.perf_counter() < limite:
                    datos = alta(plantilla.trabajador(), dia_habil_atras(1), usuario_id=str(1 + numero % 2))
                    for _ in range(3):
                        cliente.validar(datos)
                    r = cliente.formulario("/capturar", datos, etiqueta="POST /capturar")
                    cliente.pedir("GET", "/", etiqueta="GET /")
                    with candado:
                        if r.estado in (302, 303):
                            capturas[0] += 1
                        elif r.estado == 422:
                            rechazos[0] += 1

            hilos = [threading.Thread(target=usuario, args=(i,)) for i in range(usuarios)]
            inicio = time.perf_counter()
            for h in hilos:
                h.start()
            for h in hilos:
                h.join()
            duracion = time.perf_counter() - inicio
            total = len(metricas.registros)
            nivel = {
                "usuarios": usuarios, "peticiones": total,
                "peticiones_por_s": round(total / duracion, 1),
                "capturas": capturas[0], "capturas_por_min": round(capturas[0] / duracion * 60, 1),
                "rechazos_422": rechazos[0], "errores": metricas.errores(),
                "tasa_error_pct": round(100 * metricas.errores() / max(total, 1), 2),
                "validar": metricas.resumen("/api/validar"),
                "capturar": metricas.resumen("POST /capturar"),
                "tablero": metricas.resumen("GET /"),
                "memoria_mb": srv.memoria_mb(),
                "tipos_error": dict(sorted(metricas.tipos_error.items(), key=lambda x: -x[1])[:3]),
            }
            niveles.append(nivel)
            log(f"  {usuarios:>2} usuario(s): {nivel['peticiones_por_s']:>6} pet/s · "
                f"{nivel['capturas_por_min']:>6} capturas/min · validar p95 "
                f"{nivel['validar'].get('p95_ms')} ms · capturar p50/p95 "
                f"{nivel['capturar'].get('p50_ms')}/{nivel['capturar'].get('p95_ms')} ms · tablero p95 "
                f"{nivel['tablero'].get('p95_ms')} ms · errores {nivel['errores']} · "
                f"memoria {nivel['memoria_mb'] and round(nivel['memoria_mb'], 1)} MB")
        conexion = srv.bd()
        en_bd = conexion.execute("SELECT COUNT(*) FROM movimiento").fetchone()[0]
        conexion.close()
        excepciones = srv.excepciones()
    log(f"  Movimientos acumulados en la base al terminar: {en_bd} · excepciones: {excepciones}")
    log("")
    RESULTADOS["D"] = {"niveles": niveles, "memoria_inicial_mb": memoria_inicial,
                       "movimientos_en_bd": en_bd, "excepciones_servidor": excepciones,
                       "duracion_nivel_s": DURACION_NIVEL}


# ==========================================================================
# Bloque E — Volumen
# ==========================================================================
NIVELES_VOLUMEN = [1000, 5000, 10000]


def _precargar(ruta_bd, movimientos, plantilla, pendientes=500):
    """Inserta un historial ya exportado más `pendientes` movimientos por exportar."""
    conexion = sqlite3.connect(ruta_bd)
    cur = conexion.cursor()
    patron_id = cur.execute("SELECT id FROM patron LIMIT 1").fetchone()[0]
    marca = datetime.now().isoformat(sep=" ", timespec="seconds")
    filas_bitacora = []
    creados = 0
    while creados < movimientos:
        t = plantilla.trabajador()
        cur.execute("INSERT INTO trabajador (nombre_completo, curp, nss, rfc) VALUES (?, ?, ?, ?)",
                    (t["nombre_completo"], t["curp"], t["nss"], t["rfc"]))
        trabajador_id = cur.lastrowid
        historial = [("08", ddmmaaaa(dia_habil_atras(40)), "1"), ("02", ddmmaaaa(dia_habil_atras(20)), "")]
        for tipo, fecha, _ in historial:
            if creados >= movimientos:
                break
            estado = "Válido" if creados >= movimientos - pendientes else "Exportado"
            cur.execute(
                """INSERT INTO movimiento (trabajador_id, patron_id, tipo_movimiento, fecha_movimiento,
                       tipo_trabajador, tipo_salario, tipo_jornada, sdi, causa_baja, estado,
                       exportado, creado_en) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (trabajador_id, patron_id, tipo, fecha,
                 t["tipo_trabajador"] if tipo == "08" else "", "0" if tipo == "08" else "",
                 "1" if tipo == "08" else "", t["sdi"] if tipo == "08" else "",
                 "" if tipo == "08" else "1", estado, estado == "Exportado", marca))
            filas_bitacora.append((1, cur.lastrowid, "Movimiento capturado", "Precarga de volumen", marca))
            creados += 1
    cur.executemany("INSERT INTO bitacora (usuario_id, movimiento_id, accion, detalle, timestamp)"
                    " VALUES (?, ?, ?, ?, ?)", filas_bitacora)
    conexion.commit()
    conexion.close()


def bloque_e(modo):
    log("=" * 78)
    log(f"BLOQUE E — VOLUMEN ({', '.join(f'{n:,}' for n in NIVELES_VOLUMEN)} movimientos)")
    log("=" * 78)
    niveles = []
    for volumen in NIVELES_VOLUMEN:
        plantilla = Plantilla(55 + volumen)
        srv = Servidor(modo)
        try:
            srv.iniciar()
            srv.detener()
            _precargar(srv.base, volumen, plantilla)
            srv.iniciar()
            metricas = Metricas()
            cliente = Cliente(srv.puerto, metricas=metricas)
            apellido = urllib.parse.quote("Garza")
            for _ in range(20):
                cliente.pedir("GET", "/", etiqueta="tablero")
                cliente.pedir("GET", f"/?q={apellido}", etiqueta="busqueda")
                cliente.pedir("GET", f"/api/movimiento/{random.randint(1, volumen)}", etiqueta="detalle")
            for _ in range(10):
                cliente.pedir("GET", "/?estado=V%C3%A1lido&pagina=5", etiqueta="filtro")
                datos = alta(plantilla.trabajador(), dia_habil_atras(1))
                cliente.validar(datos)
                cliente.formulario("/capturar", datos, etiqueta="captura")
            r = cliente.formulario("/exportar", {"usuario_id": "1"}, etiqueta="exportacion")
            lineas = 0
            if srv.lotes():
                with open(srv.lotes()[-1], encoding="utf-8") as f:
                    lineas = sum(1 for linea in f if linea.strip())
            srv.detener()
            tamano = os.path.getsize(srv.base) / 1024 / 1024
            nivel = {"movimientos": volumen, "tamano_bd_mb": round(tamano, 2),
                     "arranque_s": round(srv.arranques[-1], 2),
                     "tablero": metricas.resumen("tablero"), "busqueda": metricas.resumen("busqueda"),
                     "filtro": metricas.resumen("filtro"), "detalle": metricas.resumen("detalle"),
                     "captura": metricas.resumen("captura"),
                     "exportacion_ms": round(r.segundos * 1000, 1), "lineas_exportadas": lineas,
                     "errores": metricas.errores(), "excepciones_servidor": srv.excepciones()}
            niveles.append(nivel)
            log(f"  {volumen:>6,} movimientos · base {nivel['tamano_bd_mb']} MB · tablero p50/p95 "
                f"{nivel['tablero'].get('p50_ms')}/{nivel['tablero'].get('p95_ms')} ms · búsqueda p95 "
                f"{nivel['busqueda'].get('p95_ms')} ms · detalle p95 {nivel['detalle'].get('p95_ms')} ms · "
                f"captura p95 {nivel['captura'].get('p95_ms')} ms · exportar {lineas} líneas en "
                f"{nivel['exportacion_ms']} ms · errores {nivel['errores']}")
        finally:
            srv.__exit__()
    log("")
    RESULTADOS["E"] = {"niveles": niveles}


# ==========================================================================
# Bloque F — Recuperación ante una caída del servidor
# ==========================================================================
def bloque_f(modo):
    log("=" * 78)
    log("BLOQUE F — CAÍDA ABRUPTA DEL SERVIDOR A MEDIA CAPTURA")
    log("=" * 78)
    plantilla = Plantilla(56)
    confirmados = []
    fallidos = [0]
    candado = threading.Lock()
    detener = threading.Event()
    srv = Servidor(modo)
    try:
        srv.iniciar()

        def usuario(numero):
            cliente = Cliente(srv.puerto)
            while not detener.is_set():
                datos = alta(plantilla.trabajador(), dia_habil_atras(1), usuario_id=str(1 + numero % 2))
                r = cliente.formulario("/capturar", datos)
                with candado:
                    if r.estado in (302, 303):
                        confirmados.append(datos["curp"])
                    elif r.estado == 0:
                        fallidos[0] += 1
                if r.estado == 0:
                    time.sleep(0.2)

        hilos = [threading.Thread(target=usuario, args=(i,)) for i in range(5)]
        for h in hilos:
            h.start()
        time.sleep(4)
        srv.detener()                      # equivalente a cerrar el proceso de golpe
        caida = time.perf_counter()
        time.sleep(1.5)
        detener.set()
        for h in hilos:
            h.join()
        srv.iniciar()
        recuperacion = time.perf_counter() - caida
        conexion = srv.bd()
        integridad = conexion.execute("PRAGMA integrity_check").fetchone()[0]
        curps = {fila[0] for fila in conexion.execute("SELECT curp FROM trabajador")}
        perdidos = sum(1 for curp in confirmados if curp not in curps)
        huerfanos = conexion.execute(
            """SELECT COUNT(*) FROM movimiento m WHERE NOT EXISTS (SELECT 1 FROM bitacora b
               WHERE b.movimiento_id = m.id AND b.accion = 'Movimiento capturado')""").fetchone()[0]
        conexion.close()
        sigue = Cliente(srv.puerto).pedir("GET", "/").estado
    finally:
        srv.__exit__()
    resumen = {"capturas_confirmadas_antes_de_la_caida": len(confirmados),
               "peticiones_sin_respuesta_durante_la_caida": fallidos[0],
               "capturas_confirmadas_perdidas": perdidos, "integridad": integridad,
               "movimientos_sin_bitacora": huerfanos,
               "tiempo_hasta_servicio_restablecido_s": round(recuperacion, 2),
               "arranque_tras_caida_s": round(srv.arranques[-1], 2),
               "estado_tras_reinicio": sigue}
    log(f"  Capturas confirmadas antes de la caída: {len(confirmados)} · peticiones sin respuesta "
        f"durante la caída: {fallidos[0]}")
    log(f"  Tras reiniciar: integridad '{integridad}' · confirmadas perdidas {perdidos} · movimientos "
        f"sin asiento en bitácora {huerfanos} · servicio restablecido en {resumen['tiempo_hasta_servicio_restablecido_s']} s")
    log("")
    RESULTADOS["F"] = resumen


# ==========================================================================
# Bloque G — Operación en red y seguridad
# ==========================================================================
CABECERAS_SEGURIDAD = ["x-content-type-options", "x-frame-options", "content-security-policy",
                       "referrer-policy"]


def bloque_g(modo):
    log("=" * 78)
    log("BLOQUE G — OPERACIÓN EN RED Y SEGURIDAD")
    log("=" * 78)
    plantilla = Plantilla(57)
    pruebas = []

    def registrar(clave, descripcion, resultado, seguro):
        pruebas.append({"clave": clave, "descripcion": descripcion, "resultado": resultado,
                        "seguro": seguro})
        log(f"  [{'OK' if seguro else 'HALLAZGO'}] {clave} {descripcion}: {resultado}")

    with Servidor(modo) as srv:
        cliente = Cliente(srv.puerto)
        portada = cliente.pedir("GET", "/")
        servidor = portada.cabeceras.get("server", "(sin cabecera)")
        registrar("G01", "Servidor HTTP que atiende las peticiones", servidor,
                  "werkzeug" not in servidor.lower())

        consola = cliente.pedir("GET", "/console")
        registrar("G02", "Consola de depuración de Werkzeug (/console)",
                  f"HTTP {consola.estado}" + (" · consola expuesta a la red" if consola.estado == 200 else ""),
                  consola.estado != 200)

        grande = cliente.pedir("GET", "/api/movimiento/99999999999999999999")
        filtra = "too large" in grande.texto or "Overflow" in grande.texto
        registrar("G03", "Folio fuera de rango en /api/movimiento",
                  f"HTTP {grande.estado}" + (" · muestra el detalle técnico del error" if filtra else ""),
                  grande.estado < 500 and not filtra)

        t = plantilla.trabajador()
        ajeno = cliente.formulario("/capturar", alta(t, dia_habil_atras(1)),
                                   origen="http://sitio-externo.example")
        registrar("G04", "Captura enviada desde otro sitio (Origin ajeno, CSRF)",
                  f"HTTP {ajeno.estado}" + (" · el movimiento se guardó" if ajeno.estado in (302, 303) else ""),
                  ajeno.estado not in (302, 303))

        inyeccion = cliente.pedir("GET", "/?q=" + urllib.parse.quote("' OR '1'='1"))
        sigue = cliente.pedir("GET", "/").estado == 200
        coincidencias = re.search(r"(\d+) registro\(s\)", inyeccion.texto)
        registrar("G05", "Inyección SQL en el buscador",
                  f"HTTP {inyeccion.estado} · {coincidencias.group(1) if coincidencias else '?'} resultados · "
                  f"tablas intactas: {'sí' if sigue else 'no'}",
                  inyeccion.estado == 200 and coincidencias and coincidencias.group(1) == "0" and sigue)

        t = plantilla.trabajador()
        r = cliente.formulario("/capturar", dict(alta(t, dia_habil_atras(1)),
                                                nombre_completo="<script>alert(1)</script> Pérez Luna"))
        pagina = cliente.pedir("GET", "/").texto if r.estado in (302, 303) else r.texto
        ejecutable = "<script>alert(1)</script>" in pagina
        registrar("G06", "Nombre con etiqueta <script>",
                  f"HTTP {r.estado} · " + ("se mostraría sin escapar" if ejecutable else "texto escapado, no se ejecuta"),
                  not ejecutable)

        faltan = [c for c in CABECERAS_SEGURIDAD if c not in portada.cabeceras]
        registrar("G07", "Cabeceras de seguridad HTTP",
                  "faltan: " + ", ".join(faltan) if faltan else "presentes: " + ", ".join(CABECERAS_SEGURIDAD),
                  not faltan)

        ip = ip_lan()
        lan = Cliente(srv.puerto, host=ip).pedir("GET", "/")
        registrar("G08", f"Acceso desde la red local ({ip})", f"HTTP {lan.estado}", True)
        excepciones = srv.excepciones()
    log("")
    RESULTADOS["G"] = {"pruebas": pruebas, "hallazgos": sum(1 for p in pruebas if not p["seguro"]),
                       "excepciones_servidor": excepciones}


# ==========================================================================
# Bloque H — Accesibilidad: contraste de la paleta (WCAG 2.1, criterio 1.4.3)
# ==========================================================================
def _luminancia(color):
    color = color.lstrip("#")
    canales = [int(color[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lineal = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lineal[0] + 0.7152 * lineal[1] + 0.0722 * lineal[2]


def contraste(a, b):
    la, lb = sorted((_luminancia(a), _luminancia(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


PARES_CONTRASTE = [
    ("Texto principal sobre tarjeta", "--texto", "--superficie"),
    ("Texto secundario sobre tarjeta", "--texto-suave", "--superficie"),
    ("Texto tenue (fechas, ayudas) sobre tarjeta", "--texto-tenue", "--superficie"),
    ("Texto tenue sobre fondo de página", "--texto-tenue", "--fondo"),
    ("Mensaje de error sobre su fondo", "--error", "--error-fondo"),
    ("Mensaje de aviso sobre su fondo", "--aviso", "--aviso-fondo"),
    ("Estado Exportado sobre su fondo", "--exito", "--exito-fondo"),
    ("Etiqueta informativa sobre su fondo", "--info", "--info-fondo"),
    ("Texto de botón sobre acento", "--acento-texto", "--acento"),
]


def bloque_h():
    log("=" * 78)
    log("BLOQUE H — CONTRASTE DE LA PALETA (WCAG 2.1, criterio 1.4.3, mínimo 4.5:1)")
    log("=" * 78)
    with open(os.path.join(CODIGO, "static", "css", "estilos.css"), encoding="utf-8") as f:
        css = f.read()
    temas = {"claro": css[css.find(":root {"):css.find("}", css.find(":root {"))]}
    inicio_oscuro = css.find(":root:not([data-tema=\"claro\"])")
    temas["oscuro"] = css[inicio_oscuro:css.find("}", inicio_oscuro)]
    filas = []
    for tema, bloque in temas.items():
        variables = dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})", bloque))
        for descripcion, frente, fondo in PARES_CONTRASTE:
            if frente in variables and fondo in variables:
                razon = contraste(variables[frente], variables[fondo])
                filas.append({"tema": tema, "par": descripcion, "frente": variables[frente],
                              "fondo": variables[fondo], "razon": round(razon, 2),
                              "cumple_aa": razon >= 4.5})
                log(f"  {tema:<7} {descripcion:<44} {variables[frente]} / {variables[fondo]} = "
                    f"{razon:.2f}:1 {'CUMPLE' if razon >= 4.5 else 'NO CUMPLE'}")
    log("")
    RESULTADOS["H"] = {"pares": filas, "incumplen": sum(1 for f in filas if not f["cumple_aa"])}


# ==========================================================================
# Ejecución
# ==========================================================================
BLOQUES = {"A": bloque_a, "B": bloque_b, "C": bloque_c, "D": bloque_d, "E": bloque_e,
           "F": bloque_f, "G": bloque_g, "H": lambda _modo: bloque_h()}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    global CODIGO
    por_defecto = "produccion" if os.path.exists(os.path.join(RAIZ, "servidor.py")) else "desarrollo"
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--codigo", default=RAIZ,
                        help="carpeta con otra versión del sistema (por ejemplo, la de la Entrega 4)")
    parser.add_argument("--servidor", choices=["produccion", "desarrollo"], default=por_defecto)
    parser.add_argument("--bloques", default="ABCDEFGH")
    parser.add_argument("--etiqueta", default="")
    argumentos = parser.parse_args()
    CODIGO = os.path.abspath(argumentos.codigo)

    sufijo = f"_{argumentos.etiqueta}" if argumentos.etiqueta else ""
    log("REPORTE DE RESULTADOS — VALIDACIÓN EN AMBIENTE RELEVANTE (ENTREGA 5 / TRL 5)")
    log("Sistema para la automatización de altas y bajas de seguro social")
    log(f"Fecha: {datetime.now():%d/%m/%Y %H:%M} · servidor: {argumentos.servidor} · "
        f"Python {sys.version.split()[0]} · {os.cpu_count()} núcleos lógicos")
    log("")
    RESULTADOS["meta"] = {"fecha": datetime.now().isoformat(timespec="seconds"),
                          "servidor": argumentos.servidor, "python": sys.version.split()[0],
                          "nucleos": os.cpu_count(), "etiqueta": argumentos.etiqueta,
                          "codigo": CODIGO}
    inicio = time.perf_counter()
    for clave in argumentos.bloques.replace(",", "").upper():
        BLOQUES[clave](argumentos.servidor)
    RESULTADOS["meta"]["duracion_total_s"] = round(time.perf_counter() - inicio, 1)
    log(f"Duración total: {RESULTADOS['meta']['duracion_total_s']} s")

    with open(os.path.join(RAIZ, f"resultados_ambiente_relevante{sufijo}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(REPORTE))
    with open(os.path.join(RAIZ, f"resultados_ambiente_relevante{sufijo}.json"), "w", encoding="utf-8") as f:
        json.dump(RESULTADOS, f, ensure_ascii=False, indent=2)
    print(f"\nReporte guardado en resultados_ambiente_relevante{sufijo}.txt y .json")


if __name__ == "__main__":
    main()
