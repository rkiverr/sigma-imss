---
tipo: entregable
tags: [trl4, prototipo, integracion, sqlite, postgresql]
fuentes: ["raw/entregables/e4-trl4-prototipo-integrado.md"]
actualizado: 2026-10-04
---

# Entregable 4 — TRL 4: diseño e integración del prototipo

**Fuente cruda:** `raw/entregables/e4-trl4-prototipo-integrado.md` (Word y PDF de unas 20 páginas, 9 figuras y
2 tablas; entregado alrededor del 15 de sep).
**Código:** commit `4c79ce4` de Pedro (10 de sep), integrado a `main` por el PR #1 (`9533587`, 11 de sep).

## Qué se demostró
Los componentes probados por separado en el E3 quedaron **integrados en una sola aplicación** operable de punta
a punta, en 4 capas: presentación, aplicación, persistencia y salida ([[arquitectura-general]]).

## Secciones (rúbrica del TRL 4)
Diseño detallado, diagrama eléctrico (**No aplica**), diagrama de control, diagrama de flujo, diagrama de
conexión, selección de componentes, diseño mecánico (**No aplica**), programación, integración de sensores,
actuadores y controlador, pruebas de laboratorio, resultados, ajustes y referencias.

## Ideas clave del E4
- **Tres principios:** un solo validador, integridad transaccional, y errores distintos de avisos
  ([[adr-003-un-solo-validador]], [[errores-vs-avisos]]).
- **Sensores virtuales:**
  - El formulario con máscaras.
  - `/api/validar`.
  - Las consultas de estado a la base.
- **Actuadores virtuales:**
  - La escritura transaccional.
  - La bitácora.
  - El lote IDSE.
  - La respuesta al operador.
- **Controlador:** `app.py`.
- **Diagrama de control:** lo llamó "lazo **abierto** con retroalimentación al operador". Después Pedro lo
  corrigió a lazo cerrado ([[adr-015-lazo-cerrado]]).
- **Diagrama de conexión:** puerto 5050, solo la LAN; la base nunca es accesible desde el navegador.
- **Selección definitiva:** Python 3, Flask 3 y Jinja2, PostgreSQL con psycopg2, **SQLite como respaldo** (el
  único cambio respecto al E2, [[adr-002-doble-motor-de-base-de-datos]]), HTML/CSS/JS propios, Git/GitHub y
  Windows 11.

## Pruebas y resultados
- 20 pruebas, todas correctas:
  - 8 casos de validación.
  - Exportación y concurrencia.
  - CURP repetida con otro NSS (422), duplicado (422), baja sin causa y RFC incoherente.
  - Usuario inválido, exportar sin pendientes y descargar sin lote.
  - Ruta inexistente (404), inyección SQL y XSS.
- Los 5 criterios de aceptación del E3 se cumplieron.

## Ajustes (9 defectos corregidos)
Todos están en [[bugs-corregidos]]:
- `IntegrityError` → 422.
- Usuario inválido.
- Descarga sin lote.
- Transacción sin revertir.
- Patrón vacío.
- El formulario perdía lo capturado.
- Cada exportación sobrescribía el lote.
- SQLite como respaldo.
- Casos C2 y C5 con catálogo.

## Trabajo planeado que dejó
Login, layout oficial del IDSE, correo a RH y servidor de producción. El **servidor de producción** se hizo en
el E5; lo demás sigue en [[hoja-de-ruta-trl6]].

## Cómo se generó
Sobre la plantilla de Word de Pedro, con 5 diagramas Mermaid renderizados en Chrome headless y 4 capturas
reales. El índice se arregló cambiando el campo a `\o "1-3"`. Detalle en [[sesion-2026-09-10-rediseno-y-entregable-4]].

## ⚠ Nota sobre metadatos
El archivo del E4 quedó con autor "BRENDA JANETT ALONSO GUTIERREZ", heredado de una plantilla externa. En el E5
se cambió a "Equipo 4".

Anterior: [[entregable-3-trl3]] · Siguiente: [[entregable-5-trl5]] · Hub: [[entregables-trl]]
