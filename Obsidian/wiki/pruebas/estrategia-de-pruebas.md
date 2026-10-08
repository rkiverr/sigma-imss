---
tipo: prueba
tags: [pruebas, estrategia, regresion, arnes]
fuentes: ["pruebas/test_prueba_concepto.py", "pruebas/prueba_ambiente_relevante.py", "pruebas/prueba_integracion.py"]
actualizado: 2026-10-07
---

# Estrategia de pruebas

Sigma tiene **tres arneses**, que corresponden a tres niveles TRL (el tercero, solo en la rama `trl6/correcciones`). No hay pytest ni CI: las pruebas se corren a mano
y **producen reportes de texto** que alimentan los informes.

| | [[arnes-prueba-de-concepto]] | [[arnes-ambiente-relevante]] | [[arnes-integracion]] |
|---|---|---|---|
| Nivel | TRL 3 (laboratorio) | TRL 5 (ambiente relevante) | TRL 6 (sistema integrado) |
| Cómo prueba | Llama a las funciones directamente | **Caja negra por HTTP**, con el servidor como proceso aparte | Igual que el del E5, por la IP de la LAN y con inicio de sesión |
| Datos | 8 casos escritos a mano | Plantilla sintética realista (cientos de trabajadores) | La misma plantilla, en un escenario de 23 casos |
| Base | `pruebas/resultados/sigma_pruebas.db` (se borra al empezar) | Una copia aislada por bloque en un directorio temporal | Igual que el del E5 |
| Duración | Unos 2 s | Unos 3 min (todo) | Unos 40 s |
| Para qué hoy | **Regresión obligatoria**: debe dar 8/8 | Validación ante cambios grandes; comparar el antes y el después | Lote campo por campo, login, roles, respaldo y seguridad |

## Qué cubre cada bloque del arnés del E5
| Dimensión de calidad (ISO/IEC 25010) | Bloque |
|---|---|
| Adecuación funcional | A (mes simulado) y B (errores de captura) |
| Eficiencia de desempeño | D (carga) y E (volumen) |
| Fiabilidad | C (carreras) y F (caída del servidor) |
| Seguridad | G (red) |
| Capacidad de interacción y accesibilidad | H (contraste) y la simulación de daltonismo, que no está en el arnés ([[accesibilidad]]) |
| Compatibilidad | G08 (acceso por la IP de la LAN) y la emulación del navegador |

## Rutina mínima después de un cambio
```bash
python -m compileall -q servidor.py sigma pruebas
python pruebas/test_prueba_concepto.py                       # 8/8
python pruebas/prueba_ambiente_relevante.py --bloques B,C,G  # 96.9 %, 0 duplicados, 0 hallazgos
python pruebas/prueba_integracion.py --bloques F,L,S         # rama del E6: 23/23, lote conforme, solo S-03
```
Todas las salidas quedan en `pruebas/resultados/`, que está en `.gitignore`; se puede borrar la carpeta entera.

Si el cambio **no debería alterar el comportamiento** (reorganizar, renombrar, limpiar), además compara contra
`main`: [[verificar-un-cambio-contra-main]].

## Lo que no está automatizado
- Revisar la interfaz a ojo (capturas, temas, móvil). Sin la extensión de Chrome se puede con Chrome headless
  ([[verificar-un-cambio-contra-main]], paso 5).
- PostgreSQL: no hay uno instalado en el equipo de prueba.
- El envío real al IDSE: depende de la e.firma. La estructura del lote ya se verifica campo por campo
  (bloque L), pero la codificación, el CRLF y la Ñ solo los confirma el IDSE ([[lote-idse]]).
- El respaldo de PostgreSQL (`pg_dump`): sin PostgreSQL no se puede probar ([[modulo-respaldo]]).
- La lectura del acuse del IMSS: no existe todavía.

Ver también: [[resultados-de-pruebas]] · [[guia-para-modificar-el-codigo]]
