---
tipo: modulo
tags: [pruebas, arnes, trl6, integracion, lote, seguridad, respaldo]
fuentes: ["pruebas/prueba_integracion.py", "raw/resultados/e6-arnes-integracion.md"]
actualizado: 2026-10-07
---

# `pruebas/prueba_integracion.py` — arnés del Entregable 6

Tiene 767 líneas. Demuestra el **sistema completo integrado** ([[entregable-6-trl6]]):
- el servidor de producción corre como proceso aparte sobre una copia aislada;
- un "equipo de captura" entra por la **IP de la red local**, inicia sesión y recorre una semana de operación.

Solo existe en la rama `trl6/correcciones` y exige esa versión. Si no encuentra `sigma/usuarios.py`, termina con
un mensaje.

```bash
python pruebas/prueba_integracion.py                          # todo (~40 s)
python pruebas/prueba_integracion.py --bloques F,L --capturas # además guarda el HTML de las pantallas
python pruebas/prueba_integracion.py --etiqueta prueba        # sufijo en los nombres de los reportes
```

Genera `pruebas/resultados/resultados_integracion[_etiqueta].txt` y `.json`. Con `--capturas`, también guarda en
`pruebas/resultados/integracion/`:
- el HTML de las pantallas (login, rechazo, aviso, tablero y exportado);
- el intercambio de `/api/validar`, con la cookie enmascarada;
- los dos archivos del lote.

## Cómo trabaja
- Reutiliza `Servidor`, `Cliente` y `Plantilla` de [[arnes-ambiente-relevante]]. Hereda sus principios: caja
  negra por HTTP, una copia aislada por bloque y nunca toca `sigma_imss.db` ([[adr-016-arnes-como-caja-negra]]).
- En cada copia, `Servidor` fija la contraseña `prueba-sigma-2026` a los dos usuarios semilla con
  `python -m sigma.usuarios contrasena … --contrasena`.
- `Cliente(usuario_id=…)` inicia sesión la primera vez que lo necesita y guarda la cookie.
- Con sesión, una **redirección a `/login` cuenta como falla (401)**, no como captura guardada (lección de P-20,
  [[bugs-corregidos]]).
- `consola(srv, …)` corre `sigma.usuarios` o `sigma.respaldo` sobre la copia, con `SIGMA_DB=sqlite` y
  `SQLITE_PATH` apuntando a ella.

## Bloques
| Bloque | Prueba | Resultado final (2026-10-07) |
|---|---|---|
| F | Escenario de una semana por la IP de la LAN, en 23 casos (PF-01…PF-23): login fallido y correcto, validación en vivo, rechazo y corrección, historial (alta vigente, baja repetida, reingreso), plazo vencido, salario bajo, UMF faltante, apellidos al revés, rol captura sin lote (403), lote por tipo, descarga, búsqueda, historial "Incluido en lote IDSE", bitácora por sesión, cookie tras cerrar sesión | 23/23 |
| L | 42 movimientos (30 altas y 12 bajas): genera el lote y compara **cada campo de cada registro** con la base. Revisa 168 posiciones, "9" final, tipo por archivo, NSS, fecha, salario topado en centavos, jornada 0, UMF, CURP, causa, CRLF y Windows-1252 | Conforme |
| S | 14 comprobaciones: S-01 sin sesión, S-02 `usuario_id` ajeno, S-03 tráfico en claro, S-04 banderas de la cookie, S-05 métodos (405), S-06 rutas con `../`, S-07 página de error, S-08 POST sin sesión ni `Origin`, S-09 8 MB (413), S-10 puerto 5432, S-11 bloqueo, S-12 roles, S-13 cookie copiada tras cerrar sesión, S-14 diez logins simultáneos con la misma cuenta | 1 hallazgo (S-03) |
| R | Captura 40, respalda con `sigma.respaldo` y revisa su integridad; captura 5 más, borra la base y restaura | Íntegro en 0.16 s; restauración y arranque en 0.85 s |
| C | 300 peticiones de pantalla y de validación por `127.0.0.1` y por la IP de la LAN; tamaño y tiempo de cada enlace | p95 13.6 ms y 8.5 ms por la LAN |

Salida literal: `raw/resultados/e6-arnes-integracion.md`. Las cifras completas están en [[resultados-de-pruebas]].

## Trampas al mantenerlo
- **S-03** es un hallazgo esperado mientras no haya HTTPS. No lo "arregles" en el arnés; se cierra con P-11
  ([[hoja-de-ruta-trl6]]).
- Si cambian posiciones del lote, el bloque L lo detecta campo por campo. Actualiza primero `ESTRUCTURA` en
  [[modulo-exportar-idse]] y después las posiciones de `_campo()` en el arnés.
- En R, la bitácora tiene un asiento más después de restaurar: es el inicio de sesión de la verificación. Por eso
  `datos_recuperados` compara solo trabajadores y movimientos.
- Las 5 capturas posteriores al respaldo se pierden a propósito: miden el punto de recuperación.

Ver también: [[estrategia-de-pruebas]] · [[arnes-prueba-de-concepto]] · [[seguridad-web]] · [[lote-idse]]
