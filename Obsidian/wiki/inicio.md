---
tipo: hub
tags: [sigma, panorama, inicio]
fuentes: ["README.md", "CLAUDE.md", "raw/entregables/e6-trl6-integracion-y-demostracion.md", "raw/historial/git-log.md"]
actualizado: 2026-10-07
---

# Sigma — panorama del proyecto

**Sigma** es un sistema web para capturar, validar y exportar las **altas y bajas de trabajadores ante el
IMSS** (los movimientos afiliatorios). Se hizo para **Desarrollos Eléctricos y Soluciones Avanzadas S.A. de
C.V.**, una contratista de instalaciones eléctricas de Escobedo, N.L. que hoy hace este trámite a mano en un
Excel donde el estado de cada trabajador se marca solo con colores ([[empresa-y-problematica]]).

Es el proyecto académico del **Equipo 4** para Laboratorio de Automatización, que se presenta por niveles
TRL ([[equipo-y-contexto-academico]]).

## Estado actual (2026-10-07)

| | |
|---|---|
| Nivel de madurez | **TRL 6**: sistema completo integrado y demostrado en ambiente relevante; 9 de 10 criterios ([[entregable-6-trl6]]) |
| Rama de trabajo | `main` (la copia del escritorio). El 2026-10-08 se le integró `trl6/correcciones` (avance rápido, `7fffd1c`): lote oficial de 168 posiciones, inicio de sesión con roles, respaldo automático, rediseño del login y arnés del E6 ([[sesion-2026-10-07-correcciones-trl6]]) |
| Rama publicada | `main` en GitHub (`github.com/rkiverr/sigma-imss`). Incluye el E5 desde el merge `cffd375`, la corrección del calendario (`3afbc9a`), este segundo cerebro y la reorganización en `sigma/` y `pruebas/` (merge `fb3a4a8`, [[adr-017-paquete-sigma-y-carpeta-de-pruebas]]) ([[cronologia]]) |
| Cómo se arranca | `python servidor.py` → `http://localhost:5050`. En la rama del E6, antes: `python -m sigma.usuarios contrasena admin.rrhh` ([[como-arrancar]]) |
| Pruebas | `python pruebas/test_prueba_concepto.py` (8/8), `python pruebas/prueba_ambiente_relevante.py` y, en la rama del E6, `python pruebas/prueba_integracion.py` ([[resultados-de-pruebas]]) |
| Siguiente nivel | TRL 7: piloto en la oficina con datos reales, después de HTTPS y de un lote de prueba en el IDSE ([[hoja-de-ruta-trl6]]) |

## Qué hace, en una línea por paso

```mermaid
flowchart LR
  A["Capturista escribe<br/>el movimiento"] --> B["Validación en vivo<br/>campo por campo"]
  B --> C["Servidor valida otra vez:<br/>formato, ley, historial"]
  C -- "error" --> A
  C -- "válido" --> D[("Base de datos<br/>+ bitácora")]
  D --> E["Lote de texto<br/>para el IDSE"]
  E --> F["El usuario lo carga<br/>en el IDSE del IMSS"]
```

1. El capturista escribe un **alta (08)** o una **baja (02)** en el navegador ([[modulo-interfaz]]).
2. Mientras escribe, la página pregunta al servidor si cada campo es válido ([[normalizacion-de-datos]]).
3. Al guardar, el servidor revisa formato, reglas de la LSS, plazo legal e historial del trabajador
   ([[reglas-de-validacion]], [[flujo-de-captura]]).
4. Si todo está bien, lo guarda junto con un asiento en la bitácora ([[modelo-de-datos]]). Si no, devuelve el
   formulario con el error de cada campo.
5. Al final, administración arma el **lote**: un archivo de altas y uno de bajas, de 168 posiciones por
   registro, que se cargan en el **IDSE** ([[lote-idse]]). Desde el E6 todo pasa por un inicio de sesión con
   roles ([[modulo-usuarios]]).

## Cómo está hecho

Python 3 con Flask y waitress, PostgreSQL con SQLite como respaldo automático, y HTML/CSS/JS propios sin
dependencias externas. Ver [[arquitectura-general]].

| Archivo | Página |
|---|---|
| `servidor.py` | [[modulo-servidor]] |
| `sigma/app.py` (y `sigma/__main__.py`, el arranque de desarrollo) | [[modulo-app]] |
| `sigma/validaciones.py` | [[modulo-validaciones]] |
| `sigma/plazo.py` | [[modulo-plazo]] |
| `sigma/database.py` | [[modulo-database]] |
| `sigma/exportar_idse.py` | [[modulo-exportar-idse]] |
| `sigma/usuarios.py` (rama del E6) | [[modulo-usuarios]] |
| `sigma/respaldo.py` (rama del E6) | [[modulo-respaldo]] |
| `sigma/templates/`, `sigma/static/` | [[modulo-interfaz]] |
| `pruebas/test_prueba_concepto.py` | [[arnes-prueba-de-concepto]] |
| `pruebas/prueba_ambiente_relevante.py` | [[arnes-ambiente-relevante]] |
| `pruebas/prueba_integracion.py` (rama del E6) | [[arnes-integracion]] |

Por qué está organizado así: [[adr-017-paquete-sigma-y-carpeta-de-pruebas]].

## Lo que no se vuelve a discutir

Las decisiones de diseño y sus porqués están en [[decisiones]]. Las cinco más importantes:
- El sistema se modela como **lazo cerrado** ([[sigma-como-sistema-de-control]]).
- **Un solo validador** compartido por navegador y servidor ([[adr-003-un-solo-validador]]).
- **Errores ≠ avisos**: un error impide guardar; un aviso solo pide confirmar ([[errores-vs-avisos]]).
- **Doble motor** PostgreSQL / SQLite ([[doble-motor-de-base-de-datos]]).
- La **unicidad** de cada movimiento la garantiza la base de datos ([[adr-010-unicidad-del-movimiento-en-la-base]]).

## Números que conviene recordar

- Detección de errores típicos de captura: **96.9 %** (antes del E5: 50 %).
- Capturas simultáneas del mismo movimiento: **0 duplicados y 0 errores 500** (antes: 5 y 7).
- Capacidad: unas **3,900 capturas por minuto** con 10 usuarios sin pausa en la versión con inicio de sesión
  (5,600–5,900 sin él); la empresa supone hasta 140 al mes.
- Lote: **42 de 42** registros conformes con la estructura oficial del IMSS (bloque L del [[arnes-integracion]]).
- Detalle en [[resultados-de-pruebas]].

## Pendientes principales

- **HTTPS** en la red local: el único criterio del TRL 6 que no se cumple (P-11, [[hoja-de-ruta-trl6]]).
- Un lote de prueba en el IDSE para confirmar codificación, CRLF y Ñ ([[lote-idse]]); servidor PostgreSQL (P-14).
- Cargar cada año los días inhábiles del IMSS y las jornadas electorales ([[mantenimiento-anual]]). No hay bugs
  abiertos ([[bugs-conocidos]]).

## Mapa del wiki

- **Proyecto:** [[empresa-y-problematica]] · [[equipo-y-contexto-academico]] · [[trayectoria-trl]] · [[riesgos]] · [[hoja-de-ruta-trl6]]
- **Entregables:** [[entregables-trl]] y una página por informe (E1–E6).
- **Arquitectura:** [[arquitectura-general]] · [[flujo-de-captura]] · [[rutas-http]] · [[modelo-de-datos]] · [[sigma-como-sistema-de-control]]
- **Reglas del IMSS:** [[reglas-de-validacion]] · [[plazo-legal]] · [[salario-sdi-y-limites]] · [[historial-afiliatorio]] · [[catalogos-idse]] · [[lote-idse]]
- **Conceptos:** [[glosario]] y los conceptos técnicos.
- **Operación:** [[como-arrancar]] · [[configuracion]] · [[mantenimiento-anual]] · [[problemas-frecuentes]] · [[guia-para-modificar-el-codigo]]
- **Calidad:** [[estrategia-de-pruebas]] · [[resultados-de-pruebas]] · [[bugs-corregidos]] · [[bugs-conocidos]]
- **Historia:** [[cronologia]] y las sesiones de trabajo.
- **Preguntas frecuentes:** [[preguntas-frecuentes]]
