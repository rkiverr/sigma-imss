---
tipo: historial
tags: [sesion, entregable-6, trl6, login, respaldo, lote, rama-local]
fuentes: ["raw/historial/git-log.md", "raw/entregables/e6-trl6-integracion-y-demostracion.md", "raw/resultados/e6-arnes-integracion.md"]
actualizado: 2026-10-07
---

# Sesión del 7 de oct de 2026: Entregable 6 y correcciones del TRL 6

Trabajo de Pedro con Claude Code.

## 1. Lo que pidió Pedro
1. **El Entregable 6** ("TRL 6: Integración y demostración del sistema"), con la rúbrica de 12 puntos
   (`raw/entregables/e6-rubrica-del-maestro.md`), en el formato de siempre y con capturas.
   - Primero pidió **no tocar el código**: "trabaja con lo que tenemos del proyecto".
   - Aceptó dos recomendaciones: el hospedaje **local** en la oficina, no en la nube, y tratar "Instalación o
     montaje" como la instalación del software.
2. Con la v1 del documento terminada, pidió **corregir en `sigma-imss` los problemas encontrados**. Sus
   respuestas:
   - **Alcance:** "la mejor opción", es decir, todas las correcciones de código, sin instalar programas en su
     PC. HTTPS y el servidor PostgreSQL quedan planeados.
   - **Documento:** actualizar el E6.
   - **Git:** solo local. Rama `trl6/correcciones` desde `main`, sin merge ni push.

## 2. Primera demostración (`main`, `7f43596`)
- Instalación limpia desde GitHub en 14.2 s. Escenario de 17 casos por la IP de la LAN: 17/17.
- Arneses: E3 8/8 y E5 10/10. Cumplió **7 de 9** criterios del TRL 6.
- Al comparar con el PDF oficial del IMSS (`EstructuraMovimientosAfiliatorios.pdf`), el lote cumplía **7 de 18**
  aspectos. El catálogo de jornada no era el oficial (P-06 y P-07).
- Seguridad: 6 de 10 comprobaciones con hallazgo. No había inicio de sesión; el tráfico iba en claro; un 405 se
  volvía 500; no había límite de tamaño.
- Otros: el selector de usuario volvía a `admin.rrhh` y `requirements.txt` no instalaba psycopg2 en Python 3.14.

## 3. Correcciones (rama `trl6/correcciones`)
| Commit | Qué |
|---|---|
| `02aaad0` | Lote de 168 posiciones por tipo ([[adr-019-lote-con-la-estructura-oficial]]); nombre separado y UMF; jornada oficial con migración ([[adr-021-migraciones-de-datos-unicas]]); login, roles y token ([[adr-018-inicio-de-sesion-roles-y-token]]); respaldo ([[adr-020-respaldo-automatico]]); 405/413; `.clave_sesion`; aviso de montos; asiento "Incluido en lote IDSE"; pie TRL 6 |
| `540a313` | [[arnes-integracion]] nuevo; arneses E3 y E5 al día (detectan la versión, así que `--codigo` sigue sirviendo con el E4) |
| `882d60f` | P-19: `127.0.0.1` y `connect_timeout=1` en el `DATABASE_URL` por omisión |
| `86038c2` | P-20: token de sesión atómico; el arnés del E5 cuenta la redirección al login como falla |
| `aee7bc0` | S-14: diez inicios de sesión simultáneos con la misma cuenta |
| `8914883` | P-22: el aviso de exportación decía "1 bajas" |

## 4. Hallazgos al verificar
- **P-20, el más serio.** La prueba de caída mostró 640 capturas "confirmadas" que no estaban en la base.
  - No se habían perdido: el arnés recibía una redirección a `/login` y la contaba como éxito.
  - La causa real: cuando dos clientes iniciaban sesión a la vez con la misma cuenta, cada uno escribía su propio
    token y el primero quedaba fuera.
  - Se corrigieron el sistema y el arnés.
- **P-19:** con psycopg2 ya instalado y sin servidor, cada arranque esperaba 4 s, porque `localhost` probaba
  IPv6 y luego IPv4.
- **P-21:** verificar el respaldo dejaba `-wal` y `-shm`; se resolvió con `journal_mode = DELETE` en la copia.
- **Costo del login:** con 10 usuarios bajó el rendimiento, de 5,609 a 3,935 capturas por minuto. Sigue muy
  dentro de la meta.

## 5. Resultado final (instalación limpia de la rama)
- Instalación en 16.9 s. Arneses: E3 8/8 con el lote de 168 posiciones, y E5 10/10.
- [[arnes-integracion]]: F 23/23, L conforme (42 registros) y S con 1 hallazgo de 14 (S-03, sin HTTPS).
- **9 de 10** criterios del TRL 6 ([[entregable-6-trl6]], [[resultados-de-pruebas]]).
- El informe v2 (33 páginas) sobrescribió la v1 en `LAB AUTO/`.

## 6. Documentación
- `README.md`, `CLAUDE.md` e `instrucciones/` del repo: usuarios, respaldos, variables nuevas y el arnés del E6.
- Este wiki:
  - ADR-018 a ADR-021, [[modulo-usuarios]] y [[modulo-respaldo]].
  - [[lote-idse]], [[catalogos-idse]] y [[bugs-corregidos]].
  - [[hoja-de-ruta-trl6]] y las páginas de módulos, rutas y configuración.
  - `raw/` con el informe, la rúbrica y las salidas de los arneses.

## 7. Pendientes
- **La copia del escritorio quedó en la rama `trl6/correcciones`.** Antes de usarla hay que correr
  `python -m sigma.usuarios contrasena admin.rrhh` (y `captura.obra1`). La base existente se migra sola al
  arrancar, con un respaldo previo.
- El maestro solo recibe el documento, así que la rama no tiene que publicarse para él. Publicarla e
  integrarla a `main` es cosa del equipo, si Pedro lo pide.
- Pedro da Sigma por terminado para la materia: HTTPS, el lote de prueba en el IDSE y PostgreSQL no se harán.
- Planeado para el piloto: HTTPS (P-11), servidor PostgreSQL (P-14), lote de prueba en el IDSE y guía real de la
  subdelegación ([[hoja-de-ruta-trl6]]).

Ver también: [[cronologia]] · [[entregable-6-trl6]]
