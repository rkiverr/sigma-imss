---
tipo: modulo
tags: [interfaz, templates, javascript, css, accesibilidad, tema]
fuentes: ["sigma/templates/base.html", "sigma/templates/index.html", "sigma/templates/error.html", "sigma/static/js/app.js", "sigma/static/css/estilos.css"]
actualizado: 2026-10-08
---

# Interfaz: `sigma/templates/` y `sigma/static/`

HTML, CSS y JS **propios**, sin CDN ni frameworks ([[adr-006-frontend-sin-dependencias]]). Todo es
**progresivo**: sin JavaScript, el formulario se envía igual y el servidor valida igual.

## Plantillas (Jinja2)
| Archivo | Contenido |
|---|---|
| `base.html` | Esqueleto: barra superior (logo Σ, insignias de patrón y motor, botón de tema), notificaciones (*flash*), pie. Incluye un **script en línea con `nonce`** que aplica el tema guardado **antes de pintar**, para que no parpadee en blanco |
| `index.html` | Tablero de 5 métricas, formulario de captura, tarjeta de exportación, bitácora (15), tabla de movimientos con filtros y páginas, y diálogo de detalle (`<dialog>`) |
| `error.html` | Páginas 403, 404, 500 y 503; la 503 trae ayuda para PostgreSQL |

## Formulario de captura (`index.html`)
- **Grupos de campos:**
  - Identificación: nombre, CURP, NSS y RFC.
  - Movimiento: tipo, fecha y calendario.
  - Condiciones de contratación (solo en un alta).
  - Motivo de la baja (solo en una baja).
  - Usuario que captura.
- **Marcas por campo:**
  - `data-estado="error"`: borde rojo y mensaje; no deja guardar.
  - `data-estado="aviso"`: borde ámbar; sí deja guardar.
  - `data-estado="ok"`: borde verde.
- CURP, NSS, RFC y fecha usan **`data-longitud`** (18, 11, 13, 8), **no `maxlength`**
  ([[adr-011-normalizacion-unica-y-data-longitud]]).
- Si el servidor rechaza (422), la página vuelve con un **resumen de errores** arriba y los valores intactos.
- Los catálogos se arman desde `validaciones.py`, pasando por `CATALOGOS` de `app.py`.

## `sigma/static/js/app.js`
| Función | Qué hace |
|---|---|
| `iniciarTema`, `aplicarTema`, `temaEfectivo` | Tema claro u oscuro con 3 estados. Solo se guarda en `localStorage` si el usuario lo elige |
| `iniciarNotificaciones` | Las notificaciones se ocultan solas a los 7 s, salvo las de error |
| `validarEnServidor`, `programarValidacion` | Envía el formulario completo a `/api/validar` a los 260 ms de dejar de escribir o al salir de un campo, y pinta solo los campos ya "tocados" |
| `aplicarMascaras`, `longitudDe`, `recortar` | Solo dígitos en NSS y fecha, mayúsculas y `[A-ZÑ&0-9]` en CURP y RFC. **Primero limpia y luego recorta** a `data-longitud` |
| `actualizarContador` | Contador "8/18" junto a la etiqueta |
| `iniciarFecha` | El calendario nativo rellena el campo DDMMAAAA y viceversa |
| `iniciarCamposCondicionales` | Muestra los campos de alta o de baja según el tipo; los ocultos se deshabilitan y **no se envían** |
| `iniciarFormulario` | Al enviar, deshabilita el botón 6 s ("Guardando…") para evitar el doble envío. "Limpiar" reinicia todo |
| `iniciarFiltros` | Los filtros se envían al cambiar; la búsqueda, a los 480 ms de dejar de escribir |
| `iniciarDetalle` | Al dar clic o Enter en una fila, carga `/api/movimiento/<id>` y lo muestra en el diálogo, escapando el texto |

## `sigma/static/css/estilos.css` (851 líneas)
- Los colores son variables CSS, declaradas **tres veces**:
  1. `:root`, el tema claro.
  2. `@media (prefers-color-scheme: dark) :root:not([data-tema="claro"])`.
  3. `:root[data-tema="oscuro"]`.

  Así, el botón gana en las dos direcciones.
- **Paleta azul marino:** acento `#1c3f77`. Se cambió del verde original porque las tarjetas se perdían contra
  el fondo.
- **Métricas:** navy (total), ámbar (pendientes), teal (exportados), azul cielo (altas) y gris azulado (bajas).
- **`--texto-tenue: #5c6b84`** en el tema claro. En el E5 subió de 3.15:1 a **5.4:1** de contraste
  ([[accesibilidad]]).
- Los estados en la tabla son **pastillas con texto** ("Válido", "Exportado"), no solo color.

## Trampas
- Un script en línea nuevo necesita `nonce="{{ csp_nonce }}"`; si no, la CSP lo bloquea ([[seguridad-web]]).
- Si cambias las máscaras o las longitudes, actualiza `emular_navegador()` en [[arnes-ambiente-relevante]].
- Después de cambiar CSS o JS, recarga con `Ctrl + Shift + R`.


## Cambios del TRL 6 (2026-10-07)
- `templates/login.html` (nueva) y en la barra de `base.html` el usuario con su rol y el botón **Salir**.
- `index.html`: tres campos de nombre (`maxlength="27"`), UMF con `data-longitud="3"`; sin selectores de usuario;
  el panel de exportación solo aparece al administrador, con un botón de descarga por tipo y el aviso de montos.
- `app.js`: máscara de dígitos para la UMF, limpieza de espacios en los tres campos del nombre, redirección a
  `/login` si la API responde 401 y detalle con apellidos y UMF.
- `estilos.css`: `.sesion`, `.pagina-login`, `.formulario-login`, `.aviso-montos`, `.descargas` (el aviso usa el par
  de color ya medido en [[accesibilidad]]: 4.76:1).
- Pie: "TRL 6".

## Rediseño del inicio de sesión (2026-10-07, a pedido de Pedro)
- `login.html` es una **tarjeta dividida**, centrada en el alto disponible.
  - Panel de marca azul marino: lema, cuatro ventajas con icono, trama de puntos y una Σ de marca de agua.
  - Formulario: campos con icono, botón para **ver u ocultar la contraseña** y "Entrar" a todo el ancho.
  - Responsivo: a ≤ 860 px el panel va arriba; a ≤ 560 px se ocultan las ventajas.
- **Acceso de prueba (temporal):** recuadro con los usuarios y contraseñas de prueba para el equipo, con un botón
  "Usar" que llena el formulario.
  - Está entre los comentarios `{# ===== TEMPORAL … #}` y `{# ===== FIN DEL BLOQUE TEMPORAL ===== #}`. Para
    quitarlo basta borrar ese bloque.
  - Las contraseñas están escritas en la plantilla. Si cambian con `python -m sigma.usuarios`, este recuadro
    queda desactualizado.
- `base.html`:
  - El `body` acepta `{% block clase_cuerpo %}`; el login usa `cuerpo-login`, que lo pone en columna para que
    el `main` crezca.
  - El pie dice solo "Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V.".
- `estilos.css`:
  - Tokens `--login-panel`, `--login-panel-borde`, `--login-texto` y `--login-texto-suave` en los dos temas.
  - Contraste medido: blanco ≥ 8.3:1 y texto suave ≥ 5.6:1 sobre todo el degradado. El bloque H del arnés del
    E5 sigue en 14/14.
- `app.js` → `iniciarLogin()`: muestra los botones que dependen de JavaScript (empiezan con `hidden`), alterna
  el tipo del campo de contraseña y llena los campos con "Usar".
- Trampa: `.boton` y `.ver-contrasena` definen `display`, así que el atributo `hidden` necesita su propia regla
  (`.ver-contrasena[hidden]`, `.credenciales-prueba [hidden]`).
- Para revisarlo en móvil con Chrome headless: la ventana no baja de 491 px. Se usa un `iframe` de 390 px
  dentro de una ventana más ancha.

## Letras más grandes (2026-10-08, a pedido de Pedro)
- Pedro veía las letras demasiado chicas en pantallas anchas. Se subió la escala tipográfica entre 12 y 15 %:
  - `body`: 15 → 16 px; etiquetas de campo: 12.5 → 14.
  - Tabla: 13.5 → 15; títulos de tarjeta: 15.5 → 18; métricas: 27 → 32.
  - Bitácora: 13.5 → 15 y 11 → 12.5; pie: 12.3 → 13.5.
- El contenedor y la barra pasan de 1180 a **1360 px**, y el diálogo de detalle de 560 a 640 px.
- En `index.html`, el texto "Hay N movimiento(s) listo(s)…" tiene su tamaño en línea: 13.5 → 15 px.
- Los filtros de la tabla ya no se parten de uno en uno:
  - `.tarjeta-encabezado > .filtros` crece (`flex: 1 1 560px`);
  - el título del encabezado usa `flex: 1 1 320px`.
- El login conserva sus tamaños propios; solo hereda la base de 16 px y las etiquetas de 14.
- Se verificó con capturas en 1920 y 1366 px y en móvil; el bloque H del E5 sigue en 14/14 y el E3 en 8/8.
- Segundo ajuste, el mismo día, porque Pedro pidió un poco más:
  - `body`: 17 px; títulos de tarjeta: 20; descripciones: 16; etiquetas: 15; `.ayuda` ("Se registrará a nombre
    de…", "Formato IDSE…"): 14.5.
  - Las leyendas de sección (`.grupo-campos legend`: Identificación del trabajador, Movimiento, Condiciones de
    contratación y Motivo de la baja) quedan en **negritas** (700), de 14 px y color `--texto-suave`.
  - El aviso de pendientes en línea de `index.html` sube a 16 px.
- Tercer ajuste, a pedido de Pedro: cuadros de métricas y barra superior más grandes.
  - Métricas: relleno 20/22/20/26, nombre de 15.5 px, **número de 42 px** (34 en móvil), nota de 14.5 y
    columnas mínimas de 200 px.
  - Barra: logo de 48 px, nombre de 22 y subtítulo de 15, insignias de 15 px con más relleno y botones
    "Salir" y de tema de 46 px de alto con letra de 15.5.
  - Con la barra más alta, en pantallas ≥ 941 px se queda en un solo renglón (`flex-wrap: nowrap`): la
    insignia del patrón cede espacio con puntos suspensivos. Debajo de ese ancho se parte como antes.
- Cuarto ajuste, a pedido de Pedro: todo el texto del **login** más grande.
  - Tarjeta de 1040 a 1200 px y relleno de 48/50 px.
  - Lema de 33 px, ventajas de 17/15.5, título "Iniciar sesión" de 31 y etiquetas de 17.
  - Campos de 56 px de alto con letra de 17; botón "Entrar" de 18.
  - Recuadro temporal: rol de 15.5, usuario y contraseña de 15.5 en monoespaciada y botón "Usar" de 15.5.
  - Con eso la tarjeta mide unos 860 px de alto y la página se desplaza en ventanas bajas.

Ver también: [[accesibilidad]] · [[normalizacion-de-datos]] · [[arquitectura-general]]
