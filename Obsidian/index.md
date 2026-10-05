---
tipo: hub
tags: [indice, catalogo]
actualizado: 2026-10-04
---

# Índice del segundo cerebro de Sigma

Catálogo de todas las páginas. Empieza por [[inicio]]. Las reglas del wiki están en `Obsidian/CLAUDE.md` y
la bitácora en [[log]].

## Punto de partida
- [[inicio]]: panorama, estado actual, módulos, decisiones que no se vuelven a discutir y mapa del wiki.

## Proyecto
- [[empresa-y-problematica]]: el contratista de instalaciones eléctricas, el proceso actual en Excel y las multas del IMSS.
- [[equipo-y-contexto-academico]]: Equipo 4, materias, maestros, quién es dueño del repo (Gael, `rkiverr`).
- [[trayectoria-trl]]: cómo maduró el proyecto del TRL 1 al 5, y las contradicciones entre entregables.
- [[riesgos]]: R-01 a R-12, con probabilidad, impacto y mitigación.
- [[hoja-de-ruta-trl6]]: lo que falta para el piloto en ambiente real.

## Entregables
- [[entregables-trl]]: hub de los informes y formato del Mtro. Cortés Coss.
- [[entregable-1-trl1]]: problemática, variables del IMSS y objetivos.
- [[entregable-2-trl2]]: 3 alternativas, arquitectura elegida, costos y carta de inicio.
- [[entregable-3-trl3]]: prueba de concepto, 8/8 casos.
- [[entregable-4-trl4]]: prototipo integrado, 20 pruebas y 9 defectos corregidos.
- [[entregable-5-trl5]]: validación en ambiente relevante; de 6/10 a 10/10 criterios.

## Arquitectura
- [[arquitectura-general]]: las 4 capas y cómo se conectan los archivos.
- [[flujo-de-captura]]: lo que pasa, paso a paso, en un `POST /capturar`.
- [[rutas-http]]: todas las rutas con método, respuesta y códigos de estado.
- [[modelo-de-datos]]: las 5 tablas, índices, restricciones y estados.
- [[sigma-como-sistema-de-control]]: el lazo cerrado con sus dos lazos (interno y externo).

## Módulos (código)
- [[modulo-app]]: `sigma/app.py`, el controlador HTTP con CSRF, CSP y manejo de errores.
- [[modulo-validaciones]]: `sigma/validaciones.py`, el comparador de reglas.
- [[modulo-database]]: `sigma/database.py`, persistencia y selección de motor.
- [[modulo-exportar-idse]]: `sigma/exportar_idse.py`, el lote de texto (actuador).
- [[modulo-plazo]]: `sigma/plazo.py`, los 5 días hábiles.
- [[modulo-servidor]]: `servidor.py`, arranque en producción con waitress.
- [[modulo-interfaz]]: `sigma/templates/` y `sigma/static/`.
- [[arnes-prueba-de-concepto]]: `pruebas/test_prueba_concepto.py` (E3), regresión de 8 casos.
- [[arnes-ambiente-relevante]]: `pruebas/prueba_ambiente_relevante.py` (E5), bloques A–H.

## Reglas de negocio
- [[reglas-de-validacion]]: las 30 reglas, con su tipo (error o aviso) y su lugar en el código.
- [[plazo-legal]]: 5 días hábiles (art. 15 LSS y art. 74 LFT).
- [[salario-sdi-y-limites]]: SDI entre el salario mínimo y 25 UMA; tope en el lote.
- [[historial-afiliatorio]]: sin alta sobre alta vigente, sin doble baja y sin baja anterior al alta.
- [[catalogos-idse]]: tipos de movimiento, de trabajador, de salario, de jornada y causas de baja.
- [[lote-idse]]: formato del lote y el riesgo #1 (layout sin confirmar).

## Conceptos
- [[glosario]]: términos del IMSS, del proyecto y técnicos.
- [[curp]]: estructura y dígito verificador de RENAPO.
- [[nss]]: número de seguridad social y Luhn.
- [[rfc]]: RFC y su coherencia con la CURP.
- [[errores-vs-avisos]]: qué bloquea y qué solo advierte.
- [[normalizacion-de-datos]]: limpieza única de lo capturado.
- [[doble-motor-de-base-de-datos]]: PostgreSQL y SQLite con la misma lógica.
- [[seguridad-web]]: CSRF, CSP, cabeceras, OWASP y datos personales.
- [[accesibilidad]]: el estado no depende del color; contraste WCAG.
- [[niveles-trl]]: qué significa cada nivel TRL.

## Decisiones (ADR)
- [[decisiones]]: hub con la tabla de los 16 ADR.
- [[adr-001-cliente-servidor-con-sgbd-relacional]]: la Alternativa 3 del E2.
- [[adr-002-doble-motor-de-base-de-datos]]: PostgreSQL como objetivo y SQLite como respaldo.
- [[adr-003-un-solo-validador]]: el navegador y el servidor usan las mismas reglas.
- [[adr-004-errores-y-avisos-son-distintos]]: los avisos no bloquean.
- [[adr-005-422-conservando-lo-capturado]]: el rechazo no borra lo escrito.
- [[adr-006-frontend-sin-dependencias]]: sin CDN ni frameworks.
- [[adr-007-marcas-de-tiempo-texto-iso]]: fechas como texto ISO.
- [[adr-008-sql-con-marcadores-psycopg2]]: todo SQL con `%s`.
- [[adr-009-servidor-de-produccion-waitress]]: waitress; depuración solo a petición.
- [[adr-010-unicidad-del-movimiento-en-la-base]]: índice UNIQUE contra duplicados.
- [[adr-011-normalizacion-unica-y-data-longitud]]: pegar datos sin perder caracteres.
- [[adr-012-csrf-por-origin-y-csp-con-nonce]]: protección contra CSRF y XSS.
- [[adr-013-reglas-de-historial]]: validar contra el historial del trabajador.
- [[adr-014-limites-legales-del-sdi]]: límites del art. 28 LSS.
- [[adr-015-lazo-cerrado]]: la clasificación vigente del sistema.
- [[adr-016-arnes-como-caja-negra]]: el arnés del E5 prueba por HTTP.
- [[adr-017-paquete-sigma-y-carpeta-de-pruebas]]: la app es el paquete `sigma/` y los arneses viven en `pruebas/`.

## Operación
- [[como-arrancar]]: instalar, arrancar en desarrollo y en producción.
- [[configuracion]]: variables de entorno (`DATABASE_URL`, `SIGMA_DEBUG`, etc.).
- [[mantenimiento-anual]]: salario mínimo, UMA y días inhábiles que caducan cada año.
- [[problemas-frecuentes]]: errores comunes al arrancar y cómo resolverlos.
- [[guia-para-modificar-el-codigo]]: reglas y rutina para no romper nada.
- [[verificar-un-cambio-contra-main]]: demostrar que un cambio funciona igual que `main` (arnés en las dos versiones, lado a lado por HTTP y Chrome headless).
- [[como-se-hizo-el-entregable-5]]: receta completa del informe (python-docx, Mermaid, capturas y Word por COM).

## Pruebas
- [[estrategia-de-pruebas]]: los dos arneses y la rutina mínima después de un cambio.
- [[resultados-de-pruebas]]: cifras de antes y después y los criterios CA5-1 a CA5-10.

## Bugs
- [[bugs-corregidos]]: los del E4, E-01 a E-15 y BUG-01 (feriado de la LFT). No reintroducir.
- [[bugs-conocidos]]: sin bugs abiertos; limitaciones planeadas E-16 a E-20 y otras limitaciones.

## Historial
- [[cronologia]]: todos los hechos con fecha, commits y ramas.
- [[sesion-2026-09-10-rediseno-y-entregable-4]]: rediseño, PR #1 y Entregable 4.
- [[sesion-2026-10-04-entregable-5]]: Entregable 5, merge a `main` y creación de este wiki.
- [[sesion-2026-10-04-estructura-de-carpetas]]: reorganización del repo en `sigma/` y `pruebas/`.

## Consultas
- [[preguntas-frecuentes]]: usuarios semilla, insignia del patrón, punto verde, base local, ramas, etc.

---

## Fuentes crudas (`raw/`, inmutables)
**Entregables**
- `raw/entregables/e1-trl1-problematica.md`: texto del Entregable 1.
- `raw/entregables/e2-trl2-alternativas-y-arquitectura.md`: texto del Entregable 2.
- `raw/entregables/e3-trl3-prueba-de-concepto.md`: texto del Entregable 3.
- `raw/entregables/e4-trl4-prototipo-integrado.md`: texto del Entregable 4.
- `raw/entregables/e5-trl5-ambiente-relevante.md`: texto del Entregable 5.
- `raw/entregables/e5-rubrica-del-maestro.md`: rúbrica de 12 puntos del E5.

**Normativa**
- `raw/normativa/lss-ley-del-seguro-social.md`: arts. 15, 28, 304 A y 304 B (reforma DOF 15-01-2026).
- `raw/normativa/racerf-reglamento-afiliacion.md`: arts. 45, 46 y 47.
- `raw/normativa/lfpdppp-datos-personales.md`: arts. 14, 15, 18 y 19 (DOF 20-03-2025).
- `raw/normativa/lft-ley-federal-del-trabajo.md`: art. 74 (días de descanso obligatorio).
- `raw/normativa/valores-oficiales-2026.md`: salario mínimo y UMA de 2026.

**Historial y resultados**
- `raw/historial/git-log.md`: ramas, grafo y commits hasta `3afbc9a`; no incluye el commit que agrega este wiki.
- `raw/resultados/e3-arnes-prueba-de-concepto.md`: salida del arnés del E3 con el código vigente.
- `raw/resultados/e5-arnes-ambiente-relevante-antes.md`: salida del arnés del E5 con el código del E4.
- `raw/resultados/e5-arnes-ambiente-relevante-despues.md`: salida del arnés del E5 con el código ajustado.
