---
tipo: entregable
tags: [trl6, integracion, demostracion, instalacion, lote, login, respaldo, seguridad]
fuentes: ["raw/entregables/e6-trl6-integracion-y-demostracion.md", "raw/entregables/e6-rubrica-del-maestro.md", "raw/resultados/e6-arnes-integracion.md", "raw/resultados/e5-arnes-ambiente-relevante-trl6-version-corregida.md", "raw/resultados/e5-arnes-ambiente-relevante-trl6-codigo-e4.md"]
actualizado: 2026-10-07
---

# Entregable 6 — TRL 6: integración y demostración del sistema

**Fuentes crudas:**
- `raw/entregables/e6-trl6-integracion-y-demostracion.md`: el informe en su **versión 2**, de 33 páginas, con
  13 figuras y 21 tablas.
- `raw/entregables/e6-rubrica-del-maestro.md`: la rúbrica.

**Estado:** redactado el 2026-10-07; falta subirlo a la plataforma (fecha por confirmar).

**Código:** rama `trl6/correcciones`, con 6 commits de código sobre `main`. El 2026-10-08 se integró a
`main` con avance rápido y se publicó en GitHub (`7fffd1c`) para que el equipo la descargue.

## Lo que pedía el maestro
"Demostrar la tecnología en un **ambiente relevante**, con **integración de sus principales componentes**". Son 12
puntos, todos cubiertos como H2 y en ese orden:
1. Integración completa.
2. Instalación o montaje.
3. Configuración del sistema.
4. Programación definitiva preliminar.
5. Comunicación entre dispositivos.
6. Pruebas funcionales.
7. Pruebas de seguridad.
8. Pruebas de desempeño.
9. Resultados cuantitativos.
10. Comparación antes/después.
11. Problemas encontrados.
12. Correcciones implementadas.

## Cómo se planteó
- **Dos tiempos el mismo día:**
  1. Primera demostración con `main` (`7f43596`), sin tocar el código. Cumplió **7 de 9** criterios y reveló
     18 problemas (P-01…P-18).
  2. Pedro pidió corregirlos en el repo. Se corrigieron en la rama `trl6/correcciones`, se reinstaló desde cero y
     se repitieron todas las pruebas.

  La v2 del informe describe la versión corregida y usa la primera como "antes" ([[sesion-2026-10-07-correcciones-trl6]]).
- **Hospedaje local en la oficina**, no en la nube: datos personales, la Alternativa 3
  ([[adr-001-cliente-servidor-con-sgbd-relacional]]), captura sin internet y sin renta. La nube queda para
  cuando haya HTTPS.
- **"Instalación o montaje"** es la instalación del software: clon limpio, venv, `pip`, contraseñas y
  `servidor.py`, cronometrados. La versión corregida respondió por la IP de la LAN en **16.9 s**.
- **Segundo equipo emulado** por la IP de la LAN (192.168.0.8), como en el E5. Las PC físicas van en el piloto.
- **Arnés nuevo** [[arnes-integracion]] (bloques F, L, S, R y C), más los arneses del E3 y del E5 sobre la versión
  instalada.

## Criterios de aceptación del TRL 6
| Criterio | Meta | Resultado (versión corregida) |
|---|---|---|
| CA6-1 Instalación | En servicio por la LAN en ≤ 10 min | 16.9 s · cumple |
| CA6-2 Integración funcional | Todos los casos del escenario, 0 excepciones | 23/23 · cumple |
| CA6-3 Regresión | E3 8/8 y lote conforme; E5 10/10 | Cumple |
| CA6-4 Comunicación | Enlaces por la LAN; p95 validación ≤ 200 ms, pantalla ≤ 500 ms | 8.5 / 13.6 ms · cumple |
| CA6-5 Seguridad de configuración | 0 hallazgos en G y en S-05, S-06, S-07, S-09, S-10 | Cumple |
| CA6-6 Desempeño | 10 usuarios sin errores, p95 ≤ 500 ms; tablero con 10,000 ≤ 500 ms | 85.4 / 21.5 ms · cumple |
| CA6-7 Recuperación | 0 perdidas tras la caída; restauración íntegra del respaldo | 0 de 940; 0.85 s · cumple |
| CA6-8 Compatibilidad con el IDSE | Cada registro conforme a la estructura oficial | 42/42 · cumple |
| CA6-9 Autenticación y control de acceso | Sin sesión no se entra; bitácora por sesión; roles; bloqueo | Cumple |
| CA6-10 Cifrado en la red | Datos y sesión no legibles en la red | **No cumple** (S-03, falta HTTPS) |

**9 de 10.** En la v1, el CA6-9 era "autenticación y cifrado" y no se cumplía. Se dividió en dos para separar lo
corregido de lo pendiente.

## Resultados clave
| Medida | 1.ª demostración (`7f43596`) | Versión corregida (`8914883`) |
|---|---|---|
| Criterios del TRL 6 | 7 de 9 | 9 de 10 |
| Escenario de demostración | 17/17 | 23/23 |
| Comprobaciones de seguridad con hallazgo | 6 de 10 | 1 de 14 |
| Aspectos del lote conformes (de 18) | 7 | 18 (42 registros revisados) |
| Capturas por minuto con 10 usuarios | 5,609 | 3,935 |
| p95 / máx. de la captura con 20 usuarios | 164.6 ms / 3.1 s | 127.8 ms / 0.58 s |
| p95 de la validación en vivo por la LAN | 5.5 ms | 8.5 ms |

El rendimiento bajó porque cada petición lee en la base el usuario y su token, y la captura valida más campos.
Sigue muy por debajo de la meta de 500 ms. Frente al código del E4, el arnés del E5 da 6/10 → 10/10, 50.0 % →
96.9 % de detección y 7/2 → 0/0 duplicados y pares con error 500 ([[resultados-de-pruebas]]).

## Problemas y correcciones
- **P-01…P-04**: integración (ya en `main`).
- **P-05…P-18**: primera demostración; corregidos en `02aaad0`, salvo P-11 (HTTPS) y P-14 (servidor
  PostgreSQL), que siguen planeados, y P-17 (montos anuales), mitigado con un aviso.
- **P-19…P-22**: aparecieron al verificar las correcciones; todos corregidos.

El detalle con commits está en [[bugs-corregidos]]. Las decisiones nuevas son
[[adr-018-inicio-de-sesion-roles-y-token]], [[adr-019-lote-con-la-estructura-oficial]],
[[adr-020-respaldo-automatico]] y [[adr-021-migraciones-de-datos-unicas]].

## Cómo se hizo (diferencias con el E5)
El método base es [[como-se-hizo-el-entregable-5]]. Lo nuevo:
- **Instalación limpia cronometrada:** un script de PowerShell clona la rama local en una carpeta vacía, crea el
  venv, instala, fija contraseñas con `--contrasena`, arranca `servidor.py` y espera a que responda por la IP de
  la LAN.
- **Pantallas:**
  - Salen del HTML que guarda `prueba_integracion.py --capturas`.
  - Se cambia `<base href>` a un servidor vivo y se renderizan con Chrome headless (`data-tema="claro"`).
  - El rechazo se recortó a la zona del formulario y la bitácora.
- **Figuras de texto (terminal, HTTP, tráfico, lote):**
  - Se renderizan en HTML.
  - Las líneas largas se parten en espacios.
  - El lote va en dos tramos de 84 posiciones con regla.
  - Mermaid: un `;` dentro de un mensaje del diagrama de secuencia rompe el parser.
- **Comprobaciones del documento:**
  - `assert` contra los JSON finales.
  - Los H2 iguales a la rúbrica.
  - Cada referencia citada en el cuerpo.
  - Huecos ≤ 18 %, ajustando anchos y el orden de las figuras.
  - La última fila de una tabla nunca queda sola.
  - Metadatos "Equipo 4", después de Word.

## Pendientes antes de entregarlo
- Que Pedro revise el documento y lo suba.
- Nada del repo: el maestro **solo recibe el documento**; el repo es del equipo. Publicar la rama o
  integrarla a `main` es para coordinarse con el equipo, y solo si Pedro lo pide.
- Pedro da Sigma por **terminado para la materia** (2026-10-07). Lo de [[hoja-de-ruta-trl6]] queda como
  trabajo planeado, sin fecha.

Anterior: [[entregable-5-trl5]] · Hub: [[entregables-trl]] · Siguiente: [[hoja-de-ruta-trl6]]
