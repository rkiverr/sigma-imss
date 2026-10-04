---
tipo: entregable
tags: [trl2, alternativas, arquitectura, costos, riesgos]
fuentes: ["raw/entregables/e2-trl2-alternativas-y-arquitectura.md"]
actualizado: 2026-10-04
---

# Entregable 2 — TRL 2: alternativas, arquitectura y carta de inicio

**Fuente cruda:** `raw/entregables/e2-trl2-alternativas-y-arquitectura.md` (PDF de 13 páginas; la carta de
inicio firmada son 2 páginas escaneadas sin texto).

## Las tres alternativas
| # | Alternativa | Por qué sí | Por qué no |
|---|---|---|---|
| 1 | Macros VBA en Excel | Rápida y barata | No resuelve la concurrencia ni la auditoría |
| 2 | Aplicación de escritorio con base local (SQLite o Access) | Datos estructurados | Una sola persona a la vez; los residentes no tienen acceso |
| **3** | **Cliente-servidor con SGBD relacional** | Concurrencia por bloqueos, interfaz con texto en lugar de colores, trazabilidad | Más desarrollo e infraestructura |

**Se eligió la Alternativa 3** por normalización y concurrencia ([[adr-001-cliente-servidor-con-sgbd-relacional]]).
Todos los entregables posteriores la citan como "Alternativa 3 del Entregable 2".

## Diagrama de bloques (lazo cerrado)
- **Referencia:** solicitud de alta o baja que debe procesarse en 5 días hábiles.
- **Controlador lógico:** algoritmos de validación (regex).
- **Actuador lógico:** exportación al formato IDSE. Hay un actuador secundario: alertas de plazo.
- **Proceso:** el IMSS procesa el movimiento.
- **Perturbaciones:** errores de captura, avisos tardíos de los residentes, caídas del portal.
- **Sensor:** lectura del acuse del IMSS, que actualiza el estado. **Nunca se implementó**; está en
  [[hoja-de-ruta-trl6]].

Ver [[sigma-como-sistema-de-control]].

## Variables en snake_case
- **Entrada:** `nss_trabajador`, `curp_trabajador`, `rfc_trabajador`, `salario_diario_integrado`,
  `fecha_movimiento`, `tipo_movimiento`, `causa_baja`.
- **Salida:** `lote_exportacion`, `folio_envio`, `acuse_notarial`, `codigo_error`.
- **Controladas:** `estado_afiliacion`, `cumplimiento_plazo`.
- **Perturbaciones:** `errores_captura`, `retraso_informacion`.

## Requerimientos, costos y riesgos
- **Comunicación:** HTTP/HTTPS por LAN o internet; conexión segura con el IDSE.
- **Servidor:** físico en la oficina o en la nube (AWS). **Clientes:** PC estándar con navegador.
  **Autenticación patronal:** e.firma y registro patronal.
- **Costos:** de 150 a 180 horas de ingeniería = **3,000 a 4,000 MXN** en un solo pago. Infraestructura de 400 a
  1,200 MXN al mes. Licencias en 0 MXN (todo es código abierto).
- **Riesgos iniciales:** cambios o caídas del IMSS, migración de datos históricos y resistencia al cambio. Los
  tres siguen en [[riesgos]].

## ⚠ Defectos conocidos del PDF entregado
La autorrevisión del equipo detectó varios defectos:
- La sección "Controlador requerido" repite el texto de "Actuadores requeridos".
- La cifra de costos puede no coincidir con la carta firmada (por confirmar).
- Falta el riesgo del layout del IDSE.
- Dice "principios y tecnológicos".

Si el maestro pide una versión final integrada, hay que corregirlos.

Anterior: [[entregable-1-trl1]] · Siguiente: [[entregable-3-trl3]] · Hub: [[entregables-trl]]
