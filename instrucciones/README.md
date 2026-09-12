# Comandos rápidos

Lo mínimo para levantar Sigma y verla en el navegador.

---

## Levantar la página

Abre una terminal **en la carpeta `sigma-imss`** (no en `instrucciones`) y corre:

```bash
pip install -r requirements.txt
python app.py
```

La primera línea solo hace falta la primera vez.

## Verla

Abre en el navegador:

```
http://localhost:5050
```

Deja la terminal abierta mientras uses la página.

## Detenerla

En esa misma terminal:

```
Ctrl + C
```

---

## Otros comandos

```bash
# Correr las pruebas automáticas (genera resultados_prueba_concepto.txt)
python test_prueba_concepto.py
```

```bash
# Empezar de cero: detén el servidor, borra la base y vuelve a arrancar
rm sigma_imss.db
python app.py
```

```powershell
# Windows: borrar la base
Remove-Item sigma_imss.db
```

```powershell
# Windows: si el puerto 5050 quedó ocupado
taskkill /F /IM python.exe
```

---

## Si algo falla

| Error | Solución |
|---|---|
| `python no se reconoce` | Instala Python marcando "Add Python to PATH", o usa `py app.py` |
| `No module named flask` | Corre `pip install -r requirements.txt` |
| `Address already in use` | Ya hay un servidor corriendo: ciérralo con `Ctrl + C` |
| La página se ve sin estilos | Recarga forzando con `Ctrl + Shift + R` |

---

## Más detalle

- **[Ejecutar.md](Ejecutar.md)** — guía completa de instalación, PostgreSQL y solución de problemas.
- **[Instrucciones.md](Instrucciones.md)** — qué hace la página y cómo se usa.
