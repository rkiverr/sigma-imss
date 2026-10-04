---
tipo: historial
tags: [sesion, rediseno, entregable-4, pr-1]
fuentes: ["raw/historial/git-log.md", "raw/entregables/e4-trl4-prototipo-integrado.md"]
actualizado: 2026-10-04
---

# Sesión del 10 al 15 de sep de 2026: rediseño y Entregable 4

Trabajo de Pedro con Claude Code. Resultados: el commit `4c79ce4`, el PR #1 y el [[entregable-4-trl4]].

## 10 de sep: rediseño completo
**Lo que pidió Pedro:** una interfaz moderna, mejor lógica, un botón de modo claro y oscuro, y terminar la página
y correrla.

**Hallazgo inicial:** en la laptop no había PostgreSQL ni `psycopg2` (el puerto 5432 estaba cerrado), así que la
app del E3 **no arrancaba**. De ahí salió el doble motor ([[adr-002-doble-motor-de-base-de-datos]]).

**Lo que se hizo:**
- **Frontend nuevo sin dependencias** ([[adr-006-frontend-sin-dependencias]], [[modulo-interfaz]]):
  - Tablero de métricas.
  - Validación en vivo por campo.
  - Máscaras de captura.
  - Calendario que llena `DDMMAAAA`.
  - Campos condicionales de alta y baja.
  - Búsqueda, filtros y paginación.
  - Diálogo de detalle.
  - Tema claro y oscuro que se recuerda.
- **`database.py`** ([[modulo-database]]):
  - Selección automática de motor.
  - *Context manager* transaccional.
  - Detección de conflictos de identidad y de duplicados.
- **`validaciones.py`** ([[modulo-validaciones]]):
  - Errores por campo.
  - Catálogos IDSE.
  - Coherencia entre CURP y RFC.
  - SDI con topes.
  - Luhn del NSS como **aviso** ([[errores-vs-avisos]]).
- **`app.py`** ([[modulo-app]]):
  - `/api/validar` y `/api/movimiento/<id>`.
  - Páginas de 404, 422, 500 y 503.
  - Un formulario que conserva lo capturado ([[adr-005-422-conservando-lo-capturado]]).
- Lotes con marca de tiempo en `exportaciones/`.
- **Verificación** por HTTP: altas, bajas, duplicados, conflictos, exportación, descarga, 404, inyección SQL y
  XSS. Hubo 0 errores en el log y el arnés dio 8/8.

## 10 de sep: paleta, documentación y subida
- **Paleta:** se cambió el verde por **azul marino** (`#1c3f77`), porque las tarjetas se perdían contra el fondo
  verdoso. Quedó un fondo azul grisáceo con tarjetas blancas.
- **Documentación:** se crearon `CLAUDE.md` en la raíz del repo y `instrucciones/` con tres guías.
- **Subida:** el commit va en la rama `mejora/interfaz-y-validaciones` y se abrió el **PR #1** para que Gael decidiera.
  `main` no se tocó. Gael lo fusionó el 11 de sep (`9533587`).

## ~15 de sep: Entregable 4
- Se redactó sobre la plantilla de Word de Pedro, que ya traía portada y encabezados.
- **Figuras:**
  - 5 diagramas en Mermaid renderizados en Chrome headless y recortados con Pillow: arquitectura, control,
    flujo en dos columnas, conexión y entidad-relación.
  - 4 capturas reales.
- **Índice:** se actualizó con Word por COM. El campo TOC de la plantilla usaba `\t "Heading 1,…"` (nombres en
  inglés) y el Word en español no lo llenaba; se cambió a `\o "1-3"`.
- **Script generador:** Pedro no quiso archivos extra en el repo y se descartó. El método se reutilizó y mejoró
  en el E5 ([[como-se-hizo-el-entregable-5]]).
- Las fuentes Mermaid del E4 se describen en [[arquitectura-general]], [[flujo-de-captura]] y
  [[modelo-de-datos]].

## Preguntas que surgieron
Las respuestas están en [[preguntas-frecuentes]]:
- Los usuarios del desplegable.
- La insignia del patrón.
- El punto verde.
- Si "se enlazó una base de datos".
- La rama que aparece dos veces en GitHub.

## Lo que dejó abierto
- La clasificación "lazo abierto con retroalimentación al operador". Pedro la cambió a lazo cerrado el 19 de sep
  ([[adr-015-lazo-cerrado]]).
- Login, layout oficial del IDSE, correo a RH y servidor de producción. El servidor se hizo en
  [[sesion-2026-10-04-entregable-5]]; lo demás sigue en [[hoja-de-ruta-trl6]].

Ver también: [[cronologia]]
