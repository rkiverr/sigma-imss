---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [frontend, offline, progresivo]
fuentes: ["sigma/templates/", "sigma/static/"]
actualizado: 2026-10-04
---

# ADR-006: Frontend sin dependencias externas

**Decisión.** HTML, CSS y JavaScript propios. **Cero CDN, cero frameworks.** Todo es **progresivo**: sin
JavaScript, el formulario se envía y el servidor valida igual.

**Por qué.**
- El prototipo debe demostrarse **sin internet**.
- Una dependencia externa en un trabajo académico agrega superficie de falla sin aportar nada.
- Facilita la CSP estricta (`script-src 'self'`) del E5 ([[seguridad-web]]).

**Consecuencias.**
- Las máscaras, la validación en vivo, el calendario y el diálogo de detalle son **comodidades**, no requisitos.
- El tema claro u oscuro usa variables CSS declaradas tres veces ([[modulo-interfaz]]).
- `app.js` está escrito en ES5 (`var`, `function`) para máxima compatibilidad.

Ver: [[modulo-interfaz]] · [[decisiones]]
