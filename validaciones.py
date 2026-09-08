"""
Módulo de validación algorítmica.
Implementa las reglas descritas en la Entrega 1 / Entrega 3:
CURP (18 caracteres), NSS (11 dígitos), RFC y fecha de movimiento (DDMMAAAA).
"""
import re
from datetime import datetime

# CURP: 4 letras + 6 dígitos (fecha nacimiento) + sexo (H/M) + 5 letras + 1 alfanumérico + 1 dígito verificador
CURP_REGEX = re.compile(r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$")

# NSS: exactamente 11 dígitos
NSS_REGEX = re.compile(r"^\d{11}$")

# RFC persona física: 4 letras + 6 dígitos (fecha) + 3 caracteres alfanuméricos (homoclave)
RFC_REGEX = re.compile(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$")

# Fecha en formato DDMMAAAA
FECHA_REGEX = re.compile(r"^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])(\d{4})$")

TIPOS_MOVIMIENTO_VALIDOS = {"08", "02"}


def validar_curp(valor: str):
    if not valor or not CURP_REGEX.match(valor.upper()):
        return False, "CURP inválida: debe tener 18 caracteres con el formato oficial (4 letras, 6 dígitos, sexo H/M, 5 letras, 1 alfanumérico, 1 dígito)."
    return True, None


def validar_nss(valor: str):
    if not valor or not NSS_REGEX.match(valor):
        return False, "NSS inválido: debe tener exactamente 11 dígitos numéricos."
    return True, None


def validar_rfc(valor: str):
    if not valor or not RFC_REGEX.match(valor.upper()):
        return False, "RFC inválido: formato esperado de 12-13 caracteres (letras + fecha + homoclave)."
    return True, None


def validar_fecha(valor: str):
    if not valor or not FECHA_REGEX.match(valor):
        return False, "Fecha inválida: el formato debe ser DDMMAAAA (p. ej. 05092026)."
    dia, mes, anio = valor[0:2], valor[2:4], valor[4:8]
    try:
        datetime(int(anio), int(mes), int(dia))
    except ValueError:
        return False, "Fecha inválida: la combinación de día/mes/año no existe en el calendario."
    return True, None


def validar_tipo_movimiento(valor: str):
    if valor not in TIPOS_MOVIMIENTO_VALIDOS:
        return False, "Tipo de movimiento inválido: debe ser '08' (Alta/Reingreso) o '02' (Baja)."
    return True, None


def validar_movimiento(datos: dict):
    """
    Recibe un diccionario con los campos capturados y devuelve:
    (es_valido: bool, errores: list[str])
    Aplica todas las reglas de validación algorítmica descritas en la Entrega 1/3.
    """
    errores = []

    ok, msg = validar_curp(datos.get("curp", ""))
    if not ok:
        errores.append(msg)

    ok, msg = validar_nss(datos.get("nss", ""))
    if not ok:
        errores.append(msg)

    ok, msg = validar_rfc(datos.get("rfc", ""))
    if not ok:
        errores.append(msg)

    ok, msg = validar_fecha(datos.get("fecha_movimiento", ""))
    if not ok:
        errores.append(msg)

    ok, msg = validar_tipo_movimiento(datos.get("tipo_movimiento", ""))
    if not ok:
        errores.append(msg)

    if not datos.get("nombre_completo", "").strip():
        errores.append("El nombre completo del trabajador es obligatorio.")

    return (len(errores) == 0), errores
