---
tipo: decision
estado: vigente
fecha: 2026-10-04 (después del Entregable 5)
tags: [estructura, carpetas, paquete, pruebas, organizacion]
fuentes: ["sigma/__init__.py", "sigma/__main__.py", "servidor.py", "pruebas/test_prueba_concepto.py", "pruebas/prueba_ambiente_relevante.py", ".gitignore"]
actualizado: 2026-10-04
---

# ADR-017: La aplicación es el paquete `sigma/` y los arneses viven en `pruebas/`

**Contexto.** Hasta el E5 todo estaba suelto en la raíz del repositorio: los seis módulos de la aplicación, los dos
arneses, las guías y lo que se genera al usar el sistema. El arnés del E3, además, escribía su reporte y su lote de
prueba en la carpeta desde donde se corriera. Pedro pidió ordenar los archivos y las carpetas (2026-10-04).

**Decisión.**
- `sigma/` es un paquete de Python con `app.py`, `validaciones.py`, `plazo.py`, `database.py`,
  `exportar_idse.py`, `templates/` y `static/`. Dentro del paquete los imports son **relativos**
  (`from .database import …`, `from . import plazo`).
- `sigma/__main__.py` es el servidor de desarrollo: `python -m sigma` sustituye a `python app.py`.
- `servidor.py` se queda en la raíz e importa `from sigma.app import app`. **El arranque de la oficina no
  cambia:** `python servidor.py`.
- `pruebas/` guarda los dos arneses. Todo lo que generan (bases, lote de prueba y reportes) va a
  `pruebas/resultados/`, que está en `.gitignore`.
- `sigma_imss.db` y `exportaciones/` **se quedan en la raíz**, fuera del paquete: `database.RAIZ` y
  `exportar_idse.DIRECTORIO_SALIDA` apuntan a la carpeta de arriba de `sigma/`.

**Por qué.**
- Es la estructura estándar de una aplicación Flask (un paquete con sus plantillas y estáticos). Al abrir el repo
  se distingue de un vistazo qué es el sistema, qué son las pruebas y qué es documentación.
- Los arneses ya no dejan archivos sueltos en la raíz.
- La base y los lotes son **datos de trabajo**, no código. Si la base se hubiera movido, una copia ya instalada
  arrancaría con la base vacía al actualizar.

**Consecuencias.**
- `python sigma/app.py` ya no funciona (imports relativos); el arranque de desarrollo es `python -m sigma`.
- Los arneses se corren desde la raíz: `python pruebas/test_prueba_concepto.py` y
  `python pruebas/prueba_ambiente_relevante.py`.
- El arnés del E3 agrega la raíz a `sys.path`, porque al correrlo directo Python solo ve `pruebas/`.
- El arnés del E5 acepta con `--codigo` versiones con **cualquiera de las dos estructuras**:
  `codigo_en_paquete()` decide cómo importar la app en modo desarrollo y dónde leer `estilos.css`. Así se sigue
  pudiendo medir el código del E4 (commit `4c79ce4`) contra el actual. Además ya no copia `pruebas/` ni
  `Obsidian/` al directorio temporal.
- El informe del E5 cita el arnés solo por nombre y cita la rama `trl5/ambiente-relevante`, que conserva la
  estructura anterior: no queda ninguna referencia rota.

**Verificación (2026-10-04).** Arnés del E3: 8/8, los tres bloques CUMPLE. Arnés del E5 completo sobre la nueva
estructura: 96.9 % de detección, 0 rechazos indebidos, 0 falsos positivos, 0 duplicados y 0 errores 500 en las
carreras, 0 capturas perdidas tras la caída, 8/8 en seguridad y contraste AA en todos los pares. `--codigo` contra
la estructura anterior funciona con los dos servidores ([[sesion-2026-10-04-estructura-de-carpetas]]). Se integró a
`main` con el merge `fb3a4a8`. El método de verificación quedó en [[verificar-un-cambio-contra-main]].

**Alternativas descartadas.**
- **Reorganización ligera** (dejar los módulos en la raíz y mover solo los arneses): no cambiaba ningún comando,
  pero la raíz seguía mezclando la aplicación con todo lo demás.
- **Estructura `src/`:** obliga a instalar el paquete (`pip install -e .`) para correrlo. Es más ceremonia sin
  beneficio para un proyecto que no se distribuye.
- **Carpeta `datos/` para la base:** descartada por el problema de la base vacía al actualizar.

Ver: [[arquitectura-general]] · [[como-arrancar]] · [[adr-009-servidor-de-produccion-waitress]] ·
[[adr-016-arnes-como-caja-negra]] · [[decisiones]]
