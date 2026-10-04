---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 2 — TRL 2.pdf"
extraido: 2026-10-04
formato_original: pdf
nota: Transcripción automática del archivo entregado. NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 2 — TRL 2: alternativas, arquitectura y carta de inicio

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 2 — TRL 2.pdf` (carpeta del 7.° semestre de Pedro).
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

Índice Alternativas de solución............................................................................................................... 1 Comparación de alternativas....................................................................................................... 1 Alternativa 1. Macros en Excel...................................................................................................1 Alternativa 2. Aplicación de escritorio local................................................................................2 Alternativa 3. Sistema cliente-servidor.......................................................................................2 Selección de la solución...............................................................................................................2 Justificación de la alternativa seleccionada..............................................................................2 Arquitectura general del sistema................................................................................................ 3 Diagrama de bloques.................................................................................................................... 3 Identificación de entradas y salidas............................................................................................4 Variables de entrada...................................................................................................................5 Variables de salida..................................................................................................................... 5 Variables controladas y perturbaciones.....................................................................................5 Sensores requeridos.................................................................................................................... 6 Actuadores requeridos................................................................................................................. 6 Controlador requerido..................................................................................................................6 Sistemas de comunicación...........................................................................................................7 Software requerido....................................................................................................................... 7 Requerimientos técnicos............................................................................................................. 7 Estimación preliminar de costos................................................................................................. 8 Riesgos iniciales............................................................................................................................8 Carta de Inicio de la Empresa...................................................................................................... 9

## Página 3 del PDF

Alternativas de solución Para resolver la problemática del control de movimientos de afiliación y la falta de validación y trazabilidad operativa, se plantean tres posibles alternativas de automatización:

- Automatización mediante macros (VBA) en Excel. Consiste en mantener el uso de las hojas de cálculo actuales, pero programando scripts internos que automaticen la exportación de los datos a los formatos requeridos por el IMSS y que muestran cuadros de diálogo para advertir sobre errores de captura.

- Aplicación de escritorio con base de datos local. Desarrollo de un software ejecutable instalado en un ordenador del departamento administrativo. Este sistema utilizaría un motor de base de datos local, como SQLite o Microsoft Access, para organizar la información de los trabajadores mediante tablas y eliminar el uso de Excel.

- Sistema centralizado con arquitectura cliente-servidor y Sistema Gestor de Base de Datos (SGBD) relacional. Desarrollo de una aplicación web o de red local en la que los datos se alojan de forma centralizada en un Sistema Gestor de Base de Datos (SGBD) relacional. Los usuarios acceden simultáneamente a través de una interfaz gráfica (cliente) que incorpora control de acceso basado en roles, validación algorítmica desde la captura y módulos de exportación automática para la plataforma IDSE.

Comparación de alternativas Alternativa 1. Macros en Excel Es la opción más rápida y económica a corto plazo. Sin embargo, no soluciona el problema de concurrencia, ya que las hojas de cálculo no están diseñadas para procesos transaccionales en los que varios usuarios editan información simultáneamente. Además, carece de un sistema de registro nativo para auditar qué usuario realizó cada movimiento.

## Página 4 del PDF

Alternativa 2. Aplicación de escritorio local Resuelve el problema de la estructuración de los datos al utilizar tablas relacionales y evitar la redundancia. No obstante, al estar instalada en un solo equipo, se mantiene el cuello de botella operativo: solo una persona puede trabajar a la vez y se dificulta el acceso a la información por parte de los residentes de obra o supervisores.

Alternativa 3. Sistema cliente-servidor Es la alternativa que requiere un mayor esfuerzo de desarrollo e infraestructura inicial. A cambio, el gestor de la base de datos maneja la concurrencia mediante bloqueos de registros, lo que permite el trabajo simultáneo sin sobrescribir información. Esta opción facilita la creación de interfaces accesibles con identificadores semánticos que solucionan el problema de interpretación por colores y asegura la trazabilidad total mediante registros de marcas de tiempo y usuarios.

Selección de la solución Se selecciona la Alternativa 3.

Justificación de la alternativa seleccionada La selección de la alternativa 3 se justifica por su cumplimiento de los principios y tecnológicos necesarios para erradicar los retrasos del proceso actual: principio de normalización y concurrencia. Al emplear un SGBD relacional bajo las formas normales de Codd, se garantiza que la información de los empleados se encuentre en un solo lugar, lo que elimina las anomalías de actualización. La arquitectura cliente-servidor solucionará la problemática del control, ya que permitirá que varios usuarios trabajen al mismo tiempo sin afectar a la integridad de los datos.

- Validación y automatización. El sistema aplicará validación algorítmica y expresiones regulares desde la captura para impedir la introducción de información errónea, como errores en los 18 caracteres de la CURP o los 11 dígitos del NSS. Además, aplicará la abstracción de datos para mapear y exportar automáticamente la información a los formatos de texto plano requeridos por el sistema IDSE.

## Página 5 del PDF

- Auditoría y control de acceso. A diferencia de las hojas de cálculo, este sistema implementará un control de acceso basado en roles y registros (logs), que asegurará el principio de no repudio al estampar cada movimiento con una marca de tiempo (timestamp) y el ID del usuario responsable.

- Accesibilidad y usabilidad. La interfaz gráfica (UI) se diseñará utilizando identificadores semánticos en lugar de depender exclusivamente de la percepción del color. Esto mitigará los errores operativos documentados y cumplirá con las pautas de accesibilidad estandarizadas.

Arquitectura general del sistema El sistema está estructurado bajo una arquitectura cliente-servidor, en la que los datos residen de forma centralizada y los usuarios acceden a través de una interfaz gráfica (cliente). Esta configuración garantiza que el gestor de la base de datos maneje la concurrencia mediante bloqueos de registros, lo que permite que varios usuarios administrativos trabajen de manera simultánea sin sobrescribir la información del otro.

A nivel de diseño, la interfaz (cliente) integra principios de interacción humano-computadora para asegurar la accesibilidad, utilizando indicadores de texto semánticos y estados claros en lugar de depender exclusivamente de códigos de color para transmitir el estado del trámite. Por su parte, el servidor (backend) aloja el motor de validación algorítmica y aplica la abstracción de datos para traducir la información visual del usuario a las variables exactas exigidas por el sistema IDSE. Finalmente, la capa de persistencia se sustenta en una base de datos relacional normalizada que centraliza los datos del patrón, los trabajadores y el historial de movimientos, eliminando la redundancia y permitiendo el registro de auditoría de cada usuario.

Diagrama de bloques Al basarse en un enfoque de sistema de lazo cerrado, el flujo lógico compara continuamente el estado de los trámites con los plazos planificados para detectar

## Página 6 del PDF

desviaciones. El diagrama de bloques lógico se compone de los siguientes elementos adaptados al software:

- Referencia (entrada). Solicitud de alta o baja con la información del trabajador, que debe procesarse en el plazo legal de cinco días hábiles.

- Controlador lógico. Algoritmos de validación que verifican la longitud y el formato de los datos mediante expresiones regulares (Regex) antes de permitir el registro en el sistema.

- Actuador lógico (salida de control). Módulo de exportación automática que estructura y genera archivos de texto plano compatibles con la plataforma IDSE.

- Proceso. Envío y procesamiento del movimiento afiliatorio en la plataforma del IMSS.

- Perturbaciones (internas/externas). Errores de captura humana, retrasos en la notificación por parte de los residentes de obra o caídas temporales del portal del IMSS.

- Sensor (retroalimentación). Recepción y lectura de la cadena de respuesta del IMSS, que actualiza automáticamente el estado del trabajador en la base de datos.

Identificación de entradas y salidas Siguiendo las normas metodológicas de programación establecidas para este desarrollo, todas las variables del sistema se han declarado utilizando la sintaxis snake_case.

## Página 7 del PDF

Variables de entrada

- nss_trabajador. Número de seguridad social de 11 dígitos.

- curp_trabajador. Clave Única de Registro de Población de 18 caracteres.

- rfc_trabajador. Registro Federal de Contribuyentes con homoclave de 13 caracteres.

- salario_diario_integrado. Salario Base de Cotización, valor numérico con dos decimales.

- fecha_movimiento. Fecha de ingreso o baja en formato DDMMAAAA.

- tipo_movimiento. Clave numérica.

- causa_baja. Clave numérica del 1 al 9.

Variables de salida

- lote_exportacion. Archivo de texto estructurado generado por el sistema para carga masiva.

- folio_envio. Identificador único generado internamente para rastrear el trámite.

- acuse_notarial. Cadena de respuesta de aceptación emitida por el IMSS.

- codigo_error. Variable que captura los errores.

Variables controladas y perturbaciones

- estado_afiliacion (controlada). Estatus operativo y legal del empleado frente al seguro social.

- cumplimiento_plazo (controlada). Verificación de que el trámite ocurra dentro de los 5 días hábiles.

- errores_captura (perturbación interna). Datos introducidos incorrectamente antes de la validación algorítmica.

## Página 8 del PDF

- retraso_informacion (perturbación interna). Demora de los contratistas al reportar la entrada o salida de personal de las cuadrillas.

Sensores requeridos En un entorno de software con un esquema de lazo cerrado, los sensores son los módulos de lectura e interpretación de datos. Concretamente, se trata de scripts que analizan la cadena de texto de la respuesta del servidor del IMSS, Estos sensores detectan el resultado del trámite, extraen la variable codigo_error y actualizan automáticamente la variable controlada del trabajador en la base de datos. Esto elimina la necesidad de que una persona verifique manualmente los estados.

Actuadores requeridos Los actuadores son las rutinas de ejecución que modifican el estado del sistema. El actuador principal es el módulo de abstracción y exportación de datos, que toma la información validada de las tablas relacionales y la procesa algorítmicamente en archivos de texto plano estructurados según las normativas exactas que exige el sistema IDSE para la carga en masa. Un actuador secundario es el sistema interno de la interfaz, que genera alertas semánticas para los usuarios cuando un movimiento está a punto de rebasar el límite legal de cinco días hábiles.

Controlador requerido Los actuadores son las rutinas de ejecución que modifican el estado del sistema. El actuador principal es el módulo de abstracción y exportación de datos, que toma la información validada de las tablas relacionales y la procesa algorítmicamente en archivos de texto plano estructurados según las normativas que exige el sistema IDSE para la carga en masa. Un actuador secundario es el sistema interno de la interfaz, que genera alertas semánticas para los usuarios cuando un movimiento está a punto de superar el límite legal de cinco días hábiles.

## Página 9 del PDF

Sistemas de comunicación La infraestructura requiere una arquitectura de red en dos niveles. A nivel interno, utiliza una comunicación cliente-servidor mediante los protocolos HTTP/HTTPS a través de la red local (LAN) o Internet, lo que permite la concurrencia de múltiples usuarios hacia la base de datos. A nivel externo, es necesaria una conexión ininterrumpida y segura con los servidores gubernamentales (portal IDSE) para transmitir los lotes de afiliación.

Software requerido

- Backend. Entorno de ejecución y framework para programar reglas de decisión lógica y aritmética directa.

- Base de datos. Un sistema gestor de bases de datos (SGBD) relacional para aplicar el principio de normalización y estructurar la información sin redundancias.

- Frontend. Tecnologías web que aplican principios rigurosos de interacción entre humanos y ordenadores. La interfaz de usuario (UI) integrará identificadores semánticos en texto cumpliendo con las normas de accesibilidad WCAG.

Requerimientos técnicos

- Servidor. Instancia de alojamiento como un servidor físico local en las oficinas de Monterrey o en un entorno en la nube, como AWS, con capacidad de procesamiento para operar el SGBD de forma centralizada y gestionar la concurrencia.

- Equipos cliente. Equipos de escritorio estándar con acceso a internet de banda ancha estable y un navegador web actualizado, sin necesidad de hardware especializado.

- Autenticación patronal. Archivos vigentes de la firma electrónica y del registro patronal de la empresa para habilitar la autenticación del envío ante el portal IDSE.

## Página 10 del PDF

Estimación preliminar de costos

- Ingeniería y desarrollo. La inversión principal se destina a las horas de trabajo para la normalización de la base de datos, el diseño de la interfaz accesible y la programación de las expresiones regulares y rutinas de exportación. Con un total aproximado de 150 a 180 horas de trabajo técnico, este apartado tiene un coste estimado de entre 3,000 y 4,000 MXN como pago único por la creación del sistema.

- Infraestructura. Coste operativo mensual por el alojamiento en la nube de la base de datos y el servidor backend. Este servicio se estima en un rango asequible de 400 a 1,200 MXN mensuales, que puede variar ligeramente según el tráfico de peticiones y el volumen de trabajadores registrados.

- Licenciamiento. Se implementarán herramientas de código abierto para el lenguaje de programación y el SGBD relacional, lo que permitirá eliminar por completo los gastos en licencias propietarias de software. Este apartado se mantiene en 0 MXN.

Riesgos iniciales

- Riesgos técnicos externos. Modificaciones imprevistas en la estructura de recepción de datos por parte de la plataforma del IMSS o caídas temporales de su servidor, lo que supone una perturbación externa incontrolable que puede retrasar los acuses.

- Migración de datos. Posible pérdida de datos o corrupción de la información histórica de los trabajadores al transcribir los registros desde los archivos de cálculo manuales al nuevo SGBD relacional.

- Operatividad humana. Resistencia al cambio tecnológico por parte del personal administrativo, que deberá abandonar las hojas de cálculo para adaptarse a un flujo de trabajo centralizado.

## Página 11 del PDF

Carta de Inicio de la Empresa

## Página 12 del PDF



## Página 13 del PDF


