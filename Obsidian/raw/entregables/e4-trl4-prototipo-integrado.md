---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 4 — TRL 4.docx"
extraido: 2026-10-04
formato_original: docx
nota: Transcripción automática del archivo entregado. NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 4 — TRL 4: diseño e integración del prototipo

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 4 — TRL 4.docx` (carpeta del 7.° semestre de Pedro).
> Las figuras no se transcriben; solo se conserva su leyenda.

INFORME TÉCNICO

| Título del Proyecto | Sistema para la automatización de altas y bajas de seguro social |
|---|---|
| Tipo de Desarrollo | Software |
| Área Geográfica de Incidencia | Nuevo León |

| Concepto | Nombre | Afiliación |
|---|---|---|
| Nombre del Maestro | Cortes Coss Agustin |  |
| Nombre del Asesor Interno |  |  |
| Nombre del Alumno | Garza Díaz de León Emilio Beas Hernández Ernesto Rivera Diego Gael Antonio Garza Pachicano Hector Gabriel Luna Salas Pedro |  |

| Razón Social de la Empresa | Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V. |
|---|---|
| Página Web | No aplica |
| Dirección | Av. Los Pinos 230, Nexxus Sector Dorado, Joyas de Anahuac, 66055 Cdad. Gral. Escobedo, N.L. |

Índice

*[Índice automático de Word]*

## Diseño e integración del prototipo

Este entregable documenta el diseño detallado y la integración del prototipo Sigma, sistema para la automatización de altas y bajas de trabajadores ante el Instituto Mexicano del Seguro Social (IMSS), desarrollado para Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V. El prototipo eleva a TRL 4 la prueba de concepto validada en el Entregable 3: los componentes que ahí se probaron por separado , validación algorítmica, persistencia relacional, exportación al formato IDSE y bitácora de auditoría; quedan ahora integrados en una sola aplicación cliente-servidor operable de principio a fin por un usuario final, con interfaz de captura, retroalimentación inmediata y verificación funcional documentada.

### Diseño detallado

El prototipo integra los componentes definidos en la Alternativa 3 del Entregable 2 , cliente web, servidor de aplicación, sistema gestor de base de datos relacional, módulo de exportación al formato IDSE y bitácora de auditoría; con la lógica de negocio desarrollada a partir de la prueba de concepto del Entregable 3: el validador algorítmico por campo, las reglas de coherencia entre identificadores oficiales (CURP, NSS y RFC), los catálogos del IDSE para las condiciones de contratación y la selección automática del motor de base de datos.

La arquitectura se organiza en cuatro capas con responsabilidades separadas, de modo que cada una pueda modificarse o sustituirse sin afectar a las demás:

- Capa de presentación (navegador). Formulario de captura, tablero de métricas, tabla de movimientos con filtros y línea de tiempo de la bitácora. Se construyó con HTML, CSS y JavaScript propios, sin frameworks ni bibliotecas externas, por lo que funciona sin conexión a internet. La lógica de cliente es progresiva: aporta máscaras de captura, contadores y validación en vivo, pero el formulario se envía y el servidor valida igual aunque el navegador no ejecute JavaScript.

- Capa de aplicación (servidor Flask). El controlador HTTP (app.py) recibe las peticiones, orquesta la validación, la persistencia y la exportación, y responde con la vista correspondiente. El módulo de validación (validaciones.py) concentra todas las reglas de negocio y es la única fuente de verdad: lo consume tanto el envío del formulario como el punto de validación en vivo. El módulo de abstracción de datos (exportar_idse.py) traduce los movimientos válidos al archivo de texto plano que exige la plataforma IDSE.

- Capa de persistencia. El módulo database.py implementa el modelo relacional normalizado y decide, al arrancar, qué motor usar: PostgreSQL cuando hay un servidor accesible (motor objetivo del proyecto) o SQLite como respaldo local. Toda la capa superior escribe SQL estándar, por lo que el comportamiento es idéntico con cualquiera de los dos motores.

- Salida. El lote IDSE se genera como archivo de texto con marca de tiempo en la carpeta exportaciones/. La carga a la plataforma del IMSS la realiza el usuario, ya que el IDSE no expone una interfaz de programación pública para envío automatizado.

*[Imagen]*

*Figura 1. Arquitectura por capas del prototipo Sigma y flujo de la información entre componentes.*

El modelo de datos consta de cinco tablas normalizadas. Un patrón (registro patronal y razón social) carga uno o más movimientos; un trabajador se registra una sola vez, con CURP y NSS únicos y acumula a lo largo del tiempo sus altas, bajas y reingresos como registros de movimiento; cada acción del sistema queda asentada en la bitácora con el usuario que la ejecutó, la marca de tiempo y, cuando aplica, el movimiento asociado. Separar trabajador y movimiento evita duplicar los datos de identidad y permite reconstruir el historial afiliatorio completo de cada persona.

*[Imagen]*

*Figura 2. Modelo entidad-relación de la base de datos: patron, usuario, trabajador, movimiento y bitacora.*

Tres principios guiaron el diseño detallado. Primero, un solo validador: la retroalimentación inmediata del navegador llama al mismo código que aplica el servidor al guardar, de manera que ambos no puedan desincronizarse. Segundo, integridad transaccional: toda escritura ocurre dentro de un administrador de contexto que garantiza confirmación, reversión y cierre de la conexión aunque se produzca una excepción a mitad de la captura. Tercero, errores y avisos como categorías distintas: los errores impiden guardar y señalan el campo exacto a corregir; los avisos, como un dígito verificador de NSS que no cuadra, se muestran pero no bloquean, porque existen números históricos legítimos que no cumplen el algoritmo actual.

### Diagrama eléctrico

No aplica. El sistema no incluye componentes eléctricos físicos (sensores, actuadores, cableado, tarjetas de adquisición ni fuentes de alimentación dedicadas). Toda la funcionalidad del proyecto se ejecuta como software sobre hardware de propósito general , un equipo de cómputo que actúa como servidor y los equipos de los usuarios que acceden desde el navegador, por lo que no existe un circuito eléctrico propio del proyecto que documentar más allá de la alimentación estándar de dichos equipos.

### Diagrama de control

El sistema se modela como un lazo de control de lazo abierto con retroalimentación al operador. La entrada es el conjunto de datos del movimiento afiliatorio que captura el operador; el bloque de muestreo corresponde al formulario web, donde cada envío constituye una muestra; el comparador corresponde al módulo validaciones.py, que contrasta cada campo contra la referencia , las reglas de formato del IMSS, los catálogos del IDSE y las restricciones de integridad de la base ; y la salida es el estado resultante del movimiento (Válido o Rechazado), que se materializa como un registro en la base de datos y un asiento en la bitácora.

*[Imagen]*

*Figura 3. Diagrama de control del sistema: la salida del comparador regresa al operador como errores por campo, no al proceso.*

No existe actuación automática sobre el proceso: el sistema no corrige por sí mismo los datos de entrada. La única trayectoria de retroalimentación va del comparador al operador, en forma de mensajes de error por campo, tanto en vivo mientras escribe como al intentar guardar, y es el operador quien decide la corrección y genera una nueva muestra. Esta clasificación es consistente con la naturaleza del sistema: un asistente de captura y validación no debe alterar información oficial de un trabajador sin intervención humana.

### Diagrama de flujo

Flujo de ejecución de la captura de un movimiento, desde que el operador envía el formulario hasta que el sistema decide si lo persiste como válido o lo devuelve con los errores señalados:

- 1. Inicio: el operador envía el formulario de captura (POST /capturar).

- 2. Normalizar los campos (mayúsculas en CURP y RFC, solo dígitos en NSS y fecha) y validar el formato de CURP, NSS, RFC, fecha (DDMMAAAA) y tipo de movimiento (08 o 02).

- 3. ¿Hay errores de formato? Si se confirma, registrar en bitácora el intento rechazado y pasar al paso de devolución.

- 4. Validar las reglas por tipo de movimiento: un alta exige tipo de trabajador, tipo de salario, tipo de jornada y salario diario integrado; una baja exige la causa de baja del catálogo IDSE. Verificar además la coherencia entre CURP y RFC.

- 5. ¿Hay errores de negocio? Si se confirma, registrar el intento rechazado y devolver.

- 6. Consultar la base de datos: ¿la CURP ya está registrada con otro NSS?, ¿el NSS pertenece a otro trabajador?, ¿ya existe el mismo movimiento (trabajador, tipo y fecha)?

- 7. ¿Hay conflicto de identidad o duplicado? Si se confirma, registrar y devolver.

- 8. Obtener el expediente del trabajador —o crearlo si es la primera vez— e insertar el movimiento con estado Válido.

- 9. Registrar en bitácora 'Movimiento capturado' con el usuario y la hora, y confirmar la transacción.

- 10. Mostrar la confirmación al operador junto con los avisos no bloqueantes, si los hay.

- 11. Fin. En la rama de rechazo, el formulario se devuelve con los valores capturados intactos y el mensaje de error de cada campo, para que el operador corrija sin volver a escribir todo.

*[Imagen]*

*Figura 4. Diagrama de flujo de la captura de un movimiento. La columna izquierda cubre la validación (pasos 1 a 7) y la derecha la persistencia y respuesta (8 a 11).*

### Diagrama de conexión

Conexión real entre los componentes del prototipo y los puntos de acceso, para los tres recorridos que realiza la información: la captura y consulta desde el navegador, la validación en vivo campo por campo y la exportación del lote hacia el IDSE.

*[Imagen]*

*Figura 5. Diagrama de conexión: recorrido de captura y consulta (arriba), validación en vivo (centro) y exportación al IDSE (abajo).*

El servidor Flask escucha en el puerto 5050 y es alcanzable únicamente desde la red local de la empresa; no se expone a internet. El motor de base de datos nunca es accesible desde el navegador: con PostgreSQL el puerto 5432 se limita a la interfaz local del servidor, y con SQLite la base es un archivo que solo lee el proceso de la aplicación. Toda comunicación cliente-servidor usa HTTP con formularios y JSON; el punto /api/validar responde en JSON con los errores y avisos indexados por campo. La exportación produce un archivo de texto en la carpeta exportaciones/ del servidor, que el usuario descarga desde la interfaz y carga manualmente en la plataforma IDSE del IMSS.

### Selección definitiva de componentes

- Python 3: lenguaje de implementación de toda la lógica de servidor.

- Flask 3 y Jinja2: framework web ligero y motor de plantillas para las vistas.

- PostgreSQL: motor de base de datos relacional objetivo, accedido mediante psycopg2.

- SQLite 3: motor de respaldo incluido en la biblioteca estándar de Python; permite ejecutar el prototipo en cualquier equipo sin instalar un servidor de base de datos.

- HTML5, CSS3 y JavaScript (ECMAScript 5): capa de presentación sin dependencias externas, con tema claro y oscuro definido mediante variables CSS.

- Git y GitHub: control de versiones y revisión de cambios mediante ramas y pull requests.

- Windows 11: sistema operativo del equipo de desarrollo y demostración.

La selección se mantiene respecto a la propuesta de la Alternativa 3 del Entregable 2, con un único ajuste: se incorporó SQLite como motor de respaldo. Durante la integración se comprobó que exigir un servidor PostgreSQL instalado impedía ejecutar el prototipo en equipos sin esa infraestructura; como toda la capa de negocio usa SQL estándar, el respaldo se agregó sin modificar una sola consulta. PostgreSQL sigue siendo el motor objetivo y se selecciona automáticamente en cuanto está disponible.

### Diseño mecánico

No aplica. El proyecto es un desarrollo de software y no involucra ninguna estructura, carcasa, soporte ni componente mecánico físico que diseñar o fabricar.

### Programación

Se implementaron e integraron los siguientes módulos, todos versionados en un repositorio Git en GitHub (github.com/rkiverr/sigma-imss):

- app.py — controlador HTTP. Define las rutas de la aplicación: la pantalla principal con filtros y paginación (GET /), la captura de movimientos (POST /capturar), la generación del lote (POST /exportar), la descarga del último lote (GET /descargar-lote), la validación en vivo (POST /api/validar) y el detalle de un movimiento con su bitácora (GET /api/movimiento/<id>). Incluye los manejadores de error 404, 500 y 503 con páginas propias.

- validaciones.py — validación algorítmica. Expresiones regulares para CURP, NSS, RFC y fecha; comprobación de que la fecha de nacimiento embebida en la CURP exista en el calendario; coherencia entre las iniciales y la fecha de CURP y RFC; catálogos IDSE de tipo de trabajador, tipo de salario, tipo de jornada y causa de baja; validación numérica del salario diario integrado con topes; y el dígito verificador del NSS por el algoritmo de Luhn como aviso no bloqueante. La función validar_campos devuelve errores y avisos indexados por campo.

- database.py — persistencia. Esquema de las cinco tablas para ambos motores, selección automática de motor, administrador de contexto transaccional y operaciones de dominio: registro en bitácora, obtención o creación del trabajador, detección de conflictos de identidad, detección de movimientos duplicados y contadores para el tablero.

- exportar_idse.py — abstracción de datos. Traducción de los movimientos válidos a líneas de texto plano con campos delimitados, limpieza de caracteres que romperían el archivo y generación de lotes con nombre único por marca de tiempo.

- templates/ — vistas. Plantilla base con barra superior, interruptor de tema y notificaciones; pantalla principal con tablero, formulario, exportación, bitácora y tabla de movimientos; y página de error.

- static/ — presentación. Hoja de estilos con el sistema de diseño y los temas claro y oscuro; script de cliente con máscaras de captura, contadores, selector de calendario sincronizado con el formato DDMMAAAA, campos condicionales según el tipo de movimiento, validación en vivo y diálogo de detalle.

- test_prueba_concepto.py — arnés de pruebas. Ejecuta los tres bloques del desarrollo experimental sobre una base propia y genera el reporte de resultados.

*[Imagen]*

*Figura 6. Pantalla principal del prototipo: tablero de métricas, formulario de captura con campos condicionales, exportación a IDSE y bitácora.*

*[Imagen]*

*Figura 7. Respuesta del servidor ante una captura inválida: resumen de errores, marca por campo y conservación de los valores capturados.*

*[Imagen]*

*Figura 8. Tabla de movimientos con búsqueda, filtros por estado y tipo, y estados Válido y Exportado.*

*[Imagen]*

*Figura 9. Tema oscuro de la interfaz, seleccionable desde la barra superior y persistente entre sesiones.*

### Integración de sensores

Al tratarse de un sistema de software, los sensores son virtuales: los componentes que captan la información de entrada y el estado del proceso. Quedaron integrados y validados con datos reales los siguientes:

- Formulario de captura con máscaras. Capta los datos del movimiento y los normaliza en el origen: convierte a mayúsculas la CURP y el RFC, restringe el NSS y la fecha a dígitos, muestra contadores de longitud y ofrece un selector de calendario que rellena el campo en el formato DDMMAAAA del IDSE.

- Punto de validación en vivo (/api/validar). Cada vez que el operador abandona un campo, el navegador envía el formulario completo al servidor y recibe los errores y avisos de cada campo, ejecutados por el mismo validador que se aplica al guardar.

- Consultas de estado a la base de datos. Antes de insertar, el sistema lee el expediente existente del trabajador para detectar una CURP registrada con otro NSS, un NSS que pertenece a otra persona o un movimiento idéntico ya capturado; y lee los contadores de movimientos pendientes, exportados, altas y bajas que alimentan el tablero.

Queda fuera del alcance de esta fase la verificación en línea de la CURP contra el RENAPO y del NSS contra el IMSS, ya que ninguna de las dos instituciones ofrece una interfaz de programación pública para consulta automatizada; el sistema valida la estructura y la coherencia interna de los identificadores, que es lo que sí puede comprobarse sin conexión.

### Integración de actuadores

Los actuadores virtuales son los componentes que producen un efecto a partir de la decisión del comparador. Están integrados y validados:

- Escritura transaccional en la base de datos. Inserción del trabajador (si es nuevo) y del movimiento con estado Válido, dentro de una transacción que se revierte por completo si cualquier paso falla.

- Registro en bitácora. Cada captura aceptada, cada intento rechazado, con el detalle de los errores y cada exportación quedan asentados con usuario y marca de tiempo.

- Generación del lote IDSE. Traducción de los movimientos válidos pendientes al archivo de texto plano, cambio de su estado a Exportado para que no se incluyan dos veces y descarga desde la interfaz.

- Respuesta al operador. Marcado del campo con error, resumen de errores, notificaciones flotantes de éxito o rechazo y conservación de lo capturado.

El envío automático del lote a la plataforma IDSE no es un actuador implementable: el IDSE opera mediante carga manual de archivo con firma electrónica del patrón y no expone una interfaz para automatizarlo. Las notificaciones por correo electrónico al responsable de recursos humanos se identifican como trabajo planeado para una fase posterior.

### Integración del controlador

El controlador de software es el módulo app.py, que quedó completamente integrado y operativo. Ante cada petición de captura ejecuta la cadena de mando en orden fijo: normaliza los datos del formulario; invoca al validador y recibe los errores y avisos por campo; abre una conexión transaccional; verifica el usuario que captura contra la tabla de usuarios; consulta los conflictos de identidad y los duplicados; y, según el resultado, persiste el movimiento y confirma, o registra el rechazo y devuelve el formulario con los errores. Para la exportación, selecciona los movimientos válidos pendientes, genera el archivo, actualiza su estado y registra la operación.

El controlador también gobierna las condiciones anómalas: un usuario inválido, una base de datos inaccesible o una excepción no prevista producen una respuesta controlada (página de error 422, 503 o 500) en lugar de un fallo del servidor, y la conexión se cierra siempre gracias al administrador de contexto. Esta cadena fue validada en la prueba de concepto del Entregable 3 y se volvió a verificar en esta fase con las pruebas de la sección siguiente.

### Pruebas de laboratorio

Las pruebas se ejecutaron directamente sobre el prototipo integrado, sin entorno de laboratorio separado, en dos modalidades: el arnés automatizado del desarrollo experimental (bloques de validación, exportación y concurrencia) y pruebas funcionales por HTTP sobre la aplicación en ejecución, incluyendo casos de robustez y seguridad.

*Tabla 1. Pruebas ejecutadas sobre el prototipo integrado y resultado obtenido.*

| Prueba | Resultado obtenido |
|---|---|
| C1 — Alta válida con todos los campos | Aceptada · estado Válido · asiento en bitácora |
| C2 — Baja válida con causa del catálogo | Aceptada · estado Válido |
| C3 — CURP con longitud incorrecta (9 caracteres) | Rechazada: 'La CURP debe tener 18 caracteres; se capturaron 9' |
| C4 — NSS con letras | Rechazada: 'El NSS solo admite dígitos' |
| C5 — Fecha con guiones (12-09-2026) | Rechazada: 'Formato de fecha inválido: debe ser DDMMAAAA' |
| C6 — Fecha inexistente (31 de febrero) | Rechazada: 'La combinación de día, mes y año no existe' |
| C7 — Tipo de movimiento 99 | Rechazada: 'debe ser 08 (Alta o Reingreso) o 02 (Baja)' |
| C8 — Nombre vacío | Rechazada: 'El nombre completo del trabajador es obligatorio' |
| Exportación del lote (bloque 2) | 2 movimientos exportados (C1 y C2), archivo con una línea por movimiento y campos delimitados por '\|' |
| Concurrencia: dos usuarios capturan a la vez (bloque 3) | Dos movimientos con id distinto, cada uno atribuido a su usuario en la bitácora, sin pérdida de datos |
| CURP ya registrada con otro NSS | HTTP 422 · 'La CURP ya está registrada a nombre de … Verifica el NSS capturado' |
| Mismo trabajador, tipo y fecha capturados dos veces | HTTP 422 · 'Este movimiento ya fue capturado (folio #1)' |
| Baja sin causa de baja | HTTP 422 · 'La causa de baja es obligatoria para este tipo de movimiento' |
| RFC incoherente con la CURP | HTTP 422 · 'Las primeras 4 letras del RFC no coinciden con las de la CURP' |
| Usuario que captura inválido (usuario_id=abc) | HTTP 422 · 'Selecciona un usuario válido' (antes: error 500) |
| Exportar sin movimientos pendientes | Aviso 'No hay movimientos válidos pendientes de exportar' |
| Descargar lote cuando no existe ninguno | Aviso y regreso al inicio (antes: excepción) |
| Ruta inexistente | HTTP 404 con página de error propia |
| Inyección SQL en el buscador (' OR '1'='1 y DROP TABLE) | 0 resultados; la tabla sigue intacta (consultas parametrizadas) |
| Inyección de HTML en el nombre (<script>) | Texto mostrado escapado, sin ejecución (autoescape de plantillas) |

### Resultados

Las veinte pruebas arrojaron el resultado esperado en todos los casos. El arnés automatizado reporta 8 de 8 casos de validación correctos (100 %) y los bloques de exportación y concurrencia cumplen; las pruebas funcionales por HTTP produjeron en cada caso la respuesta controlada prevista, y el registro del servidor no muestra ninguna excepción no manejada durante toda la sesión de pruebas. El sistema distingue correctamente entre errores de formato, errores de negocio y conflictos de integridad, conserva lo capturado cuando rechaza, no exporta dos veces el mismo movimiento y resiste entradas maliciosas.

*Tabla 2. Cumplimiento de los criterios de aceptación definidos para la prueba de concepto.*

| Criterio de aceptación | Estado |
|---|---|
| 1) Rechazo de CURP y NSS inválidos | CUMPLE (8/8 casos correctos) |
| 2) Rechazo de fechas inválidas | CUMPLE (casos C5 y C6) |
| 3) Estructura del archivo de exportación IDSE | CUMPLE (lote generado y descargable) |
| 4) Asociación de cada movimiento a usuario y marca de tiempo en bitácora | CUMPLE (bloques 1 y 3) |
| 5) Sin pérdida de datos en captura concurrente | CUMPLE (bloque 3) |

Con estos resultados el prototipo alcanza el nivel TRL 4: los componentes validados por separado en el Entregable 3 operan integrados en una aplicación completa, ejercitada de extremo a extremo con datos representativos de la empresa, y con un comportamiento verificado tanto en el camino normal como en las condiciones de error.

### Ajustes realizados

Durante la integración se detectaron y corrigieron los siguientes defectos de la prueba de concepto, todos reproducibles con datos de captura normales:

- Una CURP ya registrada con un NSS distinto provocaba un error de integridad de la base (IntegrityError) y una respuesta 500. Ahora el conflicto se detecta antes de insertar y se devuelve un mensaje que indica el campo y el expediente en conflicto.

- Un identificador de usuario vacío o no numérico provocaba un ValueError y una respuesta 500. Ahora se valida contra la tabla de usuarios.

- La descarga del lote lanzaba una excepción cuando aún no se había generado ninguno. Ahora se comprueba su existencia y se avisa al usuario.

- Una excepción a mitad de la captura dejaba la conexión abierta y la transacción sin revertir. Se introdujo un administrador de contexto que garantiza confirmación, reversión y cierre.

- Con la tabla de patrones vacía el sistema fallaba al obtener el registro patronal. Ahora se crea automáticamente.

- El formulario rechazado perdía todo lo capturado al redirigir. Ahora se devuelve la misma vista con los valores intactos y el error de cada campo.

- Cada exportación sobrescribía el archivo anterior. Los lotes se guardan ahora con marca de tiempo en una carpeta dedicada.

- Se incorporó SQLite como motor de respaldo con selección automática, tras comprobar que el prototipo no arrancaba en equipos sin servidor PostgreSQL.

- Los casos de prueba C2 y C5 del arnés, cuya causa de baja era texto libre, se actualizaron para usar el catálogo IDSE incorporado en esta fase; el resultado esperado de cada caso no cambió. El arnés se configuró para usar una base de datos propia, de modo que sus resultados sean reproducibles.

Se documentan como trabajo planeado, no como ajuste correctivo: la autenticación de usuarios con inicio de sesión (hoy el usuario que captura se elige de una lista, por lo que la bitácora documenta la autoría pero no la demuestra), la confirmación del layout del archivo de exportación contra la especificación oficial vigente del IDSE, las notificaciones por correo electrónico y el despliegue sobre un servidor de aplicaciones de producción en lugar del servidor de desarrollo de Flask.

### Referencias

- Cámara de Diputados del H. Congreso de la Unión. (2024). Ley del Seguro Social. https://www.diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf

- Gobierno de México. (s.f.). Consulta tu CURP. https://www.gob.mx/curp/

- Instituto Mexicano del Seguro Social. (s.f.). IDSE — IMSS desde su empresa. https://idse.imss.gob.mx/

- Pallets Projects. (s.f.). Flask Documentation. https://flask.palletsprojects.com/

- Pallets Projects. (s.f.). Jinja Documentation. https://jinja.palletsprojects.com/

- PostgreSQL Global Development Group. (s.f.). PostgreSQL Documentation. https://www.postgresql.org/docs/

- Psycopg. (s.f.). Psycopg — PostgreSQL database adapter for Python. https://www.psycopg.org/docs/

- Python Software Foundation. (s.f.). sqlite3 — DB-API 2.0 interface for SQLite databases. https://docs.python.org/3/library/sqlite3.html

- SQLite Consortium. (s.f.). SQLite Documentation. https://www.sqlite.org/docs.html
