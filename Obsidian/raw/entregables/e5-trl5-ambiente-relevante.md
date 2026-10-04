---
tipo: fuente-cruda
origen: "LAB AUTO/Entregable 5 — TRL 5.docx"
extraido: 2026-10-04
formato_original: docx
nota: Transcripción automática del archivo entregado. NO editar; si el original cambia, se vuelve a extraer.
---

# Entregable 5 — TRL 5: validación en ambiente relevante

> Fuente cruda e inmutable. Texto extraído de `LAB AUTO/Entregable 5 — TRL 5.docx` (carpeta del 7.° semestre de Pedro).
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

## Validación en ambiente relevante

Este entregable documenta la validación del prototipo Sigma, sistema para la automatización de altas y bajas de trabajadores ante el Instituto Mexicano del Seguro Social (IMSS), en un ambiente relevante: en condiciones semejantes a las que existen en Desarrollos Eléctricos y Soluciones Avanzadas S.A. de C.V. En el nivel TRL 5 la tecnología deja de probarse con casos de laboratorio aislados y se somete a las condiciones del entorno donde va a operar (Mankins, 1995): varios capturistas trabajando a la vez desde la red local, la plantilla y la rotación propias de una contratista eléctrica, los errores de captura que se cometen en una oficina, el plazo legal para presentar cada movimiento y un servidor que debe seguir respondiendo aunque falle.

El punto de partida es el prototipo integrado del Entregable 4, que superó 20 pruebas de laboratorio. Para esta fase se construyó un arnés de pruebas nuevo, prueba_ambiente_relevante.py, que ejecuta el sistema completo como lo usaría la empresa y mide su comportamiento; cada error que reveló se corrigió en el código y se volvió a medir con la misma prueba. El ambiente es emulado: no se usaron datos reales de trabajadores, porque la CURP, el NSS y el salario son datos personales protegidos por la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, y porque el envío real al IDSE requiere la firma electrónica del patrón. La operación con datos reales dentro de la oficina corresponde a la demostración en ambiente real de los niveles TRL 6 y 7.

### Descripción del ambiente real

La empresa es una contratista de instalaciones eléctricas del área metropolitana de Monterrey que trabaja por proyecto: arma cuadrillas para cada obra (Grupo Multimedios, Bolerama La Pastora, la parte eléctrica de diversas colonias y el Hospital Sierra Madre, entre otras) y las disuelve o reasigna al terminar, por lo que el número de trabajadores cambia constantemente a lo largo del año (Entregable 1). Cada ingreso o salida de un trabajador genera un movimiento afiliatorio que debe presentarse ante el IMSS dentro de un plazo de cinco días hábiles.

El proceso que Sigma va a operar ocurre en tres lugares (Figura 1):

- En la obra. El residente de obra avisa por teléfono o mensaje que un trabajador entra o sale de su cuadrilla. Es el origen de cada movimiento y también la primera fuente de retraso: si el aviso llega tarde, el plazo legal empieza a correr antes de que la oficina se entere.

- En la oficina administrativa (Escobedo, N.L.). Hoy una sola persona captura los movimientos en un archivo de Excel y comunica su estado con colores de celda. Con Sigma, los capturistas escriben cada movimiento en el navegador de su computadora y el servidor de la oficina lo valida, lo guarda y lo registra en la bitácora. Los equipos se comunican por la red local; la base de datos vive en el servidor y no se expone fuera de él.

- En la plataforma IDSE del IMSS. El área administrativa genera en Sigma el lote de movimientos y lo carga en el IDSE por internet, autenticándose con la firma electrónica del patrón. Días después, el IMSS devuelve el acuse o el rechazo de cada movimiento.

Visto como sistema de control, el ambiente real tiene dos lazos cerrados con escalas de tiempo muy distintas. El lazo interno se cierra en segundos dentro de la oficina: el comparador (validaciones.py) contrasta cada captura con las reglas del IMSS y devuelve los errores por campo al capturista, que corrige y vuelve a enviar. El lazo externo se cierra en días: el acuse o el rechazo del IMSS es la medición real de si el movimiento quedó bien presentado. En el laboratorio solo existía el primero; el segundo es propio del ambiente real y por eso se trata en la sección de diferencias.

La empresa no proporcionó cifras de volumen ni de equipamiento, así que las condiciones del ambiente real se fijaron como supuestos de diseño a partir de lo descrito en los entregables 1 y 2 (Tabla 1). Las pruebas se dimensionaron con márgenes amplios sobre estos supuestos, de modo que la conclusión no dependa de que sean exactos.

*Tabla 1. Supuestos del ambiente real de la empresa.*

| Parámetro | Supuesto | Fundamento |
|---|---|---|
| Trabajadores activos | 60 a 90, repartidos en 4 a 6 obras simultáneas | Cuadrillas por obra y cartera de proyectos (Entregable 1) |
| Movimientos por mes | Hasta 140 en un mes de rotación alta: altas de arranque, rotación entre obras y bajas de cierre | Movimiento constante del personal (Entregable 1) |
| Pico diario | 20 a 30 altas el día que arranca una obra | Las cuadrillas se arman al iniciar cada proyecto |
| Personas que capturan | Hasta 3 a la vez: capturista principal, capturista de apoyo y administración | Requerimiento de que varias personas operen la base (Entregable 1) |
| Equipos | PC de oficina con Windows 10 u 11 y navegador actualizado; una de ellas funciona como servidor | Requerimientos técnicos (Entregable 2) |
| Red | Red local de la oficina; internet solo para cargar el lote en el IDSE | Sistemas de comunicación (Entregable 2) |
| Tipo de trabajador | Mayoría eventual de la construcción (tipo 3) y personal permanente (tipo 1) | Giro de la empresa |
| Salario diario | Del salario mínimo general (315.04 pesos en 2026) a unos 1,200 pesos para supervisores | Supuesto del equipo con el salario mínimo vigente |

*[Imagen]*

*Figura 1. Ambiente real de operación de Sigma: obras, oficina con red local y plataforma IDSE, con el lazo interno (segundos) y el lazo externo (días).*

### Diferencias entre laboratorio y empresa

Las pruebas del Entregable 3 y del Entregable 4 se hicieron en condiciones de laboratorio: un solo usuario, ocho casos escritos a mano, el servidor de desarrollo de Flask y la máquina del propio desarrollador. La Tabla 2 compara esas condiciones con las de la empresa e indica cómo se reprodujo cada diferencia en esta fase.

*Tabla 2. Diferencias entre el laboratorio y la empresa, y forma en que se emularon.*

| Aspecto | Laboratorio (E3 y E4) | Empresa | Cómo se emuló en el E5 |
|---|---|---|---|
| Servidor | Servidor de desarrollo de Flask con depuración activa | Servidor permanente en una PC de la oficina | Servidor de producción waitress; el de desarrollo se midió para comparar |
| Usuarios | Uno a la vez (dos hilos en la prueba de concurrencia) | Hasta 3 capturistas a la vez | Capturistas virtuales concurrentes: 3 en operación nominal y hasta 20 en estrés |
| Acceso | El mismo equipo (localhost) | Otras PC por la red local | Acceso por la IP de la red local y pruebas de seguridad en red |
| Datos | 8 casos escritos a mano | Plantilla con rotación, nombres con acentos y ñ | Plantilla sintética con CURP, RFC y NSS coherentes y con dígito verificador |
| Errores de captura | Errores evidentes (longitud, letras en el NSS) | Errores sutiles: un dígito transpuesto, un punto corrido, un dato pegado con espacios | 128 errores inyectados en 16 categorías y 24 datos válidos con otro formato |
| Interfaz | Valores enviados tal cual | El navegador recorta y limpia lo que se pega | El arnés emula la longitud máxima y las máscaras de captura de la página |
| Historial | Movimientos aislados | Altas, bajas y reingresos del mismo trabajador | Secuencias de alta, baja, reingreso y cambio de obra |
| Plazo legal | No se consideraba | Cinco días hábiles por movimiento | Fechas relativas al día de la prueba, dentro y fuera de plazo |
| Volumen | Menos de 30 registros | Años de historial acumulado | Base precargada con 1,000, 5,000 y 10,000 movimientos |
| Fallas | No se probaban | Cortes de luz o cierre del equipo | Caída abrupta del servidor a media captura |
| Personal | Desarrolladores | Personal administrativo; el encargado anterior era daltónico | Simulación de daltonismo y medición de contraste WCAG |
| Equipo | Laptop de desarrollo | PC de oficina | Equipo de escritorio (Intel Core i5-10400F, 32 GB), más potente que una PC de oficina típica |

El equipo de prueba es más potente que una PC de oficina típica, así que las capacidades medidas deben leerse como el desempeño del software y no como una garantía para cualquier equipo; aun así, los márgenes obtenidos son tan amplios (sección de parámetros) que una PC de oficina los conserva con holgura. Quedan además dos diferencias que no pueden emularse sin la empresa y se declaran fuera del alcance de esta fase: el envío real del lote al IDSE, que exige la firma electrónica del patrón y el layout oficial del archivo, y el lazo externo del acuse del IMSS. Ambas se trasladan a la demostración en ambiente real (TRL 6).

La Figura 2 muestra el ambiente emulado. Cada bloque de pruebas ejecuta una copia aislada del sistema en un directorio temporal, con su propia base SQLite, para que los resultados sean reproducibles y no se mezclen con la base de trabajo.

*[Imagen]*

*Figura 2. Ambiente de prueba emulado: el arnés y el navegador acceden a una copia aislada de Sigma con su propia base de datos.*

### Condiciones de operación

La Tabla 3 resume las condiciones en las que se espera que opere Sigma y las que se aplicaron en las pruebas. En la oficina, el servidor se arranca con python servidor.py, que publica la aplicación con waitress en el puerto 5050 de la red local; la base de datos queda en el mismo equipo y no se expone a la red.

*Tabla 3. Condiciones de operación en la empresa y en las pruebas.*

| Condición | En la empresa | En la prueba |
|---|---|---|
| Servidor de aplicación | waitress con 8 hilos, puerto 5050 | waitress (después); servidor de Flask con depuración (antes) |
| Motor de base de datos | SQLite en el servidor; PostgreSQL cuando la empresa lo instale | SQLite (el equipo de prueba usa Python 3.14, para el que no hay psycopg2 disponible) |
| Usuarios simultáneos | Hasta 3 | 3 con pausas de lectura (nominal); 1, 3, 5, 10 y 20 sin pausa (estrés) |
| Volumen mensual | Hasta 140 movimientos | 140 movimientos en tres etapas, con exportación al cierre de cada una |
| Volumen acumulado | Unos 1,700 movimientos por año | 1,000, 5,000 y 10,000 movimientos (hasta unos seis años) |
| Navegador y pantalla | Chrome o Edge en pantallas de 1366 × 768 o mayores | Chrome 154 a 1366 × 768 |
| Red | Red local; internet solo para el IDSE | Acceso local y por la IP de la red local |
| Plazo legal | 5 días hábiles a partir del día siguiente al movimiento | Movimientos de 0 a 3 días hábiles (en plazo) y de 8 a 15 (vencidos) |
| Energía | Sin UPS (supuesto) | Caída abrupta del proceso del servidor |
| Conservación | 5 años (art. 15, fr. II, LSS) | Historial de hasta 10,000 movimientos |

Para dar por validado el prototipo en este ambiente se fijaron diez criterios de aceptación (Tabla 4). Los tiempos de respuesta se acotaron con los límites de percepción de Nielsen (1993): por debajo de un segundo, el usuario no pierde el hilo de lo que está haciendo.

*Tabla 4. Criterios de aceptación del TRL 5.*

| Clave | Criterio | Meta |
|---|---|---|
| CA5-1 | Operación nominal: un mes de movimientos con 3 capturistas | 0 fallas del servidor; todo lo aceptado llega al lote IDSE y a la bitácora con su usuario |
| CA5-2 | Tiempo de respuesta en operación nominal | p95 de la captura ≤ 500 ms; p95 de la validación en vivo ≤ 200 ms |
| CA5-3 | Detección de errores típicos de captura | ≥ 90 % bloqueados o avisados; 0 falsos positivos; 0 datos válidos rechazados |
| CA5-4 | Capturas simultáneas del mismo movimiento | 0 duplicados en la base; 0 errores 500 |
| CA5-5 | Capacidad | 10 usuarios sin pausa, sin errores y con p95 de la captura ≤ 500 ms |
| CA5-6 | Volumen | Con 10,000 movimientos: tablero p95 ≤ 500 ms; lote de 500 movimientos en ≤ 2 s |
| CA5-7 | Recuperación ante una caída | 0 capturas confirmadas perdidas; base íntegra; servicio de vuelta en ≤ 1 min |
| CA5-8 | Seguridad en la red local | 0 hallazgos en 8 pruebas de configuración, inyección y CSRF |
| CA5-9 | Accesibilidad | Estados identificables sin depender del color; contraste ≥ 4.5:1 (WCAG 2.1 AA) |
| CA5-10 | Regresión | Arnés del Entregable 3: 8 de 8 casos correctos |

### Pruebas realizadas

Las pruebas se automatizaron en el arnés prueba_ambiente_relevante.py, que quedó en el repositorio junto al arnés del Entregable 3 para que cualquier integrante del equipo pueda repetirlas con un solo comando. A diferencia de aquel, que llamaba directamente a las funciones de validación, este arnés trata a Sigma como caja negra: levanta el servidor como proceso independiente y lo usa por HTTP igual que el navegador. Cada capturista virtual valida en vivo al salir de cada campo, envía el formulario y lee la respuesta; antes de enviar, aplica la longitud máxima y las máscaras de captura de la interfaz, para que al servidor llegue exactamente lo que llegaría si el dato se pegara en la página. La Figura 3 muestra un extracto de la ejecución final.

*[Imagen]*

*Figura 3. Extracto de la ejecución del arnés con el código ajustado: capturas simultáneas, caída del servidor y seguridad en red.*

Los datos provienen de una plantilla sintética que imita a la de la empresa: nombres con acentos y ñ, CURP construida con las reglas de RENAPO y con su dígito verificador, RFC coherente con la CURP, NSS con dígito verificador de Luhn, trabajadores eventuales de la construcción y permanentes, y salarios diarios integrados de ayudantes, oficiales electricistas y supervisores calculados con el factor de integración mínimo (383/365). La Tabla 5 resume los bloques de prueba.

*Tabla 5. Bloques de prueba del arnés de ambiente relevante.*

| Bloque | Prueba | Condición de la empresa que reproduce | Volumen |
|---|---|---|---|
| A | Mes de operación simulado | Arranque de obras, rotación de cuadrillas, cierre de obra y reingresos, con exportación del lote al cierre de cada etapa | 140 movimientos, 3 capturistas |
| B | Errores típicos de captura | Datos tecleados o pegados con los errores que comete el personal de oficina | 128 errores en 16 categorías, 24 datos con otro formato y 60 capturas limpias |
| C | Capturas simultáneas | Dos capturistas reciben el mismo aviso del residente y lo registran a la vez | 60 pares en 3 variantes |
| D | Carga | Picos de actividad y margen de crecimiento | 1, 3, 5, 10 y 20 usuarios sin pausa, 15 s por nivel |
| E | Volumen | Años de historial acumulado | 1,000, 5,000 y 10,000 movimientos |
| F | Recuperación | Corte de energía o cierre del servidor a media captura | 5 capturistas activos durante la caída |
| G | Operación en red y seguridad | Acceso desde otras PC de la oficina | 8 pruebas |
| H | Accesibilidad | Personal con daltonismo (Entregable 1) | 14 pares de color en dos temas y simulación de daltonismo |
| E3 | Regresión | Que los ajustes no rompan lo ya validado | 8 casos del Entregable 3 |

Cada bloque se ejecutó dos veces en el mismo equipo el 4 de octubre de 2026: una con el código entregado en el Entregable 4 y su servidor de desarrollo (antes) y otra con el código ajustado y el servidor de producción (después).

### Parámetros de funcionamiento

La Tabla 6 reúne los parámetros medidos en ambas ejecuciones. Los tiempos se reportan con el percentil 95 (p95), es decir, el tiempo dentro del cual se atendió el 95 % de las peticiones, que describe mejor la experiencia del usuario que el promedio.

*Tabla 6. Parámetros de funcionamiento medidos antes y después de los ajustes.*

| Parámetro | Antes (E4) | Después (E5) |
|---|---|---|
| Operación nominal: 3 capturistas, 140 movimientos | Operación nominal: 3 capturistas, 140 movimientos | Operación nominal: 3 capturistas, 140 movimientos |
| Validación en vivo, p50 / p95 | 7.9 / 24.8 ms | 6.2 / 8.3 ms |
| Captura (guardar), p50 / p95 | 15.2 / 31.3 ms | 13.2 / 23.0 ms |
| Tablero después de capturar, p95 | 22.1 ms | 18.1 ms |
| Generación del lote IDSE, máximo | 15.1 ms | 13.9 ms |
| Fallas del servidor | 0 | 0 |
| Carga sin pausa | Carga sin pausa | Carga sin pausa |
| Capturas completadas por minuto, 10 usuarios | 3,809 | 5,931 |
| Captura p95, 10 / 20 usuarios | 100.6 / 497.6 ms | 94.7 / 120.0 ms |
| Captura más lenta, 20 usuarios | 3.3 s | 6.0 s |
| Errores HTTP, todos los niveles | 0 | 0 |
| Memoria del servidor al inicio / con 20 usuarios | 43.3 / 71.7 MB | 44.6 / 67.5 MB |
| Volumen | Volumen | Volumen |
| Tablero p95, 1,000 / 10,000 movimientos | 24.6 / 41.0 ms | 12.9 / 17.9 ms |
| Búsqueda por apellido p95, 10,000 movimientos | 37.7 ms | 24.0 ms |
| Lote de 510 movimientos con 10,000 en la base | 21.0 ms | 23.5 ms |
| Tamaño de la base con 10,000 movimientos | 2.27 MB | 2.52 MB |
| Calidad de la captura | Calidad de la captura | Calidad de la captura |
| Errores inyectados detectados (128) | 50.0 % | 96.9 % |
| Datos válidos rechazados por su formato | 24 de 24 | 0 de 24 |
| Falsos positivos en 60 capturas limpias | 0 | 0 |
| Integridad y recuperación | Integridad y recuperación | Integridad y recuperación |
| Duplicados / errores 500 en 60 pares simultáneos | 5 / 7 | 0 / 0 |
| Capturas confirmadas perdidas tras la caída | 0 de 852 | 0 de 1,250 |
| Arranque del servidor tras la caída | 0.58 s | 0.61 s |

La Figura 4 muestra cómo cambian el tiempo de captura y la capacidad con el número de usuarios simultáneos. Con el servidor de desarrollo, la capacidad se estanca en unas 3,800 capturas por minuto y el p95 de la captura sube a 497.6 ms con 20 usuarios; con waitress, la capacidad llega a unas 5,900 capturas por minuto y el p95 se mantiene en 120.0 ms. Para dimensionarlo: el mes de rotación alta del supuesto suma 140 movimientos, así que el sistema puede capturar en un minuto más de lo que la empresa registraría en tres años.

*[Imagen]*

*Figura 4. Tiempo de captura (p95) y capturas completadas por minuto según el número de usuarios simultáneos, antes y después de los ajustes.*

El tiempo máximo con 20 usuarios sin pausa sí fue alto: una captura tardó 6.0 s (3.3 s antes de los ajustes). La causa es que SQLite admite una sola escritura a la vez y las demás esperan su turno (SQLite Consortium, s.f.). Ocurre solo en una condición casi siete veces mayor que el pico supuesto y no afecta al p95, pero es una de las razones para migrar a PostgreSQL en el siguiente nivel.

El volumen acumulado tampoco degrada la operación (Figura 5): con 10,000 movimientos, unos seis años de operación con el volumen supuesto, el tablero se arma en 17.9 ms y la búsqueda por apellido en 24.0 ms. La base ocupa 2.52 MB, una cantidad que cabe sin problema en cualquier equipo y en cualquier medio de respaldo.

*[Imagen]*

*Figura 5. Tiempo de carga del tablero y de búsqueda (p95) según el número de movimientos almacenados.*

### Resultados

El mes de operación simulado (bloque A) se completó sin una sola falla en ambas versiones: 140 movimientos capturados por tres capturistas a la vez, 140 exportados en tres lotes, todos con su asiento en la bitácora y atribuidos al usuario correcto. El sistema ya funcionaba en el camino normal; las diferencias aparecieron cuando las condiciones dejaron de ser las del laboratorio. La Figura 6 muestra la pantalla principal al terminar la simulación.

La prueba de errores de captura (bloque B) fue la más reveladora. De 128 errores inyectados, la versión del Entregable 4 detectó la mitad (Figura 7): bloqueaba los de formato evidente, pero aceptaba sin advertencia un salario con el punto corrido, un movimiento fuera del plazo legal, un alta para un trabajador que ya estaba dado de alta o una baja anterior a su alta. Además, rechazaba las 24 capturas válidas pegadas con espacios, que es como suele copiarse un NSS. Con los ajustes, la detección subió a 96.9 % sin un solo falso positivo en 60 capturas limpias, y las 24 capturas con otro formato se aceptaron. La Tabla 7 detalla cada categoría.

*[Imagen]*

*Figura 6. Pantalla principal con un mes de operación simulado: 91 movimientos, 11 pendientes de exportar y la bitácora con capturas aceptadas y rechazadas.*

*[Imagen]*

*Figura 7. Resultado de los 128 errores de captura inyectados: bloqueados, avisados y no detectados, antes y después de los ajustes.*

*Tabla 7. Resultado por categoría de error de captura (8 casos por categoría).*

| Categoría | Esperado | Antes (E4) | Después (E5) |
|---|---|---|---|
| B01. CURP y RFC en minúsculas con espacios a los lados | Aceptar | 8 rechazados | 8 aceptados |
| B02. CURP pegada con espacios internos | Aceptar | 8 rechazados | 8 aceptados |
| B03. NSS pegado con espacios de agrupación | Aceptar | 8 rechazados | 8 aceptados |
| B04. CURP con un carácter de menos | Bloquear | 8 bloqueados | 8 bloqueados |
| B05. Letra O en lugar de cero en la CURP | Bloquear | 8 bloqueados | 8 bloqueados |
| B06. CURP con una consonante equivocada (longitud correcta) | Avisar | 8 aceptados sin aviso | 4 avisados, 4 aceptados sin aviso |
| B07. NSS con dos dígitos transpuestos | Avisar | 8 avisados | 8 avisados |
| B08. NSS con un dígito equivocado | Avisar | 8 avisados | 8 avisados |
| B09. RFC con fecha distinta a la de la CURP | Bloquear | 8 bloqueados | 8 bloqueados |
| B10. Nombre con un cero en lugar de la letra O | Bloquear | 8 aceptados sin aviso | 8 bloqueados |
| B11. SDI con el punto decimal corrido (45.05 en vez de 450.50) | Bloquear | 8 aceptados sin aviso | 8 bloqueados |
| B12. SDI mayor al tope de 25 UMA | Avisar | 8 aceptados sin aviso | 8 avisados |
| B13. Alta sin condiciones de contratación | Bloquear | 8 bloqueados | 8 bloqueados |
| B14. Baja sin causa de baja | Bloquear | 8 bloqueados | 8 bloqueados |
| B15. Movimiento capturado fuera del plazo de 5 días hábiles | Avisar | 8 aceptados sin aviso | 8 avisados |
| B16. Alta de un trabajador que ya tiene alta vigente (cambio de obra) | Bloquear | 8 aceptados sin aviso | 8 bloqueados |
| B17. Baja de un trabajador que ya fue dado de baja | Bloquear | 8 aceptados sin aviso | 8 bloqueados |
| B18. Baja con fecha anterior a la de su alta | Bloquear | 8 aceptados sin aviso | 8 bloqueados |
| B19. Movimiento repetido (mismo trabajador, tipo y fecha) | Bloquear | 8 bloqueados | 8 bloqueados |

Las cuatro capturas que siguen sin detectarse son CURP con una consonante cambiada. El dígito verificador de RENAPO suma cada carácter multiplicado por un peso y toma el residuo entre 10, de modo que algunos cambios de letra producen el mismo dígito y pasan inadvertidos; confirmar esos casos exige consultar la CURP en RENAPO, que no ofrece una interfaz pública para hacerlo de forma automática. Es una limitación del algoritmo, no del código, y se trata como riesgo residual.

Las figuras 8 y 9 muestran cómo responde ahora el sistema a tres de estas situaciones: un movimiento fuera de plazo, que se guarda con un aviso que indica cuándo venció, y dos errores que antes se aceptaban y hoy bloquean la captura.

*[Imagen]*

*Figura 8. Aviso no bloqueante de un movimiento capturado fuera del plazo legal de cinco días hábiles, con la fecha en que venció.*

*[Imagen]*

*Figura 9. Respuesta del servidor ante dos errores del ambiente real que la versión anterior aceptaba: (a) salario diario integrado menor al salario mínimo; (b) alta de un trabajador que ya tiene un alta vigente.*

La prueba de accesibilidad (bloque H) atendió directamente la causa que originó el proyecto: la persona encargada del archivo de Excel era daltónica y el estado de cada trabajador se comunicaba solo con el color de la celda. La Figura 10 muestra la tabla de movimientos de Sigma como la vería una persona con deuteranopía o protanopía, simulada con el modelo de Machado et al. (2009): el verde de «Exportado» se vuelve gris y deja de distinguirse por color, pero cada estado y cada tipo de movimiento siguen escritos con texto, por lo que la información no se pierde. La medición de contraste encontró dos combinaciones del tema claro que no alcanzaban el mínimo de 4.5:1 de las WCAG 2.1 (World Wide Web Consortium, 2018): el texto tenue de fechas y ayudas, con 3.15:1 sobre las tarjetas y 2.71:1 sobre el fondo. Tras el ajuste, los 14 pares medidos cumplen.

*[Imagen]*

*Figura 10. Tabla de movimientos con visión típica y con simulación de deuteranopía y protanopía: el estado se sigue leyendo porque está escrito, no solo coloreado.*

Las capturas simultáneas (bloque C) confirmaron un defecto que en el laboratorio nunca apareció: cuando dos capturistas registran el mismo movimiento al mismo tiempo, ambos pasan la revisión de duplicados antes de que cualquiera de los dos guarde. Con la versión anterior, 5 de 25 reingresos quedaron duplicados en la base y 7 de 25 altas de trabajadores nuevos terminaron en un error 500. Con la restricción de unicidad en la base de datos, en los 60 pares uno se guardó y el otro recibió un mensaje claro, sin duplicados ni errores.

La caída abrupta del servidor (bloque F) no perdió ninguna captura confirmada en ninguna de las dos versiones: las 1,250 capturas que recibieron confirmación antes del cierre seguían en la base, ésta pasó la verificación de integridad y ningún movimiento quedó sin su asiento en la bitácora. Las 5 peticiones que estaban en curso durante la caída no recibieron respuesta, por lo que el capturista sabe que debe repetirlas; el servidor volvió a atender 0.61 s después de reiniciarse. Este resultado valida en condiciones adversas el diseño transaccional del Entregable 4.

La operación en red (bloque G) reveló cinco problemas de configuración con el servidor de desarrollo, que se describen en la sección siguiente; con el servidor de producción y los ajustes, las ocho pruebas resultaron seguras.

### Errores detectados

La Tabla 8 reúne los errores que el ambiente relevante sacó a la luz. Ninguno se había manifestado en las 20 pruebas de laboratorio del Entregable 4, porque todos dependen de una condición propia de la empresa: varios usuarios, la red local, datos pegados, el historial de un trabajador o el calendario legal. La severidad se asignó según el efecto en la empresa: alta si puede provocar una multa, una pérdida de datos o un acceso indebido; media si produce un dato incorrecto o un error visible; baja si solo afecta la comodidad o la presentación.

*Tabla 8. Errores detectados en el ambiente relevante.*

| Clave | Error | Cómo se reveló | Severidad | Estado |
|---|---|---|---|---|
| E-01 | El servidor de desarrollo, con depuración activa, publicaba en la red local la consola de Werkzeug (/console) y su versión en la cabecera Server | Bloque G, acceso por la IP de la red local | Alta | Corregido |
| E-02 | Un folio fuera de rango en /api/movimiento producía un error 500 con el detalle técnico | Bloque G | Media | Corregido |
| E-03 | Una captura enviada desde otro sitio (CSRF) se guardaba | Bloque G | Alta | Corregido |
| E-04 | Las respuestas no llevaban cabeceras de seguridad (CSP, nosniff, X-Frame-Options) | Bloque G | Media | Corregido |
| E-05 | Dos capturas simultáneas del mismo movimiento dejaban duplicados (5 de 25) o un error 500 (7 de 25) | Bloque C | Alta | Corregido |
| E-06 | Pegar la CURP o el NSS con espacios recortaba el dato: 24 de 24 capturas válidas rechazadas | Bloque B, emulación del navegador | Media | Corregido |
| E-07 | La validación en vivo y el servidor limpiaban distinto: el NSS con espacios y la fecha con diagonales se marcaban como error en vivo y el servidor los aceptaba | Bloque B, envío sin JavaScript | Baja | Corregido |
| E-08 | Se aceptaba un salario diario integrado menor al salario mínimo (punto corrido) | Bloque B (B11) | Alta | Corregido |
| E-09 | Un salario mayor al tope de 25 UMA se aceptaba sin aviso y se exportaba sin topar | Bloque B (B12) | Media | Corregido |
| E-10 | Un movimiento fuera del plazo de cinco días hábiles no generaba ningún aviso | Bloque B (B15) | Alta | Corregido |
| E-11 | Se aceptaban un alta sobre un alta vigente, la baja de alguien ya dado de baja y una baja anterior a su alta | Bloque B (B16 a B18) | Alta | Corregido |
| E-12 | El nombre admitía dígitos (un cero en lugar de la letra O) | Bloque B (B10) | Baja | Corregido |
| E-13 | Una letra equivocada en la CURP con formato válido no se detectaba | Bloque B (B06) | Media | Corregido en parte (4 de 8) |
| E-14 | El texto tenue tenía contraste de 3.15:1 y 2.71:1, bajo el mínimo de 4.5:1 | Bloque H | Baja | Corregido |
| E-15 | Mensaje sin concordancia: «La causa de baja es obligatorio» | Bloque B (B14) | Baja | Corregido |
| E-16 | Con 20 usuarios sin pausa, una captura llegó a tardar 6.0 s por la espera de escritura de SQLite | Bloque D | Baja | Planeado (TRL 6) |
| E-17 | No hay autenticación: el usuario que captura se elige de una lista | Revisión de seguridad | Alta | Planeado (TRL 6) |
| E-18 | El tráfico en la red local viaja sin cifrar (HTTP) | Revisión de seguridad | Media | Planeado (TRL 6) |
| E-19 | No hay respaldo automático: la base es un archivo en una sola PC | Análisis del bloque F | Alta | Planeado (TRL 6) |
| E-20 | El layout del lote IDSE no está confirmado contra el instructivo oficial (campos delimitados, sin nombre del trabajador, UTF-8) | Revisión del lote exportado | Alta | Planeado (TRL 6) |

### Ajustes

Cada error corregido se atendió con un cambio en el código, versionado en la rama trl5/ambiente-relevante del repositorio (github.com/rkiverr/sigma-imss), y se verificó volviendo a ejecutar el mismo bloque de pruebas que lo había revelado:

- Servidor de producción (E-01 y E-02). Se agregó servidor.py, que publica la aplicación con waitress, un servidor WSGI de producción que funciona en Windows sin componentes nativos (Pylons Project, s.f.). app.py quedó solo para desarrollo: escucha únicamente en el propio equipo y activa la depuración solo si se pide de forma expresa con SIGMA_DEBUG=1. Verificación: la consola de depuración responde 404 y la cabecera del servidor ya no revela versiones.

- Protección contra capturas desde otros sitios (E-03). Toda captura o exportación cuyo origen (cabecera Origin o Referer) no sea la propia página de Sigma se rechaza con el código 403. Verificación: la captura enviada desde otro sitio ya no se guarda (Figura 11).

- Cabeceras de seguridad (E-04). Cada respuesta incluye una política de seguridad de contenido con un valor único por petición, que solo permite ejecutar los scripts del propio sistema, además de X-Content-Type-Options, X-Frame-Options y Referrer-Policy.

- Folio fuera de rango (E-02). La consulta del detalle responde 404 cuando el folio rebasa el máximo que admite la base, en lugar de un error 500.

- Restricción de unicidad del movimiento (E-05). Se agregó un índice único sobre trabajador, tipo y fecha del movimiento, que la base aplica aunque dos capturas lleguen al mismo tiempo. Si ocurre, la transacción se revierte y el capturista recibe una respuesta 422 que le pide revisar la tabla. Verificación: 60 pares simultáneos, 0 duplicados y 0 errores 500.

- Normalización única de lo capturado (E-06 y E-07). Una sola función limpia los datos para el formulario y para la validación en vivo: quita espacios y guiones de la CURP, el RFC y el NSS y deja la fecha solo con dígitos. En la interfaz, la longitud máxima se aplica después de limpiar y no antes. Verificación: 24 de 24 datos pegados con espacios aceptados y validación en vivo coherente con el servidor.

- Límites legales del salario (E-08 y E-09). El salario diario integrado menor al salario mínimo general se bloquea y el mayor a 25 UMA genera un aviso; en el lote IDSE se exporta el salario topado, como lo exige el artículo 28 de la LSS. Los montos de cada año quedan en una tabla del código: 315.04 pesos de salario mínimo (Comisión Nacional de los Salarios Mínimos, 2025) y 117.31 pesos de UMA (Instituto Nacional de Estadística y Geografía, 2026) para 2026.

- Plazo legal (E-10). El nuevo módulo plazo.py cuenta los días hábiles transcurridos desde el movimiento, descontando fines de semana y los días de descanso obligatorio del artículo 74 de la Ley Federal del Trabajo, y avisa cuando el plazo de cinco días está por vencer o ya venció. En una captura a tiempo, el mensaje de confirmación indica la fecha límite para presentarla en el IDSE. La lógica proviene de la versión alterna de la prueba de concepto del Entregable 3.

- Reglas de historial afiliatorio (E-11). Antes de guardar, el sistema consulta el último movimiento del trabajador y rechaza un alta si ya tiene una vigente, una baja si ya fue dado de baja y cualquier baja o reingreso con fecha anterior al movimiento previo. La baja de alguien sin historial en Sigma, como el personal contratado antes de su puesta en marcha, solo genera un aviso.

- Validación del nombre y de la CURP (E-12, E-13 y E-15). El nombre ya no admite dígitos ni símbolos; la CURP se contrasta con su dígito verificador y, si no coincide, se avisa al capturista; se corrigió la concordancia de los mensajes de catálogo.

- Contraste del texto (E-14). El color del texto tenue pasó de #8492a9 a #5c6b84, que alcanza 5.4:1 sobre las tarjetas y 4.6:1 sobre el fondo.

Después de los ajustes se volvió a ejecutar el arnés del Entregable 3, que siguió dando 8 de 8 casos correctos, y el arnés completo de esta fase, con los resultados ya reportados.

Se documentan como trabajo planeado, no como ajuste correctivo, los errores E-16 a E-20: la autenticación de usuarios con contraseña, el cifrado HTTPS dentro de la red local, el respaldo automático de la base, la migración a PostgreSQL para repartir mejor las escrituras simultáneas y la confirmación del layout del archivo contra el instructivo oficial del IDSE.

### Análisis de riesgos

Los riesgos se evaluaron con una matriz de probabilidad por impacto, ambas en escala de 1 (baja) a 3 (alta); el producto clasifica el riesgo como alto (6 a 9), medio (3 a 4) o bajo (1 a 2). La Tabla 9 retoma los tres riesgos iniciales del Entregable 2, agrega los que surgieron en esta fase e indica el nivel residual, después de las mitigaciones ya implementadas.

*Tabla 9. Matriz de riesgos con su nivel residual.*

| Clave | Riesgo | P | I | Nivel | Mitigación | Estado |
|---|---|---|---|---|---|---|
| R-01 | El layout del lote no coincide con el oficial del IDSE y el IMSS rechaza el lote completo | 3 | 3 | Alto (9) | Conseguir con la empresa el instructivo oficial; definir el layout como tabla configurable; probar primero con un lote de un solo movimiento | Abierto |
| R-02 | Pérdida de la base por una falla del equipo servidor | 2 | 3 | Alto (6) | Respaldo diario automático a otro equipo y UPS en el servidor; la caída abrupta ya no pierde capturas confirmadas | Planeado |
| R-03 | Suplantación de usuario: la bitácora registra quién captura, pero no lo comprueba | 2 | 3 | Alto (6) | Inicio de sesión con contraseña cifrada y roles | Planeado |
| R-04 | Aviso tardío del residente de obra: movimiento extemporáneo y multa de 20 a 350 UMA | 2 | 2 | Medio (4) | Aviso de plazo y fecha límite en cada captura; acordar con los residentes avisar el mismo día | Mitigado en parte |
| R-05 | Un error de captura pasa la validación (una letra de la CURP, un nombre mal escrito) | 2 | 2 | Medio (4) | Avisos por dígito verificador; confirmar contra el documento; el acuse del IMSS como medición final | Mitigado en parte |
| R-06 | Exposición de datos personales en la red local | 1 | 3 | Medio (3) | Servidor de producción sin depuración, base no expuesta, CSRF bloqueado y cabeceras de seguridad; falta HTTPS | Mitigado en parte |
| R-07 | Cambios o caídas de la plataforma del IMSS (Entregable 2) | 2 | 2 | Medio (4) | Los lotes se conservan con marca de tiempo y pueden cargarse después; el aviso de plazo indica el margen restante | Mitigado en parte |
| R-08 | Montos de salario mínimo y UMA desactualizados al cambiar el año | 2 | 2 | Medio (4) | Tabla de montos por año en el código; actualizarla en enero y febrero | Procedimiento |
| R-09 | Migración de los datos históricos del Excel (Entregable 2) | 2 | 2 | Medio (4) | La baja de un trabajador sin historial solo genera aviso; cargar la plantilla vigente como altas iniciales | Mitigado en parte |
| R-10 | Resistencia al cambio del personal administrativo (Entregable 2) | 2 | 1 | Bajo (2) | Mensajes en lenguaje llano por campo, validación en vivo y capacitación breve | Mitigado |
| R-11 | Saturación por usuarios simultáneos o por volumen | 1 | 2 | Bajo (2) | Margen medido muy superior al supuesto (bloques D y E); PostgreSQL en TRL 6 | Mitigado |
| R-12 | Duplicados por capturas simultáneas | 1 | 2 | Bajo (2) | Restricción de unicidad en la base (bloque C) | Mitigado |

### Consideraciones de seguridad

Por ser un proyecto de software, Sigma no presenta riesgos eléctricos ni mecánicos para quien lo opera. Su relación con la seguridad de las personas es indirecta pero seria: el sistema existe para que los trabajadores, expuestos a riesgo eléctrico y a trabajo en altura, estén asegurados ante el IMSS desde el primer día (Entregable 1). Un alta que no se presenta a tiempo deja a un trabajador sin cobertura y a la empresa obligada a cubrir el costo de un accidente. Por eso el plazo legal y la coherencia del historial se trataron en esta fase como requisitos de seguridad y no solo de comodidad.

En cuanto a la seguridad de la información, el sistema maneja datos personales de los trabajadores (nombre, CURP, NSS, RFC y salario). Las consideraciones se organizaron con la lista OWASP Top 10:2025 (OWASP Foundation, 2025):

- Configuración insegura (A02). Fue el problema más grave encontrado: el servidor de desarrollo publicaba en toda la red local una consola de depuración y el detalle técnico de los errores. Se resolvió con el servidor de producción y la depuración apagada por omisión.

- Control de acceso (A01). Las capturas enviadas desde otros sitios se rechazan (Figura 11). Sigue pendiente el control de acceso por usuario: hoy cualquier persona con acceso a la red local puede abrir el sistema.

- Inyección (A05). Todas las consultas a la base usan parámetros, las plantillas escapan el texto y la política de contenido impide ejecutar scripts ajenos. Las pruebas de inyección SQL y de código en el nombre no tuvieron efecto.

- Autenticación (A07). No existe todavía; el usuario se elige de una lista. Es el primer pendiente de seguridad para TRL 6.

- Registro y alertas (A09). Cada captura, rechazo y exportación queda en la bitácora con usuario y hora; falta protegerla contra modificaciones hechas directamente en la base.

- Manejo de condiciones excepcionales (A10). Los errores de la base, los folios fuera de rango y las capturas simultáneas producen respuestas controladas (404, 422 o 503) sin exponer información interna.

Fuera del software se recomiendan tres medidas físicas y administrativas, en línea con el artículo 18 de la LFPDPPP: ubicar el equipo servidor en un área de acceso restringido, cifrar su disco y limitar el uso del sistema al personal de recursos humanos. La firma electrónica del patrón nunca se almacena en Sigma: el lote se carga manualmente en el IDSE, de modo que una falla del sistema no compromete la firma de la empresa.

*[Imagen]*

*Figura 11. Página que muestra Sigma cuando recibe una captura enviada desde otro sitio: la solicitud se rechaza y no se guarda nada.*

### Consideraciones normativas

La Tabla 10 relaciona las disposiciones aplicables con la forma en que Sigma las atiende. Las citas corresponden al texto vigente de cada ordenamiento, consultado en octubre de 2026.

*Tabla 10. Disposiciones normativas aplicables y forma en que Sigma las atiende.*

| Norma | Disposición | Cómo la atiende Sigma |
|---|---|---|
| LSS, art. 15, fr. I | Comunicar altas y bajas en plazos no mayores de cinco días hábiles | Aviso de plazo por vencer o vencido y fecha límite en cada captura (plazo.py) |
| LSS, art. 15, fr. II | Conservar los registros durante los cinco años siguientes | Movimientos y bitácora se conservan sin borrado; el respaldo automático queda planeado |
| LSS, art. 28 | El salario base de cotización tiene como límite inferior el salario mínimo y como superior 25 veces el salario mínimo del Distrito Federal, referencia que desde la reforma constitucional de 2016 se entiende hecha a la UMA | Error si el SDI es menor al salario mínimo; aviso si supera el tope; el lote lleva el SDI topado |
| LSS, arts. 304 A, fr. II, y 304 B, fr. IV | Inscribir de forma extemporánea es infracción y se multa con 20 a 350 veces la UMA (de 2,346.20 a 41,058.50 pesos en 2026) | Justifica tratar el plazo como dato de control y no como recordatorio |
| RACERF, art. 45 | La inscripción puede hacerse desde el día hábil anterior al inicio de la relación laboral; los salarios se comunican sin exceder los límites del art. 28 | Se admiten fechas futuras cercanas; el lote lleva el salario topado |
| RACERF, art. 46 | Cinco o más movimientos en una sola exhibición se presentan por medios no impresos | Sigma agrupa los movimientos pendientes en un lote electrónico |
| RACERF, art. 47 | El aviso de inscripción debe contener la CURP del trabajador | CURP obligatoria, con validación de formato, fecha de nacimiento y dígito verificador |
| LFT, art. 74 | Días de descanso obligatorio | Se descuentan al contar los días hábiles del plazo |
| LFPDPPP (DOF 20/03/2025), arts. 14, 15, 18 y 19 | Aviso de privacidad; medidas de seguridad administrativas, técnicas y físicas; aviso de vulneraciones | Medidas técnicas implementadas; el aviso de privacidad a los trabajadores corresponde a la empresa antes de la operación con datos reales |
| WCAG 2.1, criterios 1.4.1 y 1.4.3 | No transmitir información solo con color; contraste mínimo de 4.5:1 | Estados escritos con texto; 14 de 14 pares de color cumplen |
| ISO/IEC 25010:2023 | Modelo de calidad del producto de software | Marco de la evaluación del desempeño (sección siguiente) |

### Evaluación del desempeño

La Tabla 11 compara los resultados con los criterios de aceptación de la Tabla 4. La versión del Entregable 4 cumplía seis de los diez; la versión ajustada cumple los diez.

*Tabla 11. Cumplimiento de los criterios de aceptación del TRL 5.*

| Criterio | Meta | Antes (E4) | Después (E5) |
|---|---|---|---|
| CA5-1 Operación nominal | 0 fallas; todo al lote y a la bitácora | 140 de 140, 0 fallas · cumple | 140 de 140, 0 fallas · cumple |
| CA5-2 Tiempo de respuesta | Captura ≤ 500 ms; validación ≤ 200 ms (p95) | 31.3 / 24.8 ms · cumple | 23.0 / 8.3 ms · cumple |
| CA5-3 Detección de errores | ≥ 90 %; 0 falsos positivos; 0 rechazos indebidos | 50.0 %; 0; 24 · no cumple | 96.9 %; 0; 0 · cumple |
| CA5-4 Capturas simultáneas | 0 duplicados; 0 errores 500 | 5; 7 · no cumple | 0; 0 · cumple |
| CA5-5 Capacidad | 10 usuarios sin errores, p95 ≤ 500 ms | 0 errores; 100.6 ms · cumple | 0 errores; 94.7 ms · cumple |
| CA5-6 Volumen | Tablero ≤ 500 ms; lote ≤ 2 s (10,000 movimientos) | 41.0 ms; 21.0 ms · cumple | 17.9 ms; 23.5 ms · cumple |
| CA5-7 Recuperación | 0 perdidas; base íntegra; ≤ 1 min | 0; íntegra; 0.58 s · cumple | 0; íntegra; 0.61 s · cumple |
| CA5-8 Seguridad en red | 0 hallazgos en 8 pruebas | 5 hallazgos · no cumple | 0 hallazgos · cumple |
| CA5-9 Accesibilidad | Estados con texto; contraste ≥ 4.5:1 | 2 pares bajo 4.5:1 · no cumple | 14 de 14 pares · cumple |
| CA5-10 Regresión | 8 de 8 casos del Entregable 3 | 8 de 8 · cumple | 8 de 8 · cumple |

Más allá de los criterios, el desempeño se evaluó con las características de calidad del modelo ISO/IEC 25010:2023 (International Organization for Standardization, 2023):

- Adecuación funcional. El sistema completó el ciclo del mes simulado (captura, validación, exportación y bitácora) y ahora aplica las reglas que dependen del calendario y del historial, que eran el origen de los errores del archivo de Excel.

- Eficiencia de desempeño. En operación nominal el sistema añade 23.0 ms por captura (p95): el tiempo de cada movimiento lo marca la persona que teclea, no el sistema. Con 10,000 movimientos ninguna operación medida pasa de 25 ms.

- Compatibilidad. Funcionó desde Chrome por la IP de la red local, sin depender de internet para capturar, y acepta los datos tal como se copian de otros documentos.

- Capacidad de interacción. Los mensajes indican el campo y la causa del error en lenguaje llano; la información no depende del color y el contraste cumple las WCAG 2.1 AA.

- Fiabilidad. Ninguna caída perdió capturas confirmadas y el servicio vuelve en menos de un segundo; las capturas simultáneas ya no producen errores ni duplicados.

- Seguridad. Se cerraron los cinco hallazgos de configuración; la autenticación y el cifrado quedan como pendientes declarados.

- Mantenibilidad. Las pruebas son reproducibles con un solo comando y quedaron en el repositorio, junto con el registro de cada decisión en el archivo de contexto del proyecto.

Frente al proceso actual, la diferencia es de naturaleza y no solo de grado. En el archivo de Excel ninguno de los 128 errores inyectados se habría detectado al capturar, porque el archivo no valida datos (Entregable 1): se habrían descubierto hasta que el IMSS rechazara el movimiento o hasta recibir una multa. Sigma detecta el 96.9 % en el momento de la captura, bloquea antes de guardar el 69 % de ellos y marca con texto, no solo con color, el estado de cada movimiento.

Con estos resultados, el prototipo alcanza el nivel TRL 5: sus componentes integrados se validaron en un ambiente que reproduce las condiciones de operación de la empresa (usuarios simultáneos en red local, plantilla y rotación representativas, errores de captura reales, plazo legal, volumen de años y fallas del servidor) y cumplen los diez criterios de aceptación. Para avanzar a la demostración en ambiente real (TRL 6) quedan cinco trabajos: autenticación de usuarios, cifrado HTTPS en la red local, respaldo automático de la base, migración a PostgreSQL y, sobre todo, la confirmación del layout del lote contra el instructivo oficial del IDSE, que es el riesgo principal del proyecto. Resueltos estos puntos, el siguiente paso es una prueba piloto en la oficina con datos reales, previo aviso de privacidad a los trabajadores, en la que el acuse del IMSS cierre por primera vez el lazo externo del sistema.

### Referencias

- Cámara de Diputados del H. Congreso de la Unión. (2005). Reglamento de la Ley del Seguro Social en Materia de Afiliación, Clasificación de Empresas, Recaudación y Fiscalización. https://www.diputados.gob.mx/LeyesBiblio/regley/Reg_LSS_MACERF.pdf

- Cámara de Diputados del H. Congreso de la Unión. (2025). Ley Federal de Protección de Datos Personales en Posesión de los Particulares. https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf

- Cámara de Diputados del H. Congreso de la Unión. (2026). Ley del Seguro Social. https://www.diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf

- Cámara de Diputados del H. Congreso de la Unión. (s.f.). Ley Federal del Trabajo. https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf

- Comisión Nacional de los Salarios Mínimos. (2025). Salarios mínimos 2026. https://www.gob.mx/conasami

- Instituto Mexicano del Seguro Social. (s.f.). IDSE — IMSS desde su empresa. https://idse.imss.gob.mx/

- Instituto Nacional de Estadística y Geografía. (2026). Unidad de Medida y Actualización (UMA). https://www.inegi.org.mx/temas/uma/

- International Organization for Standardization. (2023). ISO/IEC 25010:2023. Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model. https://www.iso.org/standard/78176.html

- Machado, G. M., Oliveira, M. M., & Fernandes, L. A. F. (2009). A physiologically-based model for simulation of color vision deficiency. IEEE Transactions on Visualization and Computer Graphics, 15(6), 1291–1298. https://doi.org/10.1109/TVCG.2009.113

- Mankins, J. C. (1995). Technology readiness levels: A white paper. NASA, Office of Space Access and Technology.

- Nielsen, J. (1993). Response times: The 3 important limits. Nielsen Norman Group. https://www.nngroup.com/articles/response-times-3-important-limits/

- OWASP Foundation. (2025). OWASP Top 10:2025. https://top10.owasp.org/2025/

- Pylons Project. (s.f.). Waitress documentation. https://docs.pylonsproject.org/projects/waitress/

- SQLite Consortium. (s.f.). Write-Ahead Logging. https://www.sqlite.org/wal.html

- World Wide Web Consortium. (2018). Web Content Accessibility Guidelines (WCAG) 2.1. https://www.w3.org/TR/WCAG21/
