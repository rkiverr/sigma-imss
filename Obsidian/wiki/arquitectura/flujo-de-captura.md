---
tipo: arquitectura
tags: [flujo, captura, post-capturar]
fuentes: ["sigma/app.py", "sigma/validaciones.py", "sigma/database.py"]
actualizado: 2026-10-04
---

# Flujo de captura de un movimiento (`POST /capturar`)

Qué pasa desde que el capturista oprime **Capturar movimiento** hasta que el sistema guarda o rechaza.
Código: `app.py` → `capturar()`.

```mermaid
flowchart TD
  A(["1. El navegador envía el formulario"]) --> B["2. _leer_formulario() → normalizar_datos()<br/>mayúsculas, sin espacios ni guiones en CURP/RFC/NSS, fecha solo dígitos"]
  B --> C["3. validar_campos(): errores y avisos por campo<br/>formato, coherencia CURP↔RFC, catálogos, SDI art. 28, nombre;<br/>avisos: dígitos CURP/NSS, tope 25 UMA, plazo, fecha lejana"]
  C --> D["4. Abrir conexion(commit=True)<br/>_usuario_valido()"]
  D --> E{"¿CURP y NSS<br/>con formato válido?"}
  E -- "sí" --> F["5. conflicto_de_identidad()<br/>CURP con otro NSS / NSS de otra persona"]
  E -- "no" --> G
  F --> G{"¿Hay errores?"}
  G -- "no" --> H["6. movimiento_duplicado()<br/>mismo trabajador, tipo y fecha"]
  H --> I{"¿Hay errores?"}
  I -- "no" --> J["7. _validar_historial()<br/>alta sobre alta vigente, doble baja,<br/>baja o reingreso anterior al previo"]
  J --> K{"¿Hay errores?"}
  K -- "no" --> L["8. _guardar_movimiento()<br/>trabajador + movimiento 'Válido' + bitácora"]
  L --> M{"¿IntegrityError?<br/>(otro capturista se adelantó)"}
  M -- "no" --> N["9. Commit · flash success (con fecha límite)<br/>o warning (con avisos) · 302 a /"]
  M -- "sí" --> O["rollback · error 'Otro usuario acaba de registrar…'"]
  G -- "sí" --> P
  I -- "sí" --> P
  K -- "sí" --> P
  O --> P["10. Bitácora 'Intento de captura rechazado'<br/>422 con el formulario lleno y el error por campo"]
```

## Detalle por paso
1. **Normalización** ([[normalizacion-de-datos]]). Los datos pegados con espacios ya no fallan.
2. **Validación aislada**: `validaciones.validar_campos(datos)` devuelve dos diccionarios, `errores` y `avisos`,
   indexados por campo ([[reglas-de-validacion]]).
3. **Usuario**: `_usuario_valido()` convierte `usuario_id` en un id que exista. Si no, error en `usuario_id`;
   antes del E4 eso era un `ValueError` y un error 500.
4. **Conflicto de identidad**: solo si la CURP y el NSS pasaron el formato. Detecta una CURP ya registrada con
   otro NSS o un NSS de otra persona, **antes** del INSERT (corrección del E4).
5. **Duplicado**: `movimiento_duplicado()` busca el mismo trabajador, tipo y fecha, y responde con su folio.
6. **Historial**: `_validar_historial()` usa `estado_afiliatorio()` ([[historial-afiliatorio]]). Una baja sin
   historial **solo avisa**.
7. **Guardado**: `_guardar_movimiento()` llama a `obtener_patron_id()` y `obtener_o_crear_trabajador()` (que
   actualiza nombre y RFC si el trabajador ya existía), luego al INSERT con estado `'Válido'` y
   `creado_en = now()`, y al final registra en la bitácora "Movimiento capturado".
8. **Carrera**: si dos capturistas pasan las revisiones al mismo tiempo, el índice `UNIQUE` hace fallar al
   segundo. Se atrapa `ERRORES_DE_INTEGRIDAD`, se hace `conn.rollback()` y se devuelve un error claro
   ([[adr-010-unicidad-del-movimiento-en-la-base]]).
9. **Éxito**: un *flash* `success` con "Plazo legal: preséntalo en IDSE a más tardar el DD/MM/AAAA", o un
   *flash* `warning` con los avisos. Luego `redirect` a `/` (patrón PRG).
10. **Rechazo**: se registra en la bitácora el intento con los errores unidos por " | ", y se responde **422**
    renderizando `index.html` con `form=datos`, `errores` y `avisos`, **sin perder lo capturado**
    ([[adr-005-422-conservando-lo-capturado]]).

## Antes de llegar aquí
- El navegador ya validó en vivo con `POST /api/validar`, que usa la **misma** normalización y el **mismo**
  validador, pero **no** las reglas que consultan la base: conflicto, duplicado e historial.
- `preparar_peticion()` (before_request) rechaza con **403** cualquier POST cuyo `Origin` o `Referer` no sea
  el propio host ([[seguridad-web]]).

## Exportación (`POST /exportar`)
1. Valida el usuario.
2. Selecciona los movimientos `'Válido'` con `exportado = FALSE`.
3. `exportar_idse.exportar_lote(registros)` escribe `exportaciones/lote_idse_AAAAMMDD_HHMMSS.txt`.
4. Los marca como `'Exportado'` y registra en la bitácora "Exportación de lote IDSE".

Si no hay pendientes, avisa sin generar nada. Ver [[lote-idse]].

Ver también: [[rutas-http]] · [[modulo-app]] · [[arquitectura-general]]
