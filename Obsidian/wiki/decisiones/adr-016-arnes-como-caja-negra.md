---
tipo: decision
estado: vigente
fecha: 2026-10-04 (Entregable 5)
tags: [pruebas, arnes, aislamiento]
fuentes: ["prueba_ambiente_relevante.py"]
actualizado: 2026-10-04
---

# ADR-016: El arnés del E5 prueba por HTTP sobre una copia aislada

**Decisión.**
- `prueba_ambiente_relevante.py` trata a Sigma como **caja negra**: lo levanta como proceso y lo usa por HTTP,
  emulando al navegador (longitudes y máscaras).
- Cada bloque copia el código a un **directorio temporal** con su propia base y un puerto libre.

**Por qué.**
- "Ambiente relevante" significa probar el sistema **como lo usa la empresa**, no sus funciones sueltas.
- La copia aislada **nunca toca** la base de trabajo (`sigma_imss.db`) ni los lotes reales, y da resultados
  reproducibles.
- `--codigo <carpeta>` permite medir el **antes y el después** con el mismo arnés.

**Detalles que costó descubrir.**
- Una conexión nueva por petición agotaba los puertos efímeros de Windows (WinError 10048). Por eso hay
  **keep-alive** y `SO_LINGER 0`.
- El `python.exe` del entorno virtual es un **lanzador**: hay que medir la memoria del proceso hijo y matar el
  árbol de procesos.
- En las carreras, ambos clientes abren la conexión **antes** de la barrera, para que los envíos salgan juntos.

Ver: [[arnes-ambiente-relevante]] · [[estrategia-de-pruebas]] · [[decisiones]]
