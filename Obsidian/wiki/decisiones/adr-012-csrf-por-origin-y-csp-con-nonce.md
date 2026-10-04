---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [seguridad, csrf, csp, cabeceras]
fuentes: ["app.py", "templates/base.html"]
actualizado: 2026-10-04
---

# ADR-012: CSRF por `Origin` y CSP con nonce

**Contexto (bloque G del E5).** Un POST a `/capturar` con `Origin: http://sitio-externo.example` **se guardaba**.
Cualquier página que visitara un capturista podía enviar capturas a su nombre. Además, no había cabeceras de
seguridad.

**Decisión.**
1. **CSRF:** `preparar_peticion()` (before_request) toma `Origin`, o si no viene, `Referer`, de todo POST. Si
   su `netloc` no coincide con `request.host`, responde **403**. Si no llega ninguna de las dos cabeceras, deja
   pasar: son clientes que no son navegador, y los navegadores siempre envían `Origin` en un POST.
2. **CSP con nonce:**
   - `g.csp_nonce` es aleatorio en cada petición.
   - El único script en línea (el del tema, en `base.html`) lleva `nonce="{{ csp_nonce }}"`.
   - `script-src 'self' 'nonce-…'` bloquea cualquier otro script en línea o externo.
3. **Cabeceras:** `nosniff`, `X-Frame-Options: DENY` y `Referrer-Policy: same-origin`.

**Por qué no tokens CSRF.** La verificación de origen cubre el caso con muy poco código y no obliga a cambiar
los formularios ni la API JSON. Los tokens pueden llegar junto con el login (TRL 6).

**Consecuencias.**
- Todo script en línea nuevo **necesita el nonce**.
- Un despliegue detrás de un proxy que cambie el `Host` tendría que ajustar la comparación.

Ver: [[seguridad-web]] · [[decisiones]]
