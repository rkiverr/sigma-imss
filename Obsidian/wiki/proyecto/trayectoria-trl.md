---
tipo: proyecto
tags: [trl, entregables, madurez]
fuentes: ["raw/entregables/", "raw/historial/git-log.md"]
actualizado: 2026-10-07
---

# Trayectoria TRL de Sigma

Cómo fue madurando el proyecto, entregable por entregable. Qué significa cada nivel: [[niveles-trl]].

| TRL | Entregable | Qué se demostró | Estado del código | Fecha |
|---|---|---|---|---|
| 1 | [[entregable-1-trl1]] | Problemática, variables del IMSS, objetivos | Sin código | ago 2026 |
| 2 | [[entregable-2-trl2]] | 3 alternativas; se eligió **cliente-servidor + SGBD relacional**; diagrama de bloques, costos, riesgos, carta de inicio | Sin código | ago–sep 2026 |
| 3 | [[entregable-3-trl3]] | **Prueba de concepto**: validación con regex, exportación, concurrencia con 2 hilos. 8/8 casos | Gael: commits `827835e`–`ccdfe48` (7–9 sep) | sep 2026 |
| 4 | [[entregable-4-trl4]] | **Prototipo integrado** de punta a punta; 20 pruebas; 9 defectos corregidos | Pedro: `4c79ce4` (10 sep) → PR #1 → `9533587` (11 sep) | ~15 sep 2026 |
| 5 | [[entregable-5-trl5]] | **Validación en ambiente relevante**: arnés A–H, antes y después; 10/10 criterios | Pedro + Claude: 7 commits, merge `cffd375` (4 oct) | 4 oct 2026 (redactado) |
| 6 | [[entregable-6-trl6]] | **Sistema completo integrado y demostrado** en ambiente relevante: instalación limpia, lote oficial de 168 posiciones, login con roles, respaldo; 9 de 10 criterios (falta HTTPS) | Pedro + Claude: rama local `trl6/correcciones`, 6 commits (7 oct) | 7 oct 2026 (redactado) |
| 7 | (pendiente) | Piloto en la oficina con datos reales y acuse del IMSS | — | [[hoja-de-ruta-trl6]] |

## Hilo conductor
- **E1 → E2:** del problema (Excel por colores) a la solución elegida (Alternativa 3,
  [[adr-001-cliente-servidor-con-sgbd-relacional]]).
- **E2 → E3:** el diagrama de bloques se volvió código, un módulo por bloque ([[sigma-como-sistema-de-control]]).
- **E3 → E4:** se corrigieron los problemas que el E3 dejó abiertos: el NSS repetido daba error 500 y no se
  validaban catálogos ni el SDI. También se integró todo en una aplicación usable.
- **E4 → E5:** el E4 funcionaba en laboratorio; en condiciones de empresa aparecieron 20 errores. 15 se
  corrigieron, 4 quedaron planeados y 1 es límite del algoritmo de RENAPO ([[bugs-corregidos]]).
- **E5 → E6:** la primera demostración del sistema integrado y la comparación con el PDF oficial del IMSS
  mostraron que el lote no tenía la estructura de 168 posiciones y que faltaban login y respaldo. Se
  corrigieron el mismo día; quedó pendiente solo el cifrado en la red ([[entregable-6-trl6]]).

## ⚠ Contradicciones entre entregables
- La **clasificación del lazo** cambió de nombre: el E2 y el E3 dicen "lazo cerrado"; el E4 dice "lazo abierto
  con retroalimentación al operador"; el E5 vuelve a "lazo cerrado". Lo vigente es **lazo cerrado** (decisión de
  Pedro del 2026-09-19, [[adr-015-lazo-cerrado]]).
- El E1 menciona el movimiento **07** (modificación de salario), pero ningún nivel lo implementó
  ([[hoja-de-ruta-trl6]]).
- El E5 llamaba al TRL 6 "demostración en ambiente real". La rúbrica del E6 dice "ambiente relevante": el
  piloto con datos reales pasa a TRL 7.
- El E1 ya decía "jornada 0 = normal", pero el código usó 1 hasta el E6 (P-06, [[catalogos-idse]]).
- El E2 calcula costos de 3,000 a 4,000 MXN. Una autorrevisión del equipo detectó que la carta de inicio
  firmada podría decir otra cifra (por confirmar).

Ver también: [[entregables-trl]] · [[cronologia]] · [[inicio]]
