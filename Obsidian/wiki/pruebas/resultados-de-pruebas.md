---
tipo: prueba
tags: [resultados, metricas, antes-despues, trl5]
fuentes: ["raw/resultados/e5-arnes-ambiente-relevante-antes.md", "raw/resultados/e5-arnes-ambiente-relevante-despues.md", "raw/resultados/e3-arnes-prueba-de-concepto.md", "raw/resultados/e6-arnes-integracion.md", "raw/resultados/e5-arnes-ambiente-relevante-trl6-version-corregida.md", "raw/resultados/e5-arnes-ambiente-relevante-trl6-codigo-e4.md", "raw/resultados/e3-arnes-prueba-de-concepto-trl6.md"]
actualizado: 2026-10-07
---

# Resultados de pruebas

## TRL 6: versión corregida (2026-10-07)
Son corridas sobre una **instalación limpia** de la rama local `trl6/correcciones`, en el mismo equipo
(Windows 11, i5-10400F, 32 GB, Python 3.14.3). Las salidas literales están en `raw/resultados/*trl6*` y
`raw/resultados/e6-arnes-integracion.md`.

| Arnés | Resultado |
|---|---|
| E3 ([[arnes-prueba-de-concepto]]) | 8/8, y el lote sale en dos archivos de 168 posiciones |
| E5 ([[arnes-ambiente-relevante]]) | **10/10** criterios. Detección 96.9 % (88 bloqueados, 36 avisados, 4 sin detectar); 0 duplicados; 0 hallazgos en G; 14/14 contrastes |
| E5 sobre el código del E4 (misma sesión) | 6/10. Detección 50.0 %; 7 duplicados y 2 pares con error 500; 5 hallazgos |
| E6 ([[arnes-integracion]]) | F 23/23 · L conforme (42 registros) · S 1 hallazgo de 14 (S-03) · R íntegro en 0.16 s, restauración en 0.85 s · C p95 13.6 ms (pantalla) y 8.5 ms (validación) por la LAN |

| Carga (bloque D) | 1 usuario | 3 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| Capturas por minuto | 931 | 2,022 | 3,008 | 3,935 | 3,771 |
| p95 de la captura | 22.2 ms | 46.6 ms | 55.7 ms | 85.4 ms | 127.8 ms |
| Captura más lenta | 132.2 ms | 202.2 ms | 545.4 ms | 837.2 ms | 580.1 ms |

- **Volumen (E):** con 10,000 movimientos, tablero p95 de 21.5 ms y búsqueda de 27.4 ms. La captura dio un p95
  de 261.6 ms (21–23 ms con 1,000 y 5,000).
- **Caída (F):** 0 de 940 capturas confirmadas perdidas; servicio en 2.94 s.
- **El login cuesta rendimiento.** Con 10 usuarios, de 5,609 (primera demostración, sin login) a 3,935
  capturas por minuto: cada petición consulta usuario y token, y la captura valida más campos. Con 20
  usuarios llegan menos escrituras a la vez y la captura más lenta bajó de 3.1 s a 0.58 s.

## TRL 5 (2026-10-04)

Las dos corridas finales se hicieron el **4 de octubre de 2026**, en el mismo equipo: Windows 11, Intel Core
i5-10400F (6 núcleos y 12 hilos) y 32 GB, con Python 3.14.3.
- **Antes:** el código del E4 (commit `4c79ce4`) con el servidor de desarrollo de Flask.
- **Después:** el código ajustado del E5 con waitress.

Las salidas literales están en `raw/resultados/`.

## Criterios de aceptación del TRL 5
| Criterio | Meta | Antes | Después |
|---|---|---|---|
| CA5-1 Operación nominal (140 movimientos, 3 capturistas) | 0 fallas; todo al lote y a la bitácora | 140/140 · cumple | 140/140 · **cumple** |
| CA5-2 Tiempo de respuesta (p95) | Captura ≤ 500 ms; validación en vivo ≤ 200 ms | 31.3 / 24.8 ms · cumple | 23.0 / 8.3 ms · **cumple** |
| CA5-3 Detección de errores | ≥ 90 %; 0 falsos positivos; 0 rechazos indebidos | 50.0 %; 0; 24 · **no cumple** | 96.9 %; 0; 0 · **cumple** |
| CA5-4 Capturas simultáneas | 0 duplicados; 0 errores 500 | 5; 7 · **no cumple** | 0; 0 · **cumple** |
| CA5-5 Capacidad (10 usuarios sin pausa) | Sin errores; p95 ≤ 500 ms | 0; 100.6 ms · cumple | 0; 94.7 ms · **cumple** |
| CA5-6 Volumen (10,000 movimientos) | Tablero ≤ 500 ms; lote ≤ 2 s | 41.0 ms; 21.0 ms · cumple | 17.9 ms; 23.5 ms · **cumple** |
| CA5-7 Recuperación | 0 perdidas; base íntegra; ≤ 1 min | 0; ok; 0.58 s · cumple | 0; ok; 0.61 s · **cumple** |
| CA5-8 Seguridad en red | 0 hallazgos en 8 pruebas | 5 · **no cumple** | 0 · **cumple** |
| CA5-9 Accesibilidad | Estados con texto; contraste ≥ 4.5:1 | 2 pares bajo 4.5:1 · **no cumple** | 14/14 · **cumple** |
| CA5-10 Regresión | 8 de 8 casos del E3 | 8/8 · cumple | 8/8 · **cumple** |

El código del E4 cumplía **6 de 10**; el código ajustado cumple **10 de 10**.

## Bloque B: errores de captura (8 casos por categoría)
| Categoría | Esperado | Antes | Después |
|---|---|---|---|
| B01 CURP y RFC en minúsculas con espacios a los lados | Aceptar | 8 rechazados | 8 aceptados |
| B02 CURP pegada con espacios internos | Aceptar | 8 rechazados | 8 aceptados |
| B03 NSS con espacios de agrupación | Aceptar | 8 rechazados | 8 aceptados |
| B04 CURP con un carácter de menos | Bloquear | 8 bloqueados | 8 bloqueados |
| B05 Letra O en lugar de cero en la CURP | Bloquear | 8 bloqueados | 8 bloqueados |
| B06 CURP con una consonante equivocada | Avisar | 8 sin aviso | 4 avisados, 4 sin aviso |
| B07 NSS con dos dígitos transpuestos | Avisar | 8 avisados | 8 avisados |
| B08 NSS con un dígito equivocado | Avisar | 8 avisados | 8 avisados |
| B09 RFC con otra fecha | Bloquear | 8 bloqueados | 8 bloqueados |
| B10 Nombre con un cero en lugar de la O | Bloquear | 8 sin aviso | 8 bloqueados |
| B11 SDI con el punto corrido (45.05) | Bloquear | 8 sin aviso | 8 bloqueados |
| B12 SDI mayor a 25 UMA | Avisar | 8 sin aviso | 8 avisados |
| B13 Alta sin condiciones de contratación | Bloquear | 8 bloqueados | 8 bloqueados |
| B14 Baja sin causa | Bloquear | 8 bloqueados | 8 bloqueados |
| B15 Fuera del plazo de 5 días hábiles | Avisar | 8 sin aviso | 8 avisados |
| B16 Alta con alta vigente | Bloquear | 8 sin aviso | 8 bloqueados |
| B17 Baja de quien ya fue dado de baja | Bloquear | 8 sin aviso | 8 bloqueados |
| B18 Baja anterior a su alta | Bloquear | 8 sin aviso | 8 bloqueados |
| B19 Movimiento repetido | Bloquear | 8 bloqueados | 8 bloqueados |

**Totales de los 128 errores:**
- Antes: 48 bloqueados, 16 avisados y 64 no detectados (**50.0 %**).
- Después: 88 bloqueados, 36 avisados y 4 no detectados (**96.9 %**).

En las 60 capturas limpias hubo **0 falsos positivos** en las dos versiones.

## Bloque D: carga (sin pausa, 15 s por nivel)
| Usuarios | Capturas por minuto (antes → después) | p95 de captura (antes → después) | Errores |
|---|---|---|---|
| 1 | 1,090 → 1,359 | 17.0 → 14.4 ms | 0 |
| 3 | 2,545 → 3,401 | 43.3 → 30.1 ms | 0 |
| 5 | 3,362 → 4,658 | 54.2 → 44.4 ms | 0 |
| 10 | 3,809 → 5,931 | 100.6 → 94.7 ms | 0 |
| 20 | 3,829 → 5,888 | **497.6 → 120.0 ms** | 0 |

Con 20 usuarios, la **captura más lenta** tardó 3.3 s antes y 6.0 s después, por la espera de escritura de SQLite.
El p95 no se afecta, pero es una razón para migrar a PostgreSQL. La memoria del servidor fue de 43–72 MB.

**Variabilidad entre corridas.** El p95 con 20 usuarios depende de la carga de la máquina. El mismo día, más
tarde, el código de `main` dio 182.6 y 175.2 ms, y el reorganizado en carpetas, 190.8, 218.4 y 145.8 ms, sin
errores en ninguno ([[sesion-2026-10-04-estructura-de-carpetas]]). Los 120.0 ms son los de la corrida del informe. Para comparar dos
versiones, córrelas una tras otra en la misma sesión.

## Bloque E: volumen
| Movimientos | Tablero p95 (antes → después) | Búsqueda p95 | Lote de 510 | Tamaño de la base |
|---|---|---|---|---|
| 1,000 | 24.6 → 12.9 ms | 15.0 → 15.1 ms | 20.4 → 24.7 ms | 0.29 → 0.31 MB |
| 5,000 | 34.3 → 15.6 ms | 29.8 → 19.0 ms | 20.6 → 23.0 ms | 1.17 → 1.30 MB |
| 10,000 | 41.0 → 17.9 ms | 37.7 → 24.0 ms | 21.0 → 23.5 ms | 2.27 → 2.52 MB |

## Bloques C, F, G y H
- **C:** duplicados en la base de 5 a **0**, y pares con error 500 de 7 a **0**. El doble envío a 40 ms ya
  funcionaba: 10 de 10.
- **F:** se perdieron **0** de 852 capturas confirmadas antes, y **0** de 1,250 después. Integridad `ok`, 0
  asientos huérfanos y arranque en unos 0.6 s.
- **G:** **5** hallazgos antes (Werkzeug visible, `/console` 200, folio con error 500 y detalle, CSRF aceptado,
  sin cabeceras) y **0** después.
- **H:** el texto tenue tenía 3.15:1 y 2.71:1; después, los 14 pares cumplen.

## Arnés del E3 (regresión)
8/8 con el código vigente. Salida en `raw/resultados/e3-arnes-prueba-de-concepto.md`.

Ver también: [[estrategia-de-pruebas]] · [[entregable-5-trl5]] · [[bugs-corregidos]]
