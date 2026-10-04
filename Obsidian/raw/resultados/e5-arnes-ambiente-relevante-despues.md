---
tipo: fuente-cruda
origen: "resultados_ambiente_relevante_despues.txt"
generado: 2026-10-04
nota: Salida literal del arnés prueba_ambiente_relevante.py. NO editar.
---

# Resultados del arnés de ambiente relevante — despues

> Fuente cruda e inmutable. Código ajustado de la Entrega 5 con el servidor de producción waitress.
> El .json completo con todas las métricas se generó en la misma corrida; aquí se conserva el reporte de texto.

```text
REPORTE DE RESULTADOS — VALIDACIÓN EN AMBIENTE RELEVANTE (ENTREGA 5 / TRL 5)
Sistema para la automatización de altas y bajas de seguro social
Fecha: 04/10/2026 12:28 · servidor: produccion · Python 3.14.3 · 12 núcleos lógicos

==============================================================================
BLOQUE A — MES DE OPERACIÓN SIMULADO (3 capturistas)
==============================================================================
  Arranque de obras (altas): 60 movimientos en 3.8 s; aceptados 60; lote IDSE con 60 línea(s) (HTTP 302).
  Rotación de cuadrillas (bajas y altas): 55 movimientos en 3.7 s; aceptados 55; lote IDSE con 55 línea(s) (HTTP 302).
  Cierre de obra (bajas) y reingresos: 25 movimientos en 1.6 s; aceptados 25; lote IDSE con 25 línea(s) (HTTP 302).
  Movimientos enviados: 140 · aceptados 140 · con aviso 0 · bloqueados 0 · fallas 0
  En base: 140 · exportados en lotes: 140 · sin asiento en bitácora: 0 · atribución errónea: 0
  /api/validar             n=700   p50=6.2 ms  p95=8.3 ms  máx=48.7 ms
  POST /capturar           n=140   p50=13.2 ms  p95=23.0 ms  máx=98.3 ms
  GET / (tras captura)     n=140   p50=11.7 ms  p95=18.1 ms  máx=31.2 ms
  POST /exportar           n=3     p50=12.8 ms  p95=13.9 ms  máx=13.9 ms

==============================================================================
BLOQUE B — ERRORES TÍPICOS DE CAPTURA
==============================================================================
  B01 CURP y RFC en minúsculas con espacios a los lados    bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #81 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 08/10/2026.
  B02 CURP pegada con espacios internos                    bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #89 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 08/10/2026.
  B03 NSS pegado con espacios de agrupación                bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #97 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 08/10/2026.
  B04 CURP con un carácter de menos                        bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La CURP debe tener 18 caracteres; se capturaron 17.
  B05 Letra O en lugar de cero en la CURP                  bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Formato de CURP inválido: se esperan 4 letras, 6 dígitos de fecha, sexo H o M, 5 letras, 1 alfanumérico y 1 dígito verificador.
  B06 CURP con una consonante equivocada (longitud correct bloq=0 aviso=4 acept=4 falla=0 -> REVISAR (4/8)
        ejemplo: Movimiento #105 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 08/10/2026.
  B07 NSS con dos dígitos transpuestos                     bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #113 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 7). Confírmalo contra el documento o
  B08 NSS con un dígito equivocado                         bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #121 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 8). Confírmalo contra el documento o
  B09 RFC con fecha distinta a la de la CURP               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La fecha de nacimiento del RFC no coincide con la de la CURP.
  B10 Nombre con un cero en lugar de la letra O            bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El nombre solo admite letras, espacios, punto, guion y apóstrofo: revisa si se tecleó un número o un símbolo (por ejemplo, un cero en lugar de la letr
  B11 SDI con el punto decimal corrido (45.05 en vez de 45 bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El salario diario integrado (53.48) es menor al salario mínimo general (315.04); la LSS no permite cotizar por debajo de él. Revisa si se corrió el pu
  B12 SDI mayor al tope de 25 UMA                          bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #129 validado y guardado correctamente. Avisos: El salario diario integrado rebasa el tope de 25 UMA (2,932.75); ante el IMSS se cotizará c
  B13 Alta sin condiciones de contratación                 bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.; Falta capturar el tipo de salario: es un dato obligatorio 
  B14 Baja sin causa de baja                               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Falta capturar la causa de baja: es un dato obligatorio para este tipo de movimiento.
  B15 Movimiento capturado fuera del plazo de 5 días hábil bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #145 validado y guardado correctamente. Avisos: El plazo legal de 5 días hábiles venció el 29/09/2026 (art. 15, fr. I, LSS): preséntalo en 
  B16 Alta de un trabajador que ya tiene alta vigente (cam bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El trabajador ya tiene un alta vigente desde el 29/09/2026 (folio #153). Si solo cambió de obra no necesita un alta nueva; si salió de la empresa, reg
  B17 Baja de un trabajador que ya fue dado de baja        bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El trabajador ya fue dado de baja el 30/09/2026 (folio #162); no tiene un alta vigente que cerrar.
  B18 Baja con fecha anterior a la de su alta              bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La fecha de baja (29/09/2026) es anterior a la del alta vigente (01/10/2026).
  B19 Movimiento repetido (mismo trabajador, tipo y fecha) bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Este movimiento ya fue capturado (folio #185): mismo trabajador, mismo tipo y misma fecha.
  Sin JavaScript · NSS con espacios de agrupación: validación en vivo acepta, servidor acepta
  Sin JavaScript · CURP con espacios internos: validación en vivo acepta, servidor acepta
  Sin JavaScript · Fecha escrita con diagonales: validación en vivo acepta, servidor acepta

  Errores inyectados: 128 · bloqueados 88 · avisados 36 · no detectados 4 · detección 96.9 %
  Datos válidos con otro formato: 24 · rechazados indebidamente 0
  Controles limpios: 60 · falsos positivos 0 

==============================================================================
BLOQUE C — CAPTURAS SIMULTÁNEAS DEL MISMO MOVIMIENTO
==============================================================================
  Trabajador nuevo: dos capturistas registran la misma alta: 25 pares · uno aceptado y otro rechazado 25 · ambos aceptados 0 · pares con error 5xx 0
  Reingreso: dos capturistas registran la misma alta de un trabajador conocido: 25 pares · uno aceptado y otro rechazado 25 · ambos aceptados 0 · pares con error 5xx 0
  Doble envío del mismo capturista (40 ms de diferencia): 10 pares · uno aceptado y otro rechazado 10 · ambos aceptados 0 · pares con error 5xx 0
  Movimientos duplicados que quedaron en la base: 0 · excepciones no controladas en el servidor: 0

==============================================================================
BLOQUE D — CARGA (1, 3, 5, 10, 20 usuarios, 15 s por nivel)
==============================================================================
   1 usuario(s):  113.3 pet/s · 1359.0 capturas/min · validar p95 7.0 ms · capturar p50/p95 13.0/14.4 ms · tablero p95 12.2 ms · errores 0 · memoria 51.3 MB
   3 usuario(s):  283.4 pet/s · 3400.6 capturas/min · validar p95 7.8 ms · capturar p50/p95 15.1/30.1 ms · tablero p95 24.4 ms · errores 0 · memoria 62.4 MB
   5 usuario(s):  388.2 pet/s · 4658.0 capturas/min · validar p95 9.1 ms · capturar p50/p95 16.7/44.4 ms · tablero p95 36.8 ms · errores 0 · memoria 62.7 MB
  10 usuario(s):  494.3 pet/s · 5931.2 capturas/min · validar p95 12.2 ms · capturar p50/p95 26.9/94.7 ms · tablero p95 43.5 ms · errores 0 · memoria 64.5 MB
  20 usuario(s):  490.7 pet/s · 5888.1 capturas/min · validar p95 33.8 ms · capturar p50/p95 45.5/120.0 ms · tablero p95 66.2 ms · errores 0 · memoria 67.5 MB
  Movimientos acumulados en la base al terminar: 5345 · excepciones: 0

==============================================================================
BLOQUE E — VOLUMEN (1,000, 5,000, 10,000 movimientos)
==============================================================================
   1,000 movimientos · base 0.31 MB · tablero p50/p95 11.1/12.9 ms · búsqueda p95 15.1 ms · detalle p95 7.4 ms · captura p95 15.1 ms · exportar 510 líneas en 24.7 ms · errores 0
   5,000 movimientos · base 1.3 MB · tablero p50/p95 13.2/15.6 ms · búsqueda p95 19.0 ms · detalle p95 8.8 ms · captura p95 13.6 ms · exportar 510 líneas en 23.0 ms · errores 0
  10,000 movimientos · base 2.52 MB · tablero p50/p95 16.7/17.9 ms · búsqueda p95 24.0 ms · detalle p95 8.6 ms · captura p95 13.8 ms · exportar 510 líneas en 23.5 ms · errores 0

==============================================================================
BLOQUE F — CAÍDA ABRUPTA DEL SERVIDOR A MEDIA CAPTURA
==============================================================================
  Capturas confirmadas antes de la caída: 1250 · peticiones sin respuesta durante la caída: 5
  Tras reiniciar: integridad 'ok' · confirmadas perdidas 0 · movimientos sin asiento en bitácora 0 · servicio restablecido en 2.85 s

==============================================================================
BLOQUE G — OPERACIÓN EN RED Y SEGURIDAD
==============================================================================
  [OK] G01 Servidor HTTP que atiende las peticiones: Sigma
  [OK] G02 Consola de depuración de Werkzeug (/console): HTTP 404
  [OK] G03 Folio fuera de rango en /api/movimiento: HTTP 404
  [OK] G04 Captura enviada desde otro sitio (Origin ajeno, CSRF): HTTP 403
  [OK] G05 Inyección SQL en el buscador: HTTP 200 · 0 resultados · tablas intactas: sí
  [OK] G06 Nombre con etiqueta <script>: HTTP 422 · texto escapado, no se ejecuta
  [OK] G07 Cabeceras de seguridad HTTP: presentes: x-content-type-options, x-frame-options, content-security-policy, referrer-policy
  [OK] G08 Acceso desde la red local (192.168.0.8): HTTP 200

==============================================================================
BLOQUE H — CONTRASTE DE LA PALETA (WCAG 2.1, criterio 1.4.3, mínimo 4.5:1)
==============================================================================
  claro   Texto principal sobre tarjeta                #131e35 / #ffffff = 16.60:1 CUMPLE
  claro   Texto secundario sobre tarjeta               #566380 / #ffffff = 6.01:1 CUMPLE
  claro   Texto tenue (fechas, ayudas) sobre tarjeta   #5c6b84 / #ffffff = 5.40:1 CUMPLE
  claro   Texto tenue sobre fondo de página            #5c6b84 / #eaeef6 = 4.64:1 CUMPLE
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

Duración total: 125.2 s
```
