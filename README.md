# Sigma — Prueba de Concepto (TRL 3)
Sistema para la automatización de altas y bajas de seguro social

## Requisitos
- Python 3.9+
- PostgreSQL (local, Docker, o cualquier instancia accesible)
- `pip install -r requirements.txt`

## Configurar la base de datos
Por defecto la app se conecta a:
```
postgresql://postgres:postgres@localhost:5432/sigma_imss
```
Para usar otra configuración, define la variable de entorno `DATABASE_URL` antes de correr la app:
```bash
# PowerShell
$env:DATABASE_URL = "postgresql://usuario:password@localhost:5432/sigma_imss"

# bash / macOS / Linux
export DATABASE_URL="postgresql://usuario:password@localhost:5432/sigma_imss"
```
Crea la base de datos vacía una sola vez (con PostgreSQL ya instalado y corriendo):
```bash
createdb sigma_imss
```
Las tablas y los usuarios semilla se crean automáticamente la primera vez que se ejecuta `app.py` o `test_prueba_concepto.py`.

## Estructura
- `validaciones.py` — validación algorítmica (CURP, NSS, RFC, fecha, tipo de movimiento).
- `database.py` — modelo de datos normalizado en PostgreSQL (patron, usuario, trabajador, movimiento, bitacora).
- `exportar_idse.py` — traducción de movimientos válidos al formato de lote IDSE.
- `app.py` — aplicación web (cliente-servidor) con el formulario de captura, listado, exportación y bitácora.
- `templates/index.html` — interfaz (formulario, ledger de movimientos, timeline de auditoría).
- `test_prueba_concepto.py` — arnés de pruebas automatizado que ejecuta los 3 bloques del "Desarrollo experimental"
  (validación, exportación y concurrencia) y genera `resultados_prueba_concepto.txt`.

## Cómo correr la app web (para tomar capturas de pantalla)
```bash
pip install -r requirements.txt
python app.py
```
Abrir `http://localhost:5050` en el navegador.

## Cómo correr las pruebas automáticas (para llenar Resultados / Análisis de resultados)
```bash
python test_prueba_concepto.py
```
Genera `resultados_prueba_concepto.txt` con el detalle de los 8 casos de prueba, el contenido del
lote IDSE generado y la verificación de concurrencia + bitácora.

## Notas
- El motor PostgreSQL puede sustituirse por otro compatible con `psycopg2` sin tocar la lógica de
  negocio, ya que solo se usa SQL estándar.
- La estructura de columnas del archivo IDSE en `exportar_idse.py` debe confirmarse contra el
  layout oficial vigente del IMSS antes de usarse en un entorno real.
