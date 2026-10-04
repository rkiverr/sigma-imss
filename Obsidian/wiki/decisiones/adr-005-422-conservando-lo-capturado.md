---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [ux, http, formulario]
fuentes: ["app.py"]
actualizado: 2026-10-04
---

# ADR-005: El formulario rechazado responde 422 conservando lo capturado

**Contexto.** En el E3, un `POST /capturar` con errores hacía un **redirect** y el usuario **perdía todo lo
escrito**.

**Decisión.** Si hay errores, `capturar()` **no redirige**: renderiza `index.html` con `form=datos`, `errores` y
`avisos`, y responde con **HTTP 422 (Unprocessable Entity)**. Si se guardó, hace un redirect a `/` con un
*flash* (patrón PRG).

**Por qué.** Corregir un campo no debe obligar a reescribir los demás. El 422 deja claro, para personas y para
pruebas, que el servidor entendió la petición y la rechazó por su contenido.

**Consecuencias.** Las pruebas clasifican así: 422 = bloqueado; 302 = guardado. Los rechazos por carrera
(`IntegrityError`) también responden 422 ([[adr-010-unicidad-del-movimiento-en-la-base]]).

Ver: [[flujo-de-captura]] · [[decisiones]]
