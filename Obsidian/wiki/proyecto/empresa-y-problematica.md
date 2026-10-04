---
tipo: proyecto
tags: [empresa, problematica, imss, excel, daltonismo]
fuentes: ["raw/entregables/e1-trl1-problematica.md", "raw/entregables/e2-trl2-alternativas-y-arquitectura.md"]
actualizado: 2026-10-04
---

# La empresa y el problema que resuelve Sigma

## La empresa
**Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V.**
- **Dirección:** Av. Los Pinos 230, Nexxus Sector Dorado, Joyas de Anáhuac, 66055 Cd. Gral. Escobedo, N.L.
- **Giro:** contratista de instalaciones eléctricas para otras empresas en el área metropolitana de Monterrey.
- **Cómo trabaja:** por proyecto. Arma cuadrillas para cada obra y las disuelve o reasigna al terminar, así que
  el número de trabajadores cambia todo el año.
- **Clientes:** el principal es **Grupo Multimedios**. También ha trabajado para el Bolerama La Pastora, colonias
  del área metropolitana y el Hospital Sierra Madre, y tenía pendiente un contrato con BBVA (Entregable 1).
- **Herramientas:** ya tiene sistemas propios y confiables para calcular material y hacer planos. El área
  más débil es la del **seguro social**.

## El proceso actual (lo que Sigma sustituye)
1. El **residente de obra** avisa de manera informal (teléfono o mensaje) que alguien entra o sale.
2. El **responsable administrativo** captura los datos en un **archivo de Excel**.
3. Los vuelve a escribir en el portal **IDSE** del IMSS para enviar el movimiento.
4. Guarda el acuse por separado, sin conexión con el registro original.

## La problemática (Entregable 1)
- **El estado de cada trabajador se marca solo con el color de la celda**: rojo es incidencia y verde es
  procesado, sin ningún texto. **La persona encargada era daltónica**, así que no distinguía los estados y se
  generaban muchos errores. Ver [[accesibilidad]].
- El archivo **no valida datos**: una CURP o un NSS mal tecleado se descubre cuando el IMSS rechaza el
  movimiento.
- **No registra quién hizo cada movimiento**, así que no hay auditoría.
- **No avisa cuando un trámite está por vencer**, aunque la ley da solo 5 días hábiles ([[plazo-legal]]).
- **No distingue a quien cambió de obra de quien salió de la empresa.** Eso produce bajas indebidas y altas
  que nunca se dieron de baja ([[historial-afiliatorio]]).
- El volumen y la rotación superan la capacidad de una sola persona, así que el control es **reactivo**: los
  movimientos se atienden conforme se recuerdan o cuando el IMSS los reclama.
- **La contradicción:** la función más crítica es la más frágil. De ella depende la cobertura médica y de
  riesgos de trabajo de gente con riesgo eléctrico y trabajo en altura, y se sostiene sobre un Excel
  manual operado por una sola persona.

## Consecuencias
- Se pagan **cuotas de trabajadores que ya no trabajan** ahí.
- Hay **multas** por avisar tarde: de 20 a 350 UMA, según los arts. 304 A y 304 B de la LSS ([[plazo-legal]]).
- Si un trabajador **no dado de alta a tiempo** sufre un accidente, la empresa paga el costo total de la
  atención.

## Lo que se pidió automatizar
- Tablas con los datos listos para dar altas y bajas.
- Que **varias personas** puedan trabajar sobre la base de datos al mismo tiempo.
- Saber **quién hizo cada movimiento** para poder auditar.

## Objetivos (Entregable 1)
- **General:** un sistema centralizado para los movimientos afiliatorios, con control de acceso y bitácora de
  auditoría, que elimine los errores manuales y reduzca los costos por cuotas y multas.
- **Específicos:**
  1. Estandarizar la captura con validaciones automáticas (NSS, CURP, RFC, SDI, fechas y catálogos), sin
     depender de colores.
  2. Generar automáticamente los lotes para altas (08) y bajas (02).
  3. Control de acceso y bitácora por usuario.
  4. Cumplir el plazo legal de 5 días hábiles.

## Cómo lo resuelve Sigma hoy
| Problema | Solución | Página |
|---|---|---|
| Estado por colores | Cada estado se escribe con texto; contraste WCAG AA | [[accesibilidad]] |
| Sin validación | Validación en vivo y en el servidor; 96.9 % de detección | [[reglas-de-validacion]] |
| Sin auditoría | Bitácora con usuario y hora de cada acción | [[modelo-de-datos]] |
| Sin aviso de plazo | Aviso de plazo vencido o por vencer, y fecha límite en cada captura | [[plazo-legal]] |
| Cambio de obra contra salida | Reglas de historial afiliatorio | [[historial-afiliatorio]] |
| Una sola persona | Varios capturistas a la vez, sin duplicados | [[adr-010-unicidad-del-movimiento-en-la-base]] |
| Recaptura en el IDSE | Lote de texto generado automáticamente | [[lote-idse]] |
| Control de acceso | **Pendiente**: no hay login todavía | [[hoja-de-ruta-trl6]] |

Ver también: [[entregable-1-trl1]] · [[inicio]]
