---
tipo: prueba
tags: [pruebas, arnes, operacion, trl9, regresion]
fuentes: ["pruebas/prueba_operacion.py"]
actualizado: 2026-10-18
---

# `pruebas/prueba_operacion.py` — problemas encontrados durante la operación (TRL 9)

Cuarto arnés, del Entregable 9. Cada caso reproduce un problema que apareció al **operar** el sistema y comprueba
que ya no ocurre. Usa el `Servidor` y el `Cliente` del [[arnes-ambiente-relevante]]: servidor de producción en
una copia aislada, capturista y administración por la IP de la red local.

```bash
python pruebas/prueba_operacion.py                                   # versión actual: 4 de 4
python pruebas/prueba_operacion.py --codigo <carpeta> --etiqueta antes  # otra versión (509a64d: 0 de 4)
```

| Caso | Problema | Dónde apareció | Qué comprueba |
|---|---|---|---|
| O-01 | «Último lote» ofrecía «Bajas (02)» de una exportación anterior | Operación de un mes (TRL 8) | Tras un lote solo de altas no hay botón de bajas y la descarga de bajas no entrega archivo |
| O-02 | Alta, baja y reingreso del mismo trabajador en un solo lote | PF-06 del TRL 8 | Tres lotes seguidos (altas → bajas → altas), uno por movimiento, con aviso de espera |
| O-03 | Dos lotes en el mismo segundo: el segundo sobrescribía al primero | H-02 de la marcha blanca (TRL 7) | Tres pares de exportaciones en el mismo segundo dejan 6 archivos distintos |
| O-04 | Un segundo `servidor.py` arrancaba en el mismo puerto sin error | H-01 de la marcha blanca (TRL 7) | El segundo termina con código 1 y el mensaje «ya está en uso»; el primero sigue atendiendo |

Salidas: `pruebas/resultados/resultados_operacion[_etiqueta].txt` y `.json`.

## Trampas
- O-03 espera al inicio de un segundo antes de cada par para forzar la colisión; si la máquina estuviera muy
  cargada y no hubiera ningún par en el mismo segundo, el caso falla (no demuestra nada) en lugar de pasar.
- O-04 arranca un segundo proceso sobre la misma base de la copia aislada; con la versión anterior queda vivo y el
  arnés lo termina con `taskkill`.

Ver también: [[estrategia-de-pruebas]] · [[bugs-corregidos]] · [[sesion-2026-10-18-correcciones-trl9]]
