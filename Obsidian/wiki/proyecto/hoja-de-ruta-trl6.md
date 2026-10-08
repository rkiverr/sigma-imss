---
tipo: proyecto
tags: [pendientes, trl6, trl7, roadmap]
fuentes: ["raw/entregables/e5-trl5-ambiente-relevante.md", "CLAUDE.md", "pruebas/prueba_integracion.py"]
actualizado: 2026-10-07
---

# Hoja de ruta: del TRL 6 al piloto (TRL 7)

En el E6 (2026-10-07) el sistema completo se integró y se demostró en ambiente relevante, y se corrigieron en la
rama local `trl6/correcciones` los bloqueantes que dejó el E5 ([[entregable-6-trl6]], [[bugs-corregidos]]):

| Pendiente del E5 | Estado |
|---|---|
| Layout del lote contra la estructura oficial (R-01) | **Hecho**: 168 posiciones, un archivo por tipo ([[lote-idse]]). Falta la prueba en el IDSE |
| Login con contraseña y roles (R-03, E-17) | **Hecho** ([[adr-018-inicio-de-sesion-roles-y-token]]) |
| Respaldo automático (R-02, E-19) | **Hecho** ([[adr-020-respaldo-automatico]]) |
| HTTPS en la red local (E-18) | **Pendiente** |
| Migrar a PostgreSQL (E-16) | **Pendiente**: el código lo soporta y ya instala psycopg2; falta instalar el servidor |

## Antes de la prueba piloto con datos reales (TRL 7)
1. **HTTPS en la red local.** Hoy la sesión, la contraseña y los datos viajan en claro (S-03). Opción: un proxy
   con TLS (por ejemplo Caddy) delante de waitress, con un certificado de la oficina instalado en cada PC.
2. **Lote de prueba en el IDSE** con un solo movimiento, con la e.firma de la empresa: confirma la codificación
   (Windows-1252), el CRLF, la Ñ y el salario con 2 decimales implícitos.
3. **Datos reales de la empresa:** registro patronal, guía de la subdelegación, usuarios y contraseñas.
4. **Aviso de privacidad** a los trabajadores (LFPDPPP, arts. 14–15) y medidas físicas: servidor en un área
   restringida, disco cifrado y respaldos en otro disco (art. 18).
5. ~~Publicar la rama~~ Hecho el 2026-10-08: `trl6/correcciones` está en `main` y en GitHub.

## Mejoras planeadas
6. **PostgreSQL** en la PC servidor: con 20 usuarios sin pausa, SQLite serializa las escrituras.
7. **Leer el acuse del IMSS** como sensor del **lazo externo** y marcar los movimientos como aceptados o
   rechazados ([[sigma-como-sistema-de-control]]).
8. **Notificaciones por correo** a RH (planeadas en el E4).
9. **Varios patrones** en la interfaz.
10. **Movimiento 07** (modificación de salario): la estructura oficial ya está documentada en [[lote-idse]].
11. **Proteger la bitácora** contra cambios hechos directamente en la base.

## Mantenimiento
- Montos legales de cada año (salario mínimo en enero, UMA en febrero): Sigma avisa si faltan, pero no los
  inventa ([[mantenimiento-anual]]).
- Días inhábiles que publique el IMSS en `DIAS_INHABILES_ADICIONALES`.

Ver también: [[riesgos]] · [[trayectoria-trl]] · [[entregable-6-trl6]] · [[inicio]]
