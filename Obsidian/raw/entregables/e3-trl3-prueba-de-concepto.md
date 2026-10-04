---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 3 — TRL 3.pdf"
extraido: 2026-10-04
formato_original: pdf
nota: Transcripción automática del archivo entregado. NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 3 — TRL 3: prueba de concepto

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 3 — TRL 3.pdf` (carpeta del 7.° semestre de Pedro).
> Las figuras no se transcriben; solo se conserva su leyenda.

## Página 1 del PDF

INFORME TÉCNICO Título del Proyecto Sistema para la automatización de altas y bajas de seguro social Tipo de Desarrollo Software Área Geográfica de Incidencia Nuevo León Concepto Nombre Afiliación Nombre del Maestro Cortes Coss Agustin Nombre del Asesor Interno Nombre del Alumno

1. Garza Díaz de León Emilio

2. Beas Hernández Ernesto

3. Rivera Diego Gael Antonio

4. Garza Pachicano Hector Gabriel

5. Luna Salas Pedro Razón Social de la Empresa Desarrollos Eléctricos y Soluciones Avanzadas S.A de C.V.

Página Web No aplica Dirección Av. Los Pinos 230, Nexxus Sector Dorado, Joyas de Anahuac, 66055 Cdad. Gral. Escobedo, N.L.

## Página 2 del PDF

Índice Diseño de prueba de concepto................................................................................................... 1 Variables de entrada......................................................................................................................1 Variables de salida.........................................................................................................................2 Criterios de aceptación................................................................................................................ 2 Materiales y componentes........................................................................................................... 3 Programación inicial......................................................................................................................4 Simulación, cuando corresponda................................................................................................6 Desarrollo experimental............................................................................................................... 7 Resultados......................................................................................................................................8 Análisis de resultados................................................................................................................. 11 Problemas encontrados..............................................................................................................12 Modificaciones realizadas..........................................................................................................14 Conclusiones............................................................................................................................... 15

## Página 3 del PDF

Diseño de prueba de concepto La prueba se centrará en validar el funcionamiento del lazo cerrado de control a nivel de software, simulando la interacción entre el usuario administrativo (cliente) y el motor de validación (servidor).

Para ello, se desarrollará un prototipo de interfaz web que sustituya la captura de datos tradicional en hojas de cálculo. En esta interfaz, el usuario introducirá los datos de un trabajador. El diseño establece que la información introducida pasará por un controlador lógico que ejecutará algoritmos de validación basados en expresiones regulares (Regex) para identificar anomalías antes de procesar la solicitud.

El flujo de la prueba se divide en dos escenarios para comprobar la respuesta del sistema ante perturbaciones internas:

- Simulación de perturbación. Se introducirán intencionadamente datos con errores ortográficos o de longitud incorrecta para verificar que el sistema detenga el proceso y emita una alerta, lo que demostrará su capacidad de autocorrección sin depender de códigos de color.

- Salida de control. se ingresarán datos correctos para comprobar que el actuador lógico es capaz de estructurar y generar algorítmicamente la cadena de texto plano compatible con los requerimientos de carga masiva de la plataforma IDSE del IMSS.

Variables de entrada Las variables de entrada representan la "Referencia" o valor deseado en nuestro lazo de control. Estos son los datos que el usuario ingresará en la interfaz del prototipo para solicitar un trámite:

- nss_trabajador. Número de Seguridad Social del empleado. Constituye una variable que debe contener exactamente 11 dígitos numéricos sin caracteres especiales ni letras.

- curp_trabajador. Clave Única de Registro de Población. Se procesará como una cadena de texto que obligatoriamente debe contener obligatoriamente de 18 caracteres alfanuméricos.

## Página 4 del PDF

- rfc_trabajador. Registro Federal de Contribuyentes. Cadena de 13 caracteres que incluye la homoclave del empleado.

- salario_diario_integrado. Salario Base de Cotización (SBC). Variable numérica con dos decimales que representa el sueldo del trabajador para el cálculo de cuotas.

- tipo_movimiento. Variable de selección que define la acción a ejecutar. Adoptará los valores numéricos predefinidos por el IMSS: 08 (alta o reingreso), 02 (baja) o 07 (modificación de salario).

Variables de salida Las variables de salida representan el resultado de la ejecución del actuador lógico después de pasar por el filtro del controlador. En esta prueba de concepto, se definen dos salidas principales:

- codigo_error. Variable cualitativa de texto semántico. Si el controlador detecta una anomalía en la longitud o el formato de las variables de entrada (error de captura), esta variable almacena y muestra el mensaje descriptivo exacto del fallo, sustituyendo por completo el uso de alertas visuales basadas en colores.

- lote_exportacion. Variable de tipo cadena de texto (string). Se genera únicamente si todas las validaciones son exitosas. Contiene la concatenación de los datos del patrón y del trabajador, mapeados y estructurados con la sintaxis y los espacios exactos que exige la plataforma IDSE para procesar el archivo plano final.

Criterios de aceptación Para que la prueba de concepto sea considerada exitosa y demuestre que la solución tecnológica resuelve el problema planteado, el prototipo debe cumplir estrictamente los siguientes criterios operativos:

- Filtro algorítmico (Regex) funcional. El sistema debe rechazar de manera inmediata cualquier intento de registro si la variable nss_trabajador contiene letras,

## Página 5 del PDF

espacios o tiene una longitud diferente a 11 dígitos, o si la variable curp_trabajador tiene menos de 18 caracteres.

- Validación sin colores. El sistema debe demostrar el cumplimiento de las normas de accesibilidad (WCAG) emitiendo mensajes de error explícitos en texto, comprobando que el estado no depende de la percepción visual del usuario.

- Abstracción y generación automática. Tras ingresar datos correctos, el sistema debe ser capaz de traducir la información visual al formato de máquina e imprimir en pantalla la cadena de texto plano exactamente estructurada para el portal IDSE.

- Operación simultánea simulada. El servidor web local debe poder recibir peticiones, procesar la lógica de negocio y devolver una respuesta en el navegador (arquitectura cliente-servidor), garantizando que el diseño está preparado para soportar a múltiples usuarios que trabajan al mismo tiempo sin usar archivos de Excel.

Materiales y componentes Al tratarse de una solución basada en el desarrollo de software, los materiales físicos e instrumentos se sustituyen por requisitos de infraestructura y herramientas de programación.

- Entorno de desarrollo (hardware). Equipo de cómputo estándar con capacidad para ejecutar un servidor local, con teclado y monitor para la captura y visualización de la interfaz.

- Lenguaje de programación. Python versión 3, seleccionado por su alta capacidad para el manejo de cadenas de texto y operaciones lógicas.

- Framework web. Microframework como Flask para montar la arquitectura cliente-servidor y construir las rutas de comunicación entre la interfaz de usuario y el controlador lógico.

- Librerías nativas. Módulo re de Python para la implementación matemática de las expresiones regulares (regex), que servirán como mecanismo de validación y control.

## Página 6 del PDF

- Interfaz de cliente. Navegador web estándar (Chrome, Edge o Firefox) y lenguajes de marcado (HTML/CSS) para renderizar los formularios de captura.

Programación inicial La programación inicial del prototipo se realizó en Python 3 sobre el microframework Flask, conforme a los materiales y componentes definidos en el apartado anterior. El código se organizó en cinco módulos independientes que reproducen, uno a uno, los elementos del diagrama de bloques presentado en la Entrega 2: el módulo validaciones.py opera como controlador lógico, el módulo exportar_idse.py como actuador lógico o salida de control, el módulo database.py como capa de persistencia, el archivo app.py como servidor que articula el flujo completo y la plantilla templates/index.html como interfaz de cliente. Esta separación en módulos permite que cada elemento del lazo cerrado pueda ejercitarse de forma aislada, sin depender de la interfaz gráfica, lo que resulta indispensable para la verificación experimental descrita más adelante.

La capa de persistencia se programó en el módulo database.py mediante la función init_db(), que construye un esquema relacional normalizado de cinco tablas: patron, usuario, trabajador, movimiento y bitacora. La normalización se aplicó de modo que los datos de identificación de cada trabajador se almacenan una sola vez en la tabla trabajador, mientras que la tabla movimiento los referencia a través de la llave foránea trabajador_id, eliminando así la redundancia que presentaba el archivo de cálculo original.

La integridad de los datos se refuerza mediante tres mecanismos declarativos: la activación de PRAGMA foreign_keys = ON dentro de la función get_conn(), las restricciones UNIQUE sobre los campos curp y nss de la tabla trabajador, y las restricciones CHECK que limitan el campo tipo_movimiento a los valores '08' y '02', el campo estado a 'Válido', 'Rechazado' o 'Exportado', y el campo rol a 'administrador' o 'captura'. El módulo se completa con las funciones registrar_bitacora(), que estampa cada operación con el identificador del usuario y una marca de tiempo, y obtener_o_crear_trabajador(), que evita el alta duplicada de un mismo trabajador.

## Página 7 del PDF

El controlador lógico se programó en el módulo validaciones.py a partir de cuatro expresiones regulares compiladas con la librería nativa re y un conjunto de tipos de movimiento admitidos. La constante CURP_REGEX exige la estructura oficial de dieciocho caracteres, compuesta por cuatro letras, seis dígitos de fecha de nacimiento, el carácter de sexo H o M, cinco letras, un carácter alfanumérico y un dígito verificador;

NSS_REGEX exige exactamente once dígitos numéricos; RFC_REGEX contempla las letras iniciales, la fecha y la homoclave; y FECHA_REGEX impone el formato DDMMAAAA. Sobre estas reglas se construyeron las funciones validar_curp(), validar_nss(), validar_rfc(), validar_fecha() y validar_tipo_movimiento(), coordinadas por la función validar_movimiento(), que constituye el punto único de entrada del controlador: recibe el diccionario de datos capturados y devuelve una tupla formada por un valor booleano y una lista de mensajes de error. A diferencia de una validación que se detiene ante el primer fallo, esta implementación acumula todos los errores detectados, de manera que el operador recibe en una sola respuesta el conjunto completo de correcciones que debe realizar.

Finalmente, el servidor se programó en app.py con cuatro rutas que materializan la arquitectura cliente-servidor: la ruta GET / presenta el formulario junto con el listado de movimientos y los últimos quince registros de la bitácora; la ruta POST /capturar recibe los datos del formulario, invoca validar_movimiento() y, según el resultado, persiste el movimiento o registra el intento rechazado; la ruta POST /exportar genera el lote; y la ruta GET /descargar-lote entrega el archivo resultante. El actuador lógico reside en exportar_idse.py, donde la lista CAMPOS_EXPORTACION define el orden de los once campos del layout y las funciones generar_linea_idse(), generar_lote_idse() y exportar_a_archivo() realizan el mapeo de la información almacenada hacia la cadena de texto plano. La plantilla templates/index.html se programó con HTML y CSS sin dependencia de bibliotecas externas, presentando el estado de cada movimiento como una etiqueta de texto explícita en la columna Estado y los avisos del sistema como mensajes redactados, en cumplimiento del criterio de validación sin colores.

## Página 8 del PDF

Simulación, cuando corresponda Al tratarse de un desarrollo de software, la simulación no requiere el modelado físico de un sistema, sino la ejecución controlada del lazo cerrado sobre un conjunto de datos sintéticos que reproduzcan tanto la operación normal como las perturbaciones internas descritas en la Entrega 2. Para ello se programó el módulo test_prueba_concepto.py, que funciona como banco de simulación: inyecta datos en el controlador lógico sin intervención humana, observa la respuesta del sistema y compara el resultado obtenido contra el resultado esperado para cada caso.

El conjunto de simulación se definió en la estructura CASOS_PRUEBA, integrada por ocho casos que cubren los dos escenarios planteados en el diseño de la prueba de concepto. El escenario de salida de control se representa mediante los casos C1, un alta de tipo 08 con todos los campos correctos, y C2, una baja de tipo 02 igualmente correcta.

El escenario de simulación de perturbación se representa mediante seis casos que introducen deliberadamente errores de captura:

- C3. CURP con longitud incorrecta, para verificar el rechazo por estructura incompleta.

- C4. NSS que contiene letras dentro de la cadena numérica.

- C5. Fecha capturada con guiones en lugar del formato DDMMAAAA.

- C6. Fecha sintácticamente bien formada pero inexistente en el calendario, correspondiente al 31 de febrero.

- C7. Tipo de movimiento fuera del catálogo admitido.

- C8. Nombre del trabajador vacío.

Con el fin de garantizar la reproducibilidad de la simulación, el arnés elimina el archivo prueba_concepto.db y vuelve a invocar init_db() al inicio de cada corrida, de modo que toda ejecución parte exactamente del mismo estado inicial: el patrón semilla registrado con la clave A1234567890 y los dos usuarios de prueba admin.rrhh, con rol de administrador, y captura.obra1, con rol de captura. De esta forma, los resultados

## Página 9 del PDF

observados son atribuibles a la lógica del sistema y no a residuos de ejecuciones anteriores.

La operación simultánea se simuló en la función bloque_3_concurrencia() mediante la librería threading. Dos hilos de ejecución, capturar_usuario_a() y capturar_usuario_b(), abren cada uno su propia conexión a la base de datos a través de get_conn() e insertan un movimiento afiliatorio de forma paralela, atribuyendo cada operación a un usuario distinto. Este mecanismo permite reproducir en un solo equipo la condición de dos operadores administrativos trabajando al mismo tiempo, sin necesidad de desplegar el sistema en una red con múltiples estaciones de trabajo, lo que resulta adecuado para el alcance de una prueba de concepto en entorno controlado.

Desarrollo experimental El desarrollo experimental se llevó a cabo en un equipo de cómputo estándar con Python 3 instalado, utilizando el servidor de desarrollo de Flask sobre la dirección local http://localhost:5050 y el archivo prueba_concepto.db como almacén de datos. La experimentación se organizó en dos vías complementarias: la ejecución del arnés automatizado, mediante el comando python test_prueba_concepto.py, que ejercita la lógica del servidor sin intervención manual; y la verificación de la aplicación web, mediante el comando python app.py, que permite comprobar el recorrido completo desde el formulario del navegador hasta la base de datos. El arnés se estructuró en los tres bloques que se describen a continuación.

El primer bloque, implementado en la función bloque_1_validacion(), recorre los ocho casos del conjunto de simulación y somete cada uno a la función validar_movimiento().

Por cada caso se compara el resultado obtenido contra el valor esperado declarado en el propio conjunto de datos y se imprimen los mensajes de error emitidos por el controlador.

Los casos que superan la validación se insertan en la tabla movimiento con estado 'Válido', mientras que los casos rechazados no generan ningún registro de movimiento; en ambas situaciones se invoca registrar_bitacora(), de manera que tanto las capturas

## Página 10 del PDF

exitosas como los intentos rechazados quedan documentados con usuario y marca de tiempo.

El segundo bloque, implementado en bloque_2_exportacion(), ejercita el actuador lógico.

Se ejecuta una consulta que une las tablas movimiento, trabajador y patron, filtrando aquellos registros cuyo estado sea 'Válido' y cuyo indicador exportado sea igual a cero, es decir, los movimientos válidos que aún no han sido enviados. El conjunto resultante se entrega a la función exportar_a_archivo(), que produce el archivo lote_idse_prueba.txt.

Concluida la generación, el sistema actualiza los registros exportados asignándoles el valor uno en el campo exportado y el estado 'Exportado', y deja constancia de la operación en la bitácora.

El tercer bloque, implementado en bloque_3_concurrencia(), lanza los dos hilos de captura simultánea y, una vez finalizados, consulta la tabla bitacora para comprobar que cada movimiento quedó asociado a su usuario correspondiente. De forma complementaria, se verificó el comportamiento de las cuatro rutas del servidor mediante peticiones directas a la aplicación, comprobando la respuesta de la ruta GET /, el resultado de la ruta POST /capturar ante datos correctos e incorrectos, y la generación del lote a través de la ruta POST /exportar. La totalidad de la evidencia producida por el arnés se almacena automáticamente en el archivo resultados_prueba_concepto.txt.

Resultados En el primer bloque, correspondiente a la validación de captura, los ocho casos del conjunto de prueba coincidieron con el resultado esperado, lo que arroja un desempeño de 8 de 8 casos correctos, equivalente al 100.0 % del conjunto ejercitado. Los dos casos correctos, C1 y C2, fueron aceptados por el controlador, mientras que los seis casos con perturbación fueron rechazados, cada uno acompañado del mensaje de texto que identifica la causa concreta del fallo. Los mensajes emitidos por el sistema fueron los siguientes:

## Página 11 del PDF

- C3. «CURP inválida: debe tener 18 caracteres con el formato oficial (4 letras, 6 dígitos, sexo H/M, 5 letras, 1 alfanumérico, 1 dígito).»

- C4. «NSS inválido: debe tener exactamente 11 dígitos numéricos.»

- C5. «Fecha inválida: el formato debe ser DDMMAAAA (p. ej. 05092026).»

- C6. «Fecha inválida: la combinación de día/mes/año no existe en el calendario.»

- C7. «Tipo de movimiento inválido: debe ser '08' (Alta/Reingreso) o '02' (Baja).»

- C8. «El nombre completo del trabajador es obligatorio.» En el segundo bloque se exportaron dos movimientos, que corresponden exactamente a los dos casos válidos del conjunto de prueba, generándose el archivo lote_idse_prueba.txt con una línea por movimiento y los once campos separados por el carácter delimitador. El contenido obtenido fue el siguiente:

- A1234567890|08|RIDG050515HNLVLL09|12345678901|RIDG050515AB1|05092 026|1|0|1|450.50|

- A1234567890|02|BEHE900101HNLRRN05|98765432101|BEHE900101AB2|010 92026|||||Terminación de obra En el tercer bloque, las dos capturas simultáneas se registraron con los identificadores 3 y 4 respectivamente, sin colisión ni sobrescritura entre ellas, y generaron dos entradas independientes en la bitácora: la primera atribuida al usuario admin.rrhh y la segunda al usuario captura.obra1, ambas con su marca de tiempo correspondiente. La verificación complementaria de las rutas del servidor devolvió código de respuesta 200 en la ruta GET /; el mensaje de confirmación de captura ante datos correctos y el mensaje de rechazo ante datos inválidos en la ruta POST /capturar; y la confirmación de generación del lote en la ruta POST /exportar.

El contraste de estos resultados frente a los criterios de aceptación definidos para la prueba de concepto se resume a continuación:

## Página 12 del PDF

- Filtro algorítmico (Regex) funcional. Cumple. Los ocho casos del conjunto fueron clasificados correctamente.

- Validación sin colores. Cumple. Cada rechazo se comunicó mediante un mensaje de texto explícito.

- Abstracción y generación automática. Cumple. Se generaron las dos líneas de lote correspondientes a los movimientos válidos.

- Operación simultánea simulada. Cumple. Ambas capturas concurrentes se conservaron con identificadores distintos y atribución individual.

## Página 13 del PDF

Análisis de resultados El desempeño obtenido en el primer bloque confirma que el filtro algorítmico opera como barrera efectiva de entrada. Resulta particularmente relevante el contraste entre los casos C5 y C6: el primero es rechazado por la expresión regular FECHA_REGEX, al no ajustarse al formato DDMMAAAA, mientras que el segundo supera esa primera comprobación puesto que la cadena 31022026 es sintácticamente válida y solo es detenido por la verificación posterior, que intenta construir la fecha con la librería datetime y falla al no existir el 31 de febrero en el calendario. Este comportamiento demuestra que la validación no se limita a un contraste de forma, sino que incorpora una segunda comprobación semántica, precisamente el tipo de error que el archivo de cálculo original no era capaz de detectar.

Respecto al criterio de validación sin colores, los resultados muestran que la totalidad de la información de estado se transmite mediante cadenas de texto: la función validar_movimiento() devuelve mensajes redactados en lenguaje natural que describen la causa exacta del fallo, y la interfaz los presenta como avisos escritos, mientras que la

## Página 14 del PDF

columna Estado de la tabla de movimientos muestra siempre la etiqueta textual correspondiente. El color empleado en la plantilla actúa únicamente como refuerzo visual redundante y no como portador exclusivo del significado, lo que responde directamente a la problemática documentada en la Entrega 1, donde la interpretación del archivo dependía por completo de la percepción cromática del operador.

En cuanto a la abstracción y generación automática, el análisis de las dos líneas obtenidas confirma que el sistema traduce correctamente la información almacenada en las tablas relacionales hacia una cadena de texto plano ordenada según la secuencia definida en CAMPOS_EXPORTACION, incorporando el registro patronal proveniente de la tabla patron y los datos del trabajador provenientes de la tabla trabajador sin recaptura manual. Debe precisarse, no obstante, que la estructura empleada utiliza campos delimitados y no el layout oficial de ancho fijo del IMSS, circunstancia advertida en el propio módulo exportar_idse.py; en consecuencia, el criterio se considera satisfecho a nivel de principio de exportación, que es lo que corresponde demostrar en esta etapa, pero no como formato definitivo listo para envío.

Finalmente, el resultado del bloque de concurrencia evidencia que el gestor de base de datos resolvió las dos escrituras simultáneas asignando identificadores distintos y conservando ambas operaciones íntegras, con su atribución individual en la bitácora. Este comportamiento valida el principio de no repudio planteado en la Entrega 1 y supera la limitación fundamental del archivo de cálculo compartido. Conviene delimitar, sin embargo, el alcance de la medición: el 100.0 % obtenido se refiere a un conjunto dirigido de ocho casos diseñados para cubrir las reglas implementadas, y no a una muestra estadística de la operación real de la empresa; asimismo, la concurrencia se verificó con dos hilos sobre un motor local, no bajo carga sostenida de múltiples estaciones.

Problemas encontrados El principal problema identificado durante el desarrollo se refiere a la estructura del archivo de exportación. El módulo exportar_idse.py genera actualmente los registros

## Página 15 del PDF

como campos delimitados por un separador, en lugar de emplear el layout de ancho fijo con las posiciones exactas que exige la plataforma IDSE. Esta limitación se encuentra documentada de forma explícita en el propio módulo, que advierte que la estructura de columnas debe confirmarse contra el layout oficial vigente publicado por el IMSS antes de utilizarse en un entorno real. El obstáculo no es de naturaleza algorítmica, ya que el mecanismo de mapeo está resuelto, sino de acceso a la especificación oficial actualizada, la cual deberá obtenerse para la siguiente etapa.

Un segundo problema, detectado al ejercitar el sistema con datos límite, afecta a la función obtener_o_crear_trabajador() del módulo database.py. Dicha función determina si un trabajador ya existe consultando únicamente el campo curp; en consecuencia, cuando se captura un trabajador con una CURP nueva pero un NSS que ya pertenece a otro registro, la función intenta la inserción y la restricción UNIQUE de la columna nss aborta la operación con la excepción «UNIQUE constraint failed: trabajador.nss». Al no existir un bloque de manejo de excepciones en la ruta POST /capturar, este escenario interrumpe la petición en lugar de devolver un mensaje de error semántico al operador. Conviene señalar que la restricción cumplió su función protectora, impidiendo la corrupción de los datos; lo que falta es traducir esa condición en un aviso comprensible dentro de la interfaz.

El tercer problema corresponde al alcance del control de acceso. El prototipo implementa la trazabilidad de manera completa, puesto que la tabla usuario distingue los roles de administrador y captura mediante una restricción CHECK y toda operación queda estampada en la tabla bitacora con el identificador del usuario y su marca de tiempo. Sin embargo, no se implementó un mecanismo de autenticación: el usuario responsable se selecciona desde una lista desplegable del formulario y ninguna ruta verifica permisos antes de ejecutar la operación solicitada. El prototipo demuestra, por tanto, la auditoría y el no repudio a nivel de registro, pero todavía no el control de acceso propiamente dicho.

Finalmente, se identificaron cuatro elementos declarados en las entregas previas que permanecen fuera del alcance implementado en esta prueba de concepto y que constituyen deuda técnica reconocida: el movimiento de tipo 07, correspondiente a la modificación de salario, no está habilitado, ya que tanto la constante

## Página 16 del PDF

TIPOS_MOVIMIENTO_VALIDOS como la restricción CHECK de la tabla movimiento admiten exclusivamente los valores 08 y 02; el campo causa_baja se almacena como texto libre y no como la clave numérica del uno al nueve definida en la Entrega 1; el campo sdi se conserva como cadena de texto sin una validación que garantice el valor numérico con dos decimales; y la variable controlada cumplimiento_plazo, junto con el sensor de lectura del acuse del IMSS, no se encuentran programados, por lo que el lazo se cierra actualmente del lado de la validación pero no del lado de la retroalimentación externa. A ello se añade que la aplicación se ejecuta con la opción de depuración activa y una clave de sesión fija en el código, configuración propia de un entorno de laboratorio y no de un despliegue productivo.

Modificaciones realizadas Las modificaciones que se describen a continuación corresponden a decisiones de diseño adoptadas durante la construcción del prototipo y verificables en el estado actual del código fuente. Debe precisarse que el repositorio conserva el prototipo consolidado en un único registro de integración, por lo que el detalle cronológico de los ajustes intermedios no resulta recuperable del historial de versiones y se documenta aquí a partir de la evidencia observable en los módulos.

La modificación de mayor alcance afectó a la validación de fechas. Una comprobación basada únicamente en la expresión regular FECHA_REGEX resultaba insuficiente, ya que aceptaba cadenas correctamente formadas pero imposibles en el calendario. Por ello se incorporó en la función validar_fecha() una segunda comprobación que descompone la cadena en día, mes y año e intenta construir el objeto de fecha correspondiente, capturando la excepción cuando la combinación no existe y devolviendo un mensaje diferenciado. El caso C6 del conjunto de prueba se incorporó expresamente para cubrir este escenario. En la misma línea, la función validar_movimiento() se estructuró para acumular la totalidad de los errores detectados en una lista, en lugar de interrumpirse ante el primer fallo, con el fin de evitar que el operador deba corregir los datos en iteraciones sucesivas.

## Página 17 del PDF

Un segundo grupo de ajustes se orientó a reducir los errores de captura antes de que alcancen el controlador. En la ruta POST /capturar del módulo app.py se añadió la normalización de los datos recibidos del formulario, eliminando los espacios sobrantes de todos los campos y convirtiendo a mayúsculas los campos curp y rfc, de modo que una diferencia de formato atribuible al tecleo no provoque un rechazo indebido. Asimismo, se determinó que la bitácora registrara no solo las capturas exitosas, sino también los intentos rechazados, mediante una llamada a registrar_bitacora() con la acción «Intento de captura rechazado» y el detalle de los errores detectados; de este modo la auditoría conserva evidencia de la totalidad de la actividad del usuario y no únicamente de las operaciones que prosperaron.

El tercer grupo de modificaciones reforzó la consistencia de la información. Se incorporó el indicador exportado en la tabla movimiento junto con el estado 'Exportado', de manera que la consulta de exportación selecciona exclusivamente los movimientos válidos pendientes y los marca una vez procesados, impidiendo que un mismo movimiento se incluya dos veces en lotes distintos. Paralelamente, se trasladaron al esquema de la base de datos las restricciones CHECK sobre los campos tipo_movimiento, estado y rol, así como las restricciones UNIQUE sobre curp y nss, estableciendo una segunda barrera declarativa que protege la intigridadd incluso si un dato lograra sortear la validación de la capa de aplicación.

Conclusiones El aprendizaje central de esta prueba de concepto fue comprobar que un esquema de control de lazo cerrado, formulado inicialmente como un planteamiento teórico, admite una traducción directa a componentes de software. Cada bloque conceptual encontró su equivalente en un módulo concreto: el controlador lógico en las funciones de validación, el actuador en el módulo de exportación y la capa de persistencia en el esquema relacional.

Esta correspondencia no fue evidente al inicio del desarrollo, y entenderla permitió que cada elemento pudiera programarse y verificarse de forma aislada, sin depender de la interfaz gráfica.

## Página 18 del PDF

El segundo aprendizaje se obtuvo al trabajar con las expresiones regulares. Se confirmó que constituyen un filtro necesario, pero insuficiente por sí solo: una cadena puede ajustarse perfectamente a un patrón sintáctico y aun así carecer de sentido, como ocurrió con una fecha correctamente formada que correspondía al 31 de febrero. Fue necesario incorporar una segunda comprobación que evaluara el significado del dato y no únicamente su forma. De ello se desprende una distinción que resultó valiosa para el equipo: validar la estructura de un dato y validar su coherencia son dos operaciones diferentes, y un sistema confiable requiere ambas.

Un tercer aprendizaje surgió de las restricciones declarativas del gestor de base de datos. Al establecer llaves foráneas y restricciones de unicidad, se comprobó que el propio motor detiene inserciones inconsistentes con independencia de la lógica programada en la aplicación, lo que constituye una segunda barrera de protección. Sin embargo, también quedó claro que proteger la integridad de la información no equivale a comunicarla adecuadamente: una restricción que interrumpe una operación resguarda los datos, pero deja al operador sin una explicación comprensible. La calidad de un sistema depende tanto de lo que impide como de cómo lo informa.

Finalmente, el ejercicio permitió precisar dos conceptos que suelen confundirse. Registrar qué usuario ejecutó cada operación proporciona trazabilidad, pero no constituye por sí mismo un control de acceso, ya que este último exige verificar la identidad y los permisos antes de permitir la acción. De manera análoga, se observó que la gestión de escrituras simultáneas no recae en el código de la aplicación, sino en el motor de base de datos. En conjunto, el desarrollo demostró que sustituir un archivo de cálculo por un sistema estructurado no consiste únicamente en trasladar información, sino en incorporar las validaciones, las restricciones y los registros que el formato anterior no era capaz de sostener.
