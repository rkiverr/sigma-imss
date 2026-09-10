# Cómo funciona Sigma

Explicación de qué hace la página y cómo se usa. Pensado para alguien que llega
al proyecto por primera vez.

Para instalarla y arrancarla, ve a [Ejecutar.md](Ejecutar.md).

---

## 1. El problema que resuelve

Cuando una empresa contrata o da de baja a un trabajador, tiene que avisarle al
IMSS. Ese aviso se llama **movimiento afiliatorio** y se manda por una
plataforma llamada **IDSE**.

Hacerlo a mano tiene tres problemas:

1. **Se cometen errores de dedo.** Una CURP mal escrita o una fecha inválida
   hace que el IMSS rechace el movimiento, con multas y recargos de por medio.
2. **El formato del archivo es rígido.** El IDSE recibe un archivo de texto con
   los campos en un orden exacto.
3. **No queda rastro.** Si algo sale mal, no se sabe quién capturó qué ni cuándo.

Sigma ataca los tres: **valida antes de guardar**, **arma el archivo solo** y
**registra cada acción con usuario y hora**.

---

## 2. Los dos movimientos que maneja

| Clave | Movimiento | Cuándo se usa |
|---|---|---|
| **08** | Alta / Reingreso | Entra un trabajador nuevo o regresa uno anterior |
| **02** | Baja | Se va un trabajador |

Cada uno pide datos distintos, y **el formulario se adapta solo** al que elijas:

- En un **alta** pide las condiciones de contratación: tipo de trabajador, tipo
  de salario, tipo de jornada y salario diario integrado (SDI).
- En una **baja** pide la causa, tomada del catálogo oficial del IDSE
  (término de contrato, separación voluntaria, defunción, etc.).

No tienes que acordarte de cuál va con cuál: los campos que no aplican
desaparecen de la pantalla.

---

## 3. Recorrido por la pantalla

### Barra superior

- **Registro patronal** de la empresa que manda los movimientos.
- **Motor de base de datos** activo (PostgreSQL o SQLite).
- **Botón de tema**: cambia entre claro y oscuro. Arranca siguiendo la
  configuración de tu sistema operativo y recuerda tu elección.

### Tablero de métricas

Cinco tarjetas con el estado del sistema de un vistazo:

| Tarjeta | Qué cuenta |
|---|---|
| Movimientos capturados | Total guardado, más los intentos rechazados |
| Pendientes de exportar | Válidos que todavía no van en ningún lote |
| Exportados a IDSE | Ya incluidos en un lote |
| Altas (08) / Bajas (02) | Desglose por tipo |

### Captura de movimiento

El formulario principal. Los campos marcados con **\*** son obligatorios.

Mientras escribes, la página va marcando cada campo:

- **Borde rojo con mensaje** → hay que corregirlo, no deja guardar.
- **Borde ámbar** → es un aviso, sí deja guardar (ver sección 5).
- **Borde verde** → el campo está correcto.

Ayudas de captura:

- La **CURP** y el **RFC** se convierten a mayúsculas solas y no aceptan
  símbolos raros.
- El **NSS** y la **fecha** solo aceptan números.
- Un **contador** al lado de cada etiqueta te dice cuántos caracteres llevas
  (`8/18`, por ejemplo).
- El campo **Elegir en calendario** abre un calendario normal y rellena solo la
  fecha en el formato `DDMMAAAA` que exige el IDSE.

Si algo falla al enviar, la página te devuelve un resumen arriba con todo lo que
hay que corregir **sin borrar lo que ya habías escrito**.

### Exportación a IDSE

Toma todos los movimientos válidos que aún no se han enviado y arma el archivo
de texto plano. Cada línea es un movimiento, con los campos separados por `|`:

```
A1234567890|08|RIDG050515HNLVLL09|12345678901|RIDG050515AB1|05092026|3|0|1|450.50|
```

El orden de los campos es: registro patronal, tipo de movimiento, CURP, NSS,
RFC, fecha, tipo de trabajador, tipo de salario, tipo de jornada, SDI y causa
de baja.

Al generar el lote, esos movimientos pasan de **Válido** a **Exportado** y ya no
se vuelven a incluir en lotes futuros. El botón **Descargar** te baja el último
archivo generado.

> ⚠️ **Importante:** la estructura de este archivo es una representación para la
> prueba de concepto. Antes de usarla de verdad hay que confirmarla contra el
> layout oficial vigente que publica el IMSS.

### Bitácora de auditoría

Las últimas 15 acciones del sistema, cada una con **quién**, **cuándo** y **qué**.
Registra tanto lo que se guardó como **los intentos rechazados y por qué**, que
es justo lo que sirve para detectar dónde se equivoca la gente al capturar.

### Movimientos capturados

La tabla con todo lo registrado, del más reciente al más antiguo.

- **Buscador** por nombre, CURP o NSS.
- **Filtros** por estado (pendientes / exportados) y por tipo (altas / bajas).
- **Haz clic en cualquier fila** para abrir el expediente completo con todos sus
  datos y su propia bitácora.
- Se pagina de 25 en 25.

Los tres estados posibles:

| Estado | Significa |
|---|---|
| **Válido** | Pasó las validaciones, espera a ser exportado |
| **Exportado** | Ya se incluyó en un lote IDSE |
| **Rechazado** | No pasó las validaciones (queda en la bitácora) |

---

## 4. Qué se valida antes de guardar

Estas reglas **bloquean** el guardado:

| Campo | Regla |
|---|---|
| **Nombre completo** | Obligatorio, mínimo 5 caracteres |
| **CURP** | 18 caracteres con el formato oficial, y la fecha de nacimiento que lleva dentro debe existir en el calendario |
| **NSS** | Exactamente 11 dígitos |
| **RFC** | 12 o 13 caracteres, y debe coincidir en iniciales y fecha con la CURP |
| **Fecha del movimiento** | Formato `DDMMAAAA` y fecha real (un 31 de febrero se rechaza) |
| **Tipo de movimiento** | Solo `08` o `02` |
| **Alta (08)** | Tipo de trabajador, de salario, de jornada y SDI obligatorios |
| **Baja (02)** | Causa de baja obligatoria, del catálogo IDSE |
| **SDI** | Número entre 1.00 y 10,000.00 |

Y estas reglas de integridad:

- **Un NSS no se puede repetir** entre dos trabajadores distintos.
- **Una CURP ya registrada con otro NSS** se detecta y se avisa.
- **No se puede capturar dos veces el mismo movimiento** (mismo trabajador,
  mismo tipo, misma fecha).

---

## 5. Avisos que no bloquean

Hay dos comprobaciones que **advierten pero dejan pasar**:

- **Dígito verificador del NSS.** El último dígito del NSS se calcula con el
  algoritmo de Luhn. Si no cuadra, te avisa — pero no bloquea, porque existen
  NSS antiguos, emitidos antes de que se estandarizara ese dígito, que son
  perfectamente válidos.
- **Fechas lejanas.** Si la fecha está a más de un año en el futuro o tiene más
  de cinco años de antigüedad, te pide que la confirmes.

Es una distinción a propósito: **un error impide guardar, un aviso solo pide que
lo confirmes.**

---

## 6. Cómo está armado por dentro

Aplicación web en **Python + Flask**, con cuatro capas separadas:

```
Navegador  ──►  app.py  ──►  validaciones.py  ──►  database.py
(HTML/CSS/JS)   (rutas)      (reglas)             (PostgreSQL o SQLite)
                                 │
                                 ▼
                          exportar_idse.py
                          (archivo del lote)
```

| Archivo | Qué hace |
|---|---|
| `app.py` | Recibe las peticiones y coordina todo |
| `validaciones.py` | Todas las reglas de validación |
| `database.py` | Guarda y consulta en la base de datos |
| `exportar_idse.py` | Arma el archivo del lote |
| `templates/` | Las pantallas (HTML) |
| `static/` | Estilos (CSS) y comportamiento del navegador (JS) |

Dos detalles que vale la pena conocer:

**El navegador y el servidor usan el mismo validador.** Cuando escribes en el
formulario, la página le pregunta al servidor (`/api/validar`) en vez de tener
su propia copia de las reglas. Así es imposible que la ayuda visual diga una
cosa y el servidor haga otra.

**La página funciona sin JavaScript.** Las máscaras, la validación en vivo y el
diálogo de detalle son comodidades; si el navegador no ejecuta JavaScript, el
formulario se envía igual y el servidor valida igual. Tampoco usa librerías
externas ni CDN: funciona sin conexión a internet.

---

## 7. Base de datos

Cinco tablas normalizadas:

| Tabla | Guarda |
|---|---|
| `patron` | La empresa (registro patronal y razón social) |
| `usuario` | Quién puede capturar (administrador o captura) |
| `trabajador` | El expediente de cada persona (CURP, NSS, RFC) |
| `movimiento` | Cada alta o baja, ligada a un trabajador y un patrón |
| `bitacora` | Cada acción, ligada a un usuario y opcionalmente a un movimiento |

Un trabajador se registra **una sola vez** y puede tener varios movimientos a lo
largo del tiempo (un alta, luego una baja, luego un reingreso). Por eso
`trabajador` y `movimiento` son tablas separadas.

---

## 8. Lo que todavía no hace

Es una prueba de concepto (TRL 3), así que hay límites conocidos:

- **No hay login.** El usuario se elige de un desplegable, así que la bitácora
  documenta la autoría pero no la demuestra. Para producción haría falta
  autenticación real.
- **No se conecta al IDSE.** Genera el archivo, pero subirlo sigue siendo
  manual.
- **El formato del archivo está por confirmar** contra el layout oficial del
  IMSS.
- **Maneja un solo patrón.** El modelo de datos soporta varios, pero la interfaz
  usa el primero.
