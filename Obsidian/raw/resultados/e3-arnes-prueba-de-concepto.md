---
tipo: fuente-cruda
origen: "resultados_prueba_concepto.txt"
generado: 2026-10-04
nota: Salida literal de test_prueba_concepto.py con el código vigente de main. NO editar.
---

# Resultados del arnés de la Entrega 3 (prueba de concepto)

> Fuente cruda e inmutable. Corrida del 2026-10-04 sobre `main` (ya con los ajustes del E5).

```text
REPORTE DE RESULTADOS — PRUEBA DE CONCEPTO (ENTREGA 3 / TRL 3)
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
[CUMPLE] C4 - NSS con letras: esperado=rechazado, obtenido=rechazado
        -> El NSS solo admite dígitos: se capturaron letras o símbolos.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
[CUMPLE] C5 - Fecha fuera de formato (usa guiones): esperado=rechazado, obtenido=rechazado
        -> Formato de fecha inválido: debe ser DDMMAAAA (por ejemplo 05092026).
[CUMPLE] C6 - Fecha inexistente en el calendario (31 de febrero): esperado=rechazado, obtenido=rechazado
        -> La fecha de nacimiento contenida en la CURP no existe en el calendario.
        -> La combinación de día, mes y año no existe en el calendario.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.
[CUMPLE] C7 - Tipo de movimiento inválido: esperado=rechazado, obtenido=rechazado
        -> El tipo de movimiento debe ser 08 (Alta o Reingreso) o 02 (Baja).
[CUMPLE] C8 - Nombre vacío: esperado=rechazado, obtenido=rechazado
        -> El nombre completo del trabajador es obligatorio.
        -> Falta capturar el tipo de trabajador: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de salario: es un dato obligatorio para este tipo de movimiento.
        -> Falta capturar el tipo de jornada: es un dato obligatorio para este tipo de movimiento.
        -> El salario diario integrado es obligatorio en un alta.

Resultado del bloque 1: 8/8 casos cumplen el resultado esperado (100.0%).

==============================================================================
BLOQUE 2 — EXPORTACIÓN AL FORMATO IDSE
==============================================================================
Movimientos válidos exportados: 2
Archivo generado: lote_idse_prueba.txt
Contenido del lote (una línea por movimiento, campos separados por '|'):
   A1234567890|08|RIDG050515HNLVLL09|12345678901|RIDG050515AB1|05092026|1|0|1|450.50|
   A1234567890|02|BEHE900101HNLRRN05|98765432101|BEHE900101AB2|01092026|||||1

Resultado del bloque 2: CUMPLE — se esperaban 2 movimientos válidos (C1 y C2) y se exportaron 2.

==============================================================================
BLOQUE 3 — CONCURRENCIA Y AUDITORÍA
==============================================================================
Movimiento insertado por usuario A: id=4
Movimiento insertado por usuario B: id=3
Entradas de bitácora generadas:
   2026-10-04 13:32:31 | captura.obra1 | Movimiento capturado | Prueba de concurrencia - Usuario B
   2026-10-04 13:32:31 | admin.rrhh | Movimiento capturado | Prueba de concurrencia - Usuario A

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
