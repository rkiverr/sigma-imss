"""
Módulo de abstracción de datos: traduce los movimientos válidos almacenados en
la base de datos relacional al archivo de texto plano que exige la plataforma
IDSE para su carga masiva.

NOTA: la estructura exacta de columnas y posiciones debe confirmarse contra el
layout oficial vigente publicado por el IMSS. Aquí se usan campos delimitados
por '|' como representación del principio de exportación (abstracción de
datos), suficiente para demostrar la prueba de concepto.
"""
import os
from datetime import datetime

CAMPOS_EXPORTACION = [
    "registro_patronal", "tipo_movimiento", "curp", "nss", "rfc",
    "fecha_movimiento", "tipo_trabajador", "tipo_salario", "tipo_jornada",
    "sdi", "causa_baja",
]

SEPARADOR = "|"

# Carpeta donde se depositan los lotes generados.
DIRECTORIO_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exportaciones")


def _limpiar(valor):
    """
    Normaliza un valor para el archivo plano: sin separadores ni saltos de
    línea, que romperían el parseo del lote en el lado del IMSS.
    """
    texto = "" if valor is None else str(valor)
    texto = texto.replace(SEPARADOR, " ").replace("\r", " ").replace("\n", " ")
    return texto.strip()


def generar_linea_idse(registro):
    """Convierte un movimiento en la línea de texto plano del lote."""
    return SEPARADOR.join(_limpiar(registro.get(campo, "")) for campo in CAMPOS_EXPORTACION)


def generar_lote_idse(registros):
    """Convierte una lista de movimientos en el cuerpo completo del lote."""
    return "\n".join(generar_linea_idse(registro) for registro in registros)


def nombre_de_lote(prefijo="lote_idse"):
    """Nombre único con marca de tiempo, para no sobrescribir lotes previos."""
    return f"{prefijo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


def exportar_a_archivo(registros, ruta_salida):
    """
    Escribe el lote en disco y devuelve la ruta del archivo generado.
    Crea el directorio destino si no existe.
    """
    directorio = os.path.dirname(os.path.abspath(ruta_salida))
    os.makedirs(directorio, exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8", newline="\n") as archivo:
        archivo.write(generar_lote_idse(registros) + "\n")
    return ruta_salida


def exportar_lote(registros, prefijo="lote_idse"):
    """
    Genera un lote con nombre único dentro de la carpeta de exportaciones.
    Devuelve la ruta absoluta del archivo.
    """
    return exportar_a_archivo(registros, os.path.join(DIRECTORIO_SALIDA, nombre_de_lote(prefijo)))


def ultimo_lote():
    """Ruta del lote generado más recientemente, o None si todavía no hay ninguno."""
    if not os.path.isdir(DIRECTORIO_SALIDA):
        return None
    archivos = [
        os.path.join(DIRECTORIO_SALIDA, nombre)
        for nombre in os.listdir(DIRECTORIO_SALIDA)
        if nombre.lower().endswith(".txt")
    ]
    if not archivos:
        return None
    return max(archivos, key=os.path.getmtime)
