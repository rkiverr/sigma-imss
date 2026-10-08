# Cómo levantar la página web

Guía paso a paso para poner Sigma a correr en tu computadora.

---

## Lo que necesitas

- **Python 3.9 o superior.** Compruébalo con:

  ```bash
  python --version
  ```

  Si te dice "no se reconoce el comando", instálalo desde
  <https://www.python.org/downloads/> y **marca la casilla "Add Python to PATH"**
  durante la instalación.

- Nada más. No necesitas instalar PostgreSQL (más abajo se explica por qué).

---

## Arranque en 4 pasos

### 1. Abre una terminal en la carpeta del proyecto

En Windows: entra a la carpeta `sigma-imss`, haz clic derecho en un espacio
vacío y elige **"Abrir en Terminal"**.

### 2. Instala las dependencias (solo la primera vez)

```bash
pip install -r requirements.txt
```

### 3. Asigna las contraseñas (solo la primera vez)

Sigma pide inicio de sesión. Los usuarios `admin.rrhh` (administrador) y
`captura.obra1` (captura) ya existen, pero sin contraseña:

```bash
python -m sigma.usuarios contrasena admin.rrhh
python -m sigma.usuarios contrasena captura.obra1
```

Te pide la contraseña dos veces (mínimo 8 caracteres). Para más personas:
`python -m sigma.usuarios crear <usuario> captura` (o `administrador`), y
`python -m sigma.usuarios listar` para ver quién existe.

### 4. Arranca el servidor

```bash
python servidor.py
```

Verás algo así:

```
[sigma] Respaldo al arrancar: …\respaldos\sigma_imss_20261007_190000.db
[sigma] Motor de datos: SQLite - sigma_imss.db
[sigma] Servidor de producción (waitress, 8 hilos) en http://0.0.0.0:5050
```

Antes de atender, el servidor **respalda la base** en `respaldos/` (y luego
cada 24 horas). Si la base viene de una versión anterior, en ese mismo
arranque se actualiza sola: separa los nombres en apellidos y nombre y pasa la
jornada al catálogo del IMSS.

Desde otra computadora de la misma red se entra con la IP de este equipo,
por ejemplo `http://192.168.0.8:5050`. La primera vez Windows puede preguntar
si permite el acceso a Python: acepta solo **Redes privadas**.

> `python -m sigma` arranca el servidor de **desarrollo**: solo se ve desde
> este equipo y no debe usarse en la oficina.

### 5. Abre la página

Entra a **<http://localhost:5050>** en tu navegador e inicia sesión.

> **Deja esa terminal abierta.** Mientras siga abierta, la página funciona.
> Para detener el servidor, presiona `Ctrl + C` en ella.

---

## Sobre la base de datos

Sigma elige el motor solo, al arrancar:

| Situación | Qué usa |
|---|---|
| Tienes PostgreSQL corriendo y `psycopg2` instalado | **PostgreSQL** |
| No tienes PostgreSQL | **SQLite**, un archivo llamado `sigma_imss.db` |

En ambos casos la aplicación se comporta igual, porque toda la lógica usa SQL
estándar. **La barra superior te dice cuál está activo.**

Las tablas y los dos usuarios de ejemplo (`admin.rrhh` y `captura.obra1`) se
crean solos la primera vez. No tienes que hacer nada.

### Si quieres usar PostgreSQL

```powershell
# PowerShell (Windows)
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py
```

```bash
# bash (macOS / Linux)
export DATABASE_URL="postgresql://usuario:password@localhost:5432/sigma_imss"
python servidor.py
```

Antes hay que crear la base vacía una sola vez, con PostgreSQL ya instalado y
corriendo:

```bash
createdb sigma_imss
```

---

## Correr las pruebas automáticas

```bash
python pruebas/test_prueba_concepto.py
```

Ejecuta los tres bloques del "Desarrollo experimental" (validación, exportación
y concurrencia) y genera **`pruebas/resultados/resultados_prueba_concepto.txt`**,
listo para pegar en la sección de Resultados del informe.

Usa su propia base de datos (`pruebas/resultados/sigma_pruebas.db`), que borra
al empezar, así que no ensucia lo que hayas capturado desde la página web.

La validación en ambiente relevante de la Entrega 5 tarda unos 3 minutos y deja
su reporte en la misma carpeta:

```bash
python pruebas/prueba_ambiente_relevante.py
```

La demostración del sistema integrado de la Entrega 6 (escenario con inicio de
sesión, formato del lote, seguridad, respaldo y red) tarda cerca de un minuto:

```bash
python pruebas/prueba_integracion.py
```

Los arneses no usan tu base ni tus contraseñas: cada uno trabaja sobre una
copia aislada con usuarios de prueba.

---

## Respaldos

- Automáticos: al arrancar `servidor.py` y cada 24 horas, en `respaldos/`
  (se guardan los 30 más recientes). Para mandarlos a otro disco:
  `$env:SIGMA_RESPALDOS = "D:\respaldos-sigma"` antes de arrancar.
- Manual: `python -m sigma.respaldo` · ver la lista: `python -m sigma.respaldo --listar`.
- Restaurar (con el servidor detenido):
  `python -m sigma.respaldo --restaurar respaldos\sigma_imss_AAAAMMDD_HHMMSS.db`.
  Antes de reemplazar la base guarda una copia de la actual.

---

## Empezar de cero

Para borrar todo lo capturado y volver a la base vacía:

1. Detén el servidor con `Ctrl + C`.
2. Borra el archivo `sigma_imss.db`.
3. Vuelve a arrancar con `python servidor.py`.

Si además quieres borrar los lotes generados, elimina la carpeta
`exportaciones/`.

---

## Problemas frecuentes

### "python no se reconoce como un comando"

Python no está instalado o no quedó en el PATH. Reinstálalo marcando
**"Add Python to PATH"**. En algunas máquinas el comando es `py` en vez de
`python`:

```bash
py servidor.py
```

### "No module named flask"

Faltó el paso 2. Corre:

```bash
pip install -r requirements.txt
```

### "Address already in use" o "El puerto 5050 ya está en uso"

Ya tienes otra copia del servidor corriendo. Ciérrala (`Ctrl + C` en su
terminal) o, si no la encuentras, en Windows:

```powershell
taskkill /F /IM python.exe
```

### La página se ve sin estilos, toda en blanco y negro

El navegador guardó una versión vieja del CSS. Recarga forzando:
`Ctrl + Shift + R`.

### `UnicodeDecodeError` al conectar con PostgreSQL

Pasa en Windows con el sistema en español: `libpq` traduce sus mensajes de error
con una codificación distinta de UTF-8 y `psycopg2` truena al *leer* el mensaje,
en lugar de mostrar el error real. Ya está resuelto — `sigma/database.py` fuerza
`LC_ALL=C` al importarse. Si te vuelve a salir, verás debajo el error verdadero
(contraseña incorrecta, servidor caído, base inexistente).

### Cambié un archivo y no veo el cambio

- Archivos `.py` → detén el servidor (`Ctrl + C`) y vuelve a arrancarlo.
- Archivos `.css` o `.js` → recarga forzando con `Ctrl + Shift + R`.
