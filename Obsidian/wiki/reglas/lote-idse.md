---
tipo: regla
tags: [idse, lote, layout, riesgo-1, exportacion, estructura-oficial]
fuentes: ["sigma/exportar_idse.py", "raw/entregables/e3-trl3-prueba-de-concepto.md", "raw/normativa/racerf-reglamento-afiliacion.md"]
actualizado: 2026-10-07
---

# El lote IDSE (y el riesgo #1)

El **IDSE** ("IMSS desde su empresa", `idse.imss.gob.mx`) es la plataforma donde el patrón presenta los
movimientos afiliatorios. Se autentica con la **firma electrónica del patrón**.
- **RACERF, art. 46:** cinco o más movimientos en una sola exhibición se presentan por **medios no impresos**,
  es decir, un archivo.
- **RACERF, art. 47:** el aviso de inscripción debe contener la **CURP** del trabajador.

## La estructura oficial
El IMSS publica "Estructura de Movimientos afiliatorios"
(`https://www.imss.gob.mx/sites/all/statics/sua/dispmag/EstructuraMovimientosAfiliatorios.pdf`, 3 páginas): un
archivo de texto **por tipo de movimiento**, con registros de **168 posiciones** de ancho fijo. Tres tablas:
alta o reingreso (08), modificación de salario (07) y baja (02).

| Posiciones | Campo | Alta (08) | Baja (02) |
|---|---|---|---|
| 1–10 + 11 | Registro patronal y dígito | AN 10 + N 1 | igual |
| 12–21 + 22 | NSS y dígito | N 10 + N 1 | igual |
| 23–49 / 50–76 / 77–103 | Apellido paterno / materno / nombre(s) | A 27 c/u | igual |
| 104–109 | Salario base de cotización | N 6 | (104–118: 15 ceros) |
| 110–115 | Relleno | 6 espacios | |
| 116 / 117 / 118 | Tipo de trabajador / de salario / semana o jornada reducida | N 1 c/u | |
| 119–126 | Fecha DDMMAAAA | N 8 | igual |
| 127–129 + 130–131 | UMF + relleno | N 3 + 2 espacios | (127–131: 5 espacios) |
| 132–133 | Tipo de movimiento | 08 | 02 |
| 134–138 | Guía (subdelegación) | N 5 | igual |
| 139–148 | Clave del trabajador (del patrón) | AN 10 | igual |
| 149 | | espacio | causa de baja |
| 150–167 | CURP | AN 18 | 18 espacios |
| 168 | Identificador del formato | 9 | 9 |

## Cómo lo genera Sigma desde el TRL 6 ([[modulo-exportar-idse]], [[adr-019-lote-con-la-estructura-oficial]])
- `exportaciones/lote_idse_altas_AAAAMMDD_HHMMSS.txt` y `…_bajas_…txt`, en Windows-1252 con CRLF.
- La tabla anterior está en `exportar_idse.ESTRUCTURA`; `generar_linea_idse()` afirma las 168 posiciones.
- Salario topado a 25 UMA en 6 dígitos con 2 decimales implícitos (687.70 → `068770`).
- Guía = `patron.guia` (semilla `00000`); clave del trabajador = su id en Sigma.
- Toma solo los movimientos `'Válido'` no exportados y completos (`faltantes()`); pasan a `'Exportado'` y cada uno
  registra en la bitácora "Incluido en lote IDSE" con el nombre del archivo.
- Solo administración genera y descarga (`/descargar-lote?tipo=altas|bajas`).
- **La carga al IDSE sigue siendo manual**, con la e.firma; Sigma nunca la guarda.

Ejemplo (alta):
```text
A123456789012345678903RIVERA                     DIEGO                      GAEL ANTONIO               045050      30006102026035  08000001          RIDG050515HNLVLL099
```

## ⚠ Riesgo #1, ahora mitigado en parte
La estructura ya es la publicada (el [[arnes-integracion]] la verifica campo por campo: bloque L). Queda por
confirmar **con un lote de prueba de un solo movimiento en el IDSE**:
1. La codificación (Windows-1252) y el fin de línea (CRLF): el documento no los especifica.
2. Cómo se representa la Ñ.
3. Que el salario lleve 2 decimales implícitos.
4. El registro patronal y la guía reales de la empresa (los de la semilla son de ejemplo).

Hasta el E5 el lote era una representación con 11 campos separados por `|`, sin nombre, en UTF-8 y con altas y
bajas juntas: 7 de 18 aspectos compatibles con la estructura oficial.

## El lazo externo
El IMSS responde con un **acuse** (aceptado o rechazado, con su código de error). Ese acuse es el **sensor del
lazo externo** ([[sigma-como-sistema-de-control]]). Sigma todavía no lo lee; el estado `'Rechazado'` del modelo
está reservado para eso ([[modelo-de-datos]]).

Ver también: [[catalogos-idse]] · [[flujo-de-captura]] · [[salario-sdi-y-limites]] · [[riesgos]]
