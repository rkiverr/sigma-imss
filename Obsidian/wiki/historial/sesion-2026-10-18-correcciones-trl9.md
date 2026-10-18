---
tipo: historial
tags: [sesion, trl9, operacion, correcciones, lote]
fuentes: ["pruebas/prueba_operacion.py", "sigma/exportar_idse.py", "sigma/app.py", "servidor.py"]
actualizado: 2026-10-18
---

# Sesión 2026-10-18: correcciones de la operación (TRL 9)

## Qué se pidió
Pedro pidió el Entregable 9 (TRL 9, «Operación, evaluación y cierre del proyecto»). La rúbrica pide «problemas
encontrados durante la operación» y «soluciones implementadas», y Pedro aprobó corregir en el código los cuatro
hallazgos que seguían abiertos del TRL 7 y del TRL 8.

## Qué se hizo
Rama `trl9/operacion`, desde `main` `509a64d`:
1. `2b8eb5e`: sello por exportación y consecutivo (O-03).
2. `ab350dc`: «Último lote» por exportación (O-01).
3. `569d82d`: un movimiento por trabajador en cada lote (O-02, [[adr-022-un-movimiento-por-trabajador-en-cada-lote]]).
4. `635a002`: `servidor.py` revisa el puerto al arrancar (O-04).
5. `e92f533`: [[arnes-operacion]] nuevo y ajuste del [[arnes-integracion]] (PF-17, PF-18, PF-21 y bloque L).

## Resultados
- [[arnes-operacion]]: **0 de 4** en `509a64d` y **4 de 4** con las correcciones.
- Regresión: E3 8/8; E5 10/10 criterios; E6 F 23/23, L conforme (30 altas y 12 bajas en dos lotes) y S con solo S-03.
- Único dato que cambia en el E5 (no es criterio): el lote del bloque E exporta 260 líneas en lugar de 510, porque
  `_precargar()` deja pendientes el alta y la baja de 250 trabajadores y las bajas esperan al siguiente lote.

## Decisiones
- La regla es «a lo más un movimiento por trabajador en cada lote», no «un orden de carga», porque con alta, baja
  y reingreso juntos ningún orden funciona.
- El recuadro de contraseñas de prueba del login (H-03 del E7) se deja como está, por decisión previa de Pedro.

Ver también: [[cronologia]] · [[bugs-corregidos]]
