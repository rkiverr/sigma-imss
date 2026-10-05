---
tipo: decision
estado: vigente
fecha: 2026-09-10 (Entregable 4)
tags: [validacion, errores, avisos]
fuentes: ["sigma/validaciones.py"]
actualizado: 2026-10-04
---

# ADR-004: Errores y avisos son cosas distintas

**Decisión.** `validar_campos()` devuelve **dos** diccionarios por campo:
- `errores`: bloquean el guardado.
- `avisos`: se muestran, pero dejan pasar.

**Por qué.** Algunos datos son sospechosos pero legítimos. El caso de origen fue el **dígito de Luhn del NSS**:
hay NSS históricos válidos que no lo cumplen, y bloquearlos impediría capturar movimientos reales.

**Consecuencias.** En la interfaz, el error es rojo y bloquea; el aviso es ámbar y deja guardar con un *flash*
"warning". El E5 agregó más avisos con el mismo criterio: dígito de la CURP, tope de 25 UMA, plazo legal y baja
sin historial. Tabla y regla para el futuro en [[errores-vs-avisos]].

Ver: [[reglas-de-validacion]] · [[decisiones]]
