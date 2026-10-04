---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 1 — TRL 1.pdf"
extraido: 2026-10-04
formato_original: pdf
nota: Transcripción automática del archivo entregado. NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 1 — TRL 1: problemática y variables

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 1 — TRL 1.pdf` (carpeta del 7.° semestre de Pedro).
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

Índice Descripción de la empresa................................................................................................................. 1 Descripción del área o proceso involucrado........................................................................................1 Descripción detallada de la problemática........................................................................................... 2 Evidencias de las problemáticas......................................................................................................... 3 Consecuencias actuales......................................................................................................................4 Variables involucradas....................................................................................................................... 4 Datos del patrón.......................................................................................................................... 4 Datos de identificación del trabajador.......................................................................................... 4 Variables para Movimiento de Alta / Reingreso (Tipo 08)..............................................................4 Tipo de trabajador..................................................................................................................4 Tipo de salario....................................................................................................................... 5 Tipo de jornada......................................................................................................................5 Variables para Movimiento de Baja (Tipo 02)................................................................................ 5 Causa de la baja..................................................................................................................... 5 Variables de Control y Respuesta del Sistema...............................................................................6 Requerimientos de automatización....................................................................................................6 Revisión bibliográfica y tecnológica....................................................................................................6 Principios científicos y tecnológicos relacionados...............................................................................8 Justificación del proyecto...................................................................................................................9 Objetivo general.............................................................................................................................. 10 Objetivos específicos....................................................................................................................... 10 Bibliografía.......................................................................................................................................11

## Página 3 del PDF

Descripción de la empresa Es una empresa contratista dedicada al desarrollo de instalaciones eléctricas para otras empresas, con operación en el área metropolitana de Monterrey. Su modelo de trabajo es por proyecto: ejecuta la obra eléctrica bajo contrato y conforma cuadrillas que se arman y se disuelven según la carga de cada obra, por lo que el número de trabajadores varía de manera constante a lo largo del año.

Su cliente principal es Grupo Multimedios, para el cual realiza de forma recurrente los trabajos eléctricos de sus instalaciones. Además de ese cliente, la empresa maneja una cartera diversificada de proyectos, entre los que destacan la instalación eléctrica del Bolerama La Pastora, la parte eléctrica de diversas colonias del área metropolitana y la instalación eléctrica del Hospital Sierra Madre. Actualmente se encuentra pendiente de formalizar un contrato con BBVA (anteriormente Bancomer) para la habilitación eléctrica de una nueva sucursal.

Descripción del área o proceso involucrado La empresa ya cuenta con sistemas propios para el cálculo de material y para la creación de planos eléctricos, los cuales operan de forma confiable. El área donde más batallan es la de seguro médico, es decir, la gestión de altas, bajas y modificaciones salariales de los trabajadores ante el IMSS, ya que todo el proceso se realiza a mano sobre archivos de Excel. El flujo actual consiste en que el residente de obra avisa de manera informal el ingreso o la salida de un trabajador, el responsable administrativo captura los datos en el archivo, los vuelve a escribir en el portal IDSE para enviar el movimiento y guarda el acuse por separado, sin ninguna conexión con el registro original.

El punto crítico de este proceso es que el estatus de cada trabajador se indica únicamente con colores en las celdas, sin ningún texto que lo acompañe. La persona que estaba encargada del área es daltónica, por lo que no podía distinguir de manera confiable esos estados y se generaban muchos errores. A esto se suma que el archivo no valida los datos que se capturan, no registra quién hizo cada movimiento y no avisa

## Página 4 del PDF

cuando un trámite está por vencer su plazo. Por estas razones, esta es el área sobre la que se trabajará en el proyecto.

Descripción detallada de la problemática No se tiene un buen control de los empleados que trabajan en la empresa ni del estatus de su seguro, el cual debe permanecer dado de alta durante todo el tiempo que laboren ahí. Esto es indispensable para la seguridad de los trabajadores; sin embargo, resulta muy difícil de sostener cuando se trabaja con tantos trabajadores a la vez.

La dificultad aumenta por el volumen y el movimiento constante del personal. Cada trabajador que entra o sale de una obra genera al menos un movimiento afiliatorio que debe capturarse, enviarse y comprobarse dentro del plazo legal, y ese ciclo se multiplica por el número de cuadrillas activas y por la frecuencia con la que el personal se reasigna entre proyectos. Cuando varias obras avanzan al mismo tiempo, la cantidad de movimientos supera la capacidad de seguimiento manual de una sola persona, por lo que el control deja de ser preventivo y se vuelve reactivo: los movimientos se atienden conforme se recuerdan o conforme el propio IMSS los reclama, no conforme ocurren. El archivo de control tampoco distingue entre un trabajador que salió de una obra pero fue reasignado a otra y uno que realmente terminó su relación laboral con la empresa, lo que provoca al mismo tiempo bajas indebidas y altas que nunca se dieron de baja.

Esto coloca a la empresa en una contradicción operativa. El aseguramiento del personal es indispensable para su seguridad, ya que la actividad implica riesgo eléctrico, trabajo en altura y maniobras en obra, pero el mecanismo que debería garantizarlo es el más frágil de toda la operación: mientras el cálculo de material y la generación de planos cuentan con herramientas propias y confiables, la única función de la que depende la cobertura médica y de riesgos de trabajo del personal se sostiene sobre un archivo manual, sin validaciones y operado por una sola persona.

## Página 5 del PDF

Evidencias de las problemáticas Figura 1. Archivo de control de movimientos afiliatorios utilizado actualmente por la empresa.

Como evidencia principal se presenta el archivo de control de movimientos afiliatorios que utiliza actualmente la empresa, correspondiente al mes de julio de 2026. En él se observa que el estatus de cada trabajador se comunica únicamente mediante el color de fondo de la fila, sin ninguna etiqueta de texto que lo acompañe: los registros marcados en rojo corresponden a movimientos con alguna incidencia, mientras que los marcados en verde corresponden a movimientos ya procesados. Esto confirma que la interpretación del archivo depende por completo de la percepción cromática del operador, lo cual explica los errores presentados por la persona daltónica que estaba a cargo del área. Se aprecia también que el archivo concentra en una sola hoja los datos de identificación del trabajador, el proyecto asignado, las fechas de alta y baja y el estatus del movimiento, sin validaciones de captura ni ningún campo que registre qué usuario realizó cada operación.

## Página 6 del PDF

Consecuencias actuales Se ha estado gastando dinero de más por tener gente de alta en el seguro social que no deberían de estar dado de alta ya que no están trabajando o a veces por falta de comunicación se tarda en dar de alta a un trabajador lo que ha generado multas o problemas.

Variables involucradas Datos del patrón

- Registro patronal. Clave de 11 caracteres alfanuméricos asignada por el IMSS.

- RFC del patrón. Registro Federal de Contribuyentes (12 o 13 caracteres).

- Firma electrónica. Archivo y contraseña para autenticar el envío ante el IDSE.

Datos de identificación del trabajador

- Número de seguridad social. 11 dígitos numéricos.

- CURP. Clave Única de Registro de Población (18 caracteres).

- RFC del Trabajador. Con homoclave (13 caracteres).

- Nombre completo. Nombre(s), primer apellido y segundo apellido (separados).

Variables para Movimiento de Alta / Reingreso (Tipo 08)

- Fecha de movimiento / ingreso. Formato DDMMAAAA.

- Salario Diario Integrado (SDI / SBC). Salario Base de Cotización (numérico con 2 decimales).

Tipo de trabajador

- 1 = Permanente

- 2 = Eventual ciudad

- 3 = Eventual construcción

- 4 = Eventual del campo

## Página 7 del PDF

Tipo de salario

- 0 = Fijo

- 1 = Variable

- 2 = Mixto Tipo de jornada

- 0 = Normal / Completa

- 1 a 6 = Jornadas reducidas (horas/días específicos)

- Número de crédito INFONAVIT (opcional). 10 dígitos (si aplica retención desde el ingreso).

- Clave de unidad de medicina familiar. Asignada según el código postal del trabajador.

Variables para Movimiento de Baja (Tipo 02)

- Fecha de baja. Formato DDMMAAAA (debe ser posterior o igual al alta y dentro del plazo de 5 días hábiles).

Causa de la baja

- 1 = Término de contrato

- 2 = Separación voluntaria (renuncia)

- 3 = Abandono de empleo

- 4 = Defunción

- 5 = Clausura

- 6 = Otras

- 7 = Ausentismo

- 8 = Rescisión de contrato

- 9 = Jubilación / Pensión

## Página 8 del PDF

Variables de Control y Respuesta del Sistema

- Tipo de movimiento. 08 (Alta/Reingreso), 02 (Baja), 07 (Modificación de Salario).

- Folio de Envío / Lote. Identificador único generado por el sistema interno.

- Acuse Notarial / Número de Folio IDSE. Cadena de respuesta del IMSS para validar estatus (Aceptado / Rechazado).

- Código de error. Variable para capturar incidencias, por ejemplo: NSS no coincide con CURP, patrón no vigente.

Requerimientos de automatización Poder generar tablas con la información necesaria para poder dar de alta y baja de manera más sencilla y que ya estén programada por lo que solo se necesite copiar y pegar información y que varias personas puedan mover a la base de datos y saber quien es la persona que hice el movimiento para poder auditar la aplicación.

Revisión bibliográfica y tecnológica.

Para desarrollar este proyecto, se revisan las tecnologías y metodologías actuales orientadas a la gestión de recursos humanos y la automatización de procesos administrativos, y se analizan las limitaciones de las herramientas actuales.

- Limitaciones de las hojas de cálculo en procesos simultáneos. Aunque Microsoft Excel es una herramienta versátil, la documentación sobre gestión de bases de datos indica que las hojas de cálculo no son adecuadas para procesos transaccionales en los que múltiples usuarios deben introducir, editar y verificar información simultáneamente. Carecen de un sistema sólido de registros nativos que permita la trazabilidad de los usuarios, lo que incrementa el riesgo de manipulación indebida o pérdida de datos.

## Página 9 del PDF

- Accesibilidad en el diseño de interfaces de usuario (UI). El uso de códigos de color como único método para transmitir información crítica (estatus de un trabajador) viola las pautas de accesibilidad estandarizadas, como las WCAG (Web Content Accessibility Guidelines). La literatura sobre ergonomía informática y experiencia de usuario (UX) establece que los sistemas deben usar identificadores semánticos en lugar de depender exclusivamente de la percepción del color, mitigando así los errores derivados del daltonismo u otras discapacidades visuales.

- Tecnologías de bases de datos relacionales (SGBD). Para el control de los datos del patrón, trabajadores y movimientos, la tecnología estándar requerida es un sistema gestor de base de datos relacional. Estos sistemas permiten estructurar la información en tablas interconectadas, evitar la redundancia de datos (por ejemplo, un trabajador registrado múltiples veces) y realizar consultas rápidas para generar informes.

- Integración con sistemas gubernamentales (IDSE/SUA). El Instituto Mexicano del Seguro Social (IMSS) utiliza la plataforma IDSE para recibir movimientos afiliatorios. Esta plataforma permite la carga masiva de información a través de archivos planos. El sistema que se va a desarrollar se basa en la tecnología de exportación de datos estructurados, que toma los registros de la base de datos y los transforma automáticamente en las cadenas de texto exactas que los sistemas de validación del IMSS requieren.

## Página 10 del PDF

Principios científicos y tecnológicos relacionados.

El proyecto se sustenta en los siguientes principios de las ciencias de la computación y la ingeniería de software:

- Principio de normalización de bases de datos. Se aplicarán las formas normales de Codd para estructurar la base de datos. De este modo, se garantiza que la información de los empleados se encuentre en un solo lugar y se relacione de manera lógica con los registros de sus movimientos. De este modo, se eliminan las anomalías de actualización y se asegura la integridad referencial.

- Validación algorítmica y teoría de la información. Para evitar el rechazo de los movimientos por parte del IMSS, el sistema aplicará principios de validación de datos desde la captura. Esto incluye el uso de expresiones regulares (Regex) para garantizar que la CURP tenga exactamente 18 caracteres alfanuméricos válidos, que el NSS tenga 11 dígitos y que las fechas tengan el formato DDMMAAAA. Esto actúa como un filtro algorítmico que impide que información errónea entre en el sistema.

- Arquitectura cliente-servidor y concurrencia. El sistema funcionará bajo el principio de que los datos residen de forma centralizada, mientras que los usuarios acceden a ellos a través de una interfaz (cliente). Esto soluciona la problemática del control, ya que el gestor de la base de datos maneja la concurrencia (bloqueos de registros), lo que permite que varios usuarios trabajen a la vez sin sobrescribir la información del otro.

- Control de acceso basado en roles y trazabilidad. Un principio fundamental de la seguridad de la información es el no repudio. Mediante la implementación de un sistema de autenticación de usuarios y registros (logs), cada transacción quedará registrada con una marca de tiempo (timestamp) y el ID del usuario responsable.

Esto cumple con el requisito de auditoría de la aplicación.

## Página 11 del PDF

- Abstracción de datos y generación automática de informes. Principio tecnológico mediante el cual la interfaz gráfica muestra al usuario información amigable y comprensible. No obstante, en el momento de la exportación, el sistema mapea y traduce algorítmicamente esta información a las variables de máquina exigidas por el sistema IDSE.

Justificación del proyecto El proceso actual genera un costo directo para la empresa en dos frentes simultáneos.

Por un lado, el tiempo administrativo que se invierte en capturar, revisar y volver a capturar la misma información en el portal del IMSS, tiempo que se desvía de actividades de mayor valor. Por otro, el error humano derivado de un proceso manual sin validaciones, que se traduce en movimientos rechazados, cuotas pagadas por trabajadores que ya no laboran en la empresa y multas por presentar avisos fuera del plazo legal. A esto se suma un riesgo de mayor severidad: si un trabajador que no fue dado de alta a tiempo sufre un accidente, la empresa asume el costo total de las prestaciones médicas otorgadas.

Automatizar este proceso es viable porque reúne las condiciones ideales para ello: se trata de una tarea repetitiva, de alto volumen, gobernada por reglas explícitas y verificables, con formatos de salida estandarizados por la autoridad y con plazos legales que pueden calcularse de manera exacta. No existe en el proceso ningún componente que exija juicio experto y que impida sistematizarlo. Lograrlo generaría una mejora medible en los tiempos de respuesta y un ahorro directo de dinero dentro de la empresa, además de eliminar la dependencia de una sola persona y permitir que cualquier miembro del personal administrativo pueda operar el proceso.

## Página 12 del PDF

Objetivo general Desarrollar e implementar un sistema centralizado para la gestión y automatización de movimientos afiliatorios (altas y bajas ante el IMSS/IDSE), con control de acceso y registro de auditoría, para eliminar los errores operativos manuales y optimizar los costos derivados de cuotas y multas patronales.

Objetivos específicos

- Estandarizar la captura de datos. Diseñar formularios y estructuras de datos con validaciones automáticas para la información requerida por el IMSS (NSS, CURP, RFC, SDI, fechas y catálogos de movimientos), eliminando el uso de formatos manuales basados en códigos de color.

- Automatizar la generación de layouts/tabla. Programar la exportación automática de lotes de información con el formato y estructura requeridos para procesar altas (Tipo 08) y bajas (Tipo 02) sin necesidad de recaptura manual.

- Implementar control de acceso y auditoría de usuarios. Desarrollar un módulo multiusuario con autenticación y registro de bitácora (logs) que identifique qué usuario realiza, modifica o procesa cada movimiento en la base de datos.

- Reducir tiempos de procesamiento e incidencias. Disminuir el tiempo de respuesta en el trámite de movimientos afiliatorios para asegurar el cumplimiento dentro del plazo legal de 5 días hábiles, evitando multas por extemporaneidad y pagos innecesarios de cuotas por bajas no reportadas.

## Página 13 del PDF

Bibliografía

1. Amazon Web Services [AWS]. (s.f.). ¿Qué es el control de acceso basado en roles (RBAC)?. Amazon Web Services. https://aws.amazon.com/es/what-is/rbac/

2. Instituto Mexicano del Seguro Social [IMSS]. (s.f.). IMSS desde su Empresa (IDSE). Gobierno de México. http://www.imss.gob.mx/patrones/idse

3. Microsoft. (2024, 23 de mayo). Descripción de los aspectos básicos de la normalización de la base de datos.

Microsoft Learn. https://learn.microsoft.com/es-es/office/troubleshoot/access/database-normalization -description

4. Mozilla. (2023).

Expresiones regulares.

MDN Web Docs. https://developer.mozilla.org/es/docs/Web/JavaScript/Guide/Regular_expressions

5. Oracle. (s.f.). ¿Qué es una base de datos?.

Oracle México. https://www.oracle.com/mx/database/what-is-database/

6. World Wide Web Consortium [W3C]. (2018). Web Content Accessibility Guidelines (WCAG) 2.1. W3C Recommendation. https://www.w3.org/TR/WCAG21/
