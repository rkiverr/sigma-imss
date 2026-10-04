---
tipo: concepto
tags: [accesibilidad, wcag, daltonismo, contraste, color]
fuentes: ["static/css/estilos.css", "templates/index.html", "prueba_ambiente_relevante.py", "raw/entregables/e1-trl1-problematica.md"]
actualizado: 2026-10-04
---

# Accesibilidad: el estado no depende del color

Es el **origen del proyecto**. En el Excel de la empresa, el estado de cada trabajador se marcaba solo con el
color de la celda, y **la persona encargada era daltónica** ([[empresa-y-problematica]]).

## Reglas de WCAG 2.1 que se aplican
- **1.4.1 Uso del color:** la información no se transmite solo con color.
  - Cada estado se escribe con texto en una "pastilla" ("Válido", "Exportado").
  - Cada tipo también ("08 · Alta / Reingreso", "02 · Baja").
  - Los errores y avisos llevan mensaje escrito y el signo "!".
- **1.4.3 Contraste mínimo de 4.5:1** para el texto normal.

## Lo que se midió en el E5 (bloque H del arnés)
14 pares de color, en el tema claro y en el oscuro, tomados de `estilos.css`:
- **Antes:** el **texto tenue** (`--texto-tenue: #8492a9`), usado en fechas, ayudas y placeholders, tenía
  **3.15:1** sobre la tarjeta y **2.71:1** sobre el fondo. No cumplía.
- **Después:** `#5c6b84`, con **5.40:1** sobre la tarjeta y **4.64:1** sobre el fondo. Los 14 pares cumplen.

## Simulación de daltonismo
En el E5 se pasó una captura de la tabla de movimientos por las matrices de **Machado, Oliveira y Fernandes
(2009)**, con severidad 1.0, en RGB lineal:
- Con **deuteranopía** y **protanopía**, el verde de "Exportado" se vuelve gris y deja de distinguirse por color.
- El estado **se sigue leyendo porque está escrito**.

Es la prueba directa de que Sigma resuelve el problema del E1.

## Otros detalles de la interfaz
- El enlace "Saltar al contenido" y `aria-*` en los campos con error (`aria-invalid`).
- Notificaciones en `aria-live="polite"`.
- Filas de la tabla con `tabindex="0"`: se abren con Enter o espacio.
- Tema claro u oscuro que respeta la preferencia del sistema operativo.

Ver también: [[modulo-interfaz]] · [[entregable-5-trl5]]
