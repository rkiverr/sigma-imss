---
tipo: fuente-cruda
origen: "resultados_ambiente_relevante_despues.txt"
generado: 2026-10-07
nota: Salida literal del arnés prueba_ambiente_relevante.py. NO editar.
---

# Resultados del arnés de ambiente relevante — versión corregida del TRL 6

> Fuente cruda e inmutable. Corrida del 2026-10-07 (servidor de producción) sobre la instalación limpia de la rama `trl6/correcciones` en `aee7bc0`, con inicio de sesión.

```text
REPORTE DE RESULTADOS — VALIDACIÓN EN AMBIENTE RELEVANTE (ENTREGA 5 / TRL 5)
Sistema para la automatización de altas y bajas de seguro social
Fecha: 07/10/2026 19:09 · servidor: produccion · Python 3.14.3 · 12 núcleos lógicos

==============================================================================
BLOQUE A — MES DE OPERACIÓN SIMULADO (3 capturistas)
==============================================================================
  Arranque de obras (altas): 60 movimientos en 4.6 s; aceptados 60; lote IDSE con 60 línea(s) (HTTP 302).
  Rotación de cuadrillas (bajas y altas): 55 movimientos en 4.3 s; aceptados 55; lote IDSE con 55 línea(s) (HTTP 302).
  Cierre de obra (bajas) y reingresos: 25 movimientos en 2.0 s; aceptados 25; lote IDSE con 25 línea(s) (HTTP 302).
  Movimientos enviados: 140 · aceptados 140 · con aviso 0 · bloqueados 0 · fallas 0
  En base: 140 · exportados en lotes: 140 · sin asiento en bitácora: 0 · atribución errónea: 0
  /api/validar             n=700   p50=9.3 ms  p95=19.6 ms  máx=56.3 ms
  POST /capturar           n=140   p50=16.2 ms  p95=41.1 ms  máx=167.1 ms
  GET / (tras captura)     n=140   p50=14.6 ms  p95=30.6 ms  máx=48.3 ms
  POST /exportar           n=3     p50=19.1 ms  p95=19.6 ms  máx=19.6 ms

==============================================================================
BLOQUE B — ERRORES TÍPICOS DE CAPTURA
==============================================================================
  B01 CURP y RFC en minúsculas con espacios a los lados    bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #81 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 13/10/2026.
  B02 CURP pegada con espacios internos                    bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #89 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 13/10/2026.
  B03 NSS pegado con espacios de agrupación                bloq=0 aviso=0 acept=8 falla=0 -> OK (8/8)
        ejemplo: Movimiento #97 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 13/10/2026.
  B04 CURP con un carácter de menos                        bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La CURP debe tener 18 caracteres; se capturaron 17.
  B05 Letra O en lugar de cero en la CURP                  bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Formato de CURP inválido: se esperan 4 letras, 6 dígitos de fecha, sexo H o M, 5 letras, 1 alfanumérico y 1 dígito verificador.
  B06 CURP con una consonante equivocada (longitud correct bloq=0 aviso=4 acept=4 falla=0 -> REVISAR (4/8)
        ejemplo: Movimiento #105 validado y guardado correctamente. Plazo legal: preséntalo en IDSE a más tardar el 13/10/2026.
  B07 NSS con dos dígitos transpuestos                     bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #113 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 7). Confírmalo contra el documento o
  B08 NSS con un dígito equivocado                         bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #121 validado y guardado correctamente. Avisos: El dígito verificador del NSS no coincide (se esperaba 8). Confírmalo contra el documento o
  B09 RFC con fecha distinta a la de la CURP               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La fecha de nacimiento del RFC no coincide con la de la CURP.
  B10 Nombre con un cero en lugar de la letra O            bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El apellido paterno solo admite letras, espacios, punto, guion y apóstrofo: revisa si se tecleó un número o un símbolo (por ejemplo, un cero en lugar 
  B11 SDI con el punto decimal corrido (45.05 en vez de 45 bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El salario diario integrado (53.48) es menor al salario mínimo general (315.04); la LSS no permite cotizar por debajo de él. Revisa si se corrió el pu
  B12 SDI mayor al tope de 25 UMA                          bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #129 validado y guardado correctamente. Avisos: El salario diario integrado rebasa el tope de 25 UMA (2,932.75); ante el IMSS se cotizará c
  B13 Alta sin condiciones de contratación                 bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.; Falta capturar el tipo de salario: es un dato obligatorio 
  B14 Baja sin causa de baja                               bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: Falta capturar la causa de baja: es un dato obligatorio para este tipo de movimiento.
  B15 Movimiento capturado fuera del plazo de 5 días hábil bloq=0 aviso=8 acept=0 falla=0 -> OK (8/8)
        ejemplo: Movimiento #145 validado y guardado correctamente. Avisos: El plazo legal de 5 días hábiles venció el 02/10/2026 (art. 15, fr. I, LSS): preséntalo en 
  B16 Alta de un trabajador que ya tiene alta vigente (cam bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El trabajador ya tiene un alta vigente desde el 02/10/2026 (folio #153). Si solo cambió de obra no necesita un alta nueva; si salió de la empresa, reg
  B17 Baja de un trabajador que ya fue dado de baja        bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: El trabajador ya fue dado de baja el 05/10/2026 (folio #162); no tiene un alta vigente que cerrar.
  B18 Baja con fecha anterior a la de su alta              bloq=8 aviso=0 acept=0 falla=0 -> OK (8/8)
        ejemplo: La fecha de baja (02/10/2026) es anterior a la del alta vigente (06/10/2026).
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
   1 usuario(s):   77.7 pet/s ·  931.3 capturas/min · validar p95 13.7 ms · capturar p50/p95 16.0/22.2 ms · tablero p95 19.9 ms · errores 0 · memoria 54.6 MB
   3 usuario(s):  168.7 pet/s · 2021.8 capturas/min · validar p95 27.3 ms · capturar p50/p95 19.6/46.6 ms · tablero p95 38.9 ms · errores 0 · memoria 58.2 MB
   5 usuario(s):  251.0 pet/s · 3008.4 capturas/min · validar p95 32.8 ms · capturar p50/p95 21.8/55.7 ms · tablero p95 44.4 ms · errores 0 · memoria 66.5 MB
  10 usuario(s):  328.6 pet/s · 3935.3 capturas/min · validar p95 27.9 ms · capturar p50/p95 37.0/85.4 ms · tablero p95 62.2 ms · errores 0 · memoria 68.4 MB
  20 usuario(s):  315.5 pet/s · 3770.7 capturas/min · validar p95 67.3 ms · capturar p50/p95 68.8/127.8 ms · tablero p95 122.0 ms · errores 0 · memoria 71.1 MB
  Movimientos acumulados en la base al terminar: 3471 · excepciones: 0

==============================================================================
BLOQUE E — VOLUMEN (1,000, 5,000, 10,000 movimientos)
==============================================================================
   1,000 movimientos · base 0.38 MB · tablero p50/p95 13.8/15.2 ms · búsqueda p95 16.7 ms · detalle p95 10.4 ms · captura p95 21.3 ms · exportar 510 líneas en 43.6 ms · errores 0
   5,000 movimientos · base 1.42 MB · tablero p50/p95 16.6/18.3 ms · búsqueda p95 23.8 ms · detalle p95 11.2 ms · captura p95 23.2 ms · exportar 510 líneas en 46.0 ms · errores 0
  10,000 movimientos · base 2.71 MB · tablero p50/p95 20.0/21.5 ms · búsqueda p95 27.4 ms · detalle p95 11.6 ms · captura p95 261.6 ms · exportar 510 líneas en 44.7 ms · errores 0

==============================================================================
BLOQUE F — CAÍDA ABRUPTA DEL SERVIDOR A MEDIA CAPTURA
==============================================================================
  Capturas confirmadas antes de la caída: 940 · peticiones sin respuesta durante la caída: 5
  Tras reiniciar: integridad 'ok' · confirmadas perdidas 0 · movimientos sin asiento en bitácora 0 · servicio restablecido en 2.94 s

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

Duración total: 161.6 s
```
