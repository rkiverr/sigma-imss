---
tipo: modulo
tags: [interfaz, templates, javascript, css, accesibilidad, tema]
fuentes: ["sigma/templates/base.html", "sigma/templates/index.html", "sigma/templates/error.html", "sigma/static/js/app.js", "sigma/static/css/estilos.css"]
actualizado: 2026-10-04
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

Ver también: [[accesibilidad]] · [[normalizacion-de-datos]] · [[arquitectura-general]]
