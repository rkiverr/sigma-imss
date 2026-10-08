---
tipo: historial
tags: [log, bitacora]
actualizado: 2026-10-04
---

# Log del segundo cerebro

Bitácora cronológica: solo se agrega al final y lo anterior no se edita.
Últimas entradas: `grep "^## \[" Obsidian/log.md | tail -5`.

## [2026-10-04] sistema | Creación del segundo cerebro (`Obsidian/`)
- Lo pidió Pedro: una carpeta `Obsidian/` en el repo con todo el contexto del proyecto, solo en `.md`, con el
  patrón LLM Wiki (fuentes crudas inmutables, wiki del agente y esquema).
- Creado `Obsidian/CLAUDE.md`: las tres capas, las convenciones, las operaciones, el mapa de impacto y las reglas.
- Solo contenido del proyecto Sigma; nada de otras materias.
- **Sin commit ni push** hasta que Pedro lo pida. Se subirá junto con los otros archivos actualizados.

## [2026-10-04] ingesta | Fuentes crudas: entregables E1–E5 y rúbrica del E5
- `raw/entregables/`: los 5 informes convertidos a Markdown desde los Word y PDF de `LAB AUTO/` (que solo se
  leyeron), más `e5-rubrica-del-maestro.md`.
- Se limpiaron los caracteres `​` que dejan los PDF.
- Páginas creadas: [[entregables-trl]], [[entregable-1-trl1]] a [[entregable-5-trl5]], [[trayectoria-trl]],
  [[empresa-y-problematica]], [[equipo-y-contexto-academico]], [[riesgos]] y [[hoja-de-ruta-trl6]].

## [2026-10-04] ingesta | Normativa: LSS, RACERF, LFPDPPP, LFT y valores oficiales de 2026
- `raw/normativa/`: artículos literales extraídos de los PDF oficiales, más `valores-oficiales-2026.md`
  (salario mínimo de 315.04 y UMA de 117.31).
- Páginas creadas: [[plazo-legal]], [[salario-sdi-y-limites]], [[historial-afiliatorio]], [[catalogos-idse]],
  [[lote-idse]], [[seguridad-web]] y [[mantenimiento-anual]].
- **Hallazgo:** la LFT vigente (art. 74, fr. VII, DOF 30-09-2024) pone el feriado de transmisión del Ejecutivo el
  **1 de octubre**, pero `plazo.py` usa el 1 de diciembre, con `anio % 6 == 0`. Quedó como BUG-01 en
  [[bugs-conocidos]]. No afecta a 2026 y se corrige solo si Pedro lo autoriza.

## [2026-10-04] ingesta | Código de sigma-imss (`main` en `c29ad8f`)
- Se leyeron `app.py`, `validaciones.py`, `database.py`, `exportar_idse.py`, `plazo.py`, `servidor.py`, los
  dos arneses, `templates/`, `static/`, `README.md`, `instrucciones/` y `CLAUDE.md`.
- Páginas creadas:
  - Arquitectura (5): [[arquitectura-general]], [[flujo-de-captura]], [[rutas-http]], [[modelo-de-datos]] y
    [[sigma-como-sistema-de-control]].
  - Módulos (9), desde [[modulo-app]] hasta [[arnes-ambiente-relevante]].
  - Reglas: [[reglas-de-validacion]] (las 30).
  - Conceptos (10), desde [[glosario]] hasta [[niveles-trl]].
- Decisiones: [[decisiones]] y los 16 ADR, de [[adr-001-cliente-servidor-con-sgbd-relacional]] a
  [[adr-016-arnes-como-caja-negra]].
- Operación: [[como-arrancar]], [[configuracion]], [[problemas-frecuentes]] y [[guia-para-modificar-el-codigo]].

## [2026-10-04] ingesta | Historial de Git y resultados de los arneses
- `raw/historial/git-log.md`: ramas, grafo y los 16 commits, generados con un script en el scratchpad.
- `raw/resultados/`:
  - La salida del arnés del E3 con el código vigente (8/8).
  - La salida del arnés del E5 antes (6/10 criterios).
  - La salida del arnés del E5 después (10/10).
- Páginas creadas: [[estrategia-de-pruebas]], [[resultados-de-pruebas]], [[bugs-corregidos]],
  [[bugs-conocidos]], [[cronologia]] y [[preguntas-frecuentes]].

## [2026-10-04] sesion | Sesiones de trabajo registradas
- [[sesion-2026-09-10-rediseno-y-entregable-4]]: el rediseño (`4c79ce4`), el PR #1 y el Entregable 4.
- [[sesion-2026-10-04-entregable-5]]: el arnés, los 15 ajustes, el Entregable 5, el merge `cffd375` a `main`, la
  documentación al día y este wiki.
- [[como-se-hizo-el-entregable-5]]: la receta completa para repetir el informe en el E6.

## [2026-10-04] lint | Revisión inicial del wiki
- 73 páginas en `wiki/` y 15 fuentes crudas. No hay nombres duplicados ni páginas huérfanas, y todas están en
  [[index]].
- Se omiten los "enlaces" que van dentro de bloques de código (ejemplos del esquema y matrices de daltonismo).
- Se agregó al esquema la excepción de nombre para [[preguntas-frecuentes]], que es un hub sin fecha.

## [2026-10-04] sistema | Punteros al segundo cerebro en el repo
- `CLAUDE.md` del repo: un recuadro al inicio que manda a leer `Obsidian/index.md` y [[inicio]], y a seguir el
  mapa de impacto de `Obsidian/CLAUDE.md`.
- `README.md`: una fila de `Obsidian/` en la tabla "Estructura".
- Ambos cambios son locales y van **sin commit**, igual que `Obsidian/`.

## [2026-10-04] ingesta | Corrección del calendario: feriado de transmisión del Ejecutivo (`3afbc9a`)
- Pedro autorizó corregir BUG-01. `plazo.py` y el arnés usan ahora el 1 de octubre con `anio % 6 == 2` (LFT, art.
  74, fr. VII, reforma del 30-09-2024). El calendario de 2026 no cambia.
- Verificación: arnés del E3 8/8; bloques B, C y G del E5 con 96.9 %, 0 duplicados y 0 hallazgos.
- Páginas actualizadas: [[bugs-corregidos]], [[bugs-conocidos]] (ya sin bugs abiertos), [[modulo-plazo]],
  [[plazo-legal]], [[mantenimiento-anual]], [[riesgos]], [[hoja-de-ruta-trl6]], [[inicio]], [[cronologia]] y
  [[sesion-2026-10-04-entregable-5]].
- `CLAUDE.md` del repo: nota del calendario en §3.13 y fila nueva en "Bugs que ya se corrigieron".

## [2026-10-04] ingesta | Historial de Git extraído de nuevo
- `raw/historial/git-log.md` se regeneró completo: 17 commits, hasta `3afbc9a`. No incluye el commit que agrega
  `Obsidian/`, porque se extrae antes de hacerlo.
- Desde ahora el volcado **omite los correos de los autores**, porque el repo es público y basta con los nombres.

## [2026-10-04] sistema | Publicación del segundo cerebro en GitHub
- Pedro: "haz todo eso y súbelo". Un commit agrega `Obsidian/`, los punteros en `CLAUDE.md` y `README.md`, y en
  `.gitignore` las carpetas `Obsidian/.obsidian/` y `Obsidian/.trash/` (configuración personal de Obsidian).
- Se empujó `main` a `github.com/rkiverr/sigma-imss`. El repo es **público**: el texto de los entregables
  (`raw/entregables/`) queda visible, con los nombres del equipo y los datos de la empresa.

## [2026-10-04] sistema | Reorganización del repositorio en carpetas
- Pedro pidió ordenar archivos y carpetas y aceptó la recomendación: la aplicación pasa al paquete `sigma/`
  (con `templates/` y `static/`), los arneses a `pruebas/` y sus salidas a `pruebas/resultados/` (ignorada).
  `python servidor.py` no cambia; `python app.py` pasa a ser `python -m sigma`.
- Decisión nueva: [[adr-017-paquete-sigma-y-carpeta-de-pruebas]]. Sesión: [[sesion-2026-10-04-estructura-de-carpetas]].
- Páginas actualizadas: [[inicio]], [[arquitectura-general]] (sección "Estructura de carpetas"), [[como-arrancar]],
  [[configuracion]], [[guia-para-modificar-el-codigo]], [[mantenimiento-anual]], [[estrategia-de-pruebas]],
  [[resultados-de-pruebas]], [[rutas-http]], [[decisiones]], [[cronologia]], las páginas de módulos y de arneses,
  [[adr-009-servidor-de-produccion-waitress]] y el `fuentes:` de 50 páginas, que ahora lleva la ruta real.
- `Obsidian/CLAUDE.md`: árbol de §2 y mapa de impacto de §5 con las rutas nuevas, y una fila para cambios de
  estructura. `raw/` no se tocó. `raw/historial/git-log.md` se regenera cuando la rama se integre.

## [2026-10-04] sesion | Verificación de la reorganización contra main
- Pedro pidió verificar que todo funciona y cumple como antes. Mismo arnés sobre `main` y sobre la rama: 10/10
  criterios del TRL 5 en las dos y 0 diferencias funcionales; lado a lado con copias de la base real, 18/18
  respuestas HTTP idénticas; Chrome headless sin errores de consola en los dos temas.
- Se quitó el import sin uso de `init_db` en `sigma/app.py`.
- Páginas: [[sesion-2026-10-04-estructura-de-carpetas]] (sección de verificación) y [[resultados-de-pruebas]]
  (variabilidad del p95). `CLAUDE.md` del repo: §6 "Estado verificado".

## [2026-10-04] sesion | Cierre de la reorganización: PR #2, método de verificación y cómo integrarlo
- Página nueva [[verificar-un-cambio-contra-main]]: las cinco comprobaciones contra `main`, con los dos scripts ya
  probados (`criterios_trl5.py` y `verificar_contra_main.py`, que van fuera del repo) y las trampas encontradas.
- Corrección de la verificación: `/api/validar` recibe JSON. Con JSON, las 18 respuestas siguen idénticas.
- [[preguntas-frecuentes]]: qué pasa en cada computadora al aceptar el PR #2, y cómo saber que funciona igual;
  se corrigió la de `app.py` y `servidor.py`.
- Actualizadas: [[sesion-2026-10-04-estructura-de-carpetas]] (PR #2, commits, lo que pasó después), [[rutas-http]],
  [[estrategia-de-pruebas]], [[inicio]] (fila "En revisión") y [[cronologia]].

## [2026-10-04] ingesta | Reorganización integrada a main (`fb3a4a8`) e historial de Git extraído de nuevo
- Pedro pidió subir todo a `main` y quitar el PR. Merge `--no-ff` de `mejora/estructura-de-carpetas` (`fb3a4a8`).
  Comprobación sobre `main`: compila, E3 con 8/8 y el servidor responde. El PR #2 quedó cerrado como integrado
  (GitHub no permite borrar PR).
- `CLAUDE.md` del repo: ramas al día (§1), apuntador al método de verificación (§5) y §6 con el merge.
  `README.md`: nota de Python 3.13 y `psycopg2`, `__init__.py` en el árbol y una sección "Documentación".
- Páginas: [[inicio]] (rama vigente; sin la fila "En revisión"), [[cronologia]] (fila y tabla de ramas),
  [[sesion-2026-10-04-estructura-de-carpetas]] (integración y pendientes), [[preguntas-frecuentes]] y
  [[adr-017-paquete-sigma-y-carpeta-de-pruebas]].
- `raw/historial/git-log.md` se regeneró completo, hasta `fb3a4a8`. No incluye el commit de documentación que
  lo contiene.

## [2026-10-04] sistema | Limpieza final: se borra la rama de la reorganización
- Pedro preguntó si el repo quedó listo y dejó la limpieza a criterio del agente. Se borró
  `mejora/estructura-de-carpetas` en GitHub y en local (`git branch -d`: estaba integrada en `fb3a4a8`). La página
  del PR #2 conserva los commits.
- Se borraron los reportes locales de las verificaciones (`pruebas/resultados/`, ignorada por Git).
- Páginas: [[cronologia]] (tabla de ramas) y [[sesion-2026-10-04-estructura-de-carpetas]] (pendientes).
  `CLAUDE.md` del repo §1. `raw/historial/git-log.md` se extrajo de nuevo con las ramas actuales.

## [2026-10-07] sesion | Entregable 6: primera demostración y correcciones del TRL 6 (rama local)
- Primera demostración con `main` (`7f43596`), sin tocar el código: 7 de 9 criterios y 18 problemas; el lote
  cumplía 7 de 18 aspectos del PDF oficial del IMSS. Pedro pidió corregirlos en el repo: todo lo de código, sin
  instalar programas, y Git **solo local**.
- Rama `trl6/correcciones`: `02aaad0`, `540a313`, `882d60f`, `86038c2`, `aee7bc0` y `8914883`. Sin push ni
  merge. La verificación reveló P-19 (4 s de espera a PostgreSQL), P-20 (carrera del token de sesión) y P-22.
- Instalación limpia de la rama: E3 8/8, E5 10/10, [[arnes-integracion]] F 23/23, L conforme (42), S 1 de 14
  (S-03). TRL 6 con 9 de 10 criterios; falta HTTPS.
- Páginas nuevas: [[sesion-2026-10-07-correcciones-trl6]], [[entregable-6-trl6]], [[arnes-integracion]],
  [[adr-018-inicio-de-sesion-roles-y-token]], [[adr-019-lote-con-la-estructura-oficial]],
  [[adr-020-respaldo-automatico]], [[adr-021-migraciones-de-datos-unicas]], [[modulo-usuarios]] y
  [[modulo-respaldo]].
- Reescritas: [[lote-idse]], [[modulo-exportar-idse]], [[hoja-de-ruta-trl6]] y [[bugs-conocidos]]. Actualizadas:
  - [[bugs-corregidos]] (P-05…P-22), [[catalogos-idse]], [[rutas-http]], [[modelo-de-datos]] y [[configuracion]];
  - [[como-arrancar]], las páginas de módulos, [[reglas-de-validacion]], [[seguridad-web]] y [[decisiones]];
  - [[inicio]], [[cronologia]], [[trayectoria-trl]] y [[riesgos]];
  - [[estrategia-de-pruebas]], [[resultados-de-pruebas]], [[mantenimiento-anual]], los dos arneses anteriores y
    [[entregables-trl]].

## [2026-10-07] ingesta | Entregable 6 (v2), rúbrica, salidas de los arneses e historial de Git
- `raw/entregables/`: `e6-trl6-integracion-y-demostracion.md` (texto del .docx v2, 33 págs.) y
  `e6-rubrica-del-maestro.md`.
- `raw/resultados/`: `e6-arnes-integracion.md`, `e3-arnes-prueba-de-concepto-trl6.md`,
  `e5-arnes-ambiente-relevante-trl6-version-corregida.md` y `e5-arnes-ambiente-relevante-trl6-codigo-e4.md`.
  Son las corridas finales sobre la instalación limpia.
- `raw/historial/git-log.md` se regeneró: 30 commits, hasta `8914883`. Incluye la rama local
  `trl6/correcciones`, pero no el commit de documentación que lo contiene.

## [2026-10-07] sistema | Esquema: tres arneses, fuentes del E6 y mapa de impacto
- `Obsidian/CLAUDE.md` §2: `pruebas/` con los arneses de E3, E5 y E6, y `raw/entregables/` con E1–E6.
- §5: filas para `sigma/usuarios.py` y `sigma/respaldo.py`, y [[arnes-integracion]] en la fila de arneses.
- `index.md`: páginas nuevas, ADR-018 a ADR-021 y las fuentes crudas del E6.

## [2026-10-07] sesion | Sigma terminado para la materia; el maestro solo recibe el documento
- Pedro aclaró que el repo es del equipo, que el maestro solo recibe el informe y que Sigma ya está completo para
  la materia. Los pendientes de [[hoja-de-ruta-trl6]] quedan como trabajo planeado, sin fecha.
- Páginas: [[entregable-6-trl6]] y [[sesion-2026-10-07-correcciones-trl6]] (pendientes al día).

## [2026-10-07] sesion | Rediseño del inicio de sesión y pie con el nombre de la empresa
- A pedido de Pedro: login en tarjeta dividida (panel de marca + formulario), ver u ocultar la contraseña, y un
  recuadro **temporal** con los accesos de prueba para el equipo, con botón "Usar". Se quita borrando su bloque
  en `login.html`.
- Pie: solo "Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V.", sin el texto del TRL 6.
- Verificado: login 302, error 401 dentro del diseño nuevo, capturas en claro, oscuro, tableta y móvil, contraste
  AA de los pares nuevos, E3 8/8, E6 F 23/23 y S 1 de 14 (S-03), y bloque H del E5 14/14.
- Página: [[modulo-interfaz]].

## [2026-10-08] sesion | Letras más grandes en la pantalla principal
- A pedido de Pedro ("las letras están muy pequeñas"): escala tipográfica +12–15 % en `estilos.css`, contenedor
  de 1180 a 1360 px y diálogo de 560 a 640 px. Los filtros de la tabla quedan en un renglón.
- Verificado con capturas (1920, 1366 y móvil, claro y oscuro), bloque H del E5 14/14 y E3 8/8.
- Página: [[modulo-interfaz]].

## [2026-10-08] sesion | Segundo ajuste de letras: texto normal, leyendas en negritas y ayudas
- A pedido de Pedro:
  - texto base de 17 px; títulos de tarjeta de 20 y sus descripciones de 16; etiquetas de 15;
  - textos de ayuda de 14.5;
  - leyendas de sección en negritas, de 14 px.
- Verificado con capturas, bloque H del E5 14/14 y E3 8/8. Página: [[modulo-interfaz]].

## [2026-10-08] sesion | Cuadros de métricas y barra superior más grandes
- A pedido de Pedro: números de las métricas de 32 a 42 px, cuadros con más relleno y barra superior con logo,
  insignias y botones más grandes. En pantallas anchas la barra no baja de renglón.
- Verificado con capturas (1920, 1366 y móvil), bloque H del E5 14/14 y E3 8/8. Página: [[modulo-interfaz]].

## [2026-10-08] sesion | Login con letras más grandes
- A pedido de Pedro: todo el texto del inicio de sesión más grande (tarjeta de 1200 px, campos de 56 px, lema de
  33 px y recuadro de accesos de prueba a 15.5 px).
- Verificado con capturas (1920, 1366, tableta y 500 px), bloque H del E5 14/14, E3 8/8 y E6 F 23/23.
- Página: [[modulo-interfaz]].
