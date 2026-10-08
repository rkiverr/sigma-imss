---
tipo: fuente-cruda
origen: "resultados_prueba_concepto.txt"
generado: 2026-10-07
nota: Salida literal del arnés test_prueba_concepto.py. NO editar.
---

# Resultados del arnés de la Entrega 3 con la versión del TRL 6

> Fuente cruda e inmutable. Corrida del 2026-10-07 sobre la instalación limpia de la rama `trl6/correcciones`: casos con nombre separado y UMF, y bloque 2 contra la estructura de 168 posiciones.

```text
REPORTE DE RESULTADOS — PRUEBA DE CONCEPTO (ENTREGA 3 / TRL 3; casos al día con el TRL 6)
Sistema para la automatización de altas y bajas de seguro social
Persistencia: SQLite - sigma_pruebas.db

==============================================================================
BLOQUE 1 — VALIDACIÓN DE CAPTURA
==============================================================================
[CUMPLE] C1 - Alta válida: esperado=válido, obtenido=válido
[CUMPLE] C2 - Baja válida: esperado=válido, obtenido=válido
[CUMPLE] C3 - CURP con longitud incorrecta: esperado=rechazado, obtenido=rechazado
        -> La CURP debe tener 18 caracteres; se capturaron 9.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
        -> Falta la unidad de medicina familiar (UMF): el IMSS la pide en cada alta. Está en la constancia de vigencia o en el carnet del trabajador.
[CUMPLE] C4 - NSS con letras: esperado=rechazado, obtenido=rechazado
        -> El NSS solo admite dígitos: se capturaron letras o símbolos.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
        -> Falta la unidad de medicina familiar (UMF): el IMSS la pide en cada alta. Está en la constancia de vigencia o en el carnet del trabajador.
[CUMPLE] C5 - Fecha fuera de formato (usa guiones): esperado=rechazado, obtenido=rechazado
        -> Formato de fecha inválido: debe ser DDMMAAAA (por ejemplo 05092026).
[CUMPLE] C6 - Fecha inexistente en el calendario (31 de febrero): esperado=rechazado, obtenido=rechazado
        -> La fecha de nacimiento contenida en la CURP no existe en el calendario.
        -> La combinación de día, mes y año no existe en el calendario.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
        -> Falta la unidad de medicina familiar (UMF): el IMSS la pide en cada alta. Está en la constancia de vigencia o en el carnet del trabajador.
[CUMPLE] C7 - Tipo de movimiento inválido: esperado=rechazado, obtenido=rechazado
        -> El tipo de movimiento debe ser 08 (Alta o Reingreso) o 02 (Baja).
[CUMPLE] C8 - Nombre vacío (apellido paterno y nombre obligatorios): esperado=rechazado, obtenido=rechazado
        -> El apellido paterno del trabajador es obligatorio.
        -> El nombre del trabajador es obligatorio.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
        -> Falta la unidad de medicina familiar (UMF): el IMSS la pide en cada alta. Está en la constancia de vigencia o en el carnet del trabajador.

Resultado del bloque 1: 8/8 casos cumplen el resultado esperado (100.0%).

==============================================================================
BLOQUE 2 — EXPORTACIÓN AL FORMATO IDSE
==============================================================================
Movimientos válidos exportados: 2
Archivo generado: pruebas\resultados\lote_idse_prueba_altas.txt (1 registro(s) de 168 posiciones, sin separadores)
   A123456789012345678901RIVERA                     DIEGO                      GAEL ANTONIO               045050      10005092026035  08000001          RIDG050515HNLVLL099
Archivo generado: pruebas\resultados\lote_idse_prueba_bajas.txt (1 registro(s) de 168 posiciones, sin separadores)
   A123456789098765432101BEAS                       HERNANDEZ                  ERNESTO                    00000000000000001092026     02000002         1                  9

Resultado del bloque 2: CUMPLE — se esperaban 2 movimientos válidos (C1 y C2) en dos archivos (altas y bajas) de 168 posiciones por registro; se exportaron 2 en 2 archivo(s).

==============================================================================
BLOQUE 3 — CONCURRENCIA Y AUDITORÍA
==============================================================================
Movimiento insertado por usuario A: id=3
Movimiento insertado por usuario B: id=4
Entradas de bitácora generadas:
   2026-10-07 19:08:57 | admin.rrhh | Movimiento capturado | Prueba de concurrencia - Usuario A
   2026-10-07 19:08:57 | captura.obra1 | Movimiento capturado | Prueba de concurrencia - Usuario B

Resultado del bloque 3: CUMPLE — ambos movimientos se registraron con IDs distintos y cada uno quedó atribuido a su usuario correspondiente en la bitácora, sin pérdida ni sobrescritura de datos.

==============================================================================
RESUMEN GENERAL FRENTE A LOS CRITERIOS DE ACEPTACIÓN
==============================================================================
1) Rechazo de CURP/NSS inválidos: CUMPLE (8/8 casos correctos)
2) Rechazo de fechas inválidas: incluido en el bloque 1 (casos C5 y C6)
3) Estructura del archivo de exportación IDSE: CUMPLE
4) Asociación de cada movimiento a usuario + timestamp en bitácora: CUMPLE (ver bloques 1 y 3)
5) Sin pérdida de datos en captura concurrente: CUMPLE
```
