---
tipo: proyecto
tags: [pendientes, trl6, roadmap]
fuentes: ["raw/entregables/e5-trl5-ambiente-relevante.md", "CLAUDE.md"]
actualizado: 2026-10-04
---

# Hoja de ruta hacia TRL 6 (pendientes)

TRL 6 es la **demostración en ambiente real**: un piloto en la oficina de la empresa con datos reales. Esto es
lo que falta, en orden de importancia.

## Bloqueantes para operar de verdad
1. **Confirmar el layout del lote contra el instructivo oficial del IDSE.** Hoy el lote usa campos separados
   por `|`, en UTF-8 y sin nombre del trabajador. El IDSE probablemente pide ancho fijo. Es el **riesgo #1**
   (R-01) y depende de que la empresa consiga el instructivo. Ver [[lote-idse]].
2. **Login con contraseña cifrada y roles.** Hoy el usuario se elige de una lista, así que la bitácora documenta
   la autoría pero no la demuestra (R-03, error E-17 del E5).
3. **Respaldo automático de la base.** Hoy es un solo archivo en una PC (R-02, E-19).
4. **HTTPS en la red local.** Hoy el tráfico viaja sin cifrar (E-18).

## Mejoras planeadas
5. **Migrar a PostgreSQL** en el servidor de la oficina. Con 20 usuarios sin pausa, SQLite llegó a 6 s en una
   captura porque solo admite una escritura a la vez (E-16). El código ya lo soporta
   ([[doble-motor-de-base-de-datos]]).
6. **Leer el acuse del IMSS** como sensor del **lazo externo** y marcar los movimientos como aceptados o
   rechazados ([[sigma-como-sistema-de-control]]).
7. **Notificaciones por correo** a RH; se planearon en el E4 y no se han hecho.
8. **Varios patrones.** El modelo de datos los soporta, pero la interfaz usa solo el primero.
9. **Movimiento 07** (modificación de salario). Está en el E1, pero nunca se implementó.
10. **Proteger la bitácora** contra modificaciones hechas directamente en la base.

## Correcciones pendientes
11. ~~**Feriado de transmisión del Poder Ejecutivo** en `plazo.py` y en el arnés~~. **Hecho** el 2026-10-04
    (`3afbc9a`): ahora es el 1 de octubre de 2024, 2030… ([[bugs-corregidos]]).
12. **Días inhábiles que publica el IMSS** (jueves y viernes santos, etc.): hay que cargarlos cada año en
    `DIAS_INHABILES_ADICIONALES` ([[mantenimiento-anual]]).

## Para el piloto (TRL 6)
- Aviso de privacidad a los trabajadores (LFPDPPP, arts. 14–15) antes de capturar datos reales.
- Medidas físicas y administrativas: servidor en un área de acceso restringido, disco cifrado y acceso solo
  para RH (LFPDPPP, art. 18).
- Datos reales de la empresa (trabajadores activos, movimientos al mes, equipos) para sustituir los
  **supuestos** del E5.

Ver también: [[riesgos]] · [[trayectoria-trl]] · [[entregable-5-trl5]] · [[inicio]]
