---
tipo: operacion
tags: [verificacion, regresion, comparacion, main, arnes, refactor]
fuentes: ["pruebas/prueba_ambiente_relevante.py", "pruebas/test_prueba_concepto.py", "servidor.py"]
actualizado: 2026-10-04
---

# Verificar que un cambio funciona igual que `main`

Sirve para cambios que **no deberían alterar el comportamiento**: reorganizar carpetas, renombrar, limpiar código o
actualizar dependencias. Demuestra con datos que la versión nueva hace exactamente lo mismo que `main`. Se usó por
primera vez con la reorganización en `sigma/` ([[sesion-2026-10-04-estructura-de-carpetas]],
[[adr-017-paquete-sigma-y-carpeta-de-pruebas]]).

Para cambios que **sí** cambian el comportamiento (una regla nueva, una corrección) se usa la rutina normal de
[[estrategia-de-pruebas]], porque ahí las diferencias son esperadas.

## Resumen: cinco comprobaciones
| # | Qué | Cómo | Resultado esperado |
|---|---|---|---|
| 1 | Qué cambió de verdad | `git diff main -M --summary` | Los archivos movidos sin cambios salen con `(100%)` |
| 2 | Criterios del TRL 5 y resultados funcionales | Arnés del E5 sobre las dos versiones + `criterios_trl5.py` | 9/9 en las dos y **0 diferencias** |
| 3 | Regresión del E3 | El arnés del E3 en las dos versiones + `diff` | 8/8 en las dos (diferencias normales: ver trampas) |
| 4 | Respuestas HTTP | `verificar_contra_main.py` (lado a lado) | **18/18 idénticas** y el mismo lote IDSE |
| 5 | Que se vea bien | Chrome headless | Página completa en los dos temas, consola sin errores |

Los scripts van **fuera del repo** (Pedro no quiere herramientas extra en él): copia el bloque a un archivo en la
carpeta temporal y córrelo desde la raíz del repositorio. Los comandos son para Git Bash.

## 1. Qué cambió de verdad
```bash
git diff main -M --summary | grep rename    # (100%) = movido sin cambiar un byte
git diff main -M -U0 -- sigma/app.py        # en los demás, revisar que solo cambien imports y rutas
```

## 2. Arnés del E5 sobre las dos versiones
Una versión **después** de la otra, nunca a la vez, y sin otro trabajo pesado en la máquina: los tiempos se
afectan. Juntas tardan unos 5 minutos.
```bash
T=$(mktemp -d) && git archive main | tar -x -C "$T"          # copia limpia de main
python pruebas/prueba_ambiente_relevante.py --codigo "$T" --etiqueta main
python pruebas/prueba_ambiente_relevante.py --etiqueta rama
python criterios_trl5.py pruebas/resultados/resultados_ambiente_relevante_main.json \
                         pruebas/resultados/resultados_ambiente_relevante_rama.json
```
El arnés acepta con `--codigo` las dos estructuras del repo (la de `sigma/` y la anterior); ver
[[arnes-ambiente-relevante]].

`criterios_trl5.py` evalúa CA5-1 a CA5-9 ([[resultados-de-pruebas]]) y compara campo por campo todo lo que no es
tiempo: cada caso del bloque B con su mensaje, las carreras, la caída, la seguridad, el contraste y el volumen.

```python
"""Evalúa los criterios CA5-1 a CA5-9 en dos reportes JSON del arnés del E5 y
compara todo lo funcional (lo que no es tiempo) entre ellos.

Uso, desde la raíz del repositorio:
    python <ruta>\\criterios_trl5.py pruebas/resultados/resultados_ambiente_relevante_main.json ^
                                     pruebas/resultados/resultados_ambiente_relevante_rama.json
"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
ref, act = (json.load(open(r, encoding="utf-8")) for r in sys.argv[1:3])


def criterios(d):
    a, b, c, dd, e, f, g, h = (d[k] for k in "ABCDEFGH")
    n10 = next(n for n in dd["niveles"] if n["usuarios"] == 10)
    e10 = next(n for n in e["niveles"] if n["movimientos"] == 10000)
    cinco_xx = sum(v["con_5xx"] for v in c["variantes"])
    return [
        ("CA5-1 Operación nominal",
         a["clasificacion"]["aceptado"] == 140 and a["clasificacion"]["falla"] == 0
         and a["exportados_en_lotes"] == 140 and a["movimientos_sin_bitacora"] == 0
         and a["atribucion_erronea"] == 0 and a["fallas_http"] == 0,
         f'{a["clasificacion"]["aceptado"]}/140 aceptados, {a["exportados_en_lotes"]} al lote'),
        ("CA5-2 Tiempo de respuesta",
         a["latencias"]["POST /capturar"]["p95_ms"] <= 500 and a["latencias"]["/api/validar"]["p95_ms"] <= 200,
         f'captura p95 {a["latencias"]["POST /capturar"]["p95_ms"]} ms · validación p95 '
         f'{a["latencias"]["/api/validar"]["p95_ms"]} ms'),
        ("CA5-3 Detección de errores",
         b["tasa_deteccion"] >= 90 and b["falsos_positivos_controles"] == 0 and b["falsos_rechazos_formato"] == 0,
         f'{b["tasa_deteccion"]} % · falsos positivos {b["falsos_positivos_controles"]} · '
         f'rechazos indebidos {b["falsos_rechazos_formato"]}'),
        ("CA5-4 Capturas simultáneas", c["duplicados_en_bd"] == 0 and cinco_xx == 0,
         f'duplicados {c["duplicados_en_bd"]} · pares con 5xx {cinco_xx}'),
        ("CA5-5 Capacidad (10 usuarios)", n10["errores"] == 0 and n10["capturar"]["p95_ms"] <= 500,
         f'errores {n10["errores"]} · captura p95 {n10["capturar"]["p95_ms"]} ms'),
        ("CA5-6 Volumen (10,000)",
         e10["tablero"]["p95_ms"] <= 500 and e10["exportacion_ms"] <= 2000 and e10["errores"] == 0,
         f'tablero p95 {e10["tablero"]["p95_ms"]} ms · lote {e10["exportacion_ms"]} ms'),
        ("CA5-7 Recuperación",
         f["capturas_confirmadas_perdidas"] == 0 and f["integridad"] == "ok" and f["arranque_tras_caida_s"] <= 60,
         f'perdidas {f["capturas_confirmadas_perdidas"]} · integridad {f["integridad"]} · '
         f'arranque {f["arranque_tras_caida_s"]} s'),
        ("CA5-8 Seguridad en red", g["hallazgos"] == 0, f'{g["hallazgos"]} hallazgos en {len(g["pruebas"])} pruebas'),
        ("CA5-9 Accesibilidad", h["incumplen"] == 0, f'{len(h["pares"]) - h["incumplen"]}/{len(h["pares"])} pares'),
    ]


print(f'{"Criterio":<30} {"ref":<8} {"actual":<8} detalle (actual)')
for (nombre, ok_r, _), (_, ok_a, detalle) in zip(criterios(ref), criterios(act)):
    print(f'{nombre:<30} {"CUMPLE" if ok_r else "NO":<8} {"CUMPLE" if ok_a else "NO":<8} {detalle}')

# Todo lo que no es tiempo, memoria ni contador que dependa de la velocidad.
TIEMPO = ("_ms", "_s", "por_s", "por_min", "memoria", "latencias", "fecha", "codigo", "etiqueta", "tamano_bd",
          "peticiones", "capturas", "movimientos_en_bd", "rechazos_ejemplo", "validar", "capturar", "tablero",
          "busqueda", "filtro", "detalle", "captura", "tipos_error", "rechazos_422")
diferencias = []


def comparar(x, y, ruta):
    if isinstance(x, dict):
        for k in sorted(set(x) | set(y or {})):
            if not any(t in k for t in TIEMPO):
                comparar(x.get(k), (y or {}).get(k), f"{ruta}.{k}")
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (p, q) in enumerate(zip(x, y)):
            comparar(p, q, f"{ruta}[{i}]")
    elif x != y:
        diferencias.append((ruta, x, y))


comparar({k: ref[k] for k in "ABCEFGH"}, {k: act[k] for k in "ABCEFGH"}, "")
for nr, na in zip(ref["D"]["niveles"], act["D"]["niveles"]):
    if nr["errores"] != na["errores"]:
        diferencias.append((f'.D usuarios={nr["usuarios"]} errores', nr["errores"], na["errores"]))
print(f"\nDiferencias funcionales: {len(diferencias)}")
for ruta, p, q in diferencias:
    print(f"  {ruta}: ref={p!r}  actual={q!r}")
```

## 3. Arnés del E3 en las dos versiones
```bash
(cd "$T" && python test_prueba_concepto.py)       # main (estructura anterior: escribe junto al código)
python pruebas/test_prueba_concepto.py            # rama
diff <(sed -E 's/[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{8}/<FECHA>/g' "$T/resultados_prueba_concepto.txt") \
     <(sed -E 's/[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9:]{8}/<FECHA>/g' pruebas/resultados/resultados_prueba_concepto.txt)
```

## 4. Lado a lado por HTTP
`verificar_contra_main.py` levanta las dos versiones con `servidor.py` (puertos 5061 y 5062), cada una en una
carpeta temporal y con su **propia copia** de `sigma_imss.db`. Les hace las mismas 18 peticiones y compara las
respuestas. Al terminar borra la carpeta temporal: no toca la base real ni `exportaciones/`.

```python
"""Compara la versión actual de Sigma contra otra rama, lado a lado y por HTTP.

Levanta las dos versiones con servidor.py (waitress), cada una en su propia
carpeta temporal y con su propia copia de sigma_imss.db, les hace las mismas
peticiones y compara las respuestas normalizadas. No escribe nada en el repo.

Uso, desde la raíz del repositorio (guárdalo fuera del repo, p. ej. en %TEMP%):
    python <ruta>\\verificar_contra_main.py            # contra main
    python <ruta>\\verificar_contra_main.py otra-rama   # contra otra rama
"""
import http.cookiejar
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
REPO = os.getcwd()
REFERENCIA = sys.argv[1] if len(sys.argv) > 1 else "main"
TRABAJO = tempfile.mkdtemp(prefix="sigma_verificar_")

# --- Las dos versiones, cada una en su carpeta ---
VERSIONES = {REFERENCIA: (os.path.join(TRABAJO, "referencia"), 5061),
             "actual": (os.path.join(TRABAJO, "actual"), 5062)}
os.makedirs(VERSIONES[REFERENCIA][0])
archivo = subprocess.run(["git", "archive", REFERENCIA], cwd=REPO, capture_output=True, check=True).stdout
subprocess.run(["tar", "-x", "-C", VERSIONES[REFERENCIA][0]], input=archivo, check=True)
shutil.copytree(REPO, VERSIONES["actual"][0], ignore=shutil.ignore_patterns(
    ".git", "Obsidian", "pruebas", "instrucciones", "exportaciones", "*.db", "*.db-*", "__pycache__"))
base_real = os.path.join(REPO, "sigma_imss.db")
for nombre, (carpeta, _) in VERSIONES.items():
    if os.path.exists(base_real):                       # sin base real, cada una crea la suya vacía
        shutil.copy(base_real, os.path.join(carpeta, "sigma_imss.db"))

# --- Un trabajador nuevo y coherente (generador del arnés del E5) ---
sys.path[:0] = [os.path.join(REPO, "pruebas"), REPO]
import prueba_ambiente_relevante as arnes  # noqa: E402

t = arnes.Plantilla(20261004).trabajador()
ALTA = {"usuario_id": "1", "nombre_completo": t["nombre_completo"], "curp": t["curp"], "nss": t["nss"],
        "rfc": t["rfc"], "tipo_movimiento": "08", "fecha_movimiento": arnes.ddmmaaaa(arnes.dia_habil_atras(1)),
        "tipo_trabajador": "1", "tipo_salario": "0", "tipo_jornada": "1", "sdi": "450.50", "causa_baja": ""}
MALA = dict(ALTA, curp="LUSP99010", nss="1234ABC8901")


def normalizar(texto):
    """Quita lo que cambia en cada petición aunque el código sea el mismo."""
    texto = re.sub(r"nonce-[A-Za-z0-9_\-+/=]+", "nonce-X", texto)
    texto = re.sub(r'nonce="[^"]+"', 'nonce="X"', texto)
    texto = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?", "<ISO>", texto)
    texto = re.sub(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}(:\d{2})?", "<FECHA-HORA>", texto)
    texto = re.sub(r"lote_idse_\d{8}_\d{6}", "lote_idse_<TS>", texto)
    return re.sub(r"\b\d{2}:\d{2}(:\d{2})?\b", "<HORA>", texto)


class _SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


class Cliente:
    def __init__(self, puerto):
        self.base = f"http://127.0.0.1:{puerto}"
        self.abridor = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()), _SinRedireccion)

    def pedir(self, metodo, ruta, datos=None, cabeceras=None, como_json=False):
        cabeceras = dict(cabeceras or {})
        cuerpo = None
        if datos is not None and como_json:             # /api/validar recibe JSON, como lo manda app.js
            cuerpo = json.dumps(datos).encode()
            cabeceras["Content-Type"] = "application/json"
        elif datos is not None:
            cuerpo = urllib.parse.urlencode(datos).encode()
        req = urllib.request.Request(self.base + ruta, data=cuerpo, method=metodo, headers=cabeceras)
        try:
            r = self.abridor.open(req, timeout=15)
        except urllib.error.HTTPError as e:
            r = e
        # ETag: waitress lo calcula con la fecha del archivo, que cambia al copiar.
        cab = {k.lower(): normalizar(v) for k, v in r.headers.items()
               if k.lower() not in ("date", "content-length", "etag")}
        return r.status, cab, normalizar(r.read().decode("utf-8", "replace"))


# (título, método, ruta, datos, cabeceras, como_json)
PRUEBAS = [
    ("Pantalla principal", "GET", "/", None, None, False),
    ("Búsqueda y filtros", "GET", "/?q=GARZA&estado=Pendiente&tipo=08", None, None, False),
    ("CSS", "GET", "/static/css/estilos.css", None, None, False),
    ("JS", "GET", "/static/js/app.js", None, None, False),
    ("Página 404", "GET", "/no-existe", None, None, False),
    ("Detalle de movimiento 1", "GET", "/api/movimiento/1", None, None, False),
    ("Folio gigante", "GET", "/api/movimiento/99999999999999", None, None, False),
    ("Validación en vivo (válida)", "POST", "/api/validar", ALTA, None, True),
    ("Validación en vivo (con errores)", "POST", "/api/validar", MALA, None, True),
    ("Captura con errores (422)", "POST", "/capturar", MALA, None, False),
    ("Captura válida", "POST", "/capturar", ALTA, None, False),
    ("Pantalla tras la captura", "GET", "/", None, None, False),
    ("Misma captura otra vez", "POST", "/capturar", ALTA, None, False),
    ("Captura desde otro sitio (CSRF)", "POST", "/capturar", ALTA, {"Origin": "http://otro-sitio.example"}, False),
    ("Exportar lote", "POST", "/exportar", {"usuario_id": "1"}, None, False),
    ("Pantalla tras exportar", "GET", "/", None, None, False),
    ("Descargar lote", "GET", "/descargar-lote", None, None, False),
    ("Consola de depuración", "GET", "/console", None, None, False),
]

procesos = {}
try:
    for nombre, (carpeta, puerto) in VERSIONES.items():
        entorno = dict(os.environ, SIGMA_DB="sqlite", SQLITE_PATH=os.path.join(carpeta, "sigma_imss.db"),
                       SIGMA_PUERTO=str(puerto), SIGMA_HOST="127.0.0.1", SECRET_KEY="verificacion",
                       PYTHONIOENCODING="utf-8")
        entorno.pop("DATABASE_URL", None)
        procesos[nombre] = subprocess.Popen([sys.executable, "servidor.py"], cwd=carpeta, env=entorno,
                                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clientes = {n: Cliente(p) for n, (_, p) in VERSIONES.items()}
    for n, c in clientes.items():
        for _ in range(100):
            try:
                if c.pedir("GET", "/")[0] == 200:
                    break
            except OSError:
                time.sleep(0.1)
        else:
            raise RuntimeError(f"{n} no arrancó")

    iguales = 0
    for titulo, metodo, ruta, datos, cab, como_json in PRUEBAS:
        (er, hr, tr), (ea, ha, ta) = (clientes[n].pedir(metodo, ruta, datos, cab, como_json) for n in VERSIONES)
        ok = er == ea and hr == ha and tr == ta
        iguales += ok
        print(f"{'IGUAL' if ok else 'DISTINTO':<9} {ea}  {titulo}")
        if not ok:
            for k in sorted(set(hr) | set(ha)):
                if hr.get(k) != ha.get(k):
                    print(f"           cabecera {k}: {REFERENCIA}={hr.get(k)!r} actual={ha.get(k)!r}")
            for i, (a, b) in enumerate(zip(tr.splitlines(), ta.splitlines())):
                if a != b:
                    print(f"           línea {i + 1}: {a.strip()[:120]!r} vs {b.strip()[:120]!r}")
                    break
    print(f"\n{iguales}/{len(PRUEBAS)} respuestas idénticas entre {REFERENCIA} y la versión actual")
    lotes = {}
    for n, (carpeta, _) in VERSIONES.items():
        dir_lotes = os.path.join(carpeta, "exportaciones")
        nombres = sorted(os.listdir(dir_lotes)) if os.path.isdir(dir_lotes) else []
        lotes[n] = open(os.path.join(dir_lotes, nombres[-1]), encoding="utf-8").read() if nombres else None
    print(f"Lote IDSE idéntico: {lotes[REFERENCIA] == lotes['actual'] and lotes['actual'] is not None}")
finally:
    for p in procesos.values():
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
    time.sleep(0.5)
    shutil.rmtree(TRABAJO, ignore_errors=True)
```

## 5. Revisión visual con Chrome headless
Si la extensión de Chrome no está conectada, Chrome sin ventana basta. Con el servidor corriendo (por ejemplo
`SIGMA_PUERTO=5070 python servidor.py` sobre una copia de la base):
```bash
C="/c/Program Files/Google/Chrome/Application/chrome.exe"; P=$(mktemp -d)
# ¿Corrió app.js? El servidor manda title="Cambiar de tema"; app.js lo cambia al cargar.
"$C" --headless=new --disable-gpu --user-data-dir="$P" --enable-logging=stderr --v=0 \
     --virtual-time-budget=5000 --dump-dom http://127.0.0.1:5070/ 2> consola.txt | grep -o '<button[^>]*interruptor-tema[^>]*>'
grep -E "CONSOLE|Refused|Uncaught" consola.txt          # errores de JS o bloqueos de la CSP
# Capturas: tema claro (1) y oscuro (0)
"$C" --headless=new --disable-gpu --user-data-dir="$P" --hide-scrollbars --window-size=1400,1000 \
     --blink-settings=preferredColorScheme=1 --virtual-time-budget=5000 --screenshot=claro.png http://127.0.0.1:5070/
```

## Trampas (todas pasaron el 2026-10-04)
- **`/api/validar` recibe JSON**, como lo manda `app.js`. Si le mandas un formulario, responde que todo es
  obligatorio, porque no ve ningún dato. No es un bug ([[rutas-http]]).
- **`/exportar` exige `usuario_id`.** Sin él responde 302 con un mensaje de error y no genera lote.
- **El `ETag` de CSS y JS cambia** al copiar los archivos: waitress lo calcula con la fecha de modificación. Hay
  que ignorarlo; el contenido es lo que cuenta.
- **El nonce de la CSP y las horas** cambian en cada petición: se normalizan antes de comparar.
- **Ruta del lote en el E3:** la línea `Archivo generado:` dice `lote_idse_prueba.txt` en `main` y
  `pruebas\resultados\lote_idse_prueba.txt` en la estructura nueva. Es esperado.
- **Bloque 3 del E3:** cuál capturista recibe el id 3 y cuál el 4 cambia entre corridas, porque los dos hilos
  arrancan a la vez. Con `main` también pasa.
- **El p95 con 20 usuarios varía** de una corrida a otra (de 146 a 218 ms con el mismo código). Los criterios
  tienen margen de sobra (≤ 500 ms), pero no compares tiempos de corridas de días distintos.
- **Chrome headless hereda el modo oscuro de Windows.** Para la captura clara usa
  `--blink-settings=preferredColorScheme=1`.
- **`git mv` de una carpeta falla con "Permission denied"** si VS Code la tiene abierta: mueve los archivos uno
  por uno o cierra VS Code.

## Resultado de referencia (2026-10-04, reorganización en `sigma/`)
9/9 criterios del E5 y 8/8 del E3 en las dos versiones; 0 diferencias funcionales; 18/18 respuestas idénticas y el
mismo lote IDSE; página sin errores de consola en los dos temas.

Ver también: [[estrategia-de-pruebas]] · [[guia-para-modificar-el-codigo]] · [[arnes-ambiente-relevante]]
