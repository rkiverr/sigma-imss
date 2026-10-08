---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 6 — TRL 6.docx"
extraido: 2026-10-07
formato_original: docx
nota: Transcripción automática del archivo (versión 2, con las correcciones de la rama trl6/correcciones). NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 6 — TRL 6: integración y demostración del sistema

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 6 — TRL 6.docx` (carpeta del 7.° semestre de Pedro),
> versión 2 del 2026-10-07: 33 páginas con 13 figuras y 21 tablas. Las figuras no se transcriben; solo su leyenda.
> Se omiten la portada y el índice.

## Integración y demostración del sistema

Este entregable documenta la integración y la demostración de Sigma, el sistema para la automatización de altas y bajas de trabajadores ante el Instituto Mexicano del Seguro Social (IMSS) desarrollado para Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V. En el nivel TRL 6 ya no se validan componentes por separado, como en el TRL 5, sino que se demuestra el modelo o prototipo del sistema completo, con sus componentes principales integrados, en un ambiente relevante (Mankins, 1995).

La demostración se hizo el 7 de octubre de 2026 en dos tiempos. Primero se instaló desde cero y se operó por la red local la versión de la rama principal del repositorio del proyecto (github.com/rkiverr/sigma-imss, commit 7f43596), que reúne lo construido en los entregables anteriores. Esa primera demostración cumplió 7 de sus 9 criterios de aceptación y reveló 18 problemas; los más graves fueron que el lote no seguía la estructura oficial del IMSS y que el sistema no pedía iniciar sesión. Los problemas de código se corrigieron en la rama trl6/correcciones y la versión corregida se volvió a instalar desde cero y a someter a todas las pruebas. Las secciones de este informe describen la versión corregida; la primera demostración se usa como punto de comparación.

Se usaron datos sintéticos de trabajadores, con CURP, RFC y NSS coherentes y con dígito verificador válido, porque la CURP, el NSS y el salario son datos personales protegidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares. El equipo de pruebas hizo de PC servidor y la PC de captura se emuló entrando al sistema por la dirección IP de la red local, igual que en el Entregable 5. Por eso, la operación con datos reales y varios equipos físicos en la oficina queda para la prueba piloto. Las secciones siguen el orden de la rúbrica del entregable.

### Integración completa

Integrar el sistema significó, primero, reunir en una sola versión todo lo validado. Al cerrar el Entregable 5, los ajustes del TRL 5 vivían en la rama trl5/ambiente-relevante y la rama principal seguía con el código del Entregable 4. Se integraron a la rama principal, se corrigió el calendario de días inhábiles y el código se reorganizó en el paquete sigma/, separado de las pruebas. Después, para cerrar las brechas de la primera demostración, se agregaron dos componentes, usuarios.py (inicio de sesión y roles) y respaldo.py (respaldo automático), y se reescribió el actuador exportar_idse.py con la estructura oficial del IMSS. La Figura 1 muestra el sistema integrado y la Tabla 1, el papel de cada componente y el entregable en que se originó.

> Figura 1. Sistema Sigma integrado (versión corregida): componentes en la PC servidor, lazo interno de corrección con el capturista y lazo externo con el IMSS.

> Tabla 1. Componentes integrados de Sigma y su función en el lazo de control.

| Componente | Archivos | Función en el lazo de control | Origen |
|---|---|---|---|
| Interfaz web | sigma/templates/, sigma/static/ | Sensores virtuales: campos, máscaras y validación en vivo; pantalla de inicio de sesión | E3; rediseño E4; E5 y E6 |
| Servidor de producción | servidor.py | Mantiene el sistema en servicio en la red local (waitress, 8 hilos) y respalda la base al arrancar y cada 24 horas | E5; E6 |
| Controlador HTTP | sigma/app.py | Exige sesión, recibe cada captura, aplica las reglas de flujo y de historial y decide la respuesta (guardar, rechazar con 422 o prohibir con 403) | E3; E4; E5; E6 |
| Sesión y roles | sigma/usuarios.py | Comprueba la identidad y el rol de quien opera; bloquea la cuenta tras 5 intentos fallidos | E6 |
| Comparador | sigma/validaciones.py | Compara cada dato con las reglas del IMSS y devuelve errores (bloquean) y avisos (no bloquean) | E3; E5; E6 |
| Plazo legal | sigma/plazo.py | Referencia temporal: cinco días hábiles del art. 15 de la LSS, sin los descansos del art. 74 de la LFT | E5; E6 |
| Persistencia y bitácora | sigma/database.py | Memoria del sistema (6 tablas), registro de auditoría, índice único contra duplicados y migraciones de datos | E3; E4; E5; E6 |
| Actuador | sigma/exportar_idse.py | Genera un archivo por tipo de movimiento, con registros de 168 posiciones, para la plataforma IDSE | E3; E6 |
| Respaldo | sigma/respaldo.py | Copia verificada de la base, rotación y restauración | E6 |
| Pruebas de regresión | pruebas/ | Arneses de prueba de concepto (E3), de ambiente relevante (E5) y de integración (E6) | E3; E5; E6 |

El lazo interno queda integrado por completo dentro de Sigma: la validación en vivo y la respuesta del servidor devuelven al capturista los errores de cada campo en milisegundos, y el movimiento solo se guarda cuando la desviación respecto de las reglas es cero. Con el inicio de sesión, además, cada corrección queda atribuida a quien la hizo, porque el usuario de la bitácora sale de la sesión y ya no de una lista. El lazo externo, en cambio, depende del IMSS: el acuse o el rechazo llega días después en la plataforma IDSE y hoy lo revisa una persona. Su integración automática requiere operar con el registro patronal real y queda para el piloto.

La integración se comprobó sobre la misma versión instalada con tres arneses de prueba: el del Entregable 3 (8 de 8 casos correctos), el del Entregable 5 (10 de 10 criterios cumplidos) y uno nuevo de esta fase, pruebas/prueba_integracion.py, que recorre el escenario de demostración (23 de 23 casos correctos) y revisa el lote, la seguridad, el respaldo y la comunicación. Sus resultados se detallan en las secciones de pruebas.

### Instalación o montaje

Por tratarse de software, el montaje corresponde a la instalación del sistema en los equipos de la oficina: no hay estructura, gabinete ni cableado propio que armar. La primera decisión de instalación es dónde se hospeda el sistema. Se eligió el hospedaje local (en sitio): una PC de la oficina funciona como servidor y las demás entran por la red local. La Tabla 2 compara esta opción con el hospedaje en la nube.

> Tabla 2. Comparación entre hospedaje local y hospedaje en la nube para Sigma.

| Criterio | Local en la oficina (elegido) | En la nube (hosting) |
|---|---|---|
| Datos personales | Solo los alcanza quien está en la red de la oficina y tiene usuario y contraseña | Expuestos a internet; exigiría primero cifrar el tráfico (problema P-11) |
| Coherencia con el diseño | Es la arquitectura cliente-servidor en red local de la Alternativa 3 (Entregable 2) y la que se probó en los entregables 4 y 5 | Cambia la arquitectura ya evaluada |
| Dependencia de internet | Se captura sin internet; solo la carga del lote en el IDSE lo requiere | Sin internet no se puede capturar |
| Costo | Usa una PC existente; sin pago mensual | Renta mensual no prevista en la estimación de costos del Entregable 2 |
| Respaldo y mantenimiento | Respaldo automático incluido; la empresa debe guardarlo en otro disco | El proveedor ofrece respaldos administrados |
| Acceso desde las obras | No: solo dentro de la oficina | Sí, desde cualquier lugar |

El hospedaje en la nube tendría sentido si la empresa abre otra sede o quiere capturar desde las obras, pero solo después de cifrar el tráfico. La Figura 2 muestra qué se instala en cada equipo: las PC de captura no requieren instalar nada, porque usan el navegador; todo el software vive en la PC servidor, a la que conviene asignar una dirección IP fija en el router.

> Figura 2. Despliegue de Sigma en la oficina: qué se instala en cada equipo y por dónde viaja la información.

Los requisitos de la PC servidor son Windows 10 u 11, Python 3 (la demostración usó Python 3.14.3), Git y una conexión a la red local; las PC de captura solo necesitan Chrome o Edge actualizados. Como la rama trl6/correcciones todavía no se integra a la rama principal, la instalación limpia se hizo clonando esa rama del repositorio del equipo en una carpeta vacía; en la oficina se usará la rama principal cuando se integre. La Tabla 3 resume el procedimiento y la Figura 3 reproduce la terminal.

> Tabla 3. Procedimiento de instalación en la PC servidor, con el tiempo medido en la demostración.

| Paso | Acción | Comando (PowerShell) | Tiempo |
|---|---|---|---|
| 1 | Descargar el sistema | git clone -b trl6/correcciones <repositorio> | 0.6 s |
| 2 | Crear el entorno de Python | python -m venv .venv | 5.1 s |
| 3 | Instalar las dependencias (incluye el controlador de PostgreSQL) | .venv\Scripts\python -m pip install -r requirements.txt | 4.1 s |
| 4 | Fijar las contraseñas de los usuarios | .venv\Scripts\python -m sigma.usuarios contrasena admin.rrhh (y captura.obra1) | 1.8 s y 1.5 s |
| 5 | Configurar (Tabla 5) | $env:SECRET_KEY = '<clave fija>'; $env:SIGMA_RESPALDOS = '<otro disco>'; $env:SIGMA_DB = 'sqlite' | — |
| 6 | Arrancar el servidor de producción | .venv\Scripts\python servidor.py | 1.8 s hasta responder |
| 7 | Permitir el puerto en el firewall de Windows (solo red privada) | New-NetFirewallRule -DisplayName Sigma -Direction Inbound -Protocol TCP -LocalPort 5050 -Profile Private -Action Allow | Se describe; no se aplicó en el equipo de pruebas |
| 8 | Entrar desde cada PC de captura | http://<IP del servidor>:5050 e iniciar sesión | — |

La instalación completa tomó 16.9 s, 2.7 s más que en la primera demostración (14.2 s), por el paso de las contraseñas. Cada comando muestra además que no hay servidor PostgreSQL: con su controlador ya instalado, Sigma lo busca durante 1 s y continúa con SQLite. Mientras no se instale PostgreSQL, fijar SIGMA_DB=sqlite evita esa espera. La instalación se hizo con el commit aee7bc0; el último commit de la rama, 8914883, solo cambia la redacción del aviso de exportación y se aplicó con git pull antes del escenario de demostración. Para que el sistema arranque solo al encender el equipo, se recomienda una tarea del Programador de tareas de Windows que ejecute el paso 6 al iniciar sesión. La Tabla 4 resume la verificación posterior.

> Figura 3. Instalación limpia de la versión corregida: dependencias con psycopg2, contraseñas de los usuarios, respaldo al arrancar y servicio por la IP de la red local a los 16.9 s de iniciar.

> Tabla 4. Verificación posterior a la instalación.

| Verificación | Resultado | Estado |
|---|---|---|
| El servidor arranca, respalda la base y anuncia el motor de datos | Respaldo al arrancar en respaldos/; waitress con 8 hilos; motor SQLite | Cumple |
| Responde desde la red local | http://192.168.0.8:5071 respondió a los 1.8 s | Cumple |
| La base se crea con su esquema, sus migraciones y sus datos semilla | Tablas patron, usuario, trabajador, movimiento, bitacora y migracion; 2 migraciones registradas | Cumple |
| Los usuarios quedan activos y con contraseña | admin.rrhh (administrador) y captura.obra1 (captura) | Cumple |
| Se inicia sesión, se captura y se genera el lote | Casos PF-03, PF-05 y PF-17 (Tabla 11) | Cumple |
| Controlador de PostgreSQL | psycopg2-binary 2.9.13 instalado; sin servidor PostgreSQL, el sistema usa SQLite tras 1 s de espera | Observación (P-14) |

### Configuración del sistema

Sigma se configura con variables de entorno que se leen al arrancar, de modo que la misma versión del código sirve para la demostración y para la oficina sin editar ningún archivo. La Tabla 5 muestra cada variable con el valor que se usó en la demostración y el recomendado para la empresa; las cinco de en medio son nuevas en la versión corregida.

> Tabla 5. Variables de configuración del sistema.

| Variable | Para qué sirve | En la demostración | Recomendado en la oficina |
|---|---|---|---|
| SIGMA_HOST | Interfaz de red donde escucha el servidor | 0.0.0.0 (toda la red local) | 0.0.0.0 |
| SIGMA_PUERTO | Puerto del servidor | 5071 | 5050 |
| SIGMA_HILOS | Peticiones que se atienden a la vez | 8 | 8 (sin errores con 20 usuarios) |
| SECRET_KEY | Firma de la cookie de sesión | Fija para la demostración | Fija y larga; sin ella, Sigma crea y reutiliza el archivo .clave_sesion |
| SIGMA_SESION_HORAS | Duración de la sesión | 10 (valor por omisión) | 10: una jornada de trabajo |
| SIGMA_MAX_PETICION_KB | Tamaño máximo de una petición | 1024 (por omisión) | 1024 |
| SIGMA_RESPALDOS | Carpeta de los respaldos | respaldos/ en la carpeta de instalación | Otro disco o una unidad de red |
| SIGMA_RESPALDO_HORAS | Cada cuántas horas se respalda la base | 24 (por omisión) | 24, o menos en temporada de muchas altas |
| SIGMA_RESPALDOS_CONSERVAR | Respaldos que se guardan antes de borrar el más viejo | 30 (por omisión) | 30: un mes de respaldos diarios |
| DATABASE_URL | Conexión a PostgreSQL | Sin definir (127.0.0.1:5432) | La del servidor PostgreSQL al instalarlo |
| SIGMA_DB | Fuerza el motor de datos | Automático (usó SQLite) | sqlite mientras no haya PostgreSQL; después, postgres |
| SQLITE_PATH | Archivo de la base SQLite | sigma_imss.db en la carpeta de instalación | La carpeta de instalación |
| SIGMA_DEBUG | Depuración del servidor de desarrollo | Apagada | Siempre apagada |

Algunos datos de configuración están en el código porque cambian con poca frecuencia o dependen de una disposición legal (Tabla 6). Los dos primeros deben ajustarse antes de operar con datos reales y los montos legales cada año; si faltan los del año en curso, Sigma lo avisa al arrancar y en cada captura con fecha de ese año, y usa los más recientes.

> Tabla 6. Datos de configuración que viven en el código.

| Dato | Archivo | Valor actual | Cuándo se cambia |
|---|---|---|---|
| PATRON_SEMILLA y GUIA_SEMILLA | database.py | A1234567890, razón social de la empresa y guía 00000 | Antes de operar: registro patronal real y guía de la subdelegación |
| USUARIOS_SEMILLA | database.py | admin.rrhh (administrador) y captura.obra1 (captura), sin contraseña | Al definir al personal: un usuario por persona |
| SALARIO_MINIMO_GENERAL y UMA_DIARIA | validaciones.py | 2026: 315.04 y 117.31 pesos; tope de 25 UMA = 2,932.75 | Cada enero (salario mínimo) y febrero (UMA) |
| DIAS_INHABILES_ADICIONALES | plazo.py | Vacío | Cuando el IMSS publique días inhábiles |
| Catálogos IDSE | validaciones.py | Tipos de trabajador y de salario; jornada oficial 0 a 6; causas de baja | Si cambia el instructivo del IMSS |
| ESTRUCTURA del lote | exportar_idse.py | Posición, longitud y tipo de los 21 campos del alta y los 16 de la baja | Si el IMSS cambia la estructura de movimientos |
| INTENTOS_MAXIMOS, MINUTOS_BLOQUEO y LONGITUD_MINIMA | usuarios.py | 5 intentos, 15 minutos y contraseñas de 8 caracteres o más | Solo si la empresa fija otra política |
| UMBRAL_DIAS_HABILES | plazo.py | 5 | Solo si cambia el art. 15 de la LSS |

El acceso se configura con usuarios y roles. Sigma crea dos usuarios semilla sin contraseña; antes de usarlo, el personal de recursos humanos fija las contraseñas desde la consola del servidor con python -m sigma.usuarios, que también crea, desactiva y desbloquea usuarios. Las contraseñas se guardan como un hash scrypt de Werkzeug (Pallets, s.f.), nunca en texto, y la sesión se valida en cada petición contra un token guardado en la base, de modo que cerrar sesión invalida la cookie aunque alguien la haya copiado. La Tabla 7 resume lo que puede hacer cada rol y la Figura 4 muestra la pantalla con la que empieza todo uso del sistema.

> Tabla 7. Permisos de cada rol en la versión corregida.

| Acción | Rol captura | Rol administrador |
|---|---|---|
| Iniciar y cerrar sesión | Sí | Sí |
| Capturar, validar y consultar movimientos | Sí | Sí |
| Generar el lote IDSE | No (HTTP 403) | Sí |
| Descargar los archivos del lote | No (HTTP 403) | Sí |
| Crear usuarios, cambiar contraseñas y desbloquear cuentas | No | Desde la consola de la PC servidor |

> Figura 4. Pantalla de inicio de sesión: es lo primero que ve cualquier equipo de la red local que abra Sigma.

> Figura 5. Pantalla principal con la sesión de administración al final del escenario: usuario y rol en la barra superior, lote generado con un archivo por tipo y la exportación registrada en la bitácora.

Una vez dentro, la barra superior muestra en todo momento el registro patronal, el motor de datos en uso y el usuario con su rol, junto al botón Salir (Figura 5). Así, el personal de recursos humanos confirma sin entrar al servidor con qué base y con qué cuenta está trabajando.

### Programación definitiva preliminar

La programación que se demuestra es la de la rama trl6/correcciones en el commit 8914883, con 30 commits: los 24 de la rama principal y 6 de esta fase. Es definitiva porque ya integra todos los componentes y cierra las brechas que encontró la primera demostración; es preliminar porque todavía le faltan el cifrado del tráfico, el servidor PostgreSQL y la prueba del lote en el IDSE, descritos en la sección de problemas. La Tabla 8 resume el código.

> Tabla 8. Módulos de la programación definitiva preliminar (versión 8914883).

| Archivo | Líneas | Responsabilidad |
|---|---|---|
| **Aplicación (paquete sigma/)** |  |  |
| app.py | 686 | Rutas HTTP, sesión obligatoria, roles, reglas de flujo y de historial, protección contra CSRF, política de contenido y manejo de errores HTTP |
| database.py | 632 | Esquema de 6 tablas para PostgreSQL y SQLite, selección del motor, transacciones, bitácora, estado afiliatorio y migraciones únicas |
| validaciones.py | 610 | Normalización, reglas de CURP, NSS, RFC, nombres, fechas, catálogos, UMF, salario y plazo; iniciales de la CURP contra el nombre |
| usuarios.py | 226 | Contraseñas, bloqueo, token de sesión y consola de administración de usuarios |
| exportar_idse.py | 219 | Estructura oficial de 168 posiciones, un archivo por tipo de movimiento |
| respaldo.py | 163 | Respaldo verificado, rotación, restauración y consola de respaldos |
| plazo.py | 101 | Días hábiles y fecha límite del plazo legal |
| __init__.py y __main__.py | 35 | Paquete y servidor de desarrollo |
| templates/ (4 plantillas) | 606 | Pantalla principal, inicio de sesión, base común y página de error |
| static/ (estilos.css y app.js) | 1,334 | Sistema visual con tema claro y oscuro; máscaras, validación en vivo y detalle de movimientos |
| **Arranque y pruebas** |  |  |
| servidor.py | 59 | Arranque de producción con waitress y respaldo periódico |
| pruebas/test_prueba_concepto.py | 295 | Arnés del Entregable 3 (8 casos y lote de 168 posiciones) |
| pruebas/prueba_ambiente_relevante.py | 1,493 | Arnés del Entregable 5 (bloques A a H) |
| pruebas/prueba_integracion.py | 767 | Arnés del Entregable 6 (bloques F, L, S, R y C) |
| **Total: 7,226 líneas en 19 archivos; 30 commits en la rama trl6/correcciones** |  |  |

Las decisiones de programación que sostienen la integración son siete:

●  Un solo validador. La función normalizar_datos() limpia lo capturado y validar_campos() aplica las reglas, tanto en la validación en vivo (/api/validar) como al guardar, de modo que lo que el navegador marca coincide con lo que el servidor acepta.

●  Errores y avisos distintos. Un error impide guardar; un aviso (dígito verificador de la CURP o del NSS, iniciales de la CURP que no coinciden con el nombre, plazo por vencer, salario sobre el tope) se muestra pero no bloquea, porque el dato puede ser correcto.

●  La base decide en las carreras. Un índice único sobre trabajador, tipo y fecha del movimiento impide duplicados aunque dos capturas lleguen al mismo tiempo; el token de sesión también se crea con una sola instrucción condicional, para que dos equipos que entran a la vez con la misma cuenta compartan la sesión.

●  La identidad sale de la sesión. El usuario que se registra en la bitácora es el de la sesión; el formulario ya no trae un selector de usuario y, si alguien envía el campo, se ignora.

●  La estructura del lote es una tabla. Las posiciones de cada campo están en una tabla declarativa copiada del documento del IMSS; cada línea se comprueba contra 168 posiciones antes de escribirse, y un cambio del instructivo se corrige en la tabla, no en el código.

●  Respaldar antes de cambiar datos. El servidor respalda la base antes de crear o migrar tablas, y cada migración de datos se registra en la tabla migracion para que nunca se aplique dos veces.

●  Seguridad por omisión. Servidor de producción sin depuración, sesión obligatoria, rechazo de formularios enviados desde otros sitios, política de contenido con un valor único por petición, límite de tamaño de petición y consultas SQL siempre parametrizadas.

### Comunicación entre dispositivos

En la oficina intervienen tres tipos de equipo: la PC servidor, las PC de captura y el router de la red local; fuera de la oficina está la plataforma IDSE del IMSS (Instituto Mexicano del Seguro Social, s.f.-b). Toda la comunicación de Sigma ocurre dentro de la red local mediante HTTP/1.1 sobre TCP; la base de datos no se expone a la red. Cada petición, salvo la del inicio de sesión, lleva la cookie de sesión. La Tabla 9 describe cada enlace con el tamaño y el tiempo medidos por la IP de la red local, y la Figura 6 muestra la secuencia de mensajes de una jornada de captura.

> Figura 6. Secuencia de mensajes entre la PC de captura, el servidor y la base de datos: inicio de sesión, captura, exportación y descarga del lote.

> Tabla 9. Enlaces de comunicación del sistema, medidos por la IP de la red local.

| Enlace | Protocolo y ruta | Formato | Tamaño | Tiempo |
|---|---|---|---|---|
| Inicio de sesión | HTTP POST /login | Formulario (urlencoded) | 50 B → 302 y cookie | 6.8 ms |
| PC de captura → servidor: pantalla | HTTP GET / | HTML | 19,338 B | p95 13.6 ms |
| PC de captura → servidor: recursos | HTTP GET /static/… | CSS y JavaScript | 27,319 B y 17,728 B | 54.2 ms y 6.4 ms |
| Validación en vivo | HTTP POST /api/validar | JSON | 391 B → 41 B | p95 8.5 ms |
| Captura | HTTP POST /capturar | Formulario (urlencoded) | 300 B → redirección 302 | 14.0 ms |
| Detalle y bitácora de un movimiento | HTTP GET /api/movimiento/<folio> | JSON | 986 B | 9.2 ms |
| Descarga de un lote | HTTP GET /descargar-lote?tipo=altas o bajas | Texto Windows-1252, CRLF | 170 B por registro | 7.8 ms |
| Servidor ↔ base de datos | Llamada local (SQLite); TCP 5432 en 127.0.0.1 con PostgreSQL | SQL parametrizado | — | Incluido arriba |
| PC de RH → IDSE | HTTPS por internet, con la e.firma del patrón | Archivos de texto | — | Fuera de Sigma |

Para medir el costo de la red se repitieron 300 peticiones de cada tipo por la dirección del propio equipo (127.0.0.1) y por la IP de la red local (192.168.0.8). El p95 de la pantalla principal fue de 13.1 ms y 13.6 ms, y el de la validación en vivo, de 10.1 ms y 8.5 ms: la diferencia queda dentro de la variación normal entre corridas. Como la PC de captura se emuló en el mismo equipo, estas cifras no incluyen el paso por el router; en una red cableada de oficina ese paso agrega típicamente menos de un milisegundo por viaje, muy por debajo de los tiempos que percibe el capturista. La prueba con equipos físicos distintos queda para el piloto en la oficina.

La Figura 7 reproduce un intercambio real de la validación en vivo tal como viajó por la red local, ya con la cookie de sesión, que en la figura se reemplazó por un texto. La PC de captura envió solo cuatro campos en JSON y el servidor respondió, campo por campo, que faltaban el apellido paterno, el nombre y el tipo de movimiento, junto con las cabeceras de seguridad que acompañan a toda respuesta.

> Figura 7. Intercambio HTTP de la validación en vivo capturado en la red local: petición en JSON con la cookie de sesión, respuesta con errores por campo y cabeceras de seguridad.

### Pruebas funcionales

Las pruebas de esta fase se organizaron en tres niveles sobre la versión instalada: el arnés del Entregable 3, que prueba los módulos con ocho casos y el lote de 168 posiciones; el arnés del Entregable 5, que somete al sistema completo a las condiciones de la empresa; y el arnés nuevo del Entregable 6, que recorre el escenario de demostración por la IP de la red local y revisa el lote campo por campo. Para dar por demostrado el sistema se fijaron los diez criterios de la Tabla 10. El criterio de protección de datos de la primera demostración se dividió en dos, CA6-9 y CA6-10, para separar lo que ya se corrigió de lo que sigue pendiente.

> Tabla 10. Criterios de aceptación del TRL 6.

| Clave | Criterio | Meta |
|---|---|---|
| CA6-1 | Instalación | Solo con el procedimiento documentado, el sistema queda en servicio y responde por la red local en ≤ 10 min |
| CA6-2 | Integración funcional | Todos los casos del escenario de demostración correctos, sin excepciones en el servidor |
| CA6-3 | Regresión | Arnés del Entregable 3: 8 de 8 y lote conforme; criterios del Entregable 5: 10 de 10 |
| CA6-4 | Comunicación | Todos los enlaces responden por la IP de la red local; p95 de la validación en vivo ≤ 200 ms y de la pantalla ≤ 500 ms |
| CA6-5 | Seguridad de configuración | 0 hallazgos en configuración, inyección, CSRF, rutas, métodos HTTP, tamaño de petición, páginas de error y exposición de la base |
| CA6-6 | Desempeño | 10 usuarios sin errores con p95 de la captura ≤ 500 ms; tablero con 10,000 movimientos en ≤ 500 ms |
| CA6-7 | Recuperación | Tras una caída: 0 capturas confirmadas perdidas, base íntegra y servicio en ≤ 1 min. Tras perder la base: restauración íntegra desde el respaldo |
| CA6-8 | Compatibilidad con el IDSE | Cada registro del lote conforme a la estructura oficial del IMSS (168 posiciones, un archivo por tipo de movimiento) |
| CA6-9 | Autenticación y control de acceso | Sin sesión no se entra; la bitácora registra a quien inició sesión; solo administración genera lotes; bloqueo tras intentos fallidos |
| CA6-10 | Cifrado en la red | Los datos personales y la sesión no viajan legibles por la red local |

El escenario de demostración se ejecutó con la base vacía, como el primer día de uso en la oficina, y entrando por la IP de la red local. Cada caso se relacionó con lo que pidió el Entregable 1: R1, preparar la información de altas y bajas lista para el IMSS; R3, saber quién hizo cada movimiento; OE1, validar automáticamente los datos; OE2, generar el lote sin recaptura; OE3, control de acceso y bitácora; y OE4, cumplir el plazo de cinco días hábiles. La Tabla 11 muestra los 23 casos.

> Tabla 11. Escenario de demostración por la red local (versión corregida, 7 de octubre de 2026).

| Clave | Caso | Req. | Resultado |
|---|---|---|---|
| PF-01 | Abrir Sigma desde una PC de captura sin haber iniciado sesión | OE3 | 302 al inicio de sesión · correcto |
| PF-02 | Iniciar sesión con una contraseña equivocada | OE3 | 401 con mensaje genérico · correcto |
| PF-03 | Iniciar sesión como capturista (captura.obra1) | OE3 | 302 a la pantalla principal · correcto |
| PF-04 | Validación en vivo de un RFC que no corresponde a la CURP | OE1 | Error en el campo RFC antes de enviar · correcto |
| PF-05 | Alta válida con nombre separado y UMF | R1, OE4 | Guardado con su fecha límite · correcto |
| PF-06 | Alta con NSS incompleto y RFC incoherente | OE1 | 422 con 2 errores; datos conservados · correcto |
| PF-07 | El capturista corrige y reenvía el mismo movimiento | OE1 | Guardado · correcto |
| PF-08 | Segunda alta de un trabajador que sigue vigente | R1 | 422: «ya tiene un alta vigente» · correcto |
| PF-09 | Baja por término de contrato | R1 | Guardada · correcto |
| PF-10 | Baja de un trabajador ya dado de baja | R1 | 422: «ya fue dado de baja» · correcto |
| PF-11 | Reingreso del mismo trabajador a otra obra | R1 | Guardado como alta 08 · correcto |
| PF-12 | Alta con 9 días hábiles de retraso | OE4 | Guardado con aviso de plazo vencido · correcto |
| PF-13 | Alta con salario de 31.50 (punto corrido) | OE1 | 422: menor al salario mínimo · correcto |
| PF-14 | Alta sin unidad de medicina familiar | OE2 | 422: falta la UMF · correcto |
| PF-15 | Apellidos capturados al revés | OE1 | Válido, con aviso de iniciales de la CURP · correcto |
| PF-16 | La capturista intenta generar el lote | OE3 | 403: solo administración · correcto |
| PF-17 | Administración genera el lote con los pendientes | OE2 | 9 movimientos en 2 archivos · correcto |
| PF-18 | Descargar los dos archivos desde la PC de captura | OE2 | 9 registros de 168 posiciones · correcto |
| PF-19 | Buscar por NSS y filtrar por estado Exportado | R1 | Encontrado; 9 filas Exportado · correcto |
| PF-20 | Detalle de un movimiento exportado con su historial | R3 | Captura e «Incluido en lote IDSE» · correcto |
| PF-21 | Generar un lote cuando no hay pendientes | OE2 | Aviso «No hay movimientos…» · correcto |
| PF-22 | Bitácora en la base: autoría comprobada por la sesión | R3, OE3 | Todo a nombre de quien inició sesión · correcto |
| PF-23 | Cerrar sesión y volver con la cookie anterior | OE3 | 302 al inicio de sesión, también con la cookie anterior · correcto |

Los 23 casos fueron correctos y el servidor no registró ninguna excepción. La Figura 8 muestra el caso PF-06: el servidor rechazó la captura, indicó cada campo con su causa y conservó lo escrito; el formulario ya separa apellidos y nombre, y la bitácora registra el intento a nombre de quien inició sesión. La Figura 9 muestra el PF-12: un alta con nueve días hábiles de retraso se guardó con el aviso del plazo vencido, porque un aviso extemporáneo debe presentarse de todos modos.

> Figura 8. Caso PF-06: captura rechazada con un mensaje por campo y los datos conservados; la bitácora registra el intento a nombre de la capturista que inició sesión.

> Figura 9. Caso PF-12: movimiento guardado con el aviso de que el plazo legal de cinco días hábiles ya venció; la barra superior muestra la sesión de la capturista.

Además del escenario, el arnés del Entregable 6 revisó la conformidad del lote con la estructura oficial: capturó 42 movimientos (30 altas y 12 bajas) con nombres, salarios y causas variados, generó el lote y comparó cada campo de cada registro contra lo guardado en la base (Tabla 12). El resultado fue conforme en todas las revisiones.

> Tabla 12. Revisión del lote campo por campo contra la estructura oficial (bloque L).

| Revisión | Posiciones | Revisados | Correctos |
|---|---|---|---|
| Longitud del registro | 1-168 | 42 | 42 |
| Identificador del formato «9» | 168 | 42 | 42 |
| Tipo de movimiento igual al del archivo | 132-133 | 42 | 42 |
| NSS y su dígito | 12-22 | 42 | 42 |
| Fecha del movimiento DDMMAAAA | 119-126 | 42 | 42 |
| Salario con 2 decimales implícitos, topado a 25 UMA | 104-109 | 30 altas | 30 |
| Jornada normal con la clave oficial 0 | 118 | 30 altas | 30 |
| Unidad de medicina familiar | 127-129 | 30 altas | 30 |
| CURP | 150-167 | 30 altas | 30 |
| Causa de la baja | 149 | 12 bajas | 12 |
| Fin de línea CRLF y codificación Windows-1252 | — | 2 archivos | 2 |

La Figura 10 muestra un alta y una baja de los lotes que se descargaron en el escenario, con una regla de posiciones encima: los apellidos y el nombre ocupan 27 posiciones cada uno, el salario de 687.70 pesos aparece como 068770 y cada registro termina con el dígito 9 en la posición 168.

> Figura 10. Un alta y una baja de los lotes descargados en la demostración, divididos en dos tramos de 84 posiciones con su regla.

El arnés del Entregable 5 confirmó el funcionamiento con más volumen. En el mes simulado (bloque A), tres capturistas registraron 140 movimientos con 0 fallas; los 140 llegaron a los lotes y a la bitácora con su usuario, con un p95 de 41.1 ms por captura y de 19.6 ms por validación en vivo. En el bloque de errores típicos (bloque B), de 128 errores inyectados se bloquearon 88 y se avisaron 36, una detección del 96.9 %, sin falsos positivos y sin rechazar ninguno de los 24 datos válidos escritos con otro formato. El arnés del Entregable 3 dio 8 de 8 casos correctos y generó sus dos archivos de 168 posiciones.

Contra los requerimientos del Entregable 1, todos los casos tienen respaldo. Las dos salvedades de la primera demostración quedaron resueltas: el control de acceso del objetivo OE3 ya existe (PF-01 a PF-03, PF-16, PF-22 y PF-23) y el lote del objetivo OE2 ya tiene la estructura oficial (PF-17, PF-18 y bloque L).

### Pruebas de seguridad

La seguridad se probó en dos partes sobre la versión instalada: las ocho pruebas del bloque G del arnés del Entregable 5 y catorce comprobaciones del arnés del Entregable 6 (S-01 a S-14). Las diez primeras son las mismas de la primera demostración; las cuatro últimas se agregaron para probar el inicio de sesión: bloqueo, roles, cookie copiada e inicios simultáneos. La Tabla 13 reúne los resultados.

> Tabla 13. Pruebas de seguridad sobre la versión corregida.

| Clave | Prueba | Resultado | Valoración |
|---|---|---|---|
| **Bloque G del arnés del Entregable 5** |  |  |  |
| G01 | Cabecera Server sin versión | Server: Sigma | Seguro |
| G02 | Consola de depuración (/console) | 404 | Seguro |
| G03 | Folio fuera de rango | 404 | Seguro |
| G04 | Captura desde otro sitio (CSRF) | 403; no se guarda | Seguro |
| G05 | Inyección SQL en el buscador | 0 resultados; tablas intactas | Seguro |
| G06 | Código en el nombre (XSS) | 422; texto escapado | Seguro |
| G07 | Cabeceras de seguridad | CSP, nosniff, X-Frame-Options y Referrer-Policy | Seguro |
| G08 | Acceso desde la red local | 200 | Seguro |
| **Comprobaciones del arnés del Entregable 6** |  |  |  |
| S-01 | Abrir el sistema desde la red sin credenciales | 302 al inicio de sesión | Seguro |
| S-02 | Capturar con usuario_id=1 (admin) estando en sesión como capturista | Se guarda a nombre de captura.obra1; el campo se ignora | Seguro |
| S-03 | Leer una captura en tránsito por la red | CURP, NSS, RFC, nombre, salario y cookie legibles | Hallazgo |
| S-04 | Banderas de la cookie de sesión | HttpOnly y SameSite=Lax; Secure requiere HTTPS | Seguro |
| S-05 | Métodos no permitidos (TRACE, PUT, DELETE y GET /capturar) | 405 en TRACE, PUT, DELETE y GET /capturar | Seguro |
| S-06 | Rutas con ../ hacia la base y el código | 404 en las cuatro rutas | Seguro |
| S-07 | Página de error sin detalle técnico | 404 sin detalle técnico y con CSP | Seguro |
| S-08 | Captura de un programa sin sesión ni cabeceras Origin/Referer | 302 al inicio de sesión; no se guarda | Seguro |
| S-09 | Formulario de 8 MB | 413 en 56 ms, sin procesarlo | Seguro |
| S-10 | Puerto de PostgreSQL (5432) y archivo de la base desde la red | Puerto 5432 cerrado; base no accesible | Seguro |
| S-11 | Cinco contraseñas equivocadas y luego la correcta | Cuenta bloqueada: la correcta también recibe 401 | Seguro |
| S-12 | La capturista intenta generar y descargar lotes | 403 al generar y al descargar | Seguro |
| S-13 | Reutilizar una cookie copiada después de cerrar sesión | 302 al inicio de sesión | Seguro |
| S-14 | Diez equipos inician sesión a la vez con la misma cuenta | 10 de 10 siguen dentro | Seguro |

Las ocho pruebas del bloque G no tuvieron hallazgos y de las catorce comprobaciones solo una sigue abierta. En la primera demostración, seis de diez comprobaciones habían revelado cuatro problemas; ordenados según la lista OWASP Top 10:2025 (OWASP Foundation, 2025), así quedaron:

●  Autenticación y control de acceso (A01 y A07): corregido. Sin sesión, la red solo ve la pantalla de inicio (S-01 y S-08); la bitácora registra a quien inició sesión aunque el formulario diga otra cosa (S-02); cinco contraseñas equivocadas bloquean la cuenta (S-11); la capturista no puede generar ni descargar lotes (S-12); una cookie copiada deja de servir al cerrar sesión (S-13); y diez equipos que entran a la vez con la misma cuenta siguen dentro (S-14).

●  Condiciones excepcionales mal manejadas (A10): corregido. Un método no permitido responde 405 con una página propia, y ya no 500 «El movimiento no se guardó» (S-05).

●  Sin límite de tamaño de petición: corregido. Un formulario de 8 MB se rechaza con 413 antes de procesarlo (S-09).

●  Tráfico sin cifrar (A04): abierto. Un relevo TCP colocado entre la PC de captura y el servidor sigue leyendo en texto plano la CURP, el NSS, el RFC, el nombre, el salario y la cookie de sesión (Figura 11); al iniciar sesión, también la contraseña. Quien copie la cookie en la red podría usarla hasta que el usuario cierre sesión. Se corrige con HTTPS (problema P-11), que además permitirá marcar la cookie como Secure (S-04).

> Figura 11. Captura vista por un tercer equipo en la red local: aun con inicio de sesión, los datos personales y la cookie viajan sin cifrar.

Lo demás quedó demostrado en la versión instalada: la configuración del servidor, la defensa contra inyección y contra envíos desde otros sitios, el manejo de rutas, el inicio de sesión y la protección de la base. Las medidas físicas y administrativas que recomienda el artículo 18 de la LFPDPPP (servidor en un área de acceso restringido, disco cifrado, respaldos en otro disco y uso limitado al personal de recursos humanos) siguen siendo responsabilidad de la empresa.

### Pruebas de desempeño

El desempeño se midió con los bloques D (carga), E (volumen) y F (caída) del arnés del Entregable 5 sobre la versión corregida con waitress, en el equipo de pruebas (Intel Core i5-10400F con 12 núcleos lógicos, 32 GB de memoria, Windows 11 y Python 3.14.3). En el bloque D, cada nivel de usuarios captura sin pausa durante 15 s, una carga muy superior a la de la oficina, donde capturan hasta tres personas con pausas para leer y escribir. La Tabla 14 resume los resultados.

> Tabla 14. Carga con usuarios simultáneos sin pausa (versión corregida, bloque D).

| Usuarios | Peticiones por segundo | Capturas por minuto | p95 captura | Máx. captura | p95 tablero | Errores |
|---|---|---|---|---|---|---|
| 1 | 78 | 931 | 22.2 ms | 132.2 ms | 19.9 ms | 0 |
| 3 | 169 | 2,022 | 46.6 ms | 202.2 ms | 38.9 ms | 0 |
| 5 | 251 | 3,008 | 55.7 ms | 545.4 ms | 44.4 ms | 0 |
| 10 | 329 | 3,935 | 85.4 ms | 837.2 ms | 62.2 ms | 0 |
| 20 | 316 | 3,771 | 127.8 ms | 580.1 ms | 122.0 ms | 0 |

Con 10 usuarios el sistema atendió 3,935 capturas por minuto con un p95 de 85.4 ms y sin errores; con 20, el rendimiento ya no creció (el servidor llegó a su capacidad), el p95 subió a 127.8 ms y la captura más lenta tardó 580.1 ms, porque SQLite solo admite una escritura a la vez (SQLite Consortium, s.f.; problema P-14). La Figura 12 compara estas curvas con las del prototipo del Entregable 4.

> Figura 12. Desempeño del prototipo del Entregable 4 y de la versión corregida, medidos con el mismo arnés el 7 de octubre de 2026.

La versión corregida rinde menos que la de la primera demostración: con 10 usuarios atendió 3,935 capturas por minuto, frente a 5,609, y con un solo usuario el p95 de la captura pasó de 14.6 ms a 22.2 ms. Es el costo del inicio de sesión y de las validaciones nuevas: cada petición consulta en la base al usuario y su token, y cada captura revisa más campos (apellidos, UMF e iniciales de la CURP). A cambio, con 20 usuarios llegan menos escrituras a la vez y la captura más lenta bajó de 3.1 s a 0.58 s. Todos los tiempos siguen muy por debajo de la meta de 500 ms.

En volumen (bloque E), con 10,000 movimientos en la base, unos seis años de operación, el tablero respondió con un p95 de 21.5 ms, la búsqueda con 27.4 ms y la exportación de 510 movimientos tardó 44.7 ms. La captura con 10,000 movimientos tuvo un p95 de 261.6 ms, más alto que con 1,000 y 5,000 (21.3 ms y 23.2 ms), aunque dentro de la meta. En la prueba de caída (bloque F) se terminó el proceso del servidor a media captura: de 940 capturas confirmadas no se perdió ninguna, la base quedó íntegra y el servidor volvió a responder 0.71 s después de reiniciarlo (2.94 s desde la caída, incluida una pausa fija de 1.5 s del arnés).

El arnés del Entregable 6 agregó la prueba de respaldo y restauración (bloque R): con 40 movimientos capturados, el respaldo manual tardó 0.16 s y pasó la revisión de integridad de SQLite; después se capturaron 5 movimientos más, se borró el archivo de la base y se restauró el respaldo. La restauración y el arranque tomaron 0.85 s, los conteos de trabajadores y movimientos volvieron a ser idénticos a los del respaldo y el sistema respondió 200. Las 5 capturas posteriores al respaldo se perdieron, como era de esperar: ese es el punto de recuperación, y con el respaldo cada 24 horas lo más que se perdería es un día de capturas, que se rehace con los documentos de los trabajadores.

### Resultados cuantitativos

La Tabla 15 evalúa los criterios de aceptación con los resultados obtenidos.

> Tabla 15. Cumplimiento de los criterios de aceptación del TRL 6 (versión corregida).

| Criterio | Resultado medido | Estado |
|---|---|---|
| CA6-1 Instalación | En servicio y respondiendo por la red local en 16.9 s, sin errores | Cumple |
| CA6-2 Integración funcional | 23 de 23 casos correctos; 0 excepciones | Cumple |
| CA6-3 Regresión | Entregable 3: 8 de 8 y lote conforme; criterios del Entregable 5: 10 de 10 | Cumple |
| CA6-4 Comunicación | Todos los enlaces respondieron; p95 de 8.5 ms (validación) y 13.6 ms (pantalla) | Cumple |
| CA6-5 Seguridad de configuración | 0 hallazgos en el bloque G y en S-05, S-06, S-07, S-09 y S-10 | Cumple |
| CA6-6 Desempeño | 10 usuarios: 0 errores, p95 85.4 ms; tablero con 10,000: 21.5 ms | Cumple |
| CA6-7 Recuperación | 0 de 940 capturas perdidas; servicio en 2.94 s; base restaurada del respaldo en 0.85 s | Cumple |
| CA6-8 Compatibilidad con el IDSE | 42 de 42 registros conformes en dos archivos (bloque L) | Cumple |
| CA6-9 Autenticación y control de acceso | S-01, S-02, S-08 y S-11 a S-14 seguros; PF-16, PF-22 y PF-23 correctos | Cumple |
| CA6-10 Cifrado en la red | Datos y cookie legibles en la red (S-03) | No cumple |

La versión corregida cumple 9 de los 10 criterios, frente a 7 de 9 en la primera demostración. Los cumplidos demuestran lo que define al TRL 6: el sistema completo se instala, se integra, se comunica por la red local, controla quién lo usa, genera el lote con la estructura del IMSS, resiste carga, volumen, caídas y la pérdida de la base, y conserva las capacidades validadas en los niveles anteriores. El único que no se cumple, el cifrado del tráfico en la red local, no impide la demostración, pero sí debe resolverse antes de operar con datos reales.

### Comparación antes/después

La comparación se hizo en tres planos. El primero es el que importa a la empresa: el proceso actual con archivos de Excel frente al sistema integrado (Tabla 16). Donde el Entregable 1 no da cifras del proceso actual, la comparación es cualitativa.

> Tabla 16. Proceso actual con Excel frente a Sigma integrado.

| Aspecto | Antes: proceso actual (Entregable 1) | Después: Sigma integrado (medido) |
|---|---|---|
| Captura | Se escribe en Excel y se vuelve a escribir en el portal IDSE | Una sola captura; los archivos del IDSE se generan con la estructura oficial (PF-17 y PF-18) |
| Detección de errores al capturar | Ninguna: el archivo no valida datos | 96.9 % de 128 errores típicos, sin falsos positivos |
| Estado del movimiento | Color de celda; el encargado anterior era daltónico | Estado escrito (Válido, Exportado); 14 de 14 pares de color con contraste AA |
| Quién hizo cada movimiento | No se registra | Bitácora con el usuario de la sesión y la hora de cada acción (PF-22) |
| Quién puede usar los datos | Cualquiera que abra el archivo | Solo usuarios con contraseña; solo administración genera los lotes |
| Plazo legal de cinco días hábiles | Sin aviso | Fecha límite en cada captura y aviso de vencido (PF-05 y PF-12) |
| Altas duplicadas y bajas repetidas | No se detectan | Se bloquean (PF-08 y PF-10); 0 duplicados en 60 pares de capturas simultáneas |
| Varias personas a la vez | Un archivo para una persona | 20 usuarios simultáneos sin errores |
| Pérdida del archivo | Depende de que alguien lo haya copiado | Respaldo automático y restauración probada |
| Acuse del IMSS | Se guarda por separado, sin conexión con el registro | Igual: queda para el piloto |

El segundo plano es técnico: el prototipo del Entregable 4 frente a la versión corregida, medidos el mismo día, en el mismo equipo y con el mismo arnés (Tabla 17). Las cifras del Entregable 4 son muy parecidas a las que reportó el Entregable 5; las diferencias menores se deben a que las carreras entre capturas simultáneas varían de una corrida a otra.

> Tabla 17. Prototipo del Entregable 4 frente a la versión corregida (arnés del Entregable 5, 7 de octubre de 2026).

| Medida | Antes: prototipo E4 | Después: versión corregida |
|---|---|---|
| Criterios del TRL 5 cumplidos | 6 de 10 | 10 de 10 |
| Servidor | Desarrollo de Flask con depuración | Producción con waitress |
| Errores de captura detectados (128) | 50.0 % | 96.9 % |
| Datos válidos rechazados por su formato (24) | 24 | 0 |
| Duplicados / pares con error 500 (60 pares simultáneos) | 7 / 2 | 0 / 0 |
| Hallazgos de seguridad (bloque G, 8 pruebas) | 5 | 0 |
| p95 / máx. de la captura con 20 usuarios | 696.2 ms / 2.4 s | 127.8 ms / 0.58 s |
| Capturas por minuto con 10 usuarios | 3,386 | 3,935 |
| p95 del tablero con 10,000 movimientos | 42.2 ms | 21.5 ms |
| Capturas confirmadas perdidas tras la caída | 0 de 666 | 0 de 940 |
| Pares de color bajo 4.5:1 (WCAG 2.1 AA) | 2 | 0 |

La versión corregida mejora o iguala al prototipo en casi todas las medidas. Las mayores diferencias están en la detección de errores, que casi se duplica, en la eliminación de duplicados y de hallazgos de seguridad, y en el comportamiento con muchos usuarios: con el servidor de producción waitress (Pylons Project, s.f.), el p95 de la captura con 20 usuarios bajó de 696.2 ms a 127.8 ms y con 10 usuarios se atendieron 16 % más capturas por minuto. Además, todos los pares de color de la interfaz cumplen el contraste mínimo del nivel AA de las WCAG 2.1 (World Wide Web Consortium, 2018).

El tercer plano es el efecto de las correcciones de esta fase: la primera demostración, con la rama principal, frente a la versión corregida (Tabla 18).

> Tabla 18. Primera demostración frente a la versión corregida (7 de octubre de 2026).

| Medida | Primera demostración (7f43596) | Versión corregida (8914883) |
|---|---|---|
| Criterios del TRL 6 cumplidos | 7 de 9 | 9 de 10 |
| Casos del escenario de demostración | 17 de 17 | 23 de 23 |
| Comprobaciones de seguridad con hallazgo | 6 de 10 | 1 de 14 |
| Aspectos del lote conformes con la estructura oficial | 7 de 18 | 18 de 18 |
| Inicio de sesión y roles | No | Sí, con bloqueo y token en la base |
| Respaldo automático | No | Al arrancar y cada 24 horas; restauración probada |
| Controlador de PostgreSQL en la instalación | Omitido en Python 3.14 | psycopg2-binary 2.9.13 |
| Instalación limpia | 14.2 s | 16.9 s |
| Capturas por minuto con 10 usuarios | 5,609 | 3,935 |
| p95 / máx. de la captura con 20 usuarios | 164.6 ms / 3.1 s | 127.8 ms / 0.58 s |
| p95 de la validación en vivo por la red local | 5.5 ms | 8.5 ms |

Las correcciones cerraron las brechas funcionales y de seguridad a cambio de un costo de rendimiento que no se percibe en la oficina: la validación en vivo pasó de 5.5 ms a 8.5 ms, una diferencia que el capturista no percibe, y con 10 usuarios sin pausa el sistema sigue atendiendo 3,935 capturas por minuto sin errores.

El cambio de mayor peso para la empresa es el del lote, porque es lo que recibe el IMSS. La estructura que publica el IMSS para presentar cinco o más movimientos en un archivo, como exige el artículo 46 del RACERF, pide un archivo de texto por tipo de movimiento, con registros de 168 posiciones de ancho fijo (Instituto Mexicano del Seguro Social, s.f.-a). La Figura 13 reproduce la tabla oficial de las altas y reingresos, y la Tabla 19 la compara, campo por campo, con el lote de la primera demostración y con el de la versión corregida.

> Figura 13. Estructura oficial del registro de alta o reingreso (Instituto Mexicano del Seguro Social, s.f.-a).

> Tabla 19. Estructura oficial del IMSS frente al lote de la primera demostración y al de la versión corregida.

| Campo (posiciones) | Lo que pide el IMSS | Antes (7f43596) | Después (versión corregida) |
|---|---|---|---|
| Registro | 168 posiciones fijas, sin separadores | 82 caracteres (alta) o 74 (baja), separados por «\|» | 168 posiciones; se comprueba al escribir |
| Archivo | Uno por tipo de movimiento | Altas y bajas en el mismo lote | Uno de altas y uno de bajas |
| Registro patronal y su dígito (1-11) | 10 + 1 posiciones | Compatible | Conforme |
| NSS y su dígito (12-22) | 10 + 1 posiciones | Compatible | Conforme |
| Apellidos y nombre (23-103) | Paterno, materno y nombre(s), 27 posiciones cada uno | No se exportaban; el nombre era un solo campo | Se capturan por separado; mayúsculas sin acentos |
| Salario base de cotización (104-109) | 6 dígitos con 2 decimales implícitos | Con punto decimal (687.70) | 068770, topado a 25 UMA |
| Tipo de trabajador (116) | 1 a 4 | Compatible | Conforme |
| Tipo de salario (117) | 0, 1 o 2 | Compatible | Conforme |
| Semana o jornada reducida (118) | 0 = normal; 1 a 5 = días; 6 = jornada reducida | 1 = normal; 2 a 4 = combinaciones propias | Catálogo oficial; datos anteriores migrados |
| Fecha del movimiento (119-126) | DDMMAAAA | Compatible | Conforme |
| Unidad de medicina familiar (127-129) | 3 posiciones (alta) | No se capturaba | Se captura y es obligatoria en altas |
| Tipo de movimiento (132-133) | 08 o 02 | Compatible | Conforme |
| Guía (134-138) | Número asignado por la subdelegación | No existía | Dato del patrón (semilla 00000, por cambiar) |
| Clave del trabajador (139-148) | Asignada por el patrón | No se exportaba | Folio del trabajador en Sigma |
| Causa de la baja (149) | 1 a 9 y A | Compatible | Conforme |
| CURP (150-167) | En altas; en bajas, espacios | En altas y en bajas | Solo en altas |
| RFC | No forma parte de la estructura | Se exportaba | Ya no se exporta |
| Identificador del formato (168) | Dígito 9 | No existía | 9 en cada registro |

De los 18 aspectos, la primera demostración cumplía siete; la versión corregida sigue la estructura en los 18 y el bloque L lo comprobó en 42 registros. El documento del IMSS no indica la codificación de caracteres, el fin de línea ni cómo representar la Ñ; Sigma usa Windows-1252, CRLF y conserva la Ñ, y esos detalles solo se confirman cargando un lote de prueba en el IDSE con la e.firma de la empresa.

### Problemas encontrados

La Tabla 20 reúne los problemas de esta fase. Los P-01 a P-18 se encontraron durante la integración, la instalación y la primera demostración; los P-19 a P-22 aparecieron al verificar las correcciones, en la segunda instalación limpia y en las pruebas de la versión corregida. La severidad sigue el criterio del entregable anterior: alta si puede provocar una multa, una pérdida de datos o un acceso indebido; media si produce un dato incorrecto o un error visible; baja si solo afecta la comodidad o el mantenimiento.

> Tabla 20. Problemas encontrados en la integración y la demostración, con su estado al cierre.

| Clave | Problema | Cómo se reveló | Sev. | Estado |
|---|---|---|---|---|
| P-01 | Los ajustes del TRL 5 estaban en una rama aparte; la rama principal seguía con el Entregable 4 | Revisión del repositorio al integrar | Alta | Corregido |
| P-02 | El feriado de transmisión del Poder Ejecutivo se calculaba con la regla anterior a la reforma de la LFT de 2024 (1 de diciembre en lugar del 1 de octubre) | Lectura del texto vigente del art. 74 de la LFT | Media | Corregido |
| P-03 | La aplicación, los arneses y sus resultados estaban mezclados en la raíz del repositorio | Integración | Baja | Corregido |
| P-04 | Quedó una importación sin uso al separar el arranque de desarrollo | Revisión del código | Baja | Corregido |
| P-05 | Sin SECRET_KEY, cada reinicio generaba una clave nueva y cerraba las sesiones abiertas | Instalación | Baja | Corregido |
| P-06 | El catálogo de jornada no coincidía con el oficial: Sigma usaba 1 para la jornada normal y el IMSS usa 0; para el IMSS, el 1 significa «un día a la semana» | Comparación con la estructura oficial | Alta | Corregido |
| P-07 | El lote no seguía la estructura oficial de 168 posiciones (Tabla 19) | Comparación con la estructura oficial | Alta | Corregido; falta la prueba en el IDSE |
| P-08 | No había inicio de sesión: cualquiera en la red capturaba a nombre de cualquier usuario | S-01, S-02 y S-08 | Alta | Corregido |
| P-09 | El selector «Usuario que captura» regresaba al primer usuario en cada recarga; si no se cambiaba, la captura quedaba a nombre de admin.rrhh | Primera demostración | Media | Corregido |
| P-10 | Un método no permitido (por ejemplo, abrir /capturar en la barra del navegador) respondía 500 «El movimiento no se guardó» en lugar de 405 | S-05 | Media | Corregido |
| P-11 | El tráfico viaja sin cifrar por la red local | S-03 | Media | Abierto (planeado) |
| P-12 | No había respaldo automático de la base | Revisión de la instalación | Alta | Corregido |
| P-13 | requirements.txt excluía psycopg2 en Python 3.13 o superior, aunque ya existe la versión 2.9.13 para Python 3.14 (Python Package Index, 2026); el sistema caía a SQLite | Primera instalación limpia | Media | Corregido |
| P-14 | Con 20 usuarios sin pausa, la captura más lenta tardó 3.1 s en la primera demostración y 0.58 s en la corregida (una escritura a la vez en SQLite) | Bloque D | Baja | Abierto (planeado) |
| P-15 | La exportación no quedaba ligada a cada movimiento en la bitácora: su detalle no decía cuándo se exportó | Primera demostración | Baja | Corregido |
| P-16 | No había límite de tamaño para las peticiones | S-09 | Baja | Corregido |
| P-17 | Los montos legales solo llegan a 2026 y los días inhábiles del IMSS no están cargados | Revisión de la configuración | Media | Mitigado: Sigma avisa; carga anual |
| P-18 | El pie de la interfaz decía «TRL 5» | Primera demostración | Baja | Corregido |
| P-19 | Con el controlador de PostgreSQL ya instalado y sin servidor, cada arranque esperaba 4 s antes de usar SQLite | Segunda instalación limpia | Baja | Corregido |
| P-20 | Si dos equipos iniciaban sesión a la vez con la misma cuenta, cada uno escribía su propio token y uno quedaba fuera: sus capturas se redirigían al inicio de sesión sin guardarse | Bloque F: 640 capturas contadas como confirmadas no estaban en la base | Alta | Corregido |
| P-21 | Al verificar un respaldo quedaban archivos -wal y -shm junto a la copia | Prueba del respaldo | Baja | Corregido |
| P-22 | El aviso de exportación decía «1 bajas» | Revisión de las pantallas | Baja | Corregido |

El P-20 merece una explicación. Lo reveló la prueba de caída del Entregable 5: 640 capturas que el arnés contaba como confirmadas no estaban en la base. No se habían perdido; nunca se guardaron, porque esas peticiones habían sido redirigidas al inicio de sesión y el arnés tomaba la redirección como éxito. Se corrigieron las dos cosas: el sistema, para que los inicios de sesión simultáneos compartan el token, y el arnés, para que una redirección al inicio de sesión cuente como falla. La comprobación S-14 lo vigila desde entonces.

### Correcciones implementadas

Las correcciones de los P-01 a P-04 ya formaban parte de la rama principal. Las demás se implementaron en la rama trl6/correcciones, en seis commits, y se verificaron sobre una instalación limpia con los tres arneses. La Tabla 21 las reúne con su verificación.

> Tabla 21. Correcciones implementadas y su verificación.

| Problemas | Corrección | Commit | Verificación |
|---|---|---|---|
| P-01 | Integración de los ajustes del TRL 5 en la rama principal | cffd375 | Arnés del Entregable 3 y bloques B, C y G del Entregable 5 |
| P-02 | El feriado se calcula el 1 de octubre de 2024, 2030, etc., como fija el art. 74, fr. VII, de la LFT | 3afbc9a | Arneses de los entregables 3 y 5 |
| P-03 y P-04 | Paquete sigma/ y carpeta pruebas/; se quitó la importación sin uso | 3269ff1, fb3a4a8 y ac56fc1 | Criterios del TRL 5 iguales antes y después; 18 de 18 respuestas HTTP idénticas |
| P-06 y P-07 | Captura de apellidos, nombre(s) y UMF; catálogo oficial de jornada; estructura de 168 posiciones en una tabla declarativa; un archivo por tipo; migración única de los datos anteriores | 02aaad0 | Bloque L (42 de 42); PF-17 y PF-18; bloque 2 del Entregable 3 |
| P-08 y P-09 | Inicio de sesión con contraseña (hash scrypt), roles, bloqueo tras 5 intentos y token de sesión en la base; sin selector de usuario | 02aaad0 | S-01, S-02, S-08 y S-11 a S-13; PF-01 a PF-03, PF-16, PF-22 y PF-23 |
| P-12 y P-21 | Módulo respaldo.py: copia con la API de respaldo de SQLite (Python Software Foundation, s.f.), revisión de integridad, rotación y restauración; respaldo al arrancar y cada 24 horas | 02aaad0 | Bloque R: copia íntegra en 0.16 s y restauración en 0.85 s |
| P-05, P-10, P-13, P-16 y P-18 | Archivo .clave_sesion; páginas propias para 405, 413 y 400; psycopg2-binary sin marcador de versión; límite de 1 MB por petición; pie «TRL 6» | 02aaad0 | S-05 y S-09; instalación con psycopg2-binary 2.9.13 |
| P-15 y P-17 | Asiento «Incluido en lote IDSE» en cada movimiento exportado; aviso cuando faltan los montos del año | 02aaad0 | PF-20; aviso de 2027 comprobado en la instalación |
| — | Pruebas al día: arnés de integración nuevo y arneses de los entregables 3 y 5 con los campos nuevos | 540a313 | Corridas de esta fase |
| P-19 | Conexión a 127.0.0.1 con espera máxima de 1 s; SIGMA_DB=sqlite la evita | 882d60f | Instalación limpia (Figura 3) |
| P-20 | El token se crea solo si no existe y se vuelve a leer; el arnés cuenta la redirección al inicio de sesión como falla | 86038c2 y aee7bc0 | S-14 (10 de 10); bloque F: 0 de 940 perdidas |
| P-22 | El aviso dice «altas: 8 en …; bajas: 1 en …» | 8914883 | Figura 5 |

La comprobación final de todas ellas es la segunda demostración: la versión corregida, instalada desde cero, cumplió los diez criterios del Entregable 5, los 23 casos del escenario de esta fase y 9 de los 10 criterios del TRL 6. Quedan como trabajo planeado, en orden de prioridad:

●  Cifrado en la red (P-11). Un proxy con TLS delante de waitress, con un certificado de la oficina instalado en cada PC de captura. Con HTTPS, la cookie de sesión se marcará además como Secure.

●  Lote de prueba en el IDSE (P-07). Cargar un lote de un solo movimiento con la e.firma de la empresa para confirmar la codificación, el fin de línea y la Ñ, después de cambiar la guía semilla por la de la subdelegación.

●  PostgreSQL (P-14). Instalar el servidor en la PC servidor para repartir las escrituras simultáneas; el código y su controlador ya están listos.

●  Mantenimiento anual (P-17). Cargar cada año los montos legales y los días inhábiles que publique el IMSS.

Con estos resultados, Sigma alcanza el nivel TRL 6: el sistema completo, con sus componentes integrados en una sola versión, se instaló desde cero y operó por la red local en un ambiente relevante, con inicio de sesión, lote con la estructura oficial y respaldo, y cumplió nueve de los diez criterios de aceptación. Antes de la prueba piloto con datos reales en la oficina (TRL 7) quedan dos condiciones: cifrar el tráfico y cargar un lote de prueba en el IDSE. Resueltas ambas, el piloto empezará con un aviso de privacidad a los trabajadores y con el primer lote real, cuyo acuse cerrará por primera vez el lazo externo del sistema.

### Referencias

- Cámara de Diputados del H. Congreso de la Unión. (2005). Reglamento de la Ley del Seguro Social en Materia de Afiliación, Clasificación de Empresas, Recaudación y Fiscalización. https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LSS_MACERF.pdf
- Cámara de Diputados del H. Congreso de la Unión. (2025). Ley Federal de Protección de Datos Personales en Posesión de los Particulares. https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf
- Cámara de Diputados del H. Congreso de la Unión. (2026). Ley del Seguro Social. https://www.diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf
- Cámara de Diputados del H. Congreso de la Unión. (s.f.). Ley Federal del Trabajo. https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf
- Instituto Mexicano del Seguro Social. (s.f.-a). Estructura de movimientos afiliatorios. https://www.imss.gob.mx/sites/all/statics/sua/dispmag/EstructuraMovimientosAfiliatorios.pdf
- Instituto Mexicano del Seguro Social. (s.f.-b). IDSE — IMSS desde su empresa. https://idse.imss.gob.mx/
- Mankins, J. C. (1995). Technology readiness levels: A white paper. NASA, Office of Space Access and Technology.
- OWASP Foundation. (2025). OWASP Top 10:2025. https://top10.owasp.org/2025/
- Pallets. (s.f.). Werkzeug: Utilities — Security helpers. https://werkzeug.palletsprojects.com/en/stable/utils/#module-werkzeug.security
- Pylons Project. (s.f.). Waitress documentation. https://docs.pylonsproject.org/projects/waitress/
- Python Package Index. (2026). psycopg2-binary 2.9.13. https://pypi.org/project/psycopg2-binary/
- Python Software Foundation. (s.f.). sqlite3 — DB-API 2.0 interface for SQLite databases. https://docs.python.org/3/library/sqlite3.html
- SQLite Consortium. (s.f.). Write-Ahead Logging. https://www.sqlite.org/wal.html
- World Wide Web Consortium. (2018). Web Content Accessibility Guidelines (WCAG) 2.1. https://www.w3.org/TR/WCAG21/
