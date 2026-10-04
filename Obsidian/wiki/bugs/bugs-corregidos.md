---
tipo: bug
estado: corregido
tags: [bugs, regresion, no-reintroducir]
fuentes: ["CLAUDE.md", "raw/entregables/e4-trl4-prototipo-integrado.md", "raw/entregables/e5-trl5-ambiente-relevante.md"]
actualizado: 2026-10-04
---

# Bugs corregidos: no reintroducir

Antes de cambiar el código, revisa que tu cambio no vuelva a abrir ninguno.

## Corregidos en el Entregable 4 (laboratorio)
| Bug original | Corrección | Dónde |
|---|---|---|
| Una CURP repetida con otro NSS reventaba con `IntegrityError` y error 500 | `conflicto_de_identidad()` revisa **antes** del INSERT | `database.py` |
| Un `usuario_id` vacío o no numérico daba `ValueError` y error 500 | `_usuario_valido()` lo valida contra la tabla | `app.py` |
| `/descargar-lote` sin archivo lanzaba una excepción | Revisa que exista y avisa | `app.py` |
| Una excepción a media captura dejaba la conexión abierta y la transacción sin revertir | *Context manager* `conexion(commit=True)` | `database.py` |
| Con la tabla `patron` vacía, `fetchone()["id"]` daba `TypeError` | `obtener_patron_id()` crea el patrón si falta | `database.py` |
| El formulario rechazado perdía lo capturado | Se vuelve a mostrar con los valores (422) | `app.py` |
| Cada exportación sobrescribía `lote_idse.txt` | Lotes con marca de tiempo en `exportaciones/` | `exportar_idse.py` |
| La aplicación no arrancaba sin PostgreSQL | SQLite como respaldo automático | `database.py` |
| La causa de baja era texto libre | Catálogo IDSE (se ajustaron los casos C2 y C5) | `validaciones.py` |
| El botón de tema mostraba "Claro" y "Oscuro" a la vez | Ocultar `.etiqueta-oscuro` por defecto | `estilos.css` |
| La insignia del patrón desbordaba en el celular | `max-width`, `overflow: hidden` y se oculta por debajo de 720 px | `estilos.css` |

## Corregidos en el Entregable 5 (ambiente relevante)
| Clave | Bug | Corrección | Severidad |
|---|---|---|---|
| E-01 | Consola de depuración de Werkzeug y versión del servidor expuestas a la LAN | `servidor.py` con waitress; `debug` solo con `SIGMA_DEBUG=1` | Alta |
| E-02 | Un folio enorme en `/api/movimiento` daba error 500 con detalle técnico | `FOLIO_MAXIMO` → 404 | Media |
| E-03 | Una captura desde otro sitio (CSRF) se guardaba | Verificación de `Origin` → 403 | Alta |
| E-04 | No había cabeceras de seguridad | CSP con nonce, `nosniff`, `X-Frame-Options` y `Referrer-Policy` | Media |
| E-05 | Capturas simultáneas: duplicados (5/25) y errores 500 (7/25) | Índice UNIQUE + `IntegrityError` → 422 | Alta |
| E-06 | Pegar una CURP o un NSS con espacios recortaba el dato (24/24 rechazados) | `data-longitud` y una máscara que recorta al final | Media |
| E-07 | La validación en vivo y el servidor normalizaban distinto | `normalizar_datos()` compartida | Baja |
| E-08 | Se aceptaba un SDI menor al salario mínimo (45.05) | Mínimo = salario mínimo general (art. 28 LSS) | Alta |
| E-09 | Un SDI arriba de 25 UMA no daba aviso y se exportaba sin topar | Aviso y tope en el lote | Media |
| E-10 | Un movimiento fuera de plazo no daba aviso | `plazo.py` | Alta |
| E-11 | Se aceptaban un alta sobre un alta vigente, una doble baja y una baja anterior a su alta | Reglas de historial | Alta |
| E-12 | El nombre admitía dígitos (un cero en lugar de la O) | `NOMBRE_REGEX` | Baja |
| E-13 | Una letra equivocada en la CURP no se detectaba | Aviso por dígito de RENAPO (**detecta 4 de 8**: límite del algoritmo, [[curp]]) | Media |
| E-14 | El texto tenue tenía 3.15:1 de contraste | `#5c6b84` (5.4:1) | Baja |
| E-15 | "La causa de baja es obligatorio" (sin concordancia) | Mensaje de catálogo neutro | Baja |

## Corregidos después del E5
| Clave | Bug | Corrección | Commit |
|---|---|---|---|
| BUG-01 | El feriado de transmisión del Ejecutivo se calculaba con la regla anterior: el 1 de diciembre con `anio % 6 == 0` (2022, 2028). La LFT reformada (DOF 30-09-2024, art. 74, fr. VII) lo fija el **1 de octubre** de 2024, 2030… | `anio % 6 == 2` y `date(anio, 10, 1)` en `plazo.dias_de_descanso()` y en `_descansos()` del arnés. Se documentó que la fr. IX (jornada electoral) se carga en `DIAS_INHABILES_ADICIONALES` | `3afbc9a` |

BUG-01 se detectó el 2026-10-04 al extraer el texto literal de la LFT (`raw/normativa/lft-ley-federal-del-trabajo.md`).
- **Efecto en 2026:** ninguno.
- **Sin la corrección:** en 2028 el 1 de diciembre habría contado como inhábil y en 2030 no se habría
  descontado el 1 de octubre.
- **Verificación:** el arnés del E3 dio 8/8; los bloques B, C y G del E5 dieron 96.9 %, 0 duplicados y
  0 hallazgos.
- **Para no reintroducirlo:** `plazo.py` y el arnés tienen **dos copias** del calendario; si se cambia una, hay
  que cambiar la otra.

Las limitaciones que el E5 dejó planeadas (E-16 a E-20) están en [[bugs-conocidos]] y en [[hoja-de-ruta-trl6]].

Ver también: [[resultados-de-pruebas]] · [[guia-para-modificar-el-codigo]]
