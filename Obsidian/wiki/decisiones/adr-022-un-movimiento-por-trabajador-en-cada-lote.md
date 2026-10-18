---
tipo: decision
estado: vigente
fecha: 2026-10-18
tags: [lote, idse, exportacion, historial, trl9]
fuentes: ["sigma/exportar_idse.py", "sigma/app.py", "pruebas/prueba_operacion.py"]
actualizado: 2026-10-18
---

# ADR-022: a lo más un movimiento por trabajador en cada lote

## Contexto
El IDSE recibe un archivo por tipo de movimiento ([[lote-idse]]) y valida cada movimiento contra la situación del
trabajador **cuando lo procesa**. En la aceptación por requerimiento del TRL 8 un lote salió con el alta y el
reingreso de una persona en el archivo de altas y su baja en el de bajas. Cualquier orden de carga deja un
movimiento inválido: si entra primero el de altas, el reingreso cae sobre un alta vigente; si entra primero el de
bajas, la baja cae sobre alguien que aún no está dado de alta.

## Decisión
`exportar_idse.un_movimiento_por_trabajador()` deja en cada lote **solo el primer movimiento pendiente de cada
trabajador** (por orden de captura). Los demás siguen como `Válido`; `app.exportar()` los anuncia en el aviso
(«quedan para el siguiente lote… cuando el IDSE lo confirme, genere el siguiente») y en la bitácora. Commit `569d82d`.

## Por qué
- Es independiente del orden en que la persona cargue los archivos.
- Los movimientos de un trabajador se capturan en orden (las reglas de historial lo obligan:
  [[adr-013-reglas-de-historial]]), así que el orden de captura es el orden lógico.
- El caso es raro (alta y baja, o baja y reingreso, entre dos lotes) y el costo es un lote más.

## Consecuencias
- Un trabajador contratado y despedido entre dos lotes necesita dos lotes; con reingreso, tres.
- El arnés del E6 cambió en PF-17, PF-18, PF-21 y el bloque L, que esperaban esos movimientos juntos
  ([[arnes-integracion]]).

## Alternativas descartadas
- **Indicar un orden de carga** (primero altas, luego bajas): no resuelve alta + baja + reingreso juntos.
- **Bloquear la captura** del reingreso hasta exportar la baja: frena a la capturista por algo que resuelve la
  exportación.

Ver también: [[decisiones]] · [[modulo-exportar-idse]] · [[arnes-operacion]]
