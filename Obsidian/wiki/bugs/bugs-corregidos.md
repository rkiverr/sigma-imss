---
tipo: bug
estado: corregido
tags: [bugs, regresion, no-reintroducir]
fuentes: ["CLAUDE.md", "raw/entregables/e4-trl4-prototipo-integrado.md", "raw/entregables/e5-trl5-ambiente-relevante.md"]
actualizado: 2026-10-07
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


## Corregidos en el Entregable 6 (rama local `trl6/correcciones`, 2026-10-07)
Los encontró la demostración del E6 (instalación limpia, escenario por la red local, comparación con la estructura
oficial del IMSS y los arneses). Claves P-xx del informe del E6.

| Clave | Bug | Corrección | Commit |
|---|---|---|---|
| P-06 | Catálogo de jornada propio: el "1" de la jornada normal el IMSS lo lee como "un día a la semana" | Catálogo oficial 0–6 y migración | `02aaad0` |
| P-07 | Lote con campos separados por `\|`, sin nombre, UMF ni guía, altas y bajas juntas | Estructura oficial de 168 posiciones, un archivo por tipo ([[adr-019-lote-con-la-estructura-oficial]]) | `02aaad0` |
| P-08 | Sin autenticación: cualquiera en la red capturaba a nombre de cualquiera | Inicio de sesión con roles ([[adr-018-inicio-de-sesion-roles-y-token]]) | `02aaad0` |
| P-09 | El selector de usuario volvía a `admin.rrhh` en cada recarga | Sin selector: el usuario sale de la sesión | `02aaad0` |
| P-10 | `GET /capturar`, TRACE, PUT y DELETE → 500 "El movimiento no se guardó" | `error_http()` conserva el código (405) | `02aaad0` |
| P-12 | Sin respaldo de la base | `respaldo.py`, al arrancar y cada 24 h ([[adr-020-respaldo-automatico]]) | `02aaad0` |
| P-13 | `requirements.txt` no instalaba psycopg2 en Python 3.13+ | `psycopg2-binary>=2.9.11` | `02aaad0` |
| P-15 | La exportación no quedaba en el historial de cada movimiento | Asiento "Incluido en lote IDSE" | `02aaad0` |
| P-16 | Sin límite de tamaño de petición | `MAX_CONTENT_LENGTH` → 413 | `02aaad0` |
| P-17 | Montos legales solo hasta 2026, sin aviso | `aviso_montos_sin_cargar()` (los montos se siguen cargando cada año) | `02aaad0` |
| P-18 | El pie decía "TRL 5" | "TRL 6" | `02aaad0` |
| P-05 | Sin `SECRET_KEY`, cada reinicio cerraba las sesiones | `.clave_sesion` persistente | `02aaad0` |
| — | La cookie seguía sirviendo después de cerrar sesión (sesión en cookie) | Token de sesión en la base | `02aaad0` |
| P-19 | Con psycopg2 instalado y sin PostgreSQL, cada arranque esperaba 4 s (`localhost` por IPv6 e IPv4) | `127.0.0.1` y `connect_timeout=1` (1 s); `SIGMA_DB=sqlite` lo evita | `882d60f` |
| P-20 | Dos equipos que entraban a la vez con la misma cuenta escribían tokens distintos y uno quedaba fuera (la prueba de caída mostró 640 capturas "confirmadas" que no estaban en la base: eran redirecciones al inicio de sesión) | Token creado con `WHERE sesion_token IS NULL` y releído; el arnés cuenta la redirección al login como falla | `86038c2` |
| P-21 | Verificar el respaldo dejaba `-wal` y `-shm` junto a la copia | `journal_mode = DELETE` en la copia | `02aaad0` |
| P-22 | El aviso de exportación decía "1 bajas" | "altas: 8 en …; bajas: 1 en …" | `8914883` |

**Para no reintroducirlos:** el bloque L del [[arnes-integracion]] verifica el lote campo por campo; S-05, S-09,
S-13 y S-14 cubren 405, 413, la cookie copiada y los inicios de sesión simultáneos.

Ver también: [[resultados-de-pruebas]] · [[guia-para-modificar-el-codigo]]
