---
tipo: modulo
tags: [usuarios, sesion, autenticacion, consola]
fuentes: ["sigma/usuarios.py", "sigma/app.py"]
actualizado: 2026-10-07
---

# `sigma/usuarios.py` — contraseñas, inicio de sesión y consola de usuarios

Nació en el TRL 6 ([[adr-018-inicio-de-sesion-roles-y-token]]). Lo usan `app.py` (rutas `/login` y `/logout`,
`before_request`) y la consola `python -m sigma.usuarios`.

## Constantes
- `ROLES = ("administrador", "captura")` (la tabla `usuario` tiene el mismo `CHECK`).
- `INTENTOS_MAXIMOS = 5`, `MINUTOS_BLOQUEO = 15`, `LONGITUD_MINIMA = 8`.
- `MENSAJE_GENERICO = "Usuario o contraseña incorrectos."` (no delata si el usuario existe).

## Funciones
| Función | Qué hace |
|---|---|
| `buscar(conn, nombre)` / `por_id(conn, id)` | Lee el usuario (`por_id` trae `sesion_token`) |
| `fijar_contrasena(conn, nombre, contrasena)` | Hash scrypt; reinicia intentos y **borra el token** (cierra sus sesiones) |
| `autenticar(conn, nombre, contrasena)` | `(usuario, None)` o `(None, mensaje)`; cuenta intentos, bloquea y escribe en la bitácora ("Inicio de sesión", "Inicio de sesión fallido", "Cuenta bloqueada") |
| `abrir_sesion(conn, usuario)` | Devuelve el token vigente o crea uno |
| `cerrar_sesiones(conn, usuario_id)` | Borra el token: todas las cookies de ese usuario dejan de servir |
| `hay_contrasenas(conn)` | Para el aviso de primer arranque en `login.html` |
| `main()` | Consola: `listar`, `crear NOMBRE ROL`, `contrasena NOMBRE`, `activar`, `desactivar`, `desbloquear` (`--contrasena` para scripts) |

## Trampas
- Si el usuario no existe se compara contra `_HASH_DE_RELLENO`, para que la respuesta tarde lo mismo.
- `bloqueado_hasta` es texto ISO en los dos motores (como el resto de las fechas, [[adr-007-marcas-de-tiempo-texto-iso]]).
- Desactivar a un usuario también borra su token.

## Pruebas
[[arnes-integracion]]: PF-01 a PF-03, PF-16, PF-22 y PF-23; S-01, S-02, S-04, S-08, S-11, S-12 y S-13.

Ver también: [[modulo-app]] · [[seguridad-web]] · [[modelo-de-datos]]
