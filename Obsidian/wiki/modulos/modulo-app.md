---
tipo: modulo
tags: [app, flask, controlador, rutas, seguridad]
fuentes: ["sigma/app.py"]
actualizado: 2026-10-04
---

# `sigma/app.py` — controlador HTTP

Tiene 556 líneas. Es el **controlador** del lazo ([[sigma-como-sistema-de-control]]): recibe las peticiones,
orquesta la validación, la persistencia y la exportación, y responde. Crea la aplicación Flask (`app`), que
`servidor.py` sirve con waitress ([[modulo-servidor]]).

## Constantes
| Nombre | Valor | Para qué |
|---|---|---|
| `MOVIMIENTOS_POR_PAGINA` | 25 | Paginación de la tabla |
| `FOLIO_MAXIMO` | 2³¹ − 1 | Un folio mayor responde 404 en `/api/movimiento` (antes daba error 500) |
| `ETIQUETAS_TIPO` | `{"08": "Alta / Reingreso", "02": "Baja"}` | Textos de la interfaz |
| `CAMPOS_FORMULARIO` | 11 campos | Los que se leen del formulario y de la API |
| `CATALOGOS` | tipo de trabajador, de salario, de jornada, causa de baja | Desplegables y etiquetas, tomados de `validaciones.py` ([[catalogos-idse]]) |
| `app.secret_key` | `SECRET_KEY` del entorno o `secrets.token_hex(32)` | Firma de sesiones. Sin la variable, cambia en cada arranque |

## Funciones
**Lectura y reglas**
- `_leer_formulario()`: lee los campos y llama a `normalizar_datos()` ([[normalizacion-de-datos]]).
- `_validar_historial(conn, datos)`: reglas de historial afiliatorio; devuelve `(errores, avisos)`
  ([[historial-afiliatorio]]).
- `_legible(ddmmaaaa)`: DD/MM/AAAA para los mensajes.
- `_usuario_valido(conn, valor)`: convierte el valor en un id existente o en `None`, sin lanzar `ValueError`.

**Pantalla principal**
- `_consultar_movimientos(conn, filtros)`: hace el `WHERE` con parámetros, el `COUNT` y el `LIMIT/OFFSET`, y
  calcula las páginas.
- `_contexto(...)`: arma todo lo que necesita `index.html`: movimientos, usuarios, bitácora (15), patrón,
  estadísticas, catálogos, motor y si hay lote.
- `_filtros_de_peticion()`: limpia `q`, `estado`, `tipo` y `pagina`.

**Escritura**
- `_guardar_movimiento(conn, datos, usuario_id)`: patrón, trabajador, INSERT del movimiento (`'Válido'`) y
  bitácora. Devuelve el id.

**Seguridad por petición** ([[seguridad-web]])
- `preparar_peticion()` (`before_request`): genera `g.csp_nonce` y rechaza con **403** cualquier POST cuyo
  `Origin`/`Referer` no sea el host.
- `variables_de_plantilla()` (`context_processor`): expone `csp_nonce`.
- `cabeceras_de_seguridad()` (`after_request`): CSP con nonce, `nosniff`, `X-Frame-Options: DENY` y
  `Referrer-Policy`.

**Vistas:** `index`, `capturar`, `exportar`, `descargar_lote`, `api_validar` y `api_movimiento`
([[rutas-http]]). **Errores:** `error_404`, `error_403`, `error_base_de_datos` (503) y `error_no_controlado`
(500).

## Arranque de desarrollo (`sigma/__main__.py`)
- `python -m sigma` escucha en `SIGMA_HOST` (por defecto **127.0.0.1**) y `SIGMA_PUERTO` (5050). Hasta la E5
  era el bloque `if __name__ == "__main__"` de `app.py` y se arrancaba con `python app.py`; pasó a
  `__main__.py` porque `app.py` usa imports relativos y ya no se ejecuta directo
  ([[adr-017-paquete-sigma-y-carpeta-de-pruebas]]).
- `debug` solo se activa con `SIGMA_DEBUG=1`.
- **No se usa en la oficina**; ahí se arranca con `python servidor.py`
  ([[adr-009-servidor-de-produccion-waitress]]).

## Trampas al modificarlo
- **Todo SQL nuevo va con `%s`**, nunca con `?` ([[adr-008-sql-con-marcadores-psycopg2]]).
- Toda escritura va dentro de `with conexion(commit=True) as conn:`.
- Si agregas un **script en línea** en una plantilla, necesita `nonce="{{ csp_nonce }}"`; si no, la CSP lo bloquea.
- Si cambias una regla que dependa de la base, recuerda que `/api/validar` **no** la ejecuta: solo valida el
  formulario aislado.
- Un formulario rechazado responde **422** con la misma vista; no lo cambies por un redirect
  ([[adr-005-422-conservando-lo-capturado]]).

## Pruebas que lo cubren
Bloques A, B, C, F y G de [[arnes-ambiente-relevante]].

Ver también: [[flujo-de-captura]] · [[arquitectura-general]]
