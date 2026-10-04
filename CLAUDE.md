# CLAUDE.md — Contexto del proyecto Sigma

Guía para cualquier sesión futura de Claude Code sobre este repositorio.
Documenta **qué es el proyecto, cómo está construido y por qué se tomó cada
decisión**, para no volver a deducirlo desde cero.

---

## 1. Qué es

**Sigma** es un sistema para automatizar las altas y bajas de trabajadores ante
el IMSS. Es un trabajo académico (Entregas 1 a 5 de un informe por niveles TRL),
no un producto en producción. Nació como prueba de concepto (TRL 3), se integró
como prototipo (TRL 4) y en la Entrega 5 se validó en ambiente relevante
(TRL 5).

**Ramas.**
- `main` es la vigente. Desde el 2026-10-04 incluye la Entrega 5: el merge
  `cffd375` integró los 7 commits de `trl5/ambiente-relevante`.
- `trl5/ambiente-relevante` sigue publicada porque el informe la cita.
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

Aplicación Flask cliente-servidor, sin dependencias de frontend.

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Rutas HTTP, flujo, reglas de historial, seguridad por petición, errores |
| `servidor.py` | Arranque en producción con waitress (el que se usa en la oficina) |
| `plazo.py` | Plazo legal de 5 días hábiles (art. 15 LSS; descansos art. 74 LFT) |
| `validaciones.py` | Validación algorítmica y reglas de negocio |
| `database.py` | Persistencia relacional y selección de motor |
| `exportar_idse.py` | Traducción al formato de lote IDSE |
| `templates/base.html` | Esqueleto: barra, tema, notificaciones, pie |
| `templates/index.html` | Pantalla principal (hereda de `base.html`) |
| `templates/error.html` | Página de error 404 / 500 / 503 |
| `static/css/estilos.css` | Sistema de diseño completo, temas claro y oscuro |
| `static/js/app.js` | Validación en vivo, máscaras, tema, diálogo de detalle |
| `test_prueba_concepto.py` | Arnés de pruebas del "Desarrollo experimental" (E3) |
| `prueba_ambiente_relevante.py` | Arnés de validación en ambiente relevante (E5) |

Modelo de datos (5 tablas normalizadas):
`patron`, `usuario`, `trabajador`, `movimiento`, `bitacora`.

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
`POST /api/validar` la expone tal cual, y `static/js/app.js` la consume para dar
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
`Server: Sigma`. `python app.py` es solo para programar: escucha en 127.0.0.1 y
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
  mensaje de éxito dice la fecha límite.
- Dígito verificador de la CURP (RENAPO) como **aviso**. Ojo: con pesos
  módulo 10 no detecta todos los cambios de una letra (en las pruebas, 4 de 8).

### 3.14 Normalización única y longitudes sin maxlength

`validaciones.normalizar_datos()` la usan `/capturar` **y** `/api/validar`
(antes la API no quitaba espacios del NSS ni diagonales de la fecha y decía
"error" donde el servidor aceptaba). Los campos CURP/NSS/RFC/fecha usan
`data-longitud` en lugar de `maxlength`: `app.js` limpia y **después** recorta.
Con `maxlength`, pegar "4316 89 1234 5" perdía dígitos.

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

---

## 5. Comandos

```bash
python servidor.py                  # producción (waitress) en http://0.0.0.0:5050
python app.py                       # desarrollo, solo 127.0.0.1 (SIGMA_DEBUG=1 para depurar)
python test_prueba_concepto.py      # arnés del E3 → resultados_prueba_concepto.txt
python prueba_ambiente_relevante.py # arnés del E5 (~3 min) → resultados_ambiente_relevante.*
python prueba_ambiente_relevante.py --codigo <carpeta> --servidor desarrollo --etiqueta antes
```

Variables de entorno: `DATABASE_URL`, `SIGMA_DB`, `SQLITE_PATH`, `SECRET_KEY`,
`SIGMA_HOST`, `SIGMA_PUERTO`, `SIGMA_HILOS`, `SIGMA_DEBUG`.

El arnés del E5 copia el sistema a un directorio temporal por bloque (no toca
`sigma_imss.db` ni `exportaciones/`). Emula al navegador: aplica `maxlength` /
`data-longitud` leídos de la página y las máscaras de `app.js`; si cambias las
máscaras, actualiza `emular_navegador()`.

El arnés usa su propia base (`sigma_pruebas.db`), que borra al iniciar, para que
los resultados sean reproducibles y no se mezclen con lo capturado desde la web.
Fija `SQLITE_PATH` **antes** de importar `database`, porque ese módulo lee la
configuración al cargarse.

---

## 6. Estado verificado

Probado por HTTP: altas, bajas, duplicados, conflictos de identidad,
exportación, descarga, 404, inyección SQL y XSS. Sin errores en el log.

Arnés de pruebas: **8/8 casos, los tres bloques CUMPLE.**

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

⚠️ Si cambias las reglas de `validaciones.py`, **vuelve a correr el arnés**:
los casos C1 y C2 tienen que seguir saliendo válidos y C3–C8 rechazados. Al
introducir los catálogos IDSE hubo que actualizar C2 y C5, cuya causa de baja
era texto libre.

---

## 7. Límites conocidos (no son bugs)

- **No hay autenticación real.** El usuario se elige de un desplegable, así que
  la bitácora documenta la autoría pero no la demuestra. Es el pendiente #1 para
  TRL 6, junto con HTTPS en la red local.
- **El layout del archivo IDSE es una representación**, con campos separados por
  `|`. Debe confirmarse contra el layout oficial vigente del IMSS antes de
  usarse de verdad. Está advertido en el código, el README y el pie de página.
- **Sin respaldo automático de la base.** Un archivo SQLite en una sola PC.
- **Un solo patrón.** El modelo soporta varios, pero la interfaz usa el primero.
