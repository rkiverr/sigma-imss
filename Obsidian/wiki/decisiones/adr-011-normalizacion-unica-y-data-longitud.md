---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [normalizacion, interfaz, captura]
fuentes: ["sigma/validaciones.py", "sigma/app.py", "sigma/static/js/app.js", "sigma/templates/index.html"]
actualizado: 2026-10-04
---

# ADR-011: Una sola normalización; `data-longitud` en lugar de `maxlength`

**Contexto (bloque B del E5, código del E4).**
- **E-06:** pegar una CURP o un NSS con espacios hacía que el navegador recortara al `maxlength` **antes** de que
  la máscara limpiara. Se perdían caracteres y 24 de 24 capturas válidas se rechazaron.
- **E-07:** `/api/validar` no limpiaba igual que el servidor: el NSS con espacios o la fecha con diagonales
  daban "error" en vivo aunque el servidor los aceptaba.

**Decisión.**
1. `validaciones.normalizar_datos()` es la **única** normalización: la usan `/capturar` y `/api/validar`.
2. Los campos CURP, NSS, RFC y fecha usan `data-longitud` en lugar de `maxlength`. La máscara de `app.js`
   **limpia primero y recorta después** (`recortar()`).

**Por qué.** Así es como la gente copia los datos: de mensajes, PDF o credenciales, con espacios y guiones. La
validación en vivo debe decir lo mismo que el servidor ([[adr-003-un-solo-validador]]).

**Resultado.** 24 de 24 capturas pegadas aceptadas y validación en vivo coherente con el servidor.

**Trampa.** Si cambias la limpieza, actualiza las tres cosas a la vez: `normalizar_datos()`, `app.js` y
`emular_navegador()` del arnés ([[normalizacion-de-datos]]).

Ver: [[decisiones]]
