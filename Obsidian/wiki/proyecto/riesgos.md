---
tipo: proyecto
tags: [riesgos, matriz]
fuentes: ["raw/entregables/e5-trl5-ambiente-relevante.md", "raw/entregables/e2-trl2-alternativas-y-arquitectura.md"]
actualizado: 2026-10-04
---

# Riesgos del proyecto

Es la matriz del [[entregable-5-trl5]]. Retoma los tres riesgos iniciales del [[entregable-2-trl2]] y agrega los
que surgieron en las pruebas.

- **Probabilidad (P)** e **impacto (I)** van de 1 a 3.
- **Nivel** = P × I: alto de 6 a 9, medio de 3 a 4, bajo de 1 a 2.
- El nivel indicado es el **residual**, ya con las mitigaciones implementadas.

| Clave | Riesgo | P | I | Nivel | Mitigación | Estado |
|---|---|---|---|---|---|---|
| R-01 | El layout del lote no coincide con el oficial del IDSE y el IMSS rechaza el lote completo | 3 | 3 | **Alto (9)** | Conseguir con la empresa el instructivo oficial; layout configurable; probar con un lote de 1 movimiento | Abierto, es el **riesgo #1** ([[lote-idse]]) |
| R-02 | Se pierde la base por una falla del equipo servidor | 2 | 3 | Alto (6) | Respaldo diario automático y UPS. Una caída abrupta no pierde capturas confirmadas ([[resultados-de-pruebas]]) | Planeado |
| R-03 | Suplantación: la bitácora registra quién captura, pero no lo comprueba | 2 | 3 | Alto (6) | Login con contraseña cifrada y roles | Planeado |
| R-04 | El residente avisa tarde; el movimiento queda extemporáneo y se multa (20 a 350 UMA) | 2 | 2 | Medio (4) | Aviso de plazo y fecha límite ([[plazo-legal]]); acordar que avisen el mismo día | Mitigado en parte |
| R-05 | Un error de captura pasa la validación (una letra de la CURP, un nombre) | 2 | 2 | Medio (4) | Avisos por dígito verificador ([[curp]], [[nss]]); el acuse del IMSS como medición final | Mitigado en parte |
| R-06 | Exposición de datos personales en la red local | 1 | 3 | Medio (3) | Servidor de producción, base no expuesta, CSRF y cabeceras ([[seguridad-web]]); falta HTTPS | Mitigado en parte |
| R-07 | Cambios o caídas de la plataforma del IMSS (E2) | 2 | 2 | Medio (4) | Los lotes se conservan con marca de tiempo; el aviso de plazo muestra el margen | Mitigado en parte |
| R-08 | Montos de salario mínimo y UMA desactualizados al cambiar el año | 2 | 2 | Medio (4) | Tabla por año en el código; actualizar en enero y febrero ([[mantenimiento-anual]]) | Procedimiento |
| R-09 | Migración de los datos históricos del Excel (E2) | 2 | 2 | Medio (4) | La baja de alguien sin historial solo avisa; cargar la plantilla vigente como altas iniciales | Mitigado en parte |
| R-10 | Resistencia al cambio del personal (E2) | 2 | 1 | Bajo (2) | Mensajes en lenguaje llano por campo, validación en vivo y capacitación breve | Mitigado |
| R-11 | Saturación por usuarios o volumen | 1 | 2 | Bajo (2) | Margen medido muy superior al supuesto; PostgreSQL en TRL 6 | Mitigado |
| R-12 | Duplicados por capturas simultáneas | 1 | 2 | Bajo (2) | Restricción de unicidad en la base ([[adr-010-unicidad-del-movimiento-en-la-base]]) | Mitigado |

## Riesgos que aparecieron después del E5
- **Calendario de días inhábiles:** la LFT cambió en 2024 la fecha del feriado de transmisión del Poder
  Ejecutivo y el código usaba la regla anterior. **Mitigado** el 2026-10-04 (BUG-01, [[bugs-corregidos]]). Sigue
  el riesgo de que cambien otros días o de olvidar los que se cargan a mano ([[mantenimiento-anual]]). Encaja
  en R-08.

Ver también: [[hoja-de-ruta-trl6]] · [[entregable-5-trl5]]
