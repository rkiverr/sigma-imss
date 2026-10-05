---
tipo: concepto
tags: [seguridad, owasp, csrf, csp, xss, inyeccion, lfpdppp]
fuentes: ["sigma/app.py", "servidor.py", "sigma/templates/base.html", "raw/normativa/lfpdppp-datos-personales.md"]
actualizado: 2026-10-04
---

# Seguridad web y de datos personales

Sigma guarda **datos personales**: nombre, CURP, NSS, RFC y salario. La LFPDPPP (art. 18) exige medidas de
seguridad administrativas, técnicas y físicas. Las consideraciones del E5 se organizaron con la lista
**OWASP Top 10:2025**.

## Medidas implementadas
| Riesgo (OWASP 2025) | Medida | Dónde |
|---|---|---|
| **A02 Configuración insegura** | Servidor de producción waitress. `debug` solo con `SIGMA_DEBUG=1`; `app.py` escucha en 127.0.0.1; cabecera `Server: Sigma` sin versión | `servidor.py`, `app.py` ([[adr-009-servidor-de-produccion-waitress]]) |
| **A01 Control de acceso (CSRF)** | Un POST cuyo `Origin` (o `Referer`) no coincide con el host recibe **403** | `preparar_peticion()` ([[adr-012-csrf-por-origin-y-csp-con-nonce]]) |
| **A05 Inyección SQL** | Todas las consultas son parametrizadas (`%s`) | `app.py`, `database.py` |
| **A05 Inyección de código (XSS)** | Jinja2 escapa el texto; el diálogo usa `escapar()`; la **CSP con nonce** solo permite los scripts propios; el nombre ya no admite `<` ni `>` | `cabeceras_de_seguridad()`, `base.html` |
| Cabeceras | `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: same-origin` | `cabeceras_de_seguridad()` |
| **A10 Condiciones excepcionales** | Los errores de la base, los folios fuera de rango y las carreras devuelven 404, 422 o 503 controlados, sin detalle técnico | manejadores de error |
| **A09 Registro** | La bitácora guarda cada captura, rechazo y exportación con usuario y hora | `registrar_bitacora()` |
| Red | El servidor solo está en la LAN; la base nunca se expone | despliegue ([[arquitectura-general]]) |
| e.firma | Sigma **nunca** guarda la firma electrónica; la carga al IDSE es manual | por diseño |

## La CSP exacta
```text
default-src 'self'; script-src 'self' 'nonce-<aleatorio>'; style-src 'self' 'unsafe-inline';
img-src 'self' data:; form-action 'self'; frame-ancestors 'none'; base-uri 'self'
```
- `style-src 'unsafe-inline'` hace falta por los atributos `style=` de las plantillas.
- `img-src data:` hace falta por el favicon SVG en línea.

## Pendientes
| Riesgo | Estado |
|---|---|
| **A07 Autenticación:** no hay login; el usuario se elige de una lista | Planeado para TRL 6 |
| **Tráfico sin cifrar** (HTTP en la LAN) | Planeado: HTTPS |
| **Bitácora alterable** directamente en la base | Planeado |
| **Respaldo** de la base | Planeado |
| Medidas físicas y administrativas: servidor en un área restringida, disco cifrado, acceso solo para RH, aviso de privacidad a los trabajadores | Recomendado en el E5; le toca a la empresa |

## Cómo se verifica
Las 8 pruebas del bloque G de [[arnes-ambiente-relevante]]: antes había 5 hallazgos y después 0.

Ver también: [[modulo-app]] · [[riesgos]] · [[hoja-de-ruta-trl6]]
