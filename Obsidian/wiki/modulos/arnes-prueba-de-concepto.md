---
tipo: modulo
tags: [pruebas, arnes, trl3, regresion]
fuentes: ["pruebas/test_prueba_concepto.py", "raw/resultados/e3-arnes-prueba-de-concepto.md"]
actualizado: 2026-10-04
---

# `pruebas/test_prueba_concepto.py` — arnés del Entregable 3

Tiene 269 líneas. Es el "desarrollo experimental" del [[entregable-3-trl3]]. Hoy sirve como **prueba de
regresión**: si cambias reglas, **tiene que seguir dando 8/8**.

```bash
python pruebas/test_prueba_concepto.py   # → pruebas/resultados/resultados_prueba_concepto.txt
```

## Cómo trabaja
- Sin `DATABASE_URL`, fija `SIGMA_DB=sqlite` y `SQLITE_PATH=pruebas/resultados/sigma_pruebas.db`, y **borra esa
  base al iniciar**. Así los resultados son reproducibles. Lo hace **antes** de importar `sigma.database`.
- Agrega la raíz del repositorio a `sys.path`, porque al correr el archivo directo Python solo ve `pruebas/`.
- Llama directamente a `validar_movimiento()`, la interfaz estable `(bool, list[str])`. **No usa HTTP.**

## Bloques
1. **Validación**: 8 casos (`CASOS_PRUEBA`).
   - C1: alta válida.
   - C2: baja válida con causa del catálogo.
   - C3: CURP de 9 caracteres.
   - C4: NSS con letras.
   - C5: fecha con guiones.
   - C6: 31 de febrero.
   - C7: tipo 99.
   - C8: nombre vacío.

   C1 y C2 deben ser **válidos**; C3–C8, **rechazados**.
2. **Exportación**: exporta los válidos a `pruebas/resultados/lote_idse_prueba.txt` y espera exactamente 2 líneas.
3. **Concurrencia**: 2 hilos insertan a la vez con usuarios distintos y espera ids distintos y 2 asientos en la
   bitácora.

Al final imprime el resumen frente a los 5 criterios de aceptación.

## Notas
- Al introducir los catálogos en el E4 se actualizaron C2 y C5, cuya causa de baja era texto libre.
- Los ajustes del E5 no rompieron ningún caso. La salida actual está en
  `raw/resultados/e3-arnes-prueba-de-concepto.md`.
- Genera `sigma_pruebas.db`, `resultados_prueba_concepto.txt` y `lote_idse_prueba.txt`, los tres en
  `pruebas/resultados/`, que está en `.gitignore`.

Ver también: [[estrategia-de-pruebas]] · [[arnes-ambiente-relevante]] · [[resultados-de-pruebas]]
