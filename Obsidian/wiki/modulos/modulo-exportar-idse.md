---
tipo: modulo
tags: [exportacion, idse, lote, actuador, estructura-oficial]
fuentes: ["sigma/exportar_idse.py"]
actualizado: 2026-10-07
---

# `sigma/exportar_idse.py` — lote para el IDSE (el actuador)

Traduce los movimientos válidos a los archivos que se cargan en el IDSE, con la **estructura oficial del IMSS**
desde el TRL 6 ([[adr-019-lote-con-la-estructura-oficial]]). El formato campo por campo está en [[lote-idse]].

## Constantes
- `LONGITUD_REGISTRO = 168`, `CODIFICACION = "cp1252"`, `FIN_DE_LINEA = "\r\n"`.
- `NOMBRES_TIPO = {"08": "altas", "02": "bajas"}`.
- `ESTRUCTURA = {"08": [...], "02": [...]}`: lista de `(nombre, inicio, longitud, formato, fuente)`; `formato`
  es `"N"` (numérico, ceros a la izquierda), `"A"` (alfabético: mayúsculas sin acentos, la Ñ se conserva),
  `"AN"` (alfanumérico) o un relleno fijo (`" "` o `"0"`). 21 campos en el alta y 16 en la baja.
- `OBLIGATORIOS`: datos sin los que un registro no se puede generar.
- `DIRECTORIO_SALIDA = <repo>/exportaciones` (está en `.gitignore`).

## Funciones
| Función | Qué hace |
|---|---|
| `_sdi_para_cotizar(registro)` | **Topa el SDI** a 25 UMA según la fecha del movimiento ([[salario-sdi-y-limites]]) |
| `_salario_en_centavos(registro)` | 687.70 → `68770` (se rellena a 6 posiciones) |
| `_formatear(valor, longitud, tipo, nombre)` | Aplica el formato; un numérico que no cabe lanza `ValueError` |
| `faltantes(registro)` | Campos obligatorios vacíos (movimientos de bases anteriores al TRL 6) |
| `generar_linea_idse(registro)` | Un registro de 168 posiciones; afirma que cada campo empieza donde dice la tabla |
| `generar_lote_idse(registros)` | Registros terminados en CRLF |
| `nombre_de_lote(tipo)` | `lote_idse_altas_AAAAMMDD_HHMMSS.txt` |
| `exportar_a_archivo(registros, ruta)` | Escribe en Windows-1252 (registros de un solo tipo) |
| `exportar_lote(registros)` | Un archivo por tipo en `DIRECTORIO_SALIDA`; devuelve `{tipo: ruta}` |
| `ultimo_lote(tipo=None)` | El más reciente, de cualquier tipo o de `"altas"`/`"bajas"` |

Los registros llegan de `app.exportar()` con `registro_patronal`, `guia`, `trabajador_id`, apellidos y nombre(s),
`umf`, catálogos, fecha, SDI y causa.

## Trampas
- La codificación, el CRLF y la Ñ no los especifica el documento del IMSS: se confirman con un lote de prueba.
- UTF-8 desfasaría el ancho fijo (la Ñ y los acentos ocupan 2 bytes); por eso es Windows-1252.
- Un cambio del instructivo se corrige en `ESTRUCTURA`, no en el código; el `assert` de posiciones avisa si la tabla
  queda con huecos o encimada.

## Pruebas
[[arnes-prueba-de-concepto]] (bloque 2: dos archivos, 168 posiciones) y [[arnes-integracion]] (bloque L: cada campo
de cada registro contra la base, 42 registros).

Ver también: [[lote-idse]] · [[flujo-de-captura]] · [[modulo-app]]
