"""
Módulo de abstracción de datos: traduce los movimientos válidos almacenados en
la base de datos al archivo de texto que exige la plataforma IDSE para la
presentación de cinco o más movimientos (art. 46 del RACERF).

La estructura sigue el documento del IMSS "Estructura de Movimientos
afiliatorios" (https://www.imss.gob.mx/sites/all/statics/sua/dispmag/
EstructuraMovimientosAfiliatorios.pdf): un archivo de texto POR TIPO de
movimiento, con registros de 168 posiciones de ancho fijo. Las posiciones están
en las tablas ESTRUCTURA de abajo, campo por campo, para que un cambio del
instructivo se corrija en la tabla y no en el código.

Lo que el documento no especifica y queda por confirmar con un lote de prueba
en el IDSE: la codificación (aquí Windows-1252, un byte por carácter, para que
cada registro mida 168 bytes), el fin de línea (CRLF) y cómo representar la Ñ
(aquí se conserva). El salario va en 6 dígitos con 2 decimales implícitos.
"""
import os
import re
import unicodedata
from datetime import datetime

from .validaciones import TIPO_ALTA, TIPO_BAJA, limites_sbc

LONGITUD_REGISTRO = 168
CODIFICACION = "cp1252"
FIN_DE_LINEA = "\r\n"
NOMBRES_TIPO = {TIPO_ALTA: "altas", TIPO_BAJA: "bajas"}

# Carpeta donde se depositan los lotes generados: exportaciones/ en la raíz del
# repositorio (este archivo vive en sigma/).
DIRECTORIO_SALIDA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 "exportaciones")


# --------------------------------------------------------------------------
# Valores de cada campo
# --------------------------------------------------------------------------
def _sdi_para_cotizar(registro):
    """
    El salario se comunica al IMSS sin exceder el tope de 25 UMA (art. 28 LSS y
    art. 45 del RACERF). En la base se conserva el SDI real capturado; al
    lote se lleva el que efectivamente cotiza.
    """
    valor = str(registro.get("sdi") or "").replace(",", "").strip()
    if not valor:
        return ""
    monto = float(valor)
    _, tope = limites_sbc(registro.get("fecha_movimiento"))
    return f"{min(monto, tope):.2f}"


def _salario_en_centavos(registro):
    """Salario base de cotización en 6 dígitos con 2 decimales implícitos (687.70 -> 068770)."""
    valor = _sdi_para_cotizar(registro)
    return str(round(float(valor) * 100)) if valor else ""


def _rp(registro):
    return str(registro.get("registro_patronal") or "")


def _nss(registro):
    return str(registro.get("nss") or "")


ESTRUCTURA = {
    # Alta o reingreso (08). Posiciones del documento del IMSS, inciso a).
    TIPO_ALTA: [
        ("registro_patronal", 1, 10, "AN", lambda r: _rp(r)[:10]),
        ("digito_registro_patronal", 11, 1, "N", lambda r: _rp(r)[10:11]),
        ("nss", 12, 10, "N", lambda r: _nss(r)[:10]),
        ("digito_nss", 22, 1, "N", lambda r: _nss(r)[10:11]),
        ("apellido_paterno", 23, 27, "A", lambda r: r.get("apellido_paterno")),
        ("apellido_materno", 50, 27, "A", lambda r: r.get("apellido_materno")),
        ("nombres", 77, 27, "A", lambda r: r.get("nombres")),
        ("salario_base", 104, 6, "N", _salario_en_centavos),
        ("filler", 110, 6, " ", None),
        ("tipo_trabajador", 116, 1, "N", lambda r: r.get("tipo_trabajador")),
        ("tipo_salario", 117, 1, "N", lambda r: r.get("tipo_salario")),
        ("semana_jornada_reducida", 118, 1, "N", lambda r: r.get("tipo_jornada")),
        ("fecha_movimiento", 119, 8, "N", lambda r: r.get("fecha_movimiento")),
        ("unidad_medicina_familiar", 127, 3, "N", lambda r: r.get("umf")),
        ("filler", 130, 2, " ", None),
        ("tipo_movimiento", 132, 2, "N", lambda r: TIPO_ALTA),
        ("guia", 134, 5, "N", lambda r: r.get("guia")),
        ("clave_trabajador", 139, 10, "AN", lambda r: r.get("trabajador_id")),
        ("filler", 149, 1, " ", None),
        ("curp", 150, 18, "AN", lambda r: r.get("curp")),
        ("identificador_formato", 168, 1, "N", lambda r: "9"),
    ],
    # Baja (02). Inciso c): sin salario ni CURP; la causa va en la posición 149.
    TIPO_BAJA: [
        ("registro_patronal", 1, 10, "AN", lambda r: _rp(r)[:10]),
        ("digito_registro_patronal", 11, 1, "N", lambda r: _rp(r)[10:11]),
        ("nss", 12, 10, "N", lambda r: _nss(r)[:10]),
        ("digito_nss", 22, 1, "N", lambda r: _nss(r)[10:11]),
        ("apellido_paterno", 23, 27, "A", lambda r: r.get("apellido_paterno")),
        ("apellido_materno", 50, 27, "A", lambda r: r.get("apellido_materno")),
        ("nombres", 77, 27, "A", lambda r: r.get("nombres")),
        ("filler", 104, 15, "0", None),
        ("fecha_movimiento", 119, 8, "N", lambda r: r.get("fecha_movimiento")),
        ("filler", 127, 5, " ", None),
        ("tipo_movimiento", 132, 2, "N", lambda r: TIPO_BAJA),
        ("guia", 134, 5, "N", lambda r: r.get("guia")),
        ("clave_trabajador", 139, 10, "AN", lambda r: r.get("trabajador_id")),
        ("causa_baja", 149, 1, "AN", lambda r: r.get("causa_baja")),
        ("filler", 150, 18, " ", None),
        ("identificador_formato", 168, 1, "N", lambda r: "9"),
    ],
}

# Campos sin los que un registro no puede generarse (bases anteriores al TRL 6
# no tienen apellidos separados ni UMF).
OBLIGATORIOS = {
    TIPO_ALTA: ("registro_patronal", "nss", "apellido_paterno", "nombres", "sdi", "tipo_trabajador",
                "tipo_salario", "tipo_jornada", "fecha_movimiento", "umf", "guia", "curp"),
    TIPO_BAJA: ("registro_patronal", "nss", "apellido_paterno", "nombres", "fecha_movimiento", "guia",
                "causa_baja"),
}


# --------------------------------------------------------------------------
# Formato
# --------------------------------------------------------------------------
def _alfabetico(texto):
    """Mayúsculas sin acentos (la Ñ se conserva); solo letras y espacios."""
    texto = (texto or "").upper().replace("Ñ", "\0")
    texto = "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")
    texto = texto.replace("\0", "Ñ")
    texto = re.sub(r"[^A-ZÑ ]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def _formatear(valor, longitud, tipo, nombre):
    if tipo in (" ", "0"):
        return tipo * longitud
    texto = "" if valor is None else str(valor).strip()
    if tipo == "N":
        if not texto.isdigit() or len(texto) > longitud:
            raise ValueError(f"El campo {nombre} debe ser numérico de hasta {longitud} dígitos: {texto!r}")
        return texto.zfill(longitud)
    texto = _alfabetico(texto) if tipo == "A" else texto.upper()
    return texto[:longitud].ljust(longitud)


def faltantes(registro):
    """Datos obligatorios que le faltan al movimiento para poder exportarse."""
    tipo = registro.get("tipo_movimiento")
    return [campo for campo in OBLIGATORIOS.get(tipo, ()) if not str(registro.get(campo) or "").strip()]


def generar_linea_idse(registro):
    """Convierte un movimiento en un registro de 168 posiciones."""
    tipo = registro.get("tipo_movimiento")
    if tipo not in ESTRUCTURA:
        raise ValueError(f"Tipo de movimiento sin estructura de exportación: {tipo!r}")
    partes = []
    posicion = 1
    for nombre, inicio, longitud, formato, fuente in ESTRUCTURA[tipo]:
        assert inicio == posicion, f"La estructura {tipo} salta de la posición {posicion} a {inicio}"
        partes.append(_formatear(fuente(registro) if fuente else None, longitud, formato, nombre))
        posicion += longitud
    linea = "".join(partes)
    assert len(linea) == LONGITUD_REGISTRO, f"El registro mide {len(linea)} posiciones"
    return linea


def generar_lote_idse(registros):
    """Cuerpo de un lote: un registro por línea, cada una terminada en CRLF."""
    return "".join(generar_linea_idse(registro) + FIN_DE_LINEA for registro in registros)


def nombre_de_lote(tipo, prefijo="lote_idse"):
    """Nombre único con el tipo y la marca de tiempo, para no sobrescribir lotes previos."""
    return f"{prefijo}_{NOMBRES_TIPO[tipo]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


def exportar_a_archivo(registros, ruta_salida):
    """
    Escribe los registros (todos del mismo tipo) en disco y devuelve la ruta.
    Crea el directorio destino si no existe.
    """
    directorio = os.path.dirname(os.path.abspath(ruta_salida))
    os.makedirs(directorio, exist_ok=True)
    with open(ruta_salida, "w", encoding=CODIFICACION, newline="") as archivo:
        archivo.write(generar_lote_idse(registros))
    return ruta_salida


def exportar_lote(registros, prefijo="lote_idse"):
    """
    Genera un archivo por tipo de movimiento en la carpeta de exportaciones.
    Devuelve {tipo: ruta} solo con los tipos que tenían movimientos.
    """
    rutas = {}
    for tipo in (TIPO_ALTA, TIPO_BAJA):
        del_tipo = [r for r in registros if r.get("tipo_movimiento") == tipo]
        if del_tipo:
            ruta = os.path.join(DIRECTORIO_SALIDA, nombre_de_lote(tipo, prefijo))
            rutas[tipo] = exportar_a_archivo(del_tipo, ruta)
    return rutas


def ultimo_lote(tipo=None):
    """
    Ruta del lote generado más recientemente (del tipo pedido, "altas" o
    "bajas", si se indica), o None si todavía no hay ninguno.
    """
    if not os.path.isdir(DIRECTORIO_SALIDA):
        return None
    archivos = [
        os.path.join(DIRECTORIO_SALIDA, nombre)
        for nombre in os.listdir(DIRECTORIO_SALIDA)
        if nombre.lower().endswith(".txt") and (tipo is None or f"_{tipo}_" in nombre)
    ]
    if not archivos:
        return None
    return max(archivos, key=os.path.getmtime)
