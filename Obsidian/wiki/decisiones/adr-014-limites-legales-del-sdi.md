---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [sdi, lss, salario-minimo, uma]
fuentes: ["sigma/validaciones.py", "sigma/exportar_idse.py", "raw/normativa/lss-ley-del-seguro-social.md"]
actualizado: 2026-10-04
---

# ADR-014: SDI entre el salario mínimo y 25 UMA; el lote exporta el tope

**Contexto.** El límite del SDI era de 1.00 a 10,000.00:
- Un SDI de 45.05, en vez de 450.50, **se aceptaba sin aviso** (E-08).
- Un SDI de 3,500 se aceptaba **y se exportaba** por encima del tope (E-09).

**Decisión.**
- **Error** si el SDI es menor al **salario mínimo general** vigente en la fecha del movimiento.
- **Error** si pasa de 10,000, porque eso casi siempre es un punto decimal mal puesto.
- **Aviso** si pasa de **25 UMA**.
- En el lote IDSE, `_sdi_para_cotizar()` exporta **el tope**; en la base se conserva el salario real.
- Los montos van en tablas por año (`SALARIO_MINIMO_GENERAL`, `UMA_DIARIA`). La UMA nueva rige desde el 1 de
  febrero.

**Por qué.** Es lo que dicen el **art. 28 de la LSS** (límite inferior: salario mínimo; superior: 25 veces) y el
**art. 45 del RACERF** (se comunica "sin exceder los límites del art. 28"). El salario por encima del tope puede
ser real, por eso es aviso.

**Consecuencia.** **Hay que actualizar las tablas cada año** ([[mantenimiento-anual]]).

Ver: [[salario-sdi-y-limites]] · [[decisiones]]
