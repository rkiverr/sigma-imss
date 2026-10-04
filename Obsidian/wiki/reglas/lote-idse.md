---
tipo: regla
tags: [idse, lote, layout, riesgo-1, exportacion]
fuentes: ["exportar_idse.py", "raw/entregables/e3-trl3-prueba-de-concepto.md", "raw/normativa/racerf-reglamento-afiliacion.md"]
actualizado: 2026-10-04
---

# El lote IDSE (y el riesgo #1)

El **IDSE** ("IMSS desde su empresa", `idse.imss.gob.mx`) es la plataforma donde el patrón presenta los
movimientos afiliatorios. Se autentica con la **firma electrónica del patrón**.
- **RACERF, art. 46:** cinco o más movimientos en una sola exhibición se presentan por **medios no impresos**,
  es decir, un archivo.
- **RACERF, art. 47:** el aviso de inscripción debe contener la **CURP** del trabajador.

## Cómo lo genera Sigma hoy ([[modulo-exportar-idse]])
- Un archivo de texto `exportaciones/lote_idse_AAAAMMDD_HHMMSS.txt`, en UTF-8.
- **Una línea por movimiento**, con 11 campos separados por `|`: registro patronal, tipo, CURP, NSS, RFC, fecha,
  tipo de trabajador, tipo de salario, tipo de jornada, SDI (**topado a 25 UMA**) y causa de baja.
- Toma solo los movimientos `'Válido'` no exportados; al generar el lote, pasan a `'Exportado'`, así que nunca se
  exportan dos veces.
- Desde la interfaz se descarga **el último** lote.
- **La carga al IDSE es manual:** el IDSE no ofrece una API pública, y Sigma **nunca** guarda la e.firma.

## ⚠ Riesgo #1: el layout no está confirmado
El formato actual es una **representación del principio de exportación**, no el formato oficial:
1. El IDSE probablemente usa **ancho fijo** (posiciones exactas), no campos delimitados. Un carácter de desfase
   puede hacer que se rechace **el lote completo**.
2. **Faltan campos:** el nombre separado en apellido paterno, materno y nombre(s), la UMF, el crédito INFONAVIT,
   etc.
3. **La codificación:** en UTF-8, la ñ y los acentos ocupan 2 bytes y desfasarían un layout de ancho fijo.
4. Los **catálogos** también deben confirmarse ([[catalogos-idse]]).

**Mitigación planeada:**
- Que la empresa consiga el **instructivo oficial vigente**.
- Definir el layout como una **tabla de datos configurable** (como en la versión alterna del E3), no como código.
- Probar primero con un lote de un solo movimiento.

Está advertido en el docstring de `exportar_idse.py`, en el README, en el pie de la página y en todos los
informes desde el E3. Ver [[riesgos]] (R-01) y [[hoja-de-ruta-trl6]].

## El lazo externo
El IMSS responde con un **acuse** (aceptado o rechazado, con su código de error). Ese acuse es el **sensor del
lazo externo** ([[sigma-como-sistema-de-control]]). Sigma todavía no lo lee; el estado `'Rechazado'` del modelo
está reservado para eso ([[modelo-de-datos]]).

Ver también: [[flujo-de-captura]] · [[salario-sdi-y-limites]]
