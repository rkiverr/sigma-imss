---
tipo: hub
tags: [entregables, formato, informe-tecnico, trl]
fuentes: ["raw/entregables/"]
actualizado: 2026-10-04
---

# Entregables TRL (hub)

El proyecto se entrega al Mtro. Agustín Cortés Coss como un **Informe Técnico** por cada nivel de madurez
([[niveles-trl]]). Los originales (Word y PDF) están en
`C:\Users\Pedro\OneDrive\Desktop\7 semestre\LAB AUTO\`. Su texto quedó copiado en `raw/entregables/`.

| Entregable | Resumen | Fuente cruda |
|---|---|---|
| [[entregable-1-trl1]] | Problemática, variables y objetivos | `raw/entregables/e1-trl1-problematica.md` |
| [[entregable-2-trl2]] | Alternativas, arquitectura, costos y riesgos | `raw/entregables/e2-trl2-alternativas-y-arquitectura.md` |
| [[entregable-3-trl3]] | Prueba de concepto | `raw/entregables/e3-trl3-prueba-de-concepto.md` |
| [[entregable-4-trl4]] | Prototipo integrado | `raw/entregables/e4-trl4-prototipo-integrado.md` |
| [[entregable-5-trl5]] | Validación en ambiente relevante | `raw/entregables/e5-trl5-ambiente-relevante.md` y `e5-rubrica-del-maestro.md` |

## Formato que pide el maestro (se repite en todos)
- **Portada "INFORME TÉCNICO"** con tres tablas:
  1. Título del proyecto ("Sistema para la automatización de altas y bajas de seguro social"), tipo de
     desarrollo (Software) y área geográfica (Nuevo León).
  2. Concepto / Nombre / Afiliación: maestro, asesor interno (vacío) y alumnos numerados.
  3. Razón social, página web ("No aplica") y dirección.
- **Página 2: índice automático** de Word. Usar el campo `TOC \o "1-3"`: con nombres de estilo en inglés, el
  Word en español no lo llena.
- **Cuerpo:** un H1 con el tema del nivel y un H2 por cada punto de la rúbrica, **en el orden de la rúbrica**.
  Al final, Referencias en formato APA.
- **Página:** carta, márgenes de 2.54 cm, 12 pt, justificado, interlineado 1.5.
- **Tipografía:** títulos en negritas de 16 pt; leyendas de 9 pt; número de página en el pie, contando desde
  la primera página del cuerpo.
- **Figuras:** leyenda abajo, "**Figura N.** …".
- **Tablas:** leyenda arriba, "**Tabla N.** …"; encabezado sombreado `D9E2F3`, texto de 9.5 pt.
- **Viñetas:** "●" seguida de una frase inicial en negritas.

## Reglas que el maestro valora
- **Ninguna sección de la rúbrica se omite.** Si no aplica a un proyecto de software (diagrama eléctrico,
  diseño mecánico), se escribe "No aplica" con un párrafo de justificación.
- Vocabulario de control aunque sea software: sensores y actuadores virtuales, controlador, comparador, lazo
  ([[sigma-como-sistema-de-control]]).
- Variables en `snake_case`, porque así lo fijaron las "normas metodológicas" del E2.
- **Trazabilidad:** cada entregable cita lo que decidió el anterior ("Alternativa 3 del Entregable 2",
  "criterios del Entregable 3").
- Coherencia numérica entre informes y documentos firmados (costos, horas).
- Separar los **ajustes correctivos** del **trabajo planeado**.

## Cómo se generan (E4 y E5)
Con python-docx sobre una copia del informe anterior, diagramas con Mermaid y Word por COM. El método completo
está en [[como-se-hizo-el-entregable-5]].

Ver también: [[trayectoria-trl]] · [[inicio]]
