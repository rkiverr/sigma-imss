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

## Arranque en 3 pasos

### 1. Abre una terminal en la carpeta del proyecto

En Windows: entra a la carpeta `sigma-imss`, haz clic derecho en un espacio
vacío y elige **"Abrir en Terminal"**.

### 2. Instala las dependencias (solo la primera vez)

```bash
pip install -r requirements.txt
```

### 3. Arranca el servidor

```bash
python app.py
```

Verás algo así:

```
[sigma] Motor de datos: SQLite - sigma_imss.db
[sigma] Interfaz disponible en http://127.0.0.1:5050
 * Running on http://127.0.0.1:5050
```

### 4. Abre la página

Entra a **<http://localhost:5050>** en tu navegador.

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
python app.py
```

```bash
# bash (macOS / Linux)
export DATABASE_URL="postgresql://usuario:password@localhost:5432/sigma_imss"
python app.py
```

Antes hay que crear la base vacía una sola vez, con PostgreSQL ya instalado y
corriendo:

```bash
createdb sigma_imss
```

---

## Correr las pruebas automáticas

```bash
python test_prueba_concepto.py
```

Ejecuta los tres bloques del "Desarrollo experimental" (validación, exportación
y concurrencia) y genera **`resultados_prueba_concepto.txt`**, listo para pegar
en la sección de Resultados del informe.

Usa su propia base de datos (`sigma_pruebas.db`), que borra al empezar, así que
no ensucia lo que hayas capturado desde la página web.

---

## Empezar de cero

Para borrar todo lo capturado y volver a la base vacía:

1. Detén el servidor con `Ctrl + C`.
2. Borra el archivo `sigma_imss.db`.
3. Vuelve a arrancar con `python app.py`.

Si además quieres borrar los lotes generados, elimina la carpeta
`exportaciones/`.

---

## Problemas frecuentes

### "python no se reconoce como un comando"

Python no está instalado o no quedó en el PATH. Reinstálalo marcando
**"Add Python to PATH"**. En algunas máquinas el comando es `py` en vez de
`python`:

```bash
py app.py
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
en lugar de mostrar el error real. Ya está resuelto — `database.py` fuerza
`LC_ALL=C` al importarse. Si te vuelve a salir, verás debajo el error verdadero
(contraseña incorrecta, servidor caído, base inexistente).

### Cambié un archivo y no veo el cambio

- Archivos `.py` → el servidor se reinicia solo, basta recargar el navegador.
- Archivos `.css` o `.js` → recarga forzando con `Ctrl + Shift + R`.
