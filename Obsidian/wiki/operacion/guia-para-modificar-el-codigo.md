---
tipo: operacion
tags: [desarrollo, trampas, checklist, git]
fuentes: ["CLAUDE.md", "sigma/app.py", "sigma/database.py", "sigma/validaciones.py", "pruebas/prueba_ambiente_relevante.py"]
actualizado: 2026-10-04
---

# Guía para modificar el código sin romper nada

Checklist para cualquier sesión, humana o de Claude, que vaya a cambiar Sigma.

## Antes de tocar
- [ ] Lee [[inicio]], [[decisiones]] y la página del módulo que vas a tocar.
- [ ] Revisa [[bugs-corregidos]]: **no reintroduzcas** ninguno.
- [ ] `git status` limpio y `git pull` si vas a trabajar sobre `main`. El remoto es de Gael (`rkiverr`): avisa al
      equipo si subes directo a `main`.

## Reglas que no se rompen
| Regla | Por qué | ADR |
|---|---|---|
| SQL nuevo **con `%s`**, nunca `?`, y siempre con parámetros | Doble motor; evita la inyección | [[adr-008-sql-con-marcadores-psycopg2]] |
| Escrituras dentro de `with conexion(commit=True)` | Rollback y cierre garantizados | [[modulo-database]] |
| Marcas de tiempo como texto ISO (`ahora()`) | Python 3.12+ y doble motor | [[adr-007-marcas-de-tiempo-texto-iso]] |
| Las reglas de captura viven **solo** en `validaciones.py` | Un solo validador | [[adr-003-un-solo-validador]] |
| Pregunta "¿error o aviso?" antes de agregar una regla | Hay casos legítimos raros | [[errores-vs-avisos]] |
| Un formulario rechazado responde 422 con lo capturado, sin redirect | No perder lo escrito | [[adr-005-422-conservando-lo-capturado]] |
| Un script en línea nuevo lleva `nonce="{{ csp_nonce }}"` | La CSP lo bloquea | [[adr-012-csrf-por-origin-y-csp-con-nonce]] |
| Sin CDN ni frameworks | Funciona sin internet | [[adr-006-frontend-sin-dependencias]] |
| `validar_movimiento()` conserva la firma `(bool, list[str])` | La usa el arnés del E3 | [[modulo-validaciones]] |
| Todo en **español** con acentos (nombres, mensajes, comentarios) | Proyecto académico en español | [[equipo-y-contexto-academico]] |

## Si cambias…
| Cambio | Además actualiza o corre |
|---|---|
| Reglas de validación | Arnés del E3 (8/8) y bloque B del E5; [[reglas-de-validacion]] |
| Limpieza o máscaras | `normalizar_datos()`, `app.js` y `emular_navegador()` del arnés ([[normalizacion-de-datos]]) |
| El esquema | `_DDL_POSTGRES` **y** `_DDL_SQLITE`, migración en `init_db()`, [[modelo-de-datos]] |
| El calendario de días hábiles | `plazo.py` **y** la copia `_descansos` del arnés |
| Los montos del año | [[mantenimiento-anual]] |
| La forma de arrancar | README, `instrucciones/`, `CLAUDE.md` del repo, [[como-arrancar]] |

## Después de tocar
1. `python -m compileall -q servidor.py sigma pruebas`.
2. `python pruebas/test_prueba_concepto.py`: debe dar **8/8**. Sus salidas quedan en `pruebas/resultados/`.
3. `python pruebas/prueba_ambiente_relevante.py --bloques B,C,G`: deben salir 96.9 %, 0 duplicados y 0 hallazgos.
4. Revisa la página a mano con `python servidor.py`.
5. **Actualiza la documentación**: README, `instrucciones/` (sobre todo `Instrucciones.md`), `CLAUDE.md` del repo
   y **este segundo cerebro** (mapa de impacto en `Obsidian/CLAUDE.md`).
6. Commits en español, descriptivos y con la línea `Co-Authored-By` si participó Claude. **No hagas push** sin que
   Pedro lo pida.

Ver también: [[estrategia-de-pruebas]] · [[cronologia]]
