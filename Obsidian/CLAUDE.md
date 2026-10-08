# CLAUDE.md — Segundo cerebro del proyecto Sigma

Esta carpeta (`Obsidian/`) es el **segundo cerebro** del proyecto Sigma: un *LLM Wiki* que el agente
(Claude) construye y mantiene en Markdown. Sirve para no perder nunca el contexto de qué es el sistema, cómo
funciona, por qué está hecho así y qué se ha hecho en cada sesión. Pedro lo lee en Obsidian y casi nunca lo
edita; **el agente escribe y mantiene todo**.

Idioma: **español** (páginas, nombres de archivo, log y respuestas).

---

## 1. Al empezar cualquier sesión sobre Sigma

1. Lee `Obsidian/index.md`, que es el catálogo de todo el wiki.
2. Lee `wiki/inicio.md` para el panorama y el estado actual.
3. Revisa las últimas entradas del log: `grep "^## \[" Obsidian/log.md | tail -5`.
4. Abre solo las páginas que necesites, siguiendo los `[[enlaces]]`.

Con eso debes saber qué es Sigma, en qué nivel TRL va, qué decisiones no se vuelven a discutir y qué está
pendiente, **sin releer todo el código**.

---

## 2. Arquitectura (tres capas)

```
sigma-imss/                     ← repositorio (github.com/rkiverr/sigma-imss)
├── servidor.py                 ┐ CÓDIGO: fuente de verdad del comportamiento
├── sigma/                      │ la aplicación: app.py, validaciones.py…, templates/, static/
├── pruebas/                    │ los arneses de E3, E5 y E6 (salidas en pruebas/resultados/, ignorada)
│                               ┘ (el agente lo cambia solo cuando Pedro lo pide)
├── README.md, instrucciones/   ← documentación para personas
├── CLAUDE.md                   ← memoria corta del repo (la carga Claude Code); apunta aquí
└── Obsidian/                   ← ESTE segundo cerebro
    ├── CLAUDE.md               ← este archivo: esquema y reglas
    ├── index.md                ← catálogo de todas las páginas
    ├── log.md                  ← bitácora cronológica (solo se agrega al final)
    ├── raw/                    ← FUENTES CRUDAS, inmutables (.md)
    │   ├── entregables/        ← texto de los informes E1–E6 y las rúbricas del E5 y el E6
    │   ├── normativa/          ← artículos literales de LSS, RACERF, LFPDPPP, LFT y valores oficiales
    │   ├── historial/          ← volcado del historial de Git
    │   └── resultados/         ← salidas literales de los arneses de prueba
    └── wiki/                   ← páginas que escribe y mantiene el agente
        ├── inicio.md           ← panorama (hub principal)
        ├── proyecto/           ← empresa, problema, equipo, trayectoria TRL, riesgos, hoja de ruta
        ├── entregables/        ← un resumen por informe TRL + formato del maestro
        ├── arquitectura/       ← capas, flujo de captura, rutas, modelo de datos, lazo de control
        ├── modulos/            ← una página por archivo de código
        ├── reglas/             ← reglas de negocio del IMSS que aplica el sistema
        ├── conceptos/          ← glosario y conceptos técnicos
        ├── decisiones/         ← registros de decisión (ADR): qué se decidió y por qué
        ├── operacion/          ← arrancar, configurar, mantener, modificar el código
        ├── pruebas/            ← estrategia y resultados de pruebas
        ├── bugs/               ← bugs corregidos (no reintroducir) y conocidos
        ├── historial/          ← cronología y registro de cada sesión de trabajo
        └── consultas/          ← respuestas que valió la pena guardar
```

### 2.1 Fuentes crudas: regla de oro
- `raw/` **no se edita nunca**. Si la fuente original cambia (por ejemplo, se reforma una ley o se entrega
  otro informe), se **agrega** un archivo nuevo o se vuelve a extraer completo y se anota en el log.
- El **código** del repositorio también es fuente: el wiki lo describe, pero **si el wiki y el código no
  coinciden, manda el código**. Se corrige el wiki y se registra en el log como `lint`.
- Los originales de los entregables (Word y PDF) viven fuera del repo, en
  `C:\Users\Pedro\OneDrive\Desktop\7 semestre\LAB AUTO\`. Ahí solo se lee.

### 2.2 El wiki: lo que sí es del agente
- Todo `wiki/`, `index.md` y `log.md`.
- Solo Markdown (`.md`). Nada de imágenes ni binarios: los diagramas van en bloques ` ```mermaid `, que
  Obsidian dibuja.

---

## 3. Convenciones de páginas

### 3.1 Nombres
- Minúsculas, sin acentos, palabras con guiones: `flujo-de-captura.md`.
- **Únicos en todo el wiki.** Obsidian resuelve `[[nombre]]` por nombre de archivo, sin carpeta.
- Módulos: `modulo-<archivo>.md`. Decisiones: `adr-NNN-<tema>.md`. Sesiones: `sesion-AAAA-MM-DD-<tema>.md`.
  Consultas: `AAAA-MM-DD-<tema>.md`. Excepción: `preguntas-frecuentes.md` no lleva fecha, porque se va
  actualizando; las respuestas cortas van ahí y las largas, en su propia consulta con fecha.

### 3.2 Frontmatter obligatorio
```yaml
---
tipo: hub | proyecto | entregable | arquitectura | modulo | regla | concepto | decision | operacion | prueba | bug | historial | consulta
tags: [validacion, imss]
fuentes: ["validaciones.py", "raw/entregables/e5-trl5-ambiente-relevante.md"]
actualizado: 2026-10-04
---
```
Las decisiones agregan `estado: vigente | reemplazada` y `fecha:`. Los bugs agregan `estado: corregido | abierto`.

### 3.3 Contenido mínimo por tipo
- **modulo**: responsabilidad, funciones y constantes clave (con nombres exactos), con quién se relaciona,
  trampas al modificarlo y pruebas que lo cubren.
- **regla**: la regla en una frase, el fundamento legal o de negocio, dónde está en el código, si es error o
  aviso, y un ejemplo.
- **decision (ADR)**: contexto, decisión, por qué, consecuencias y alternativas descartadas.
- **entregable**: qué pedía el maestro, qué se entregó, resultados, qué dejó pendiente y su fuente cruda.
- **historial / sesión**: qué se pidió, qué se hizo, decisiones, hallazgos y pendientes.
- **consulta**: la pregunta, la respuesta con enlaces y la fecha.

### 3.4 Enlaces
- Siempre `[[nombre-de-pagina]]` sin ruta. Enlaza generosamente: cada página enlaza a su hub y a lo que
  menciona; cada concepto enlaza de vuelta a los módulos que lo implementan.
- Para citar código: `` `archivo.py` → `funcion()` ``. Para citar fuentes crudas: `` `raw/…/archivo.md` ``.
- Ninguna página huérfana: como mínimo la enlazan su hub y `index.md`.

---

## 4. Operaciones

### 4.1 Ingerir (cambio de código, nueva fuente o nueva entrega)
1. Lee el cambio completo (diff, archivo nuevo o documento).
2. Si es una fuente externa (informe, ley, resultado), guárdala en `raw/` como `.md`.
3. Actualiza **todas** las páginas afectadas usando el mapa de impacto (§5).
4. Si el cambio contradice algo escrito, corrígelo y deja nota en `## ⚠ Contradicciones` de la página.
5. Actualiza `index.md` y agrega una entrada al final de `log.md`.

### 4.2 Consultar
1. Lee `index.md` y luego las páginas relevantes. Si no alcanza, ve al código o a `raw/`.
2. Responde con enlaces `[[...]]`.
3. Si la respuesta tiene valor duradero (comparación, explicación, guía), guárdala en `wiki/consultas/` y
   regístrala en index y log.

### 4.3 Lint (revisar la salud del wiki)
Revisa y corrige:
- Páginas que ya no coinciden con el código (nombres de funciones, rutas, constantes, montos).
- Enlaces rotos, páginas huérfanas y conceptos mencionados varias veces sin página propia.
- Contradicciones entre páginas y datos viejos (montos anuales, estado de ramas, TRL actual).

Registra el lint en el log.

### 4.4 Registrar una sesión de trabajo
Al terminar una sesión con cambios importantes, crea `wiki/historial/sesion-AAAA-MM-DD-<tema>.md`, actualiza
[[cronologia]] y agrega la entrada al log.

---

## 5. Mapa de impacto: qué páginas tocar según lo que cambie

| Si cambia… | Actualiza… |
|---|---|
| `sigma/app.py` | [[modulo-app]], [[rutas-http]], [[flujo-de-captura]], [[seguridad-web]] (si toca seguridad) |
| `sigma/validaciones.py` | [[modulo-validaciones]], [[reglas-de-validacion]] y la regla específica en `reglas/` |
| `sigma/plazo.py` | [[modulo-plazo]], [[plazo-legal]], [[mantenimiento-anual]] |
| `sigma/database.py` | [[modulo-database]], [[modelo-de-datos]], [[doble-motor-de-base-de-datos]] |
| `sigma/exportar_idse.py` | [[modulo-exportar-idse]], [[lote-idse]] |
| `sigma/usuarios.py` | [[modulo-usuarios]], [[seguridad-web]], [[rutas-http]] |
| `sigma/respaldo.py` | [[modulo-respaldo]], [[configuracion]], [[como-arrancar]] |
| `servidor.py`, `sigma/__main__.py` o la forma de arrancar | [[modulo-servidor]], [[como-arrancar]], [[configuracion]] |
| `sigma/templates/` o `sigma/static/` | [[modulo-interfaz]], [[accesibilidad]] |
| La estructura de carpetas | [[arquitectura-general]], [[inicio]], [[como-arrancar]] y el árbol de §2 de este archivo |
| Arneses de prueba o sus resultados | [[arnes-prueba-de-concepto]], [[arnes-ambiente-relevante]] o [[arnes-integracion]], [[resultados-de-pruebas]] y `raw/resultados/` |
| Montos de salario mínimo o UMA | [[salario-sdi-y-limites]], [[mantenimiento-anual]] y `raw/normativa/` (archivo nuevo del año) |
| Nueva entrega TRL | `raw/entregables/`, página en `entregables/`, [[trayectoria-trl]], [[hoja-de-ruta-trl6]] |
| Ramas o publicación en GitHub | [[inicio]], [[cronologia]] y `raw/historial/git-log.md` (se regenera) |
| Cualquier bug corregido | [[bugs-corregidos]] (y quitarlo de [[bugs-conocidos]]) |

---

## 6. index.md y log.md

- **`index.md`**: catálogo por categoría. Cada línea dice `- [[pagina]] — resumen de una línea`. Se
  actualiza en **cada** cambio del wiki.
- **`log.md`**: solo se agrega al final; lo previo no se edita. Encabezados parseables:
  ```
  ## [AAAA-MM-DD] ingesta | Qué se ingirió
  ## [AAAA-MM-DD] consulta | Pregunta resumida
  ## [AAAA-MM-DD] lint | Resumen
  ## [AAAA-MM-DD] sesion | Tema de la sesión
  ## [AAAA-MM-DD] sistema | Cambio en este esquema o en la estructura
  ```
  Debajo van de 1 a 5 viñetas con las páginas creadas o modificadas y las decisiones.

---

## 7. Reglas de comportamiento del agente

1. **Nunca editar `raw/`.** Solo se agregan archivos nuevos.
2. **No inventar** datos (fechas, cifras, nombres). Si no está en una fuente, se escribe `(por confirmar)`.
3. **El código manda** sobre el wiki. Al detectar una diferencia, corrige el wiki en el mismo momento.
4. **Cada cambio del wiki termina con `index.md` y `log.md` actualizados.**
5. **Git:** esta carpeta forma parte del repo. No se hace commit ni push sin que Pedro lo pida.
6. Los cambios al código los decide Pedro. El wiki registra los **porqués** para que nadie los rediscuta
   (ver [[decisiones]]).
7. Este esquema evoluciona: si Pedro y el agente acuerdan una convención nueva, se escribe aquí y se
   registra en el log como `sistema`.
