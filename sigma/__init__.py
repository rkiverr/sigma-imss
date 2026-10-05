"""
Sigma — sistema de altas y bajas de trabajadores ante el IMSS.

Paquete con toda la aplicación: rutas HTTP (app), validación (validaciones),
plazo legal (plazo), persistencia (database), lote IDSE (exportar_idse) y la
interfaz (templates/ y static/).

Arranque:
    python servidor.py     producción con waitress (desde la raíz del repositorio)
    python -m sigma        servidor de desarrollo, solo en este equipo
"""
