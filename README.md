# Sigma — Prueba de Concepto (TRL 3)

Sistema para la automatización de altas y bajas de seguro social ante el IMSS.
Captura validada, persistencia relacional, exportación al formato IDSE y
bitácora de auditoría, en una aplicación cliente-servidor.

## Requisitos

- Python 3.9 o superior
- `pip install -r requirements.txt`
- PostgreSQL **opcional** (ver "Motor de base de datos")

```bash
pip install -r requirements.txt
python app.py
```

Abrir <http://localhost:5050>.

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
| `SIGMA_DB` | `postgres` o `sqlite` para forzar un motor |
| `SQLITE_PATH` | Ruta del archivo `.db` cuando se usa SQLite |
| `SECRET_KEY` | Clave de sesión de Flask (en desarrollo se genera sola) |

```powershell
# PowerShell — usar PostgreSQL
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"
python app.py
```

```bash
# bash / macOS / Linux
export DATABASE_URL="postgresql://usuario:password@localhost:5432/sigma_imss"
python app.py
```

Con PostgreSQL hay que crear la base vacía una sola vez (`createdb sigma_imss`).
Las tablas y los usuarios semilla se crean automáticamente en el primer arranque
con cualquiera de los dos motores.

## Estructura

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Controlador HTTP: rutas, flujo, manejo de errores, API interna |
| `validaciones.py` | Validación algorítmica y reglas de negocio (fuente única de verdad) |
| `database.py` | Persistencia relacional y selección de motor |
| `exportar_idse.py` | Traducción de movimientos al lote de texto plano IDSE |
| `templates/` | Vistas Jinja (`base.html`, `index.html`, `error.html`) |
| `static/css/estilos.css` | Sistema de diseño y temas claro/oscuro |
| `static/js/app.js` | Validación en vivo, máscaras de captura, tema y detalle |
| `test_prueba_concepto.py` | Arnés de pruebas del "Desarrollo experimental" |

## Validaciones aplicadas

Bloquean el guardado:

- **CURP** — 18 caracteres con el formato oficial y fecha de nacimiento existente.
- **NSS** — exactamente 11 dígitos.
- **RFC** — 12 o 13 caracteres; debe coincidir en iniciales y fecha con la CURP.
- **Fecha del movimiento** — formato `DDMMAAAA` y fecha real del calendario.
- **Tipo de movimiento** — solo `08` (alta/reingreso) o `02` (baja).
- **Alta (08)** — tipo de trabajador, de salario, de jornada y SDI obligatorios.
- **Baja (02)** — causa de baja obligatoria, tomada del catálogo IDSE.
- **Integridad** — no se permite repetir NSS entre trabajadores, ni capturar dos
  veces el mismo movimiento (mismo trabajador, tipo y fecha).

Se muestran como aviso, sin bloquear:

- Dígito verificador del NSS que no cuadra con el algoritmo de Luhn.
- Fecha de movimiento a más de un año en el futuro o con más de cinco de antigüedad.

El mismo módulo `validaciones.py` atiende el envío del formulario y la
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
| `/` | GET | Pantalla principal, con filtros y paginación |
| `/capturar` | POST | Valida y guarda un movimiento |
| `/exportar` | POST | Genera el lote IDSE con los movimientos pendientes |
| `/descargar-lote` | GET | Descarga el último lote generado |
| `/api/validar` | POST | Validación en vivo (JSON) |
| `/api/movimiento/<id>` | GET | Detalle de un movimiento y su bitácora (JSON) |

Los lotes se guardan en `exportaciones/` con marca de tiempo, de modo que un
lote nuevo nunca sobrescribe a uno anterior.

## Pruebas automáticas

```bash
python test_prueba_concepto.py
```

Ejecuta los tres bloques del "Desarrollo experimental" (validación, exportación
y concurrencia) y genera `resultados_prueba_concepto.txt` con el detalle de los
8 casos de prueba, el contenido del lote y la verificación de la bitácora.

El arnés trabaja sobre su propia base (`sigma_pruebas.db`), que se borra al
iniciar, para que los resultados sean reproducibles y no se mezclen con lo
capturado desde la interfaz web.

## Notas

- El motor PostgreSQL puede sustituirse por otro compatible con `psycopg2` sin
  tocar la lógica de negocio, ya que solo se usa SQL estándar.
- La estructura de columnas del archivo IDSE en `exportar_idse.py` debe
  confirmarse contra el layout oficial vigente del IMSS antes de usarse en un
  entorno real.
- El servidor de desarrollo de Flask no es apto para producción; para un
  despliegue real hay que usar un servidor WSGI (gunicorn, waitress) y fijar
  `SECRET_KEY`.

### UnicodeDecodeError al conectar con PostgreSQL en Windows

Si el sistema está en español, `libpq` traduce sus mensajes de error con una
codificación distinta de UTF-8 y `psycopg2` truena al *leer* el mensaje, en vez
de mostrar el error real. `database.py` fuerza `LC_ALL=C` y `LANG=C` al
importarse para evitarlo y dejar ver la causa verdadera.
