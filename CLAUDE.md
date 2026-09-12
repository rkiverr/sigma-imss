# CLAUDE.md — Contexto del proyecto Sigma

Guía para cualquier sesión futura de Claude Code sobre este repositorio.
Documenta **qué es el proyecto, cómo está construido y por qué se tomó cada
decisión**, para no volver a deducirlo desde cero.

---

## 1. Qué es

**Sigma** es una prueba de concepto (TRL 3) de un sistema para automatizar las
altas y bajas de trabajadores ante el IMSS. Es un trabajo académico (Entregas
1, 2 y 3 de un informe), no un producto en producción.

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
| `app.py` | Rutas HTTP, flujo, filtros de plantilla, manejo de errores |
| `validaciones.py` | Validación algorítmica y reglas de negocio |
| `database.py` | Persistencia relacional y selección de motor |
| `exportar_idse.py` | Traducción al formato de lote IDSE |
| `templates/base.html` | Esqueleto: barra, tema, notificaciones, pie |
| `templates/index.html` | Pantalla principal (hereda de `base.html`) |
| `templates/error.html` | Página de error 404 / 500 / 503 |
| `static/css/estilos.css` | Sistema de diseño completo, temas claro y oscuro |
| `static/js/app.js` | Validación en vivo, máscaras, tema, diálogo de detalle |
| `test_prueba_concepto.py` | Arnés de pruebas del "Desarrollo experimental" |

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

---

## 5. Comandos

```bash
python app.py                    # servidor en http://localhost:5050
python test_prueba_concepto.py   # arnés de pruebas → resultados_prueba_concepto.txt
```

Variables de entorno: `DATABASE_URL`, `SIGMA_DB`, `SQLITE_PATH`, `SECRET_KEY`.

El arnés usa su propia base (`sigma_pruebas.db`), que borra al iniciar, para que
los resultados sean reproducibles y no se mezclen con lo capturado desde la web.
Fija `SQLITE_PATH` **antes** de importar `database`, porque ese módulo lee la
configuración al cargarse.

---

## 6. Estado verificado

Probado por HTTP: altas, bajas, duplicados, conflictos de identidad,
exportación, descarga, 404, inyección SQL y XSS. Sin errores en el log.

Arnés de pruebas: **8/8 casos, los tres bloques CUMPLE.**

⚠️ Si cambias las reglas de `validaciones.py`, **vuelve a correr el arnés**:
los casos C1 y C2 tienen que seguir saliendo válidos y C3–C8 rechazados. Al
introducir los catálogos IDSE hubo que actualizar C2 y C5, cuya causa de baja
era texto libre.

---

## 7. Límites conocidos (no son bugs)

- **No hay autenticación real.** El usuario se elige de un desplegable, así que
  la bitácora documenta la autoría pero no la demuestra. Aceptable para TRL 3;
  para producción haría falta login.
- **El layout del archivo IDSE es una representación**, con campos separados por
  `|`. Debe confirmarse contra el layout oficial vigente del IMSS antes de
  usarse de verdad. Está advertido en el código, el README y el pie de página.
- **El servidor de desarrollo de Flask no es apto para producción.**
- **Un solo patrón.** El modelo soporta varios, pero la interfaz usa el primero.
