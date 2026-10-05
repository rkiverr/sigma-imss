---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [historial, reglas-de-negocio]
fuentes: ["sigma/app.py", "sigma/database.py"]
actualizado: 2026-10-04
---

# ADR-013: Validar cada movimiento contra el historial del trabajador

**Contexto.** Hasta el E4, cada movimiento se validaba aislado. En el bloque B del E5 se aceptaban sin aviso tres
situaciones (E-11):
- Un alta de alguien con alta vigente.
- La baja de alguien ya dado de baja.
- Una baja anterior a su alta.

Es el problema del E1: el Excel no distinguía un cambio de obra de una salida de la empresa.

**Decisión.** `app._validar_historial()` usa `database.estado_afiliatorio()` (SIN_REGISTRO, VIGENTE o
NO_VIGENTE, según el último movimiento por fecha real) y aplica la máquina de estados de
[[historial-afiliatorio]]. Se evalúa después de detectar duplicados.

**Por qué la baja sin historial es aviso y no error.** Al poner el sistema en marcha habrá personal que se dio
de alta antes, con el Excel.

**Origen.** La lógica viene de `reglas.py` de la versión alterna del E3 (no entregada).

**Resultado.** Las categorías B16, B17 y B18: 24 de 24 bloqueados.

Ver: [[decisiones]]
