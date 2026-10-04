---
tipo: prueba
tags: [pruebas, estrategia, regresion, arnes]
fuentes: ["test_prueba_concepto.py", "prueba_ambiente_relevante.py"]
actualizado: 2026-10-04
---

# Estrategia de pruebas

Sigma tiene **dos arneses**, que corresponden a dos niveles TRL. No hay pytest ni CI: las pruebas se corren a mano
y **producen reportes de texto** que alimentan los informes.

| | [[arnes-prueba-de-concepto]] | [[arnes-ambiente-relevante]] |
|---|---|---|
| Nivel | TRL 3 (laboratorio) | TRL 5 (ambiente relevante) |
| Cómo prueba | Llama a las funciones directamente | **Caja negra por HTTP**, con el servidor como proceso aparte |
| Datos | 8 casos escritos a mano | Plantilla sintética realista (cientos de trabajadores) |
| Base | `sigma_pruebas.db` (se borra al empezar) | Una copia aislada por bloque en un directorio temporal |
| Duración | Unos 2 s | Unos 3 min (todo) |
| Para qué hoy | **Regresión obligatoria**: debe dar 8/8 | Validación ante cambios grandes; comparar el antes y el después |

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
python -m py_compile *.py
python test_prueba_concepto.py                       # 8/8
python prueba_ambiente_relevante.py --bloques B,C,G  # 96.9 %, 0 duplicados, 0 hallazgos
```
Después hay que borrar las salidas (`sigma_pruebas.db`, `resultados_*`, `lote_idse_prueba.txt`); todas están en
`.gitignore`.

## Lo que no está automatizado
- Revisar la interfaz a ojo (capturas, temas, móvil).
- PostgreSQL: no hay uno instalado en el equipo de prueba.
- El envío real al IDSE: depende de la e.firma y del layout oficial ([[lote-idse]]).
- La lectura del acuse del IMSS: no existe todavía.

Ver también: [[resultados-de-pruebas]] · [[guia-para-modificar-el-codigo]]
