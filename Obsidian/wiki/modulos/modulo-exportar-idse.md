---
tipo: modulo
tags: [exportacion, idse, lote, actuador]
fuentes: ["sigma/exportar_idse.py"]
actualizado: 2026-10-04
---

# `sigma/exportar_idse.py` — lote de texto para el IDSE (el actuador)

Tiene 102 líneas. Traduce los movimientos válidos al **archivo de texto plano** que se carga en el IDSE. El
formato y su riesgo están en [[lote-idse]].

## Constantes
- `CAMPOS_EXPORTACION` tiene 11 campos, en este orden: `registro_patronal`, `tipo_movimiento`, `curp`, `nss`,
  `rfc`, `fecha_movimiento`, `tipo_trabajador`, `tipo_salario`, `tipo_jornada`, `sdi` y `causa_baja`.
- `SEPARADOR = "|"`.
- `DIRECTORIO_SALIDA = <repo>/exportaciones` (está en `.gitignore`).

## Funciones
| Función | Qué hace |
|---|---|
| `_limpiar(valor)` | Quita el separador y los saltos de línea, que romperían el archivo |
| `_sdi_para_cotizar(registro)` | **Topa el SDI** a 25 UMA según la fecha del movimiento (art. 28 LSS y art. 45 RACERF). En la base queda el real ([[salario-sdi-y-limites]]) |
| `generar_linea_idse(registro)` | Una línea por movimiento |
| `generar_lote_idse(registros)` | Une las líneas con `\n` |
| `nombre_de_lote(prefijo)` | `lote_idse_AAAAMMDD_HHMMSS.txt`, con nombre único para no sobrescribir |
| `exportar_a_archivo(registros, ruta)` | Escribe en UTF-8 con `\n` final y crea la carpeta si falta |
| `exportar_lote(registros)` | Llama a `exportar_a_archivo` dentro de `DIRECTORIO_SALIDA`; devuelve la ruta |
| `ultimo_lote()` | El `.txt` más reciente por fecha de modificación, o `None` |

Importa `limites_sbc` de `validaciones.py`.

## Ejemplo de línea
```text
A1234567890|08|GOMF880323HDGNRR00|19108815572|GOMF880323686|01102026|3|0|1|706.53|
A1234567890|02|LEGF880617HNLLMR08|39118821246|LEGF880617PT5|01102026|||||1
```

## Trampas
- **El layout no es el oficial**: es una representación con campos delimitados, en UTF-8 y sin nombre del
  trabajador. Antes de usarlo de verdad hay que confirmarlo contra el instructivo del IMSS. Está advertido en
  el docstring, el README y el pie de la página. Es el **riesgo #1**.
- Si se pasa a ancho fijo, la **ñ** y los acentos en UTF-8 ocupan 2 bytes y desfasan las columnas.

Ver también: [[lote-idse]] · [[flujo-de-captura]] · [[modulo-app]]
