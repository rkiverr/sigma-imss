---
tipo: arquitectura
tags: [rutas, api, http, flask]
fuentes: ["sigma/app.py"]
actualizado: 2026-10-04
---

# Rutas HTTP

Todas están en `app.py` ([[modulo-app]]). Puerto **5050**.

| Ruta | Método | Función | Qué hace | Respuestas |
|---|---|---|---|---|
| `/` | GET | `index()` | Pantalla principal: tablero, formulario, exportación, bitácora (últimas 15) y tabla de movimientos con filtros y páginas de 25 | 200 |
| `/capturar` | POST | `capturar()` | Valida y guarda un movimiento ([[flujo-de-captura]]) | 302 a `/` si se guardó; **422** con el formulario y los errores; 403 si el origen es ajeno |
| `/exportar` | POST | `exportar()` | Genera el lote IDSE con los pendientes y los marca como Exportado ([[lote-idse]]) | 302 a `/` (con *flash* de éxito o de error) |
| `/descargar-lote` | GET | `descargar_lote()` | Descarga el lote más reciente (por fecha de modificación) | archivo `text/plain`, o 302 con aviso si no hay ninguno |
| `/api/validar` | POST (JSON) | `api_validar()` | Validación en vivo: normaliza y llama a `validar_campos()`. Lee el cuerpo con `get_json()`: si llega como formulario, no ve ningún dato y responde que todo es obligatorio | 200 `{"valido": bool, "errores": {campo: msg}, "avisos": {campo: msg}}` |
| `/api/movimiento/<int:id>` | GET | `api_movimiento()` | Detalle de un movimiento y su bitácora (para el diálogo de la tabla) | 200 JSON; **404** si no existe o si `id > FOLIO_MAXIMO` (2³¹−1) |

## Parámetros de `GET /`
`_filtros_de_peticion()` lee:
- `q`: busca en nombre, CURP o NSS con `LIKE` parametrizado.
- `estado`: solo `Válido`, `Exportado` o `Rechazado`.
- `tipo`: `08` o `02`.
- `pagina`: entero ≥ 1.

Los valores fuera de catálogo se ignoran.

## JSON de `/api/movimiento/<id>`
Campos:
- `id`, `nombre_completo`, `curp`, `nss`, `rfc`, `registro_patronal`, `razon_social`, `tipo_movimiento`,
  `fecha_movimiento`, `estado`.
- Condiciones del alta y de la baja: `tipo_trabajador`, `tipo_salario`, `tipo_jornada`, `sdi`, `causa_baja`, y
  sus `*_etiqueta` del catálogo.
- `tipo_etiqueta`, `fecha_legible` (DD/MM/AAAA), `creado_en` formateado e `historial` (asientos de bitácora con
  `timestamp`, `usuario`, `accion` y `detalle`).

## Manejadores de error
| Código | Cuándo | Página |
|---|---|---|
| 403 | POST con `Origin` o `Referer` de otro sitio | "Solicitud rechazada" |
| 404 | Ruta inexistente | "Página no encontrada" |
| 503 | `ErrorBaseDeDatos`: no se pudo abrir la base | "Base de datos no disponible", con el detalle y una ayuda para PostgreSQL |
| 500 | Cualquier otra excepción | Mensaje genérico. El detalle técnico **solo** aparece con `app.debug`, que en producción nunca está activo |

Todas usan `sigma/templates/error.html`.

## Lo que corre en cada petición
- `before_request` → `preparar_peticion()`:
  - Genera `g.csp_nonce`.
  - Si es POST, compara `urlparse(Origin o Referer).netloc` con `request.host`; si no coinciden → 403.
  - Si no llega ninguna de las dos cabeceras, deja pasar.
- `after_request` → `cabeceras_de_seguridad()`:
  - CSP con nonce.
  - `X-Content-Type-Options: nosniff`.
  - `X-Frame-Options: DENY`.
  - `Referrer-Policy: same-origin`.

  Ver [[seguridad-web]].
- `context_processor` → expone `csp_nonce` a las plantillas.

## Filtros de plantilla
- `fecha_idse`: convierte DDMMAAAA en DD/MM/AAAA.
- `momento`: formatea marcas de tiempo, sea `datetime` (PostgreSQL) o texto ISO (SQLite).
- `etiqueta_tipo`: "08" → "Alta / Reingreso".

Ver también: [[flujo-de-captura]] · [[arquitectura-general]]
