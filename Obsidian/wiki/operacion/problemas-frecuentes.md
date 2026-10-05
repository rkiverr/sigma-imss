---
tipo: operacion
tags: [problemas, soporte, troubleshooting]
fuentes: ["instrucciones/Ejecutar.md", "README.md", "sigma/database.py"]
actualizado: 2026-10-04
---

# Problemas frecuentes

| Síntoma | Causa | Solución |
|---|---|---|
| "python no se reconoce como un comando" | Python no está en el PATH | Reinstalar marcando "Add Python to PATH", o usar `py servidor.py` |
| `No module named flask` o `waitress` | Faltan dependencias | `pip install -r requirements.txt` |
| "Address already in use" o el puerto 5050 está ocupado | Ya hay otro servidor corriendo | Cerrarlo con `Ctrl + C`; si no aparece, `taskkill /F /IM python.exe` |
| La página se ve sin estilos | El navegador guardó un CSS viejo | `Ctrl + Shift + R` |
| Cambié un `.py` y no veo el cambio | waitress no recarga solo | Reiniciar `python servidor.py` |
| `UnicodeDecodeError` al conectar con PostgreSQL | En Windows en español, `libpq` traduce los mensajes con otra codificación | Ya está resuelto: `database.py` fuerza `LC_ALL=C`. Si reaparece, el error real está debajo (contraseña, servidor caído, base inexistente) |
| Página 503 "Base de datos no disponible" | `SIGMA_DB=postgres` sin servidor, o `DATABASE_URL` mal | Revisar PostgreSQL o usar `SIGMA_DB=sqlite` |
| La barra dice "SQLite" y yo quería PostgreSQL | No hay psycopg2 (Python ≥ 3.13) o PostgreSQL no responde | Ver [[doble-motor-de-base-de-datos]] |
| Página 403 "Solicitud rechazada" al capturar | La petición no venía de una página de Sigma, o hay un proxy que cambia el `Host` | Capturar desde el formulario; si hay proxy, ajustar `preparar_peticion()` ([[seguridad-web]]) |
| Desde otra PC no se ve la página | Firewall de Windows, o se arrancó `app.py` (solo 127.0.0.1) | Usar `servidor.py` y permitir redes privadas |
| Se perdió el *flash* tras reiniciar | `SECRET_KEY` cambia en cada arranque | Fijar `SECRET_KEY` ([[configuracion]]) |
| "la base ya contiene movimientos duplicados…" al arrancar | Una base vieja con duplicados impide crear el índice único | Depurar los duplicados y reiniciar ([[adr-010-unicidad-del-movimiento-en-la-base]]) |
| Una captura tarda varios segundos con mucha gente | SQLite serializa las escrituras | Normal solo bajo estrés; para la oficina, PostgreSQL ([[hoja-de-ruta-trl6]]) |

## Preguntas que ya se hicieron
Están en [[preguntas-frecuentes]].

Ver también: [[como-arrancar]] · [[configuracion]]
