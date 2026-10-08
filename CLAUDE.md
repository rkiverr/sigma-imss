# CLAUDE.md — Contexto del proyecto Sigma

Guía para cualquier sesión futura de Claude Code sobre este repositorio.
Documenta **qué es el proyecto, cómo está construido y por qué se tomó cada
decisión**, para no volver a deducirlo desde cero.

> **Segundo cerebro: `Obsidian/`.** Es el contexto completo del proyecto en
> Markdown: entregables, normativa, módulos, reglas, decisiones (ADR), pruebas,
> bugs y el historial de sesiones. Al empezar, lee `Obsidian/index.md` y
> `Obsidian/wiki/inicio.md`. Las reglas para mantenerlo están en
> `Obsidian/CLAUDE.md`: `raw/` no se edita y, si el wiki y el código no
> coinciden, manda el código. Si cambias el código, actualiza las páginas que
> indica su mapa de impacto y agrega una entrada al final de `Obsidian/log.md`.

---

## 1. Qué es

**Sigma** es un sistema para automatizar las altas y bajas de trabajadores ante
el IMSS. Es un trabajo académico (Entregas 1 a 6 de un informe por niveles TRL),
no un producto en producción. Nació como prueba de concepto (TRL 3), se integró
como prototipo (TRL 4), en la Entrega 5 se validó en ambiente relevante (TRL 5)
y en la Entrega 6 se integró y demostró como sistema completo (TRL 6): lote
IDSE con la estructura oficial, inicio de sesión con roles y respaldo
automático.

**Ramas.**
- `main` es la publicada y es la vigente. Desde el 2026-10-08 incluye el TRL 6 (avance
  rápido hasta `7fffd1c`): lote IDSE oficial, inicio de sesión con roles, respaldo
  automático y rediseño del login. `trl6/correcciones` ya está integrada.
  Después de hacer `git pull`, cada copia debe fijar contraseñas con
  `python -m sigma.usuarios contrasena <usuario>`.
- Desde el 2026-10-04 incluye la Entrega 5 (el merge
  `cffd375` integró los 7 commits de `trl5/ambiente-relevante`) y la
  reorganización en carpetas (merge `fb3a4a8`: la app en `sigma/` y los
  arneses en `pruebas/`).
- `trl5/ambiente-relevante` sigue publicada porque el informe la cita. Conserva
  la estructura anterior, con todo en la raíz, que es la que describe el
  informe del E5.
- La rama de la reorganización (`mejora/estructura-de-carpetas`, PR #2) se
  integró directo a `main` a petición de Pedro y después se borró. La página
  del PR #2 conserva sus commits.
- `mejora/interfaz-y-validaciones` es la versión de la Entrega 4 (PR #1).

El flujo completo que implementa:

```
Captura en formulario  →  Validación algorítmica  →  Base de datos relacional
                                                   →  Lote de texto plano IDSE
                                                   →  Bitácora de auditoría
```

**Idioma del proyecto: español.** Nombres de funciones, variables, comentarios,
docstrings, mensajes de error y textos de interfaz van todos en español, con
acentos correctos. Es documentación académica y se lee así.

---

## 2. Arquitectura

Aplicación Flask cliente-servidor, sin dependencias de frontend. La aplicación
es el paquete `sigma/`; los arneses viven en `pruebas/`. En el resto de este
archivo los módulos se nombran sin carpeta (`app.py` = `sigma/app.py`).

| Archivo | Responsabilidad |
|---|---|
| `servidor.py` | Arranque en producción con waitress (el que se usa en la oficina) |
| `sigma/__main__.py` | Servidor de desarrollo (`python -m sigma`) |
| `sigma/app.py` | Rutas HTTP, flujo, reglas de historial, seguridad por petición, errores |
| `sigma/plazo.py` | Plazo legal de 5 días hábiles (art. 15 LSS; descansos art. 74 LFT) |
| `sigma/validaciones.py` | Validación algorítmica y reglas de negocio |
| `sigma/database.py` | Persistencia relacional y selección de motor |
| `sigma/exportar_idse.py` | Lote IDSE con la estructura oficial del IMSS (168 posiciones, un archivo por tipo) |
| `sigma/usuarios.py` | Contraseñas, inicio de sesión, bloqueo y consola de usuarios (`python -m sigma.usuarios`) |
| `sigma/respaldo.py` | Respaldo y restauración de la base (`python -m sigma.respaldo`) |
| `sigma/templates/base.html` | Esqueleto: barra, tema, notificaciones, pie |
| `sigma/templates/index.html` | Pantalla principal (hereda de `base.html`) |
| `sigma/templates/login.html` | Inicio de sesión |
| `sigma/templates/error.html` | Página de error 400 / 403 / 404 / 405 / 413 / 500 / 503 |
| `sigma/static/css/estilos.css` | Sistema de diseño completo, temas claro y oscuro |
| `sigma/static/js/app.js` | Validación en vivo, máscaras, tema, diálogo de detalle |
| `pruebas/test_prueba_concepto.py` | Arnés de pruebas del "Desarrollo experimental" (E3) |
| `pruebas/prueba_ambiente_relevante.py` | Arnés de validación en ambiente relevante (E5) |
| `pruebas/prueba_integracion.py` | Arnés de integración y demostración (E6): escenario, lote, seguridad, respaldo, red |

Lo que se genera al usar el sistema no se versiona: `sigma_imss.db`,
`exportaciones/`, `respaldos/` y `.clave_sesion` en la raíz (fuera del paquete, a propósito: es la base y los
lotes de trabajo), y `pruebas/resultados/` para todo lo que producen los
arneses.

⚠️ Dentro de `sigma/` los imports son **relativos** (`from .database import …`,
`from . import plazo`). Por eso `sigma/app.py` ya no se ejecuta directo: el
servidor de desarrollo es `python -m sigma`.

Modelo de datos (5 tablas normalizadas + `migracion`):
`patron` (con `guia`), `usuario` (con `password_hash`, `activo`,
`intentos_fallidos`, `bloqueado_hasta`, `sesion_token`), `trabajador` (con
`apellido_paterno`, `apellido_materno`, `nombres`; `nombre_completo` se deriva),
`movimiento` (con `umf`), `bitacora`. `migracion` registra las conversiones de
datos ya aplicadas.

---

## 3. Decisiones de diseño y su porqué

### 3.1 Doble motor de base de datos (PostgreSQL + SQLite)

`database.py` decide el motor **una sola vez al arrancar**:

1. Si `SIGMA_DB=sqlite` → SQLite.
2. Si `psycopg2` está instalado y hay un servidor accesible → PostgreSQL.
3. En cualquier otro caso → SQLite, con un aviso en consola.

**Por qué:** el proyecto declara PostgreSQL como motor objetivo (Alternativa 3
de la Entrega 2), pero en la máquina de desarrollo no había PostgreSQL ni
`psycopg2`, así que la app no arrancaba. El respaldo a SQLite permite ejecutar y
demostrar el prototipo en cualquier equipo sin perder el argumento del SGBD
relacional.

**Cómo funciona sin duplicar la lógica:** toda la capa superior escribe SQL
estándar con marcadores `%s` (estilo psycopg2). Para SQLite hay dos envoltorios
(`_ConexionSQLite`, `_CursorSQLite`) que traducen `%s` → `?` al vuelo. Solo el
DDL está duplicado (`_DDL_POSTGRES` / `_DDL_SQLITE`), porque `SERIAL` y
`INTEGER PRIMARY KEY AUTOINCREMENT` no son intercambiables.

⚠️ **Si agregas SQL nuevo, escríbelo con `%s`, nunca con `?`.** El traductor va
en un solo sentido.

⚠️ Las marcas de tiempo se guardan como **texto ISO** (`database.ahora()`), no
como objetos `datetime`. Python 3.12+ deprecó los adaptadores de fecha de
sqlite3 y una cadena ISO funciona igual en la columna `TIMESTAMP` de PostgreSQL.
Al leer, el filtro `momento` de Jinja acepta ambos tipos.

### 3.2 Un solo validador para servidor y navegador

`validaciones.validar_campos()` es la única fuente de verdad. La ruta
`POST /api/validar` la expone tal cual, y `sigma/static/js/app.js` la consume para dar
retroalimentación inmediata.

**Por qué:** si el navegador tuviera su propia copia de las reglas, las dos se
desincronizarían en cuanto alguien cambiara una. Así es imposible. La validación
del cliente es solo ayuda visual; la que manda es la del servidor.

`validar_movimiento()` se conserva con su firma original `(bool, list[str])`
porque `test_prueba_concepto.py` depende de ella.

### 3.3 Errores y avisos son cosas distintas

- **Errores** → bloquean el guardado. Diccionario indexado por campo, para que
  la interfaz marque exactamente el campo a corregir.
- **Avisos** → se muestran pero dejan pasar el movimiento.

Son avisos (no errores) a propósito:
- **Dígito verificador del NSS (Luhn).** Existen NSS históricos emitidos antes
  de que el dígito se estandarizara; bloquearlos impediría capturar movimientos
  legítimos.
- **Fechas lejanas** (más de un año al futuro o cinco de antigüedad).

### 3.4 El formulario conserva lo capturado al fallar

`POST /capturar` con errores **no redirige**: responde `422` renderizando
`index.html` con `form=datos`, `errores` y `avisos`. La versión original
redirigía y el usuario perdía todo lo escrito.

### 3.5 Lotes IDSE con marca de tiempo

Los lotes van a `exportaciones/lote_idse_<AAAAMMDD_HHMMSS>.txt`. Antes se
escribía siempre `lote_idse.txt` y cada exportación pisaba la anterior.
`/descargar-lote` sirve el más reciente por fecha de modificación.

### 3.6 Frontend sin dependencias externas

Cero CDN, cero frameworks. CSS y JS propios. **Por qué:** el prototipo debe
poder demostrarse sin internet, y meter una dependencia externa a un trabajo
académico agrega superficie de fallo sin aportar nada.

Todo es progresivo: sin JavaScript el formulario se envía y el servidor valida
igual. Las máscaras, la validación en vivo y el diálogo de detalle son mejoras,
no requisitos.

### 3.7 Tema claro / oscuro

Tres estados: sin elección (manda el sistema operativo), `data-tema="claro"`,
`data-tema="oscuro"`. Los colores viven en variables CSS declaradas tres veces:
`:root` (claro), `@media (prefers-color-scheme: dark) :root:not([data-tema="claro"])`
y `:root[data-tema="oscuro"]`, para que el botón gane en ambas direcciones.

Un script en línea en el `<head>` de `base.html` aplica el tema guardado **antes
de pintar**, para que no haya parpadeo blanco al cargar en modo oscuro.

Mientras el usuario no toque el botón no se escribe nada en `localStorage`: así
la página sigue al sistema operativo. Solo la elección explícita se persiste.

### 3.8 Paleta

Azul marino. Se cambió desde el verde original porque las tarjetas se perdían
contra un fondo verdoso de bajo contraste. El fondo es azul grisáceo y las
tarjetas blancas puras; ese contraste es lo que las despega.

Colores de las métricas: navy (total), ámbar (pendientes), teal (exportados),
azul cielo (altas), gris azulado (bajas). Cada tarjeta lleva franja lateral de
color y un velo del mismo tono al 4.5%.

### 3.9 Producción con waitress, depuración solo a petición (Entrega 5)

`python servidor.py` sirve la app con waitress en `0.0.0.0:5050` y cabecera
`Server: Sigma`. `python -m sigma` es solo para programar: escucha en 127.0.0.1 y
`debug` se activa únicamente con `SIGMA_DEBUG=1`. **Por qué:** con `debug=True`
en `0.0.0.0`, como estaba, la consola de Werkzeug (`/console`) y el detalle
técnico de cada error 500 quedaban visibles para toda la red de la oficina.

### 3.10 Seguridad por petición

- `before_request`: un POST cuyo `Origin` (o `Referer`) no sea el propio host
  recibe 403 → frena CSRF desde otra página. Sin ninguna de las dos cabeceras
  se deja pasar (clientes que no son navegador).
- `after_request`: CSP con **nonce** por petición (el único script en línea es
  el del tema, en `base.html`, y lleva `nonce="{{ csp_nonce }}"`; si agregas
  otro script en línea, necesita el nonce o el navegador lo bloquea),
  `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`.
- `/api/movimiento/<id>` responde 404 si el id rebasa `FOLIO_MAXIMO` (antes un
  id gigante tumbaba la consulta con 500).

### 3.11 Reglas de historial afiliatorio

`app._validar_historial()` usa `database.estado_afiliatorio()` (último
movimiento por fecha real): alta sobre alta vigente → error; baja de quien ya
fue dado de baja → error; baja o reingreso con fecha anterior al movimiento
previo → error; baja sin historial en Sigma → **aviso** (personal anterior a la
puesta en marcha). Es el problema del E1: el Excel no distinguía cambio de obra
de salida de la empresa.

### 3.12 Unicidad del movimiento en la base

Índice `UNIQUE(trabajador_id, tipo_movimiento, fecha_movimiento)`, creado
aparte en `init_db()` (si la base ya trae duplicados, solo avisa). En
`/capturar`, `ERRORES_DE_INTEGRIDAD` (sqlite3 o psycopg2) → rollback + 422.
**Por qué:** dos capturistas que guardan el mismo movimiento a la vez pasan
ambos la revisión previa; en las pruebas quedaban duplicados y errores 500.

### 3.13 Límites legales del SDI y plazo

- `SALARIO_MINIMO_GENERAL` y `UMA_DIARIA` en `validaciones.py` (**actualizar
  cada año**; la UMA rige desde el 1 de febrero). SDI < salario mínimo → error;
  SDI > 25 UMA → aviso, y `exportar_idse` lleva al lote el SDI topado.
- Plazo: aviso si el movimiento está VENCIDO o POR_VENCER; si está en plazo, el
  mensaje de éxito dice la fecha límite. Los descansos del art. 74 LFT se
  calculan por año en `plazo.dias_de_descanso()`, y el arnés tiene una copia
  (`_descansos()`): **si cambias uno, cambia el otro**. La transmisión del
  Ejecutivo es el 1 de octubre de 2024, 2030… (`anio % 6 == 2`). Las jornadas
  electorales (fr. IX) se agregan a mano en `DIAS_INHABILES_ADICIONALES`.
- Dígito verificador de la CURP (RENAPO) como **aviso**. Ojo: con pesos
  módulo 10 no detecta todos los cambios de una letra (en las pruebas, 4 de 8).

### 3.14 Normalización única y longitudes sin maxlength

`validaciones.normalizar_datos()` la usan `/capturar` **y** `/api/validar`
(antes la API no quitaba espacios del NSS ni diagonales de la fecha y decía
"error" donde el servidor aceptaba). Los campos CURP/NSS/RFC/fecha usan
`data-longitud` en lugar de `maxlength`: `app.js` limpia y **después** recorta.
Con `maxlength`, pegar "4316 89 1234 5" perdía dígitos.

### 3.15 Inicio de sesión, roles y token de sesión (TRL 6)

- `usuarios.py`: contraseñas con `werkzeug.security` (scrypt), bloqueo de 15 min
  tras 5 intentos fallidos, mensaje genérico. Roles: `captura` captura y
  consulta; `administrador` además genera y descarga lotes (`@requiere_rol`).
- `before_request`: sin sesión, la página va a `/login` y la API responde 401.
  El usuario de la bitácora sale de `g.usuario`; **ya no hay selector de
  usuario** (regresaba a admin en cada recarga y atribuía mal las capturas).
- La sesión vive en la cookie firmada de Flask, así que borrar la cookie no
  basta: la sesión lleva un `token` que también está en `usuario.sesion_token`.
  Cerrar sesión, cambiar la contraseña o desactivar al usuario lo borra y toda
  copia de la cookie deja de servir. Varias PC con la misma cuenta comparten el
  token (`abrir_sesion()` reutiliza el vigente).
- Clave de sesión: `SECRET_KEY` o, si no hay, `.clave_sesion` (se crea una vez),
  para que reiniciar el servidor no cierre las sesiones.

### 3.16 Lote IDSE con la estructura oficial (TRL 6)

`exportar_idse.ESTRUCTURA` transcribe, campo por campo, el PDF del IMSS
"Estructura de Movimientos afiliatorios": registros de 168 posiciones, un
archivo por tipo (`lote_idse_altas_…` / `lote_idse_bajas_…`), Windows-1252 y
CRLF. Apellido paterno, materno y nombre(s) en 27 posiciones cada uno; SBC en 6
dígitos con 2 decimales implícitos (topado a 25 UMA); jornada con el catálogo
oficial (0 = normal, 1–5 días, 6 = reducida); UMF; guía del patrón
(`patron.guia`, semilla `00000`); clave del trabajador = su id; "9" final. En la
baja, la causa va en la 149 y la CURP en blanco. `generar_linea_idse()` afirma
las 168 posiciones. ⚠️ Codificación, CRLF y Ñ se confirman con un lote de
prueba en el IDSE.

### 3.17 Respaldo automático (TRL 6)

`servidor.py` respalda **antes** de `init_db()` (protege los datos antes de
migrar) y deja un hilo cada `SIGMA_RESPALDO_HORAS`. SQLite: API `backup` →
`journal_mode = DELETE` (un solo archivo) → `integrity_check`; rotación de
`SIGMA_RESPALDOS_CONSERVAR`. PostgreSQL: `pg_dump` si existe (no probado aquí).
`--restaurar` guarda antes una copia de la base actual.

### 3.18 Migraciones de datos

`init_db()` agrega las columnas que falten (`_COLUMNAS_NUEVAS`) y aplica una sola
vez cada migración de `_MIGRACIONES` (queda en la tabla `migracion`): jornada
`1→0` y `2→6` (avisa de los `3`/`4`), y separación del nombre con
`separar_nombre()`, que elige la división que reproduce las iniciales de la
CURP. Si agregas una migración, dale una clave nueva; nunca cambies una ya
aplicada.

---

## 4. Bugs que ya se corrigieron — no reintroducir

| Bug original | Corrección |
|---|---|
| CURP repetida con otro NSS reventaba con `IntegrityError` → 500 | `conflicto_de_identidad()` verifica **antes** del INSERT |
| `usuario_id` vacío o no numérico → `ValueError` → 500 | `_usuario_valido()` valida contra la tabla `usuario` |
| `/descargar-lote` sin archivo → excepción | Comprueba existencia y avisa |
| Excepción a media captura dejaba la conexión abierta | Context manager `conexion(commit=True)` |
| Tabla `patron` vacía → `TypeError` en `fetchone()["id"]` | `obtener_patron_id()` la crea si falta |
| Formulario rechazado perdía lo capturado | Se re-renderiza con los valores |
| El interruptor mostraba "Claro" y "Oscuro" a la vez | Faltaba ocultar `.etiqueta-oscuro` por defecto |
| La insignia del patrón desbordaba en móvil | `max-width` + `overflow: hidden`, oculta bajo 720px |
| (E5) Consola de depuración expuesta a la LAN | `servidor.py` + debug solo con `SIGMA_DEBUG=1` |
| (E5) Captura simultánea: duplicados y 500 por `IntegrityError` | Índice único + rollback y 422 |
| (E5) Captura aceptada desde otro sitio (CSRF) | Verificación de `Origin`/`Referer` → 403 |
| (E5) Id gigante en `/api/movimiento` → 500 con detalle técnico | `FOLIO_MAXIMO` → 404 |
| (E5) Pegar CURP/NSS con espacios recortaba el dato | `data-longitud` + máscara que recorta al final |
| (E5) `/api/validar` normalizaba distinto que el servidor | `normalizar_datos()` compartida |
| (E5) SDI 45.05 (punto corrido) se aceptaba | Mínimo = salario mínimo general |
| (E5) Alta sobre alta vigente, doble baja, baja anterior al alta | Reglas de historial |
| (E5) "La causa de baja es obligatorio" | Mensaje de catálogo sin concordancia de género |
| (E5) Texto tenue 3.15:1 (no cumple WCAG AA) | `--texto-tenue: #5c6b84` (5.4:1) |
| Feriado de transmisión del Ejecutivo el 1 de dic con `anio % 6 == 0` (regla anterior a la reforma de la LFT de 2024) | 1 de oct con `anio % 6 == 2`, en `plazo.py` y en el arnés |
| (E6) Catálogo de jornada propio: 1 = normal, que el IMSS lee como "un día a la semana" | Catálogo oficial 0–6 y migración |
| (E6) Lote con campos separados por `|`, sin apellidos, UMF ni guía, altas y bajas juntas | Estructura oficial de 168 posiciones, un archivo por tipo |
| (E6) Sin inicio de sesión; selector de usuario que volvía a admin.rrhh | Login con roles; el usuario sale de la sesión |
| (E6) `GET /capturar` (y TRACE/PUT/DELETE) → 500 "El movimiento no se guardó" | `errorhandler` respeta las `HTTPException` (405, 413, 400) |
| (E6) Sin límite de tamaño de petición | `MAX_CONTENT_LENGTH` (`SIGMA_MAX_PETICION_KB`, 1 MB) → 413 |
| (E6) `requirements.txt` no instalaba psycopg2 en Python 3.13+ | `psycopg2-binary>=2.9.11` sin marcador |
| (E6) Sin `SECRET_KEY`, cada reinicio cerraba sesiones | `.clave_sesion` persistente |
| (E6) Cookie de sesión válida después de cerrar sesión | Token de sesión en la base |
| (E6) La exportación no quedaba en el historial de cada movimiento | Asiento "Incluido en lote IDSE" por movimiento |
| (E6) Sin respaldo de la base | `respaldo.py` + respaldo al arrancar y periódico |
| (E6) Con psycopg2 instalado y sin PostgreSQL, cada arranque esperaba 4 s ("localhost" por IPv6 e IPv4) | `DATABASE_URL` por omisión con `127.0.0.1` y `connect_timeout=1` (1 s); `SIGMA_DB=sqlite` lo evita |

---

## 5. Comandos

Siempre desde la raíz del repositorio:

```bash
python servidor.py                          # producción (waitress) en http://0.0.0.0:5050
python -m sigma                             # desarrollo, solo 127.0.0.1 (SIGMA_DEBUG=1 para depurar)
python pruebas/test_prueba_concepto.py      # arnés del E3 → pruebas/resultados/
python pruebas/prueba_ambiente_relevante.py # arnés del E5 (~3 min) → pruebas/resultados/
python pruebas/prueba_ambiente_relevante.py --codigo <carpeta> --servidor desarrollo --etiqueta antes
python pruebas/prueba_integracion.py        # arnés del E6 (~1 min); --capturas guarda el HTML de las pantallas
python -m sigma.usuarios contrasena admin.rrhh   # asignar contraseña (también: listar, crear, desactivar…)
python -m sigma.respaldo                    # respaldo manual; --restaurar ARCHIVO con el servidor detenido
```

**Primer arranque con una base nueva o migrada:** nadie tiene contraseña, así
que hay que asignarlas con `python -m sigma.usuarios contrasena <usuario>`
(la página de inicio de sesión lo recuerda).

Para demostrar que un cambio **no** altera el comportamiento (reorganizar,
renombrar, limpiar), compara contra `main` con el método de
`Obsidian/wiki/operacion/verificar-un-cambio-contra-main.md`: el arnés en las
dos versiones, los criterios CA5, el lado a lado por HTTP y Chrome headless.

Variables de entorno: `DATABASE_URL`, `SIGMA_DB`, `SQLITE_PATH`, `SECRET_KEY`,
`SIGMA_HOST`, `SIGMA_PUERTO`, `SIGMA_HILOS`, `SIGMA_DEBUG`, `SIGMA_SESION_HORAS`,
`SIGMA_MAX_PETICION_KB`, `SIGMA_RESPALDOS`, `SIGMA_RESPALDO_HORAS`,
`SIGMA_RESPALDOS_CONSERVAR`.

Desde el TRL 6, el arnés del E5 asigna contraseñas de prueba en cada copia
aislada y su `Cliente` inicia sesión con el `usuario_id` del formulario; con
`--codigo` de una versión sin `sigma/usuarios.py` funciona como antes
(`version_trl6()`). `alta()`/`baja()` mandan el nombre completo y separado y la
UMF, para servir a las dos versiones.

El arnés del E5 copia el sistema a un directorio temporal por bloque (no toca
`sigma_imss.db` ni `exportaciones/`). Emula al navegador: aplica `maxlength` /
`data-longitud` leídos de la página y las máscaras de `app.js`; si cambias las
máscaras, actualiza `emular_navegador()`. Con `--codigo` acepta versiones con
cualquiera de las dos estructuras: la de `sigma/` y la anterior, con todo en la
raíz (E3 a E5); `codigo_en_paquete()` decide cuál.

El arnés del E3 usa su propia base (`pruebas/resultados/sigma_pruebas.db`), que
borra al iniciar, para que los resultados sean reproducibles y no se mezclen con
lo capturado desde la web. Fija `SQLITE_PATH` **antes** de importar
`sigma.database`, porque ese módulo lee la configuración al cargarse, y agrega
la raíz a `sys.path` para encontrar el paquete.

---

## 6. Estado verificado

Probado por HTTP: altas, bajas, duplicados, conflictos de identidad,
exportación, descarga, 404, inyección SQL y XSS. Sin errores en el log.

Arnés de pruebas: **8/8 casos, los tres bloques CUMPLE.**

Reorganización en `sigma/` y `pruebas/` (04/10/2026, merge `fb3a4a8`),
verificada contra el `main` anterior con el mismo arnés: 10/10 criterios del TRL 5 en las dos versiones, 0
diferencias en los resultados funcionales y 18/18 respuestas HTTP idénticas
(mismo HTML, CSS, JS, mensajes y lote IDSE) sobre una copia de la base real.

Arnés de ambiente relevante (04/10/2026, waitress, misma máquina; "antes" =
código del commit 4c79ce4 con el servidor de desarrollo):

| Medida | Antes (E4) | Después (E5) |
|---|---|---|
| Errores de captura detectados (128 inyectados) | 50.0 % | 96.9 % |
| Datos válidos rechazados por formato (24) | 24 | 0 |
| Falsos positivos en 60 capturas limpias | 0 | 0 |
| Duplicados / errores 500 en carreras (60 pares) | 5 / 7 | 0 / 0 |
| Hallazgos de seguridad en red (8 pruebas) | 5 | 0 |
| p95 de captura con 20 usuarios sin pausa | 497.6 ms | 120.0 ms |
| Capturas confirmadas perdidas tras caída abrupta | 0 | 0 |

Los 4 no detectados son CURP con una consonante cambiada que el dígito de
RENAPO no distingue (límite del algoritmo, no del código).

Versión del TRL 6 (rama `trl6/correcciones`, 07/10/2026, instalación limpia
clonada de la rama; salidas en `Obsidian/raw/resultados/*trl6*` y
`e6-arnes-integracion.md`):

| Arnés | Resultado |
|---|---|
| E3 (`test_prueba_concepto.py`) | 8/8; lote en dos archivos de 168 posiciones |
| E5 (`prueba_ambiente_relevante.py`) | 10/10 criterios; 96.9 %; 0 duplicados; 0 hallazgos en G |
| E6 (`prueba_integracion.py`) | F 23/23 · L conforme (42 registros) · S 1 hallazgo de 14 (S-03, sin HTTPS) · R restauración en 0.85 s |

Con 10 usuarios sin pausa atiende 3,935 capturas por minuto (5,609 sin inicio
de sesión): cada petición consulta usuario y token. Criterios del TRL 6: 9 de
10; solo falta el cifrado (HTTPS).

⚠️ Si cambias las reglas de `validaciones.py`, **vuelve a correr el arnés**:
los casos C1 y C2 tienen que seguir saliendo válidos y C3–C8 rechazados. Al
introducir los catálogos IDSE hubo que actualizar C2 y C5, cuya causa de baja
era texto libre.

---

## 7. Límites conocidos (no son bugs)

- **Sin HTTPS.** En la red local la sesión y los datos viajan sin cifrar; hace
  falta un certificado de la oficina y un proxy con TLS (pendiente para el piloto).
- **El lote sigue la estructura publicada por el IMSS**, pero la codificación,
  el fin de línea y la Ñ solo se confirman cargando un lote de prueba en el IDSE.
  El registro patronal y la guía de la semilla son de ejemplo.
- **PostgreSQL no está instalado en el equipo de pruebas**; con 20 usuarios sin
  pausa SQLite serializa las escrituras: la captura más lenta llegó a 3.1 s sin
  inicio de sesión y a 0.58 s con él. Mientras no haya PostgreSQL,
  `SIGMA_DB=sqlite` evita 1 s de espera en cada arranque.
- **Montos legales** (salario mínimo y UMA) solo hasta 2026: el sistema avisa,
  pero hay que cargarlos cada año. Los días inhábiles del IMSS se cargan a mano.
- **Un solo patrón.** El modelo soporta varios, pero la interfaz usa el primero.
- **Sin movimiento 07** (modificación de salario).
