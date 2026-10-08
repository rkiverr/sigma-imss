# Sigma — Sistema integrado y demostrado en ambiente relevante (TRL 6)

Sistema para la automatización de altas y bajas de seguro social ante el IMSS.
Captura validada, persistencia relacional, lote IDSE con la estructura oficial
del IMSS, inicio de sesión con roles, bitácora de auditoría y respaldo
automático, en una aplicación cliente-servidor para la red local de la oficina.

## Requisitos

- Python 3.9 o superior
- `pip install -r requirements.txt`
- PostgreSQL **opcional** (ver "Motor de base de datos"). `requirements.txt`
  instala el controlador `psycopg2-binary`; si no hay servidor PostgreSQL,
  Sigma usa SQLite.

```bash
pip install -r requirements.txt
python -m sigma.usuarios contrasena admin.rrhh      # primera vez: contraseñas
python -m sigma.usuarios contrasena captura.obra1
python servidor.py      # modo producción (waitress), accesible desde la red local
```

Abrir <http://localhost:5050> (o `http://<IP del servidor>:5050` desde otra PC
de la oficina) e iniciar sesión. Los usuarios se administran con
`python -m sigma.usuarios` (`listar`, `crear`, `contrasena`, `activar`,
`desactivar`, `desbloquear`). El rol `captura` captura y consulta; el rol
`administrador` además genera y descarga los lotes IDSE.

`python -m sigma` arranca el servidor de **desarrollo** de Flask: solo escucha
en el propio equipo y la depuración queda apagada salvo con `SIGMA_DEBUG=1`. No
se usa en la oficina, porque con depuración activa publica una consola y el
detalle técnico de los errores a toda la red.

Todos los comandos se corren desde la raíz del repositorio (la carpeta
`sigma-imss`).

## Motor de base de datos

La capa de persistencia elige el motor sola, al arrancar:

| Situación | Motor usado |
|---|---|
| Hay un PostgreSQL accesible y `psycopg2` instalado | **PostgreSQL** |
| No hay servidor, o falta `psycopg2` | **SQLite** (archivo `sigma_imss.db`) |

Toda la lógica de negocio usa SQL estándar, así que el comportamiento es el
mismo en ambos casos. El motor activo se muestra en la barra superior de la
interfaz.

Variables de entorno para controlarlo:

| Variable | Para qué sirve |
|---|---|
| `DATABASE_URL` | Cadena de conexión de PostgreSQL |
| `SIGMA_DB` | `postgres` o `sqlite` para forzar un motor. En un equipo sin PostgreSQL, `sqlite` evita 1 s de espera en cada arranque |
| `SQLITE_PATH` | Ruta del archivo `.db` cuando se usa SQLite |
| `SECRET_KEY` | Clave de sesión; sin ella se crea y reutiliza `.clave_sesion` |
| `SIGMA_SESION_HORAS` | Duración de la sesión (por defecto 10 horas) |
| `SIGMA_MAX_PETICION_KB` | Tamaño máximo de una petición (por defecto 1024 KB) |
| `SIGMA_RESPALDOS` | Carpeta de respaldos (por defecto `respaldos/`; mejor otro disco) |
| `SIGMA_RESPALDO_HORAS` | Cada cuántas horas respalda `servidor.py` (por defecto 24) |
| `SIGMA_RESPALDOS_CONSERVAR` | Cuántos respaldos se guardan (por defecto 30) |
| `SIGMA_HOST` / `SIGMA_PUERTO` | Interfaz y puerto de escucha (por defecto `0.0.0.0:5050` en `servidor.py`) |
| `SIGMA_HILOS` | Peticiones simultáneas que atiende waitress (por defecto 8) |
| `SIGMA_DEBUG` | `1` para activar la depuración en `python -m sigma` |

```powershell
# PowerShell — usar PostgreSQL
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py
```

```bash
# bash / macOS / Linux
export DATABASE_URL="postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py
```

Con PostgreSQL hay que crear la base vacía una sola vez (`createdb sigma_imss`).
Las tablas y los usuarios semilla se crean automáticamente en el primer arranque
con cualquiera de los dos motores.

## Estructura

```
sigma-imss/
├── servidor.py              arranque en producción (waitress)
├── requirements.txt
├── sigma/                   la aplicación (paquete de Python)
│   ├── __init__.py
│   ├── __main__.py          servidor de desarrollo (python -m sigma)
│   ├── app.py               rutas HTTP, flujo, seguridad por petición, errores
│   ├── validaciones.py      validación algorítmica y reglas de negocio
│   ├── plazo.py             plazo legal de cinco días hábiles
│   ├── database.py          persistencia relacional y selección de motor
│   ├── exportar_idse.py     lote IDSE con la estructura oficial (168 posiciones)
│   ├── usuarios.py          contraseñas, sesión y consola de usuarios
│   ├── respaldo.py          respaldo y restauración de la base
│   ├── templates/           vistas Jinja (base, index, login, error)
│   └── static/              css/estilos.css y js/app.js
├── pruebas/                 arneses de prueba
│   ├── test_prueba_concepto.py        Entrega 3
│   ├── prueba_ambiente_relevante.py   Entrega 5
│   ├── prueba_integracion.py          Entrega 6
│   └── resultados/          lo que generan los arneses (no se versiona)
├── instrucciones/           guías de uso para personas
├── Obsidian/                segundo cerebro del proyecto
├── sigma_imss.db            base de trabajo con SQLite (no se versiona)
├── exportaciones/           lotes IDSE generados (no se versiona)
└── respaldos/               respaldos automáticos de la base (no se versiona)
```

| Archivo | Responsabilidad |
|---|---|
| `servidor.py` | Arranque en modo producción con waitress |
| `sigma/app.py` | Controlador HTTP: rutas, flujo, manejo de errores, API interna |
| `sigma/__main__.py` | Servidor de desarrollo de Flask (`python -m sigma`) |
| `sigma/validaciones.py` | Validación algorítmica y reglas de negocio (fuente única de verdad) |
| `sigma/plazo.py` | Plazo legal de cinco días hábiles (art. 15 LSS, descansos del art. 74 LFT) |
| `sigma/database.py` | Persistencia relacional y selección de motor |
| `sigma/exportar_idse.py` | Lote IDSE con la estructura oficial del IMSS: 168 posiciones, un archivo por tipo |
| `sigma/usuarios.py` | Contraseñas, inicio de sesión, bloqueo y consola de usuarios |
| `sigma/respaldo.py` | Respaldo automático y restauración de la base |
| `sigma/templates/` | Vistas Jinja (`base.html`, `index.html`, `login.html`, `error.html`) |
| `sigma/static/css/estilos.css` | Sistema de diseño y temas claro/oscuro |
| `sigma/static/js/app.js` | Validación en vivo, máscaras de captura, tema y detalle |
| `pruebas/test_prueba_concepto.py` | Arnés de pruebas del "Desarrollo experimental" (Entrega 3) |
| `pruebas/prueba_ambiente_relevante.py` | Arnés de validación en ambiente relevante (Entrega 5) |
| `pruebas/prueba_integracion.py` | Arnés de integración y demostración (Entrega 6) |
| `instrucciones/` | Guías para personas: comandos rápidos, instalación y uso de la página |
| `Obsidian/` | Segundo cerebro del proyecto en Markdown (se abre como bóveda de Obsidian): entregables, normativa, decisiones, pruebas e historial |

## Validaciones aplicadas

Bloquean el guardado:

- **Nombre** — apellido paterno y nombre(s) obligatorios, materno opcional; hasta
  27 caracteres cada uno (como en el lote del IMSS); solo letras (con acentos y
  ñ), espacios, punto, guion y apóstrofo.
- **CURP** — 18 caracteres con el formato oficial y fecha de nacimiento existente.
- **NSS** — exactamente 11 dígitos.
- **RFC** — 12 o 13 caracteres; debe coincidir en iniciales y fecha con la CURP.
- **Fecha del movimiento** — formato `DDMMAAAA` y fecha real del calendario.
- **Tipo de movimiento** — solo `08` (alta/reingreso) o `02` (baja).
- **Alta (08)** — tipo de trabajador, de salario, de jornada (catálogo oficial:
  0 = normal, 1 a 5 = días de semana reducida, 6 = jornada reducida), SDI y
  unidad de medicina familiar obligatorios.
- **SDI** — no menor al salario mínimo general vigente (art. 28 LSS).
- **Baja (02)** — causa de baja obligatoria, tomada del catálogo IDSE.
- **Integridad** — no se permite repetir NSS entre trabajadores, ni capturar dos
  veces el mismo movimiento (mismo trabajador, tipo y fecha). Una restricción
  `UNIQUE` en la base lo garantiza también cuando dos capturas llegan a la vez.
- **Historial** — no se acepta un alta de quien ya tiene alta vigente, la baja de
  quien ya fue dado de baja, ni una baja anterior a su alta.

Se muestran como aviso, sin bloquear:

- Dígito verificador del NSS que no cuadra con el algoritmo de Luhn.
- Dígito verificador de la CURP que no cuadra con el algoritmo de RENAPO.
- Iniciales de la CURP que no corresponden a los apellidos y el nombre capturados.
- Movimiento de un año cuyos montos legales todavía no están cargados.
- SDI por encima del tope de 25 UMA (en el lote IDSE se exporta el tope).
- Movimiento fuera del plazo legal de cinco días hábiles, o en su último día.
- Baja de un trabajador sin alta registrada en Sigma.
- Fecha de movimiento a más de un año en el futuro o con más de cinco de antigüedad.

El mismo módulo `sigma/validaciones.py` atiende el envío del formulario y la
retroalimentación en vivo (`POST /api/validar`), así que la ayuda visual del
navegador nunca puede desviarse de la regla real que aplica el servidor.

## Interfaz

- Tablero con el conteo de movimientos, pendientes, exportados, altas y bajas.
- Validación en vivo campo por campo, con máscaras de captura y contadores.
- Selector de fecha nativo que rellena el campo `DDMMAAAA` que exige el IDSE.
- Los campos de alta y de baja se muestran según el tipo de movimiento elegido.
- Búsqueda por nombre, CURP o NSS, con filtros por estado y tipo, y paginación.
- Detalle del expediente y su bitácora al seleccionar una fila.
- Tema claro y oscuro: sigue el sistema operativo y se puede fijar con el botón
  de la barra superior; la elección se recuerda entre visitas.
- Funciona sin JavaScript: el formulario se envía y el servidor valida igual.

## Rutas

| Ruta | Método | Descripción |
|---|---|---|
| `/login` | GET / POST | Inicio de sesión |
| `/logout` | POST | Cierre de sesión (invalida también las copias de la cookie) |
| `/` | GET | Pantalla principal, con filtros y paginación |
| `/capturar` | POST | Valida y guarda un movimiento |
| `/exportar` | POST | Genera los lotes IDSE (altas y bajas por separado); solo administración |
| `/descargar-lote?tipo=altas` o `bajas` | GET | Descarga el último lote de ese tipo; solo administración |
| `/api/validar` | POST | Validación en vivo (JSON) |
| `/api/movimiento/<id>` | GET | Detalle de un movimiento y su bitácora (JSON) |

Todas las rutas, salvo `/login`, piden sesión: la página redirige al inicio de
sesión y la API responde 401. Los lotes se guardan en `exportaciones/` con el
tipo y la marca de tiempo (`lote_idse_altas_AAAAMMDD_HHMMSS.txt`), de modo que
un lote nuevo nunca sobrescribe a uno anterior.

## Pruebas automáticas

```bash
python pruebas/test_prueba_concepto.py
```

Ejecuta los tres bloques del "Desarrollo experimental" (validación, exportación
y concurrencia) y genera `pruebas/resultados/resultados_prueba_concepto.txt`
con el detalle de los 8 casos de prueba, el contenido del lote y la
verificación de la bitácora.

El arnés trabaja sobre su propia base (`pruebas/resultados/sigma_pruebas.db`),
que se borra al iniciar, para que los resultados sean reproducibles y no se
mezclen con lo capturado desde la interfaz web.

```bash
python pruebas/prueba_ambiente_relevante.py
```

Prueba el sistema completo en condiciones semejantes a las de la empresa (unos
3 minutos): varios capturistas concurrentes, errores típicos de captura,
carreras, carga, volumen, caída del servidor, seguridad en red y contraste.
Cada bloque corre sobre una copia aislada del sistema y genera
`pruebas/resultados/resultados_ambiente_relevante.txt` y `.json`.

```bash
python pruebas/prueba_integracion.py
```

Demuestra el sistema integrado (Entrega 6, cerca de un minuto): escenario de
una semana por la IP de la red local con inicio de sesión y roles, conformidad
del lote con la estructura oficial del IMSS campo por campo, seguridad
(autenticación, bloqueo, cookie, métodos, rutas, tamaño, tráfico), respaldo y
restauración tras perder la base, y tamaños y tiempos de cada enlace.

## Documentación

| Para | Dónde |
|---|---|
| Levantar la página en dos minutos | [`instrucciones/README.md`](instrucciones/README.md) |
| Instalación, PostgreSQL y problemas frecuentes | [`instrucciones/Ejecutar.md`](instrucciones/Ejecutar.md) |
| Qué hace la página y cómo se usa | [`instrucciones/Instrucciones.md`](instrucciones/Instrucciones.md) |
| Decisiones de diseño, bugs corregidos y comandos (para programar) | [`CLAUDE.md`](CLAUDE.md) |
| Contexto completo: entregables, normativa, ADR, pruebas e historial | [`Obsidian/index.md`](Obsidian/index.md) |

## Notas

- El motor PostgreSQL puede sustituirse por otro compatible con `psycopg2` sin
  tocar la lógica de negocio, ya que solo se usa SQL estándar.
- El lote sigue la estructura publicada por el IMSS ("Estructura de Movimientos
  afiliatorios", 168 posiciones). La codificación (Windows-1252), el fin de
  línea (CRLF) y la Ñ se confirman cargando un lote de prueba en el IDSE. Antes
  de operar hay que poner el registro patronal y la guía reales de la empresa.
- En la oficina se usa `python servidor.py` (waitress): respalda la base al
  arrancar y cada 24 horas. Conviene que `SIGMA_RESPALDOS` apunte a otro disco.
- Falta HTTPS en la red local: la sesión y los datos viajan sin cifrar.
- Los montos del salario mínimo y de la UMA viven en `sigma/validaciones.py`
  (`SALARIO_MINIMO_GENERAL`, `UMA_DIARIA`) y deben actualizarse cada año.

### UnicodeDecodeError al conectar con PostgreSQL en Windows

Si el sistema está en español, `libpq` traduce sus mensajes de error con una
codificación distinta de UTF-8 y `psycopg2` truena al *leer* el mensaje, en vez
de mostrar el error real. `sigma/database.py` fuerza `LC_ALL=C` y `LANG=C` al
importarse para evitarlo y dejar ver la causa verdadera.
