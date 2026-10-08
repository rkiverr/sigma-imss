---
tipo: fuente-cruda
origen: "resultados_integracion.txt"
generado: 2026-10-07
nota: Salida literal del arnés prueba_integracion.py. NO editar.
---

# Resultados del arnés de integración (Entrega 6)

> Fuente cruda e inmutable. Corrida final del 2026-10-07 sobre una instalación limpia de la rama `trl6/correcciones` (`8914883`). El .json completo se generó en la misma corrida; aquí se conserva el reporte de texto.

```text
REPORTE DE RESULTADOS — INTEGRACIÓN Y DEMOSTRACIÓN DEL SISTEMA (ENTREGA 6 / TRL 6)
Sistema para la automatización de altas y bajas de seguro social
Fecha: 07/10/2026 22:25 · servidor de producción · Python 3.14.3 · IP de la red local 192.168.0.8

==============================================================================
BLOQUE F — ESCENARIO FUNCIONAL (una semana de operación por la red local)
==============================================================================
  PF-01 OK        6.2 ms  Abrir Sigma desde una PC de captura sin haber iniciado sesión -> HTTP 302 → /login
  PF-02 OK      144.4 ms  Iniciar sesión con una contraseña equivocada -> HTTP 401 · genérico
  PF-03 OK      135.6 ms  Iniciar sesión como capturista (captura.obra1) -> HTTP 302 → /
  PF-04 OK        8.0 ms  Validación en vivo de un RFC que no corresponde a la CURP -> HTTP 200 · errores=['rfc']
  PF-05 OK       15.5 ms  Alta válida con nombre separado y UMF -> HTTP 302 · success: Movimiento #1 validado y guardado correctamente. Plazo legal: presénta…
  PF-06 OK       18.4 ms  Alta con NSS incompleto y RFC incoherente -> HTTP 422 · 2 errores · conserva datos=True
  PF-07 OK       16.4 ms  El capturista corrige y reenvía el mismo movimiento -> HTTP 302
  PF-08 OK       18.5 ms  Segunda alta de un trabajador que sigue vigente -> HTTP 422
  PF-09 OK       14.4 ms  Baja por término de contrato -> HTTP 302
  PF-10 OK       16.4 ms  Baja de un trabajador ya dado de baja -> HTTP 422
  PF-11 OK       13.6 ms  Reingreso del mismo trabajador a otra obra -> HTTP 302
  PF-12 OK       13.4 ms  Alta con 9 días hábiles de retraso -> HTTP 302 · warning
  PF-13 OK       16.9 ms  Alta con salario de 31.50 (punto corrido) -> HTTP 422
  PF-14 OK       16.2 ms  Alta sin unidad de medicina familiar -> HTTP 422
  PF-15 OK        0.0 ms  Apellidos capturados al revés -> válido=True · aviso=sí
  PF-16 OK       10.1 ms  La capturista intenta generar el lote -> HTTP 403
  PF-17 OK       15.9 ms  Administración genera el lote con los pendientes -> HTTP 302 · 9 movimientos · 2 archivos
  PF-18 OK        7.7 ms  Descargar los dos archivos desde la PC de captura -> 9 registros · longitudes {'altas': [168], 'bajas': [168]}
  PF-19 OK       26.1 ms  Buscar por NSS y filtrar por estado Exportado -> encontrado=True · filas Exportado=9
  PF-20 OK        9.7 ms  Detalle de un movimiento exportado con su historial -> ['Movimiento capturado', 'Incluido en lote IDSE']
  PF-21 OK        9.0 ms  Generar un lote cuando no hay pendientes -> error: No hay movimientos válidos pendientes de exportar.
  PF-22 OK        0.0 ms  Bitácora en la base: autoría comprobada por la sesión -> capturó: ['captura.obra1'] · sin usuario=0
  PF-23 OK       12.5 ms  Cerrar sesión y volver con la cookie anterior -> HTTP 302 → /login · con la cookie anterior: HTTP 302 → /login
  23 de 23 casos correctos · excepciones en el servidor: 0

==============================================================================
BLOQUE L — CONFORMIDAD DEL LOTE CON LA ESTRUCTURA OFICIAL DEL IMSS
==============================================================================
  Archivos: [{'archivo': 'lote_idse_altas_20261007_222519.txt', 'tipo': '08', 'registros': 30}, {'archivo': 'lote_idse_bajas_20261007_222519.txt', 'tipo': '02', 'registros': 12}]
  Revisiones campo por campo: {'registros': 42, 'longitud_168': 42, 'identificador_9': 42, 'tipo_correcto': 42, 'nss': 42, 'fecha': 42, 'salario': 30, 'jornada_oficial': 30, 'umf': 30, 'curp': 30, 'causa': 12, 'crlf': 2, 'cp1252': 2, 'archivos': 2}
  Estructura oficial: CUMPLE (30 altas y 12 bajas)
  Campos por estructura: altas 21, bajas 16

==============================================================================
BLOQUE S — SEGURIDAD DE LA VERSIÓN INTEGRADA
==============================================================================
  [OK] S-01 Abrir el sistema desde la red sin credenciales: HTTP 302 → /login
  [OK] S-02 Capturar con usuario_id=1 (admin) estando en sesión como capturista: HTTP 302 · la bitácora registra a captura.obra1
  [HALLAZGO] S-03 Leer una captura en tránsito por la red: visibles en texto plano: curp, nss, rfc, sdi
  [OK] S-04 Banderas de la cookie de sesión: HttpOnly=sí, SameSite=Lax=sí, Secure=no
  [OK] S-05 Métodos no permitidos (TRACE, PUT, DELETE y GET /capturar): {'TRACE': 405, 'PUT': 405, 'DELETE': 405, 'GET /capturar': 405}
  [OK] S-06 Rutas con ../ hacia la base y el código: {'/static/../../sigma_imss.db': 404, '/static/..%2f..%2fsigma_imss.db': 404, '/sigma_imss.db': 404, '/static/%2e%2e/app.py': 404}
  [OK] S-07 Página de error sin detalle técnico: HTTP 404 · server=Sigma · CSP=True
  [OK] S-08 Captura de un programa sin sesión ni cabeceras Origin/Referer: HTTP 302 → /login · guardado=False
  [OK] S-09 Formulario de 8 MB: HTTP 413 en 56 ms
  [OK] S-10 Puerto de PostgreSQL (5432) y archivo de la base desde la red: 5432 abierto=False · /sigma_imss.db HTTP 404
  [OK] S-11 Cinco contraseñas equivocadas y luego la correcta: [401, 401, 401, 401, 401] → con la correcta: HTTP 401 (bloqueada)
  [OK] S-13 Reutilizar una cookie copiada después de cerrar sesión: HTTP 302 → /login
  [OK] S-14 Diez equipos inician sesión a la vez con la misma cuenta: 10 de 10 siguen dentro
  [OK] S-12 La capturista intenta generar y descargar lotes: exportar HTTP 403 · descargar HTTP 403
  Hallazgos: 1 de 14 ['S-03'] · excepciones en el servidor: 0

==============================================================================
BLOQUE R — RESPALDO Y RESTAURACIÓN ANTE LA PÉRDIDA DE LA BASE
==============================================================================
  Respaldo al arrancar el servidor: 1 archivo(s) · respaldo manual íntegro: True (0.16 s)
  Antes: {'trabajador': 40, 'movimiento': 40, 'bitacora': 42} · después de perder y restaurar: {'trabajador': 40, 'movimiento': 40, 'bitacora': 43} · recuperado: True
  Restauración y arranque: 0.85 s · acceso posterior: HTTP 200

==============================================================================
BLOQUE C — COMUNICACIÓN ENTRE EQUIPOS (tamaños y tiempos)
==============================================================================
  localhost  pantalla p95 13.1 ms · validación p95 10.1 ms
  red_local  pantalla p95 13.6 ms · validación p95 8.5 ms
  Inicio de sesión             /login                     50 B →     189 B · HTTP 302 · 6.8 ms
  Pantalla principal           /                           0 B →   19338 B · HTTP 200 · 11.1 ms
  Hoja de estilos              /static/css/estilos.css      0 B →   27319 B · HTTP 200 · 54.2 ms
  Script de la interfaz        /static/js/app.js           0 B →   17728 B · HTTP 200 · 6.4 ms
  Validación en vivo           /api/validar              391 B →      41 B · HTTP 200 · 7.5 ms
  Captura                      /capturar                 300 B →     189 B · HTTP 302 · 14.0 ms
  Detalle del movimiento       /api/movimiento/1           0 B →     986 B · HTTP 200 · 9.2 ms
  Descarga del lote de altas   /descargar-lote             0 B →     170 B · HTTP 200 · 7.8 ms

Duración total: 36.2 s
```
