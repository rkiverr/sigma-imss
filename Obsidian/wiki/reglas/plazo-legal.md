---
tipo: regla
tags: [plazo, lss, dias-habiles, multas]
fuentes: ["plazo.py", "validaciones.py", "raw/normativa/lss-ley-del-seguro-social.md", "raw/normativa/racerf-reglamento-afiliacion.md", "raw/normativa/lft-ley-federal-del-trabajo.md", "raw/normativa/valores-oficiales-2026.md"]
actualizado: 2026-10-04
---

# Plazo legal de cinco días hábiles

**Regla:** las altas y las bajas se comunican al IMSS **dentro de plazos no mayores de cinco días hábiles**.

## Fundamento
- **LSS, art. 15, fr. I:** "Registrarse e inscribir a sus trabajadores en el Instituto, comunicar sus altas y
  bajas, las modificaciones de su salario y los demás datos, dentro de plazos no mayores de cinco días hábiles".
- **LSS, art. 304 A, fr. II:** no inscribir a los trabajadores, o hacerlo en forma extemporánea, es
  infracción.
- **LSS, art. 304 B, fr. IV:** se multa con **20 a 350 veces la UMA**, es decir, de **$2,346.20 a $41,058.50** en
  2026.
- **RACERF, art. 45:** la inscripción puede hacerse desde el **día hábil anterior** al inicio de la relación
  laboral, por eso se aceptan fechas futuras.
- **LFT, art. 74:** días de descanso obligatorio, que no cuentan como hábiles.

Textos literales en `raw/normativa/`.

## Cómo lo aplica Sigma ([[modulo-plazo]])
- El conteo empieza **el día siguiente** al movimiento.
- No cuentan sábados, domingos, los días del art. 74 de la LFT ni `DIAS_INHABILES_ADICIONALES`.
- Estado:
  - **VENCIDO:** transcurrieron más de 5 días hábiles. **Aviso:** "El plazo legal de 5 días hábiles venció el
    DD/MM/AAAA (art. 15, fr. I, LSS): preséntalo en IDSE cuanto antes; el aviso extemporáneo puede multarse."
  - **POR_VENCER:** transcurrieron 4 o 5. **Aviso:** "…vence el DD/MM/AAAA: preséntalo en IDSE hoy."
  - **EN_PLAZO:** sin aviso. El mensaje de éxito dice "Plazo legal: preséntalo en IDSE a más tardar el
    DD/MM/AAAA."

## Por qué es aviso y no error
Un movimiento extemporáneo **igual se tiene que presentar**, y cuanto antes mejor. Bloquearlo empeoraría la
multa ([[errores-vs-avisos]]).

## Ejemplo
Un alta del 21/09/2026 (lunes):
- Días hábiles: 22, 23, 24, 25 y 28 de sep, así que la fecha límite es el **28/09/2026**.
- Capturada el 02/10/2026: lleva 9 días hábiles, así que es VENCIDO y sale el aviso.

## Relación con el problema
Es uno de los objetivos del [[entregable-1-trl1]]. El Excel de la empresa no avisaba cuándo vencía un trámite
([[empresa-y-problematica]]). El E2 lo planteó como "variable controlada `cumplimiento_plazo`" y quedó sin
programar hasta el E5.

## Calendario
- **Transmisión del Poder Ejecutivo:** la LFT la cambió en 2024 al 1 de octubre de cada seis años (2024,
  2030…). El código se corrigió el 2026-10-04 (BUG-01, [[bugs-corregidos]]).
- **Lo que se carga a mano cada año:** los días inhábiles que publica el IMSS y las jornadas electorales
  ([[mantenimiento-anual]]).

Ver también: [[reglas-de-validacion]] · [[modulo-plazo]]
