---
tipo: fuente-cruda
origen: "git log --all del repositorio sigma-imss"
extraido: 2026-10-04
nota: Volcado del historial de Git (sin correos de los autores). NO editar; se regenera con `git log --all --stat`.
---

# Historial de Git del repositorio sigma-imss

> Fuente cruda e inmutable. Remoto: https://github.com/rkiverr/sigma-imss

## Ramas al momento de extraer

```text
* main                                          3afbc9a [origin/main: ahead 1] Plazo: el feriado de transmisión del Ejecutivo es el 1 de octubre
  mejora/interfaz-y-validaciones                4c79ce4 [origin/mejora/interfaz-y-validaciones] Rediseña la interfaz y refuerza la validación y la persistencia
  trl5/ambiente-relevante                       b46ad50 Registra en CLAUDE.md los resultados del arnés de ambiente relevante
  remotes/origin/HEAD                           -> origin/main
  remotes/origin/main                           c29ad8f Instrucciones: actualiza la guía de uso con los cambios de la Entrega 5
  remotes/origin/mejora/interfaz-y-validaciones 4c79ce4 Rediseña la interfaz y refuerza la validación y la persistencia
  remotes/origin/trl5/ambiente-relevante        b46ad50 Registra en CLAUDE.md los resultados del arnés de ambiente relevante
```

## Grafo

```text
* 3afbc9a (HEAD -> main) Plazo: el feriado de transmisión del Ejecutivo es el 1 de octubre
* c29ad8f (origin/main, origin/HEAD) Instrucciones: actualiza la guía de uso con los cambios de la Entrega 5
* 438b7e6 CLAUDE.md: indica que main ya incluye la Entrega 5
*   cffd375 Integra la Entrega 5 (TRL 5): validación en ambiente relevante
|\  
| * b46ad50 (origin/trl5/ambiente-relevante, trl5/ambiente-relevante) Registra en CLAUDE.md los resultados del arnés de ambiente relevante
| * 0049036 Documenta el arranque en producción y las decisiones de la Entrega 5
| * cf3989b Interfaz: pegar datos sin perder caracteres, contraste AA y pie TRL 5
| * 76d101b Producción con waitress, reglas de historial y cierre de carreras y CSRF
| * cb3f643 Valida plazo legal, límites del SDI, dígito de la CURP y nombre
| * 321d660 Arnés TRL 5: conexiones persistentes, carreras reproducibles y opción --codigo
| * 26befae Agrega el arnés de pruebas en ambiente relevante (TRL 5)
* | 9533587 Merge pull request #1 from rkiverr/mejora/interfaz-y-validaciones
|\| 
| * 4c79ce4 (origin/mejora/interfaz-y-validaciones, mejora/interfaz-y-validaciones) Rediseña la interfaz y refuerza la validación y la persistencia
|/  
* ccdfe48 Actualiza README con solución a UnicodeDecodeError y agrega client_encoding a la conexión
* 7c1bc27 Documentar configuración de PostgreSQL y solución a UnicodeDecodeError
* e591752 Prototipo inicial: validación, base de datos y exportación IDSE (TRL3)
* 827835e first commit
```

## Commits (del más reciente al más antiguo)

### 3afbc9a — Plazo: el feriado de transmisión del Ejecutivo es el 1 de octubre

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 16:53:26 -0600
- **Commit:** `3afbc9aad5a500bf4abd1f0748fc73397c6ebb4a`
- **Padres:** c29ad8f

```text
Plazo: el feriado de transmisión del Ejecutivo es el 1 de octubre

La LFT reformada (DOF 30-09-2024, art. 74 fr. VII) fija el 1 de octubre de
cada seis años, cuando hay transmisión del Poder Ejecutivo Federal (2024,
2030...). El cálculo usaba la regla anterior: el 1 de diciembre con
anio % 6 == 0 (2022, 2028). Se corrige en plazo.dias_de_descanso() y en la
copia del arnés (_descansos). Las jornadas electorales de la fr. IX se
documentan como días que se agregan en DIAS_INHABILES_ADICIONALES.

No cambia el calendario de 2026. Verificado: arnés del E3 8/8 y bloques
B, C y G del arnés del E5 (96.9 %, 0 duplicados, 0 hallazgos).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 plazo.py                     | 11 +++++++----
 prueba_ambiente_relevante.py |  4 ++--
 2 files changed, 9 insertions(+), 6 deletions(-)
```

### c29ad8f — Instrucciones: actualiza la guía de uso con los cambios de la Entrega 5

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 13:21:55 -0600
- **Commit:** `c29ad8fd63f35318af1e9eb9d672e03aa85a3e6d`
- **Padres:** 438b7e6

```text
Instrucciones: actualiza la guía de uso con los cambios de la Entrega 5

Plazo legal, reglas de historial, SDI según la LSS, nuevos avisos, datos
pegados con espacios, servidor.py y plazo.py, protección en red y límites
actuales del prototipo (TRL 5).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 instrucciones/Instrucciones.md | 75 +++++++++++++++++++++++++++++++++---------
 1 file changed, 59 insertions(+), 16 deletions(-)
```

### 438b7e6 — CLAUDE.md: indica que main ya incluye la Entrega 5

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 13:18:32 -0600
- **Commit:** `438b7e6e6a97afdb11f15655d7db0a4f8c36f440`
- **Padres:** cffd375

```text
CLAUDE.md: indica que main ya incluye la Entrega 5

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 CLAUDE.md | 8 +++++++-
 1 file changed, 7 insertions(+), 1 deletion(-)
```

### cffd375 — Integra la Entrega 5 (TRL 5): validación en ambiente relevante

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 13:15:02 -0600
- **Commit:** `cffd3759d3c6436756f2f8ecf78071a5b60eb45d`
- **Padres:** 9533587 b46ad50

```text
Integra la Entrega 5 (TRL 5): validación en ambiente relevante

- Servidor de producción con waitress (servidor.py); app.py solo para
  desarrollo, en 127.0.0.1 y con depuración solo si SIGMA_DEBUG=1.
- Plazo legal de 5 días hábiles (plazo.py, art. 15 LSS y art. 74 LFT).
- SDI según el art. 28 LSS: mínimo = salario mínimo, aviso arriba de 25 UMA
  y lote IDSE con el salario topado.
- Reglas de historial: sin alta sobre alta vigente, sin doble baja y sin
  baja anterior al alta.
- Índice UNIQUE del movimiento: capturas simultáneas sin duplicados ni 500.
- CSRF por Origin, CSP con nonce y cabeceras de seguridad.
- Normalización única (datos pegados con espacios), dígito de la CURP,
  nombre sin dígitos y contraste WCAG AA.
- Arnés prueba_ambiente_relevante.py (bloques A-H) y documentación.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 .gitignore                   |    1 +
 CLAUDE.md                    |  117 +++-
 README.md                    |   52 +-
 app.py                       |  210 +++++--
 database.py                  |   53 ++
 exportar_idse.py             |   22 +-
 instrucciones/Ejecutar.md    |   22 +-
 instrucciones/README.md      |   13 +-
 plazo.py                     |   98 +++
 prueba_ambiente_relevante.py | 1382 ++++++++++++++++++++++++++++++++++++++++++
 requirements.txt             |    3 +
 servidor.py                  |   40 ++
 static/css/estilos.css       |    2 +-
 static/js/app.js             |   22 +-
 templates/base.html          |    4 +-
 templates/index.html         |    8 +-
 validaciones.py              |  160 ++++-
 17 files changed, 2107 insertions(+), 102 deletions(-)
```

### b46ad50 — Registra en CLAUDE.md los resultados del arnés de ambiente relevante

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:30:30 -0600
- **Commit:** `b46ad50c03cd6d84e937ca33fc1165024263bbd7`
- **Padres:** 0049036

```text
Registra en CLAUDE.md los resultados del arnés de ambiente relevante

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 CLAUDE.md | 16 ++++++++++++++++
 1 file changed, 16 insertions(+)
```

### 0049036 — Documenta el arranque en producción y las decisiones de la Entrega 5

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:25:50 -0600
- **Commit:** `00490363b9d46073dfc13d8dc65dc526c8b79fa5`
- **Padres:** cf3989b

```text
Documenta el arranque en producción y las decisiones de la Entrega 5

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 CLAUDE.md                 | 101 +++++++++++++++++++++++++++++++++++++++++-----
 README.md                 |  52 +++++++++++++++++++-----
 instrucciones/Ejecutar.md |  22 ++++++----
 instrucciones/README.md   |  13 ++++--
 4 files changed, 155 insertions(+), 33 deletions(-)
```

### cf3989b — Interfaz: pegar datos sin perder caracteres, contraste AA y pie TRL 5

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:25:50 -0600
- **Commit:** `cf3989b83d9c913dd586eebbe76d3e213f81e30f`
- **Padres:** 76d101b

```text
Interfaz: pegar datos sin perder caracteres, contraste AA y pie TRL 5

- CURP, NSS, RFC y fecha usan data-longitud: la máscara limpia y después
  recorta. Con maxlength, pegar un NSS con espacios perdía dígitos.
- Texto tenue #5c6b84 (5.4:1), antes 3.15:1 (no cumplía WCAG 2.1 AA).
- Nonce de CSP en el script del tema y pie actualizado a TRL 5.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 static/css/estilos.css |  2 +-
 static/js/app.js       | 22 +++++++++++++++++-----
 templates/base.html    |  4 ++--
 templates/index.html   |  8 ++++----
 4 files changed, 24 insertions(+), 12 deletions(-)
```

### 76d101b — Producción con waitress, reglas de historial y cierre de carreras y CSRF

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:25:49 -0600
- **Commit:** `76d101bd38854c9a06f61aa13995d2bb47485e30`
- **Padres:** cb3f643

```text
Producción con waitress, reglas de historial y cierre de carreras y CSRF

- servidor.py arranca con waitress; app.py queda para desarrollo, en
  127.0.0.1 y con depuración solo si SIGMA_DEBUG=1 (antes la consola de
  Werkzeug y el detalle de los errores quedaban expuestos a la red local).
- Reglas de historial: no se acepta un alta sobre un alta vigente, la baja
  de quien ya fue dado de baja ni una baja anterior a su alta.
- Índice UNIQUE del movimiento e IntegrityError -> 422: dos capturas
  simultáneas ya no dejan duplicados ni errores 500.
- POST con Origin ajeno -> 403; CSP con nonce y cabeceras de seguridad.
- Folio fuera de rango en /api/movimiento -> 404 en lugar de 500.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 app.py           | 210 ++++++++++++++++++++++++++++++++++++++++++++-----------
 database.py      |  53 ++++++++++++++
 requirements.txt |   3 +
 servidor.py      |  40 +++++++++++
 4 files changed, 265 insertions(+), 41 deletions(-)
```

### cb3f643 — Valida plazo legal, límites del SDI, dígito de la CURP y nombre

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:25:49 -0600
- **Commit:** `cb3f643ac1fa9572af5a4faa4d28e1f00851b440`
- **Padres:** 321d660

```text
Valida plazo legal, límites del SDI, dígito de la CURP y nombre

Ajustes de la validación en ambiente relevante (Entrega 5, TRL 5):
- plazo.py: cinco días hábiles del art. 15 LSS con los descansos del art. 74
  LFT; aviso si el movimiento está vencido o en su último día.
- SDI: error si es menor al salario mínimo general y aviso si rebasa 25 UMA
  (art. 28 LSS); el lote IDSE lleva el SDI topado (art. 45 RACERF).
- Dígito verificador de la CURP (RENAPO) como aviso.
- El nombre ya no admite dígitos ni símbolos (un 0 en lugar de una O).
- normalizar_datos(): una sola normalización para el formulario y la API.
- Mensajes de catálogo con concordancia correcta.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 exportar_idse.py |  22 +++++++-
 plazo.py         |  98 ++++++++++++++++++++++++++++++++++
 validaciones.py  | 160 +++++++++++++++++++++++++++++++++++++++++++++++++------
 3 files changed, 264 insertions(+), 16 deletions(-)
```

### 321d660 — Arnés TRL 5: conexiones persistentes, carreras reproducibles y opción --codigo

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:20:31 -0600
- **Commit:** `321d660ef5c08a2d47cb101185726d5bfd0be80d`
- **Padres:** 26befae

```text
Arnés TRL 5: conexiones persistentes, carreras reproducibles y opción --codigo

- Cada capturista virtual reutiliza su conexión y libera el puerto al
  cerrarla, para medir al servidor y no el agotamiento de puertos del cliente.
- En las carreras ambos envíos parten con la conexión ya abierta.
- --codigo permite probar otra versión del sistema (la de la Entrega 4).
- La memoria se mide en el intérprete hijo del lanzador del entorno virtual.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 prueba_ambiente_relevante.py | 119 +++++++++++++++++++++++++++++++++----------
 1 file changed, 93 insertions(+), 26 deletions(-)
```

### 26befae — Agrega el arnés de pruebas en ambiente relevante (TRL 5)

- **Autor:** Pedro Luna
- **Fecha:** 2026-10-04 12:02:26 -0600
- **Commit:** `26befaec84ecf2f9999fe9449c509f0befe34e94`
- **Padres:** 4c79ce4

```text
Agrega el arnés de pruebas en ambiente relevante (TRL 5)

Prueba el sistema completo en condiciones semejantes a las de la empresa:
servidor como proceso independiente, capturistas concurrentes que emulan
al navegador, plantilla sintética con identificadores oficiales coherentes,
errores típicos de captura, carreras, carga, volumen, caída del servidor,
seguridad en red y contraste WCAG. Cada bloque usa una copia aislada.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
 .gitignore                   |    1 +
 prueba_ambiente_relevante.py | 1315 ++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 1316 insertions(+)
```

### 9533587 — Merge pull request #1 from rkiverr/mejora/interfaz-y-validaciones

- **Autor:** rkiver
- **Fecha:** 2026-09-11 22:17:38 -0600
- **Commit:** `95335871bed8b6e9192b24d98eaa026dcc7714eb`
- **Padres:** ccdfe48 4c79ce4

```text
Merge pull request #1 from rkiverr/mejora/interfaz-y-validaciones

Rediseño de la interfaz y refuerzo de validación y persistencia
```

```text
 .gitignore                     |   5 +
 CLAUDE.md                      | 207 ++++++++++
 README.md                      | 167 ++++++--
 app.py                         | 484 ++++++++++++++++++-----
 database.py                    | 423 +++++++++++++++++---
 exportar_idse.py               |  85 +++-
 instrucciones/Ejecutar.md      | 170 ++++++++
 instrucciones/Instrucciones.md | 245 ++++++++++++
 instrucciones/README.md        |  77 ++++
 requirements.txt               |   7 +-
 static/css/estilos.css         | 851 +++++++++++++++++++++++++++++++++++++++++
 static/js/app.js               | 437 +++++++++++++++++++++
 templates/base.html            |  77 ++++
 templates/error.html           |  21 +
 templates/index.html           | 769 ++++++++++++++++++++-----------------
 test_prueba_concepto.py        |  27 +-
 validaciones.py                | 320 ++++++++++++++--
 17 files changed, 3766 insertions(+), 606 deletions(-)
```

### 4c79ce4 — Rediseña la interfaz y refuerza la validación y la persistencia

- **Autor:** Pedro Luna
- **Fecha:** 2026-09-10 12:09:03 -0600
- **Commit:** `4c79ce43d9f7cce71ec2252e623dbdb840aaedc8`
- **Padres:** ccdfe48

```text
Rediseña la interfaz y refuerza la validación y la persistencia

Interfaz
- Rediseño completo con sistema de diseño propio en paleta azul marino,
  sin dependencias externas ni CDN (funciona sin conexión a internet).
- Tema claro y oscuro: sigue al sistema operativo y se puede fijar con el
  botón de la barra; la elección se recuerda y no parpadea al cargar.
- Validación en vivo campo por campo contra el mismo validador del servidor
  (POST /api/validar), para que la ayuda visual no pueda desviarse de la regla.
- Máscaras de captura, contadores y selector de fecha que rellena el DDMMAAAA
  que exige el IDSE.
- Los campos de alta y de baja se muestran según el tipo de movimiento.
- Tablero de métricas, búsqueda por nombre/CURP/NSS, filtros, paginación y
  detalle del expediente con su bitácora.
- Plantillas divididas en base.html + index.html + error.html.
- Sigue funcionando sin JavaScript: el servidor valida igual.

Correcciones de estabilidad
- CURP repetida con otro NSS reventaba con IntegrityError; ahora se detecta
  antes del INSERT y devuelve un mensaje entendible.
- usuario_id vacío o no numérico provocaba ValueError; ahora se valida.
- /descargar-lote lanzaba excepción si no existía el archivo.
- Las conexiones quedaban abiertas ante una excepción; se agrega un context
  manager que garantiza commit, rollback y cierre.
- La tabla patron vacía provocaba TypeError.
- El formulario rechazado perdía todo lo capturado; ahora se conserva.

Validación
- Fecha de nacimiento contenida en la CURP y coherencia CURP/RFC.
- Catálogos IDSE para tipo de trabajador, salario, jornada y causa de baja.
- SDI numérico con topes; campos obligatorios según alta o baja.
- Detección de movimientos duplicados y de NSS repetidos.
- Avisos que no bloquean: dígito verificador del NSS y fechas lejanas.

Persistencia
- Selección automática de motor: PostgreSQL si hay servidor accesible y
  psycopg2 instalado, SQLite como respaldo. Misma lógica de negocio en ambos,
  porque toda la capa superior usa SQL estándar.
- Los lotes IDSE se guardan con marca de tiempo en exportaciones/, en lugar
  de sobrescribir siempre el mismo archivo.

Documentación
- CLAUDE.md con la arquitectura y el porqué de cada decisión.
- instrucciones/ con guía de arranque, comandos rápidos y explicación
  funcional del sistema.

Verificado por HTTP: altas, bajas, duplicados, conflictos de identidad,
exportación, descarga, 404, inyección SQL y XSS, sin errores en el log.
El arnés de pruebas sigue en 8/8 casos y los tres bloques CUMPLE.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

```text
 .gitignore                     |   5 +
 CLAUDE.md                      | 207 ++++++++++
 README.md                      | 167 ++++++--
 app.py                         | 484 ++++++++++++++++++-----
 database.py                    | 423 +++++++++++++++++---
 exportar_idse.py               |  85 +++-
 instrucciones/Ejecutar.md      | 170 ++++++++
 instrucciones/Instrucciones.md | 245 ++++++++++++
 instrucciones/README.md        |  77 ++++
 requirements.txt               |   7 +-
 static/css/estilos.css         | 851 +++++++++++++++++++++++++++++++++++++++++
 static/js/app.js               | 437 +++++++++++++++++++++
 templates/base.html            |  77 ++++
 templates/error.html           |  21 +
 templates/index.html           | 769 ++++++++++++++++++++-----------------
 test_prueba_concepto.py        |  27 +-
 validaciones.py                | 320 ++++++++++++++--
 17 files changed, 3766 insertions(+), 606 deletions(-)
```

### ccdfe48 — Actualiza README con solución a UnicodeDecodeError y agrega client_encoding a la conexión

- **Autor:** Gael Rivera
- **Fecha:** 2026-09-09 23:17:09 -0600
- **Commit:** `ccdfe48d6a44c89fc3dd0496408766a4a5e41952`
- **Padres:** 7c1bc27

```text
Actualiza README con solución a UnicodeDecodeError y agrega client_encoding a la conexión
```

```text
 app.py                  |  46 +++--
 database.py             |  95 ++++++----
 requirements.txt        |   2 +
 templates/index.html    | 448 ++++++++++++++++++++++++++++++++++++++----------
 test_prueba_concepto.py |  72 ++++----
 5 files changed, 486 insertions(+), 177 deletions(-)
```

### 7c1bc27 — Documentar configuración de PostgreSQL y solución a UnicodeDecodeError

- **Autor:** Gael Rivera
- **Fecha:** 2026-09-09 23:15:48 -0600
- **Commit:** `7c1bc2712825e4a7175bfd9d8ed9e23b7c41e543`
- **Padres:** e591752

```text
Documentar configuración de PostgreSQL y solución a UnicodeDecodeError
```

```text
 README.md | 44 +++++++++++++++++++++++++++++++-------------
 1 file changed, 31 insertions(+), 13 deletions(-)
```

### e591752 — Prototipo inicial: validación, base de datos y exportación IDSE (TRL3)

- **Autor:** Gael Rivera
- **Fecha:** 2026-09-08 00:41:44 -0600
- **Commit:** `e591752715d03916133fee0efc0c13f42922b5e5`
- **Padres:** 827835e

```text
Prototipo inicial: validación, base de datos y exportación IDSE (TRL3)
```

```text
 .gitignore              |   6 ++
 README.md               | Bin 30 -> 1798 bytes
 app.py                  | 116 +++++++++++++++++++++++
 database.py             | 109 ++++++++++++++++++++++
 exportar_idse.py        |  33 +++++++
 templates/index.html    | 112 ++++++++++++++++++++++
 test_prueba_concepto.py | 242 ++++++++++++++++++++++++++++++++++++++++++++++++
 validaciones.py         |  90 ++++++++++++++++++
 8 files changed, 708 insertions(+)
```

### 827835e — first commit

- **Autor:** Gael Rivera
- **Fecha:** 2026-09-07 23:59:57 -0600
- **Commit:** `827835e1fff9602748b994115f66febffc42c6bb`
- **Padres:** 

```text
first commit
```

```text
 README.md | Bin 0 -> 30 bytes
 1 file changed, 0 insertions(+), 0 deletions(-)
```
