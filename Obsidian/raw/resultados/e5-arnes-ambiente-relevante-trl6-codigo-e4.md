---
tipo: fuente-cruda
origen: "resultados_ambiente_relevante_antes.txt"
generado: 2026-10-07
nota: Salida literal del arnés prueba_ambiente_relevante.py. NO editar.
---

# Resultados del arnés de ambiente relevante — código del E4 (línea base del E6)

> Fuente cruda e inmutable. Corrida del 2026-10-07 con `--codigo` sobre `git archive 4c79ce4` y el servidor de desarrollo, para la comparación antes/después del E6.

```text
REPORTE DE RESULTADOS — VALIDACIÓN EN AMBIENTE RELEVANTE (ENTREGA 5 / TRL 5)
Sistema para la automatización de altas y bajas de seguro social
Fecha: 07/10/2026 19:05 · servidor: desarrollo · Python 3.14.3 · 12 núcleos lógicos

==============================================================================
BLOQUE A — MES DE OPERACIÓN SIMULADO (3 capturistas)
==============================================================================
  Arranque de obras (altas): 60 movimientos en 4.7 s; aceptados 60; lote IDSE con 60 línea(s) (HTTP 302).
  Rotación de cuadrillas (bajas y altas): 55 movimientos en 4.4 s; aceptados 55; lote IDSE con 55 línea(s) (HTTP 302).
  Cierre de obra (bajas) y reingresos: 25 movimientos en 1.8 s; aceptados 25; lote IDSE con 25 línea(s) (HTTP 302).
  Movimientos enviados: 140 · aceptados 140 · con aviso 0 · bloqueados 0 · fallas 0
  En base: 140 · exportados en lotes: 140 · sin asiento en bitácora: 0 · atribución errónea: 0
  /api/validar             n=700   p50=9.8 ms  p95=16.3 ms  máx=144.2 ms
  POST /capturar           n=140   p50=18.9 ms  p95=38.3 ms  máx=200.4 ms
  GET / (tras captura)     n=140   p50=16.8 ms  p95=33.6 ms  máx=50.0 ms
  POST /exportar           n=3     p50=17.3 ms  p95=17.5 ms  máx=17.5 ms

==============================================================================
BLOQUE B — ERRORES TÍPICOS DE CAPTURA
==============================================================================
  B01 CURP y RFC en minúsculas con espacios a los lados    bloq=8 aviso=0 acept=0 falla=0 -> REVISAR (0/8)
        ejemplo: La CURP debe tener 18 caracteres; se capturaron 16.
  B02 CURP pegada con espacios internos                    bloq=8 aviso=0 acept=0 falla=0 -> REVISAR (0/8)
        ejemplo: La CURP debe tener 18 caracteres; se capturaron 16.
  B03 NSS pegado con espacios de agrupación                bloq=8 aviso=0 acept=0 falla=0 -> REVISAR (0/8)
        ejemplo: El NSS debe tener exactamente 11 dígitos; se capturaron 8.
  B04 CURP con un carácter de menos                        bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La CURP debe tener 18 caracteres; se capturaron 17.
  B05 Letra O en lugar de cero en la CURP                  bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Formato de CURP inválido: se esperan 4 letras, 6 dígitos de fecha, sexo H o M, 5 letras, 1 alfanumérico y 1 dígito verificador.
  B06 CURP con una consonante equivocada (longitud correct bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #81 validado y guardado correctamente.
  B07 NSS con dos dígitos transpuestos                     bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #89 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 7). Confírmalo contra el documento of
  B08 NSS con un dígito equivocado                         bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #97 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 8). Confírmalo contra el documento of
  B09 RFC con fecha distinta a la de la CURP               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La fecha de nacimiento del RFC no coincide con la de la CURP.
  B10 Nombre con un cero en lugar de la letra O            bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #105 validado y guardado correctamente.
  B11 SDI con el punto decimal corrido (45.05 en vez de 45 bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #113 validado y guardado correctamente.
  B12 SDI mayor al tope de 25 UMA                          bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #121 validado y guardado correctamente.
  B13 Alta sin condiciones de contratación                 bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El tipo de trabajador es obligatorio para este tipo de movimiento.; El tipo de salario es obligatorio para este tipo de movimiento.; El tipo de jornad
  B14 Baja sin causa de baja                               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La causa de baja es obligatorio para este tipo de movimiento.
  B15 Movimiento capturado fuera del plazo de 5 días hábil bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #137 validado y guardado correctamente.
  B16 Alta de un trabajador que ya tiene alta vigente (cam bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #146 validado y guardado correctamente.
  B17 Baja de un trabajador que ya fue dado de baja        bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #163 validado y guardado correctamente.
  B18 Baja con fecha anterior a la de su alta              bloq=0 aviso=0 acept=8 falla=0 -> REVISAR (0/8)
        ejemplo: Movimiento #186 validado y guardado correctamente.
  B19 Movimiento repetido (mismo trabajador, tipo y fecha) bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Este movimiento ya fue capturado (folio #201): mismo trabajador, mismo tipo y misma fecha.
  Sin JavaScript · NSS con espacios de agrupación: validación en vivo rechaza, servidor acepta
  Sin JavaScript · CURP con espacios internos: validación en vivo rechaza, servidor rechaza
  Sin JavaScript · Fecha escrita con diagonales: validación en vivo rechaza, servidor acepta

  Errores inyectados: 128 · bloqueados 48 · avisados 16 · no detectados 64 · detección 50.0 %
  Datos válidos con otro formato: 24 · rechazados indebidamente 24
  Controles limpios: 60 · falsos positivos 0 

==============================================================================
BLOQUE C — CAPTURAS SIMULTÁNEAS DEL MISMO MOVIMIENTO
==============================================================================
  Trabajador nuevo: dos capturistas registran la misma alta: 25 pares · uno aceptado y otro rechazado 25 · ambos aceptados 0 · pares con error 5xx 2
  Reingreso: dos capturistas registran la misma alta de un trabajador conocido: 25 pares · uno aceptado y otro rechazado 18 · ambos aceptados 7 · pares con error 5xx 0
  Doble envío del mismo capturista (40 ms de diferencia): 10 pares · uno aceptado y otro rechazado 10 · ambos aceptados 0 · pares con error 5xx 0
  Movimientos duplicados que quedaron en la base: 7 · excepciones no controladas en el servidor: 2

==============================================================================
BLOQUE D — CARGA (1, 3, 5, 10, 20 usuarios, 15 s por nivel)
==============================================================================
   1 usuario(s):   90.5 pet/s · 1085.4 capturas/min · validar p95 10.8 ms · capturar p50/p95 14.6/19.6 ms · tablero p95 17.7 ms · errores 0 · memoria 51.5 MB
   3 usuario(s):  200.5 pet/s · 2406.5 capturas/min · validar p95 12.7 ms · capturar p50/p95 19.3/37.7 ms · tablero p95 31.6 ms · errores 0 · memoria 61.4 MB
   5 usuario(s):  261.5 pet/s · 3138.5 capturas/min · validar p95 15.0 ms · capturar p50/p95 24.5/59.7 ms · tablero p95 46.9 ms · errores 0 · memoria 62.2 MB
  10 usuario(s):  282.2 pet/s · 3385.9 capturas/min · validar p95 25.9 ms · capturar p50/p95 48.2/110.1 ms · tablero p95 92.6 ms · errores 0 · memoria 64.4 MB
  20 usuario(s):  277.9 pet/s · 3335.2 capturas/min · validar p95 58.2 ms · capturar p50/p95 77.6/696.2 ms · tablero p95 177.3 ms · errores 0 · memoria 72.5 MB
  Movimientos acumulados en la base al terminar: 3372 · excepciones: 0

==============================================================================
BLOQUE E — VOLUMEN (1,000, 5,000, 10,000 movimientos)
==============================================================================
   1,000 movimientos · base 0.29 MB · tablero p50/p95 14.1/16.4 ms · búsqueda p95 21.1 ms · detalle p95 11.1 ms · captura p95 19.4 ms · exportar 510 líneas en 21.5 ms · errores 0
   5,000 movimientos · base 1.17 MB · tablero p50/p95 15.5/32.5 ms · búsqueda p95 19.6 ms · detalle p95 9.8 ms · captura p95 17.9 ms · exportar 510 líneas en 25.0 ms · errores 0
  10,000 movimientos · base 2.27 MB · tablero p50/p95 19.6/42.2 ms · búsqueda p95 27.8 ms · detalle p95 12.0 ms · captura p95 24.8 ms · exportar 510 líneas en 32.8 ms · errores 0

==============================================================================
BLOQUE F — CAÍDA ABRUPTA DEL SERVIDOR A MEDIA CAPTURA
==============================================================================
  Capturas confirmadas antes de la caída: 666 · peticiones sin respuesta durante la caída: 10
  Tras reiniciar: integridad 'ok' · confirmadas perdidas 0 · movimientos sin asiento en bitácora 0 · servicio restablecido en 3.01 s

==============================================================================
BLOQUE G — OPERACIÓN EN RED Y SEGURIDAD
==============================================================================
  [HALLAZGO] G01 Servidor HTTP que atiende las peticiones: Werkzeug/3.1.9 Python/3.14.3
  [HALLAZGO] G02 Consola de depuración de Werkzeug (/console): HTTP 200 · consola expuesta a la red
  [HALLAZGO] G03 Folio fuera de rango en /api/movimiento: HTTP 500 · muestra el detalle técnico del error
  [HALLAZGO] G04 Captura enviada desde otro sitio (Origin ajeno, CSRF): HTTP 302 · el movimiento se guardó
  [OK] G05 Inyección SQL en el buscador: HTTP 200 · 0 resultados · tablas intactas: sí
  [OK] G06 Nombre con etiqueta <script>: HTTP 302 · texto escapado, no se ejecuta
  [HALLAZGO] G07 Cabeceras de seguridad HTTP: faltan: x-content-type-options, x-frame-options, content-security-policy, referrer-policy
  [OK] G08 Acceso desde la red local (192.168.0.8): HTTP 200

==============================================================================
BLOQUE H — CONTRASTE DE LA PALETA (WCAG 2.1, criterio 1.4.3, mínimo 4.5:1)
==============================================================================
  claro   Texto principal sobre tarjeta                #131e35 / #ffffff = 16.60:1 CUMPLE
  claro   Texto secundario sobre tarjeta               #566380 / #ffffff = 6.01:1 CUMPLE
  claro   Texto tenue (fechas, ayudas) sobre tarjeta   #8492a9 / #ffffff = 3.15:1 NO CUMPLE
  claro   Texto tenue sobre fondo de página            #8492a9 / #eaeef6 = 2.71:1 NO CUMPLE
  claro   Mensaje de error sobre su fondo              #b3261e / #fceceb = 5.71:1 CUMPLE
  claro   Mensaje de aviso sobre su fondo              #96610a / #fdf3e1 = 4.76:1 CUMPLE
  claro   Estado Exportado sobre su fondo              #0f766e / #e0f1ef = 4.69:1 CUMPLE
  claro   Etiqueta informativa sobre su fondo          #1d6fb8 / #e6f0fa = 4.53:1 CUMPLE
  claro   Texto de botón sobre acento                  #ffffff / #1c3f77 = 10.36:1 CUMPLE
  oscuro  Texto principal sobre tarjeta                #e6ebf4 / #131c2e = 14.23:1 CUMPLE
  oscuro  Texto secundario sobre tarjeta               #a3b0c7 / #131c2e = 7.78:1 CUMPLE
  oscuro  Texto tenue (fechas, ayudas) sobre tarjeta   #7c8aa3 / #131c2e = 4.88:1 CUMPLE
  oscuro  Texto tenue sobre fondo de página            #7c8aa3 / #0a1120 = 5.41:1 CUMPLE
  oscuro  Texto de botón sobre acento                  #07152b / #7ba6f2 = 7.45:1 CUMPLE

Duración total: 135.2 s
```
