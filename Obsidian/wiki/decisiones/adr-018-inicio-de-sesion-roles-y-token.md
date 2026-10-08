---
tipo: decision
estado: vigente
fecha: 2026-10-07 (Entregable 6)
tags: [seguridad, autenticacion, sesion, roles, bitacora]
fuentes: ["sigma/usuarios.py", "sigma/app.py", "sigma/templates/login.html"]
actualizado: 2026-10-07
---

# ADR-018: Inicio de sesión con roles y token de sesión en la base

**Contexto.** Hasta el E5 el usuario que capturaba se elegía de un desplegable: la bitácora documentaba la
autoría pero no la demostraba (E-17, R-03). En la demostración del E6 apareció además que el selector regresaba
a `admin.rrhh` en cada recarga, así que una captura quedaba fácilmente a nombre de otra persona (P-09), y que
cualquier equipo de la red podía capturar (S-01, S-02, S-08).

**Decisión.**
- Cada persona entra con usuario y contraseña (`/login`). Las contraseñas se guardan con
  `werkzeug.security.generate_password_hash` (scrypt); nunca en claro.
- Dos roles: `captura` (captura y consulta) y `administrador` (además genera y descarga lotes:
  `@requiere_rol("administrador")` → 403 a los demás).
- El usuario de la bitácora sale de la sesión (`g.usuario`); se quitaron los selectores de usuario.
- 5 contraseñas equivocadas bloquean la cuenta 15 minutos; el mensaje es genérico.
- La cookie es `HttpOnly` y `SameSite=Lax`; la sesión dura `SIGMA_SESION_HORAS` (10).
- **Token de sesión en la base** (`usuario.sesion_token`): Flask guarda la sesión en la cookie firmada, así que
  borrar la cookie al salir no invalidaba una copia. Ahora la cookie solo vale si su token coincide con el de la
  base; cerrar sesión, cambiar la contraseña o desactivar al usuario lo borra.
- Las contraseñas se asignan en la PC servidor con `python -m sigma.usuarios` ([[modulo-usuarios]]).

**Por qué.** Es lo que pedía el objetivo específico 3 del E1 (control de acceso y bitácora) y el riesgo R-03. Un
proveedor de identidad externo no tiene sentido para una oficina pequeña sin internet obligatoria; la tabla
`usuario` ya existía.

**Consecuencias.**
- Primer arranque: nadie tiene contraseña; la página de inicio lo advierte.
- Varias PC con la misma cuenta comparten el token (`abrir_sesion()` reutiliza el vigente); si una cierra
  sesión, las demás también salen.
- Los arneses asignan contraseñas de prueba en sus copias aisladas ([[arnes-ambiente-relevante]],
  [[arnes-integracion]]).
- Sin HTTPS, la cookie y la contraseña viajan en claro por la red local: sigue pendiente ([[hoja-de-ruta-trl6]]).

**Alternativas descartadas.** Sesiones del lado del servidor (Flask-Session): otra dependencia; el token en la
tabla `usuario` resuelve la invalidación sin ella. Flask-Login: no aporta nada que no sean unas líneas de
`before_request`.

Ver también: [[decisiones]] · [[seguridad-web]] · [[modulo-app]]
