"""
Módulo de validación algorítmica.

Implementa las reglas descritas en la Entrega 1 / Entrega 3 y agrega las
validaciones de coherencia que exige el IMSS al capturar un movimiento
afiliatorio:

  * Formato de CURP, NSS, RFC, fecha y tipo de movimiento.
  * Fecha de nacimiento embebida en la CURP realmente existente.
  * Coherencia entre CURP y RFC (mismas iniciales y misma fecha).
  * Reglas por tipo de movimiento (SDI obligatorio en altas, causa en bajas).

La función principal devuelve los errores indexados por campo, para que la
interfaz pueda señalar exactamente el campo que hay que corregir.
"""
import re
from datetime import datetime, date

# CURP: 4 letras + 6 dígitos (fecha nacimiento) + sexo (H/M) + 5 letras
#       (entidad y consonantes) + 1 alfanumérico + 1 dígito verificador
CURP_REGEX = re.compile(r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$")

# NSS: exactamente 11 dígitos
NSS_REGEX = re.compile(r"^\d{11}$")

# RFC persona física: 4 letras + 6 dígitos (fecha) + 3 caracteres de homoclave
RFC_REGEX = re.compile(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$")

# Fecha en formato DDMMAAAA
FECHA_REGEX = re.compile(r"^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])(\d{4})$")

TIPOS_MOVIMIENTO_VALIDOS = {"08", "02"}
TIPO_ALTA = "08"
TIPO_BAJA = "02"

# Catálogos IDSE. Se exponen para que la interfaz arme los desplegables desde
# la misma fuente de verdad que usa el validador.
TIPOS_TRABAJADOR = {
    "1": "1 — Trabajador permanente",
    "2": "2 — Trabajador eventual",
    "3": "3 — Eventual de la construcción",
    "4": "4 — Eventual del campo",
}
TIPOS_SALARIO = {
    "0": "0 — Fijo",
    "1": "1 — Variable",
    "2": "2 — Mixto",
}
TIPOS_JORNADA = {
    "1": "1 — Jornada normal (semana completa)",
    "2": "2 — Jornada reducida",
    "3": "3 — Semana reducida",
    "4": "4 — Jornada y semana reducidas",
}
CAUSAS_BAJA = {
    "1": "1 — Término de contrato",
    "2": "2 — Separación voluntaria",
    "3": "3 — Abandono de empleo",
    "4": "4 — Defunción",
    "5": "5 — Clausura",
    "6": "6 — Otra",
    "7": "7 — Ausentismo",
    "8": "8 — Rescisión de contrato",
    "9": "9 — Jubilación",
    "A": "A — Pensión",
}

# Límites operativos del SDI (el tope legal son 25 UMA diarias).
SDI_MINIMO = 1.0
SDI_MAXIMO = 10000.0

# Ventana razonable para una fecha de movimiento, en días.
DIAS_ANTIGUEDAD_MAXIMA = 365 * 5
DIAS_FUTURO_MAXIMO = 365


# --------------------------------------------------------------------------
# Validadores individuales
# --------------------------------------------------------------------------
def _fecha_desde_aammdd(texto):
    """
    Interpreta los 6 dígitos AAMMDD de una CURP/RFC.
    Los años de 00 a (año actual %100) se toman como 2000s; el resto, 1900s.
    Devuelve un date o None si la combinación no existe.
    """
    corte = datetime.now().year % 100
    anio_corto, mes, dia = int(texto[0:2]), int(texto[2:4]), int(texto[4:6])
    siglo = 2000 if anio_corto <= corte else 1900
    try:
        return date(siglo + anio_corto, mes, dia)
    except ValueError:
        return None


def validar_curp(valor):
    valor = (valor or "").strip().upper()
    if not valor:
        return False, "La CURP es obligatoria."
    if len(valor) != 18:
        return False, f"La CURP debe tener 18 caracteres; se capturaron {len(valor)}."
    if not CURP_REGEX.match(valor):
        return False, ("Formato de CURP inválido: se esperan 4 letras, 6 dígitos de fecha, "
                       "sexo H o M, 5 letras, 1 alfanumérico y 1 dígito verificador.")
    if _fecha_desde_aammdd(valor[4:10]) is None:
        return False, "La fecha de nacimiento contenida en la CURP no existe en el calendario."
    return True, None


def _digito_verificador_nss(nss):
    """
    Dígito verificador del NSS según el algoritmo de Luhn que usa el IMSS.
    Devuelve el dígito esperado para los primeros 10 caracteres.
    """
    suma = 0
    for indice, caracter in enumerate(nss[:10]):
        digito = int(caracter)
        if indice % 2:  # se duplican las posiciones pares (base 0: 1, 3, 5...)
            digito *= 2
            if digito > 9:
                digito -= 9
        suma += digito
    return (10 - (suma % 10)) % 10


def validar_nss(valor):
    valor = (valor or "").strip()
    if not valor:
        return False, "El NSS es obligatorio."
    if not valor.isdigit():
        return False, "El NSS solo admite dígitos: se capturaron letras o símbolos."
    if len(valor) != 11:
        return False, f"El NSS debe tener exactamente 11 dígitos; se capturaron {len(valor)}."
    if not NSS_REGEX.match(valor):
        return False, "El NSS debe tener exactamente 11 dígitos numéricos."
    return True, None


def verificar_digito_nss(valor):
    """
    Comprobación del dígito verificador. Se reporta como AVISO y no como error,
    porque existen NSS históricos emitidos antes de que el dígito se
    estandarizara y bloquearlos impediría capturar movimientos legítimos.
    """
    valor = (valor or "").strip()
    if not NSS_REGEX.match(valor):
        return True, None
    esperado = _digito_verificador_nss(valor)
    if int(valor[10]) != esperado:
        return False, (f"El dígito verificador del NSS no coincide (se esperaba {esperado}). "
                       "Confírmalo contra el documento oficial del trabajador.")
    return True, None


def validar_rfc(valor):
    valor = (valor or "").strip().upper()
    if not valor:
        return False, "El RFC es obligatorio."
    if not RFC_REGEX.match(valor):
        return False, ("Formato de RFC inválido: se esperan 12 o 13 caracteres "
                       "(3 o 4 letras + 6 dígitos de fecha + 3 de homoclave).")
    return True, None


def validar_fecha(valor):
    valor = (valor or "").strip()
    if not valor:
        return False, "La fecha de movimiento es obligatoria."
    if not FECHA_REGEX.match(valor):
        return False, "Formato de fecha inválido: debe ser DDMMAAAA (por ejemplo 05092026)."
    dia, mes, anio = valor[0:2], valor[2:4], valor[4:8]
    try:
        datetime(int(anio), int(mes), int(dia))
    except ValueError:
        return False, "La combinación de día, mes y año no existe en el calendario."
    return True, None


def verificar_rango_fecha(valor):
    """Aviso cuando la fecha del movimiento está muy lejos del día de hoy."""
    if not FECHA_REGEX.match((valor or "").strip()):
        return True, None
    fecha = date(int(valor[4:8]), int(valor[2:4]), int(valor[0:2]))
    diferencia = (fecha - date.today()).days
    if diferencia > DIAS_FUTURO_MAXIMO:
        return False, "La fecha está a más de un año en el futuro. Verifica que sea correcta."
    if -diferencia > DIAS_ANTIGUEDAD_MAXIMA:
        return False, "La fecha tiene más de cinco años de antigüedad. Verifica que sea correcta."
    return True, None


def validar_tipo_movimiento(valor):
    if (valor or "").strip() not in TIPOS_MOVIMIENTO_VALIDOS:
        return False, "El tipo de movimiento debe ser 08 (Alta o Reingreso) o 02 (Baja)."
    return True, None


def validar_sdi(valor, obligatorio):
    valor = (valor or "").strip()
    if not valor:
        if obligatorio:
            return False, "El salario diario integrado es obligatorio en un alta."
        return True, None
    try:
        monto = float(valor.replace(",", ""))
    except ValueError:
        return False, "El salario diario integrado debe ser un número (por ejemplo 450.50)."
    if monto < SDI_MINIMO:
        return False, f"El salario diario integrado debe ser mayor o igual a {SDI_MINIMO:.2f}."
    if monto > SDI_MAXIMO:
        return False, f"El salario diario integrado excede el tope permitido de {SDI_MAXIMO:,.2f}."
    return True, None


def validar_coherencia_curp_rfc(curp, rfc):
    """
    El RFC de una persona física se construye con las mismas iniciales y la
    misma fecha de nacimiento que la CURP. Si ambos tienen formato válido pero
    no concuerdan, hay un error de captura en alguno de los dos.
    """
    curp = (curp or "").strip().upper()
    rfc = (rfc or "").strip().upper()
    if not CURP_REGEX.match(curp) or not RFC_REGEX.match(rfc):
        return True, None  # el error de formato ya se reporta por separado
    if len(rfc) == 13 and rfc[:4] != curp[:4]:
        return False, "Las primeras 4 letras del RFC no coinciden con las de la CURP."
    if rfc[-9:-3] != curp[4:10]:
        return False, "La fecha de nacimiento del RFC no coincide con la de la CURP."
    return True, None


def validar_catalogo(valor, catalogo, etiqueta, obligatorio):
    valor = (valor or "").strip().upper()
    if not valor:
        if obligatorio:
            return False, f"{etiqueta} es obligatorio para este tipo de movimiento."
        return True, None
    if valor not in catalogo:
        opciones = ", ".join(sorted(catalogo))
        return False, f"{etiqueta} inválido. Valores permitidos: {opciones}."
    return True, None


# --------------------------------------------------------------------------
# Validación completa de un movimiento
# --------------------------------------------------------------------------
def validar_campos(datos):
    """
    Aplica todas las reglas y devuelve (errores, avisos), ambos diccionarios
    indexados por nombre de campo:
      errores -> impiden guardar el movimiento
      avisos  -> se muestran al usuario pero no bloquean la captura
    """
    errores = {}
    avisos = {}
    tipo = (datos.get("tipo_movimiento") or "").strip()
    es_alta = tipo == TIPO_ALTA
    es_baja = tipo == TIPO_BAJA

    if not (datos.get("nombre_completo") or "").strip():
        errores["nombre_completo"] = "El nombre completo del trabajador es obligatorio."
    elif len((datos.get("nombre_completo") or "").strip()) < 5:
        errores["nombre_completo"] = "El nombre completo parece incompleto (mínimo 5 caracteres)."

    for campo, validador in (("curp", validar_curp), ("nss", validar_nss),
                             ("rfc", validar_rfc), ("fecha_movimiento", validar_fecha),
                             ("tipo_movimiento", validar_tipo_movimiento)):
        ok, mensaje = validador(datos.get(campo, ""))
        if not ok:
            errores[campo] = mensaje

    if "curp" not in errores and "rfc" not in errores:
        ok, mensaje = validar_coherencia_curp_rfc(datos.get("curp"), datos.get("rfc"))
        if not ok:
            errores["rfc"] = mensaje

    ok, mensaje = validar_sdi(datos.get("sdi"), obligatorio=es_alta)
    if not ok:
        errores["sdi"] = mensaje

    ok, mensaje = validar_catalogo(datos.get("tipo_trabajador"), TIPOS_TRABAJADOR,
                                   "El tipo de trabajador", obligatorio=es_alta)
    if not ok:
        errores["tipo_trabajador"] = mensaje

    ok, mensaje = validar_catalogo(datos.get("tipo_salario"), TIPOS_SALARIO,
                                   "El tipo de salario", obligatorio=es_alta)
    if not ok:
        errores["tipo_salario"] = mensaje

    ok, mensaje = validar_catalogo(datos.get("tipo_jornada"), TIPOS_JORNADA,
                                   "El tipo de jornada", obligatorio=es_alta)
    if not ok:
        errores["tipo_jornada"] = mensaje

    ok, mensaje = validar_catalogo(datos.get("causa_baja"), CAUSAS_BAJA,
                                   "La causa de baja", obligatorio=es_baja)
    if not ok:
        errores["causa_baja"] = mensaje
    elif es_alta and (datos.get("causa_baja") or "").strip():
        errores["causa_baja"] = "Un alta (08) no debe llevar causa de baja."

    # Avisos: no bloquean, solo advierten al capturista.
    if "nss" not in errores:
        ok, mensaje = verificar_digito_nss(datos.get("nss"))
        if not ok:
            avisos["nss"] = mensaje

    if "fecha_movimiento" not in errores:
        ok, mensaje = verificar_rango_fecha(datos.get("fecha_movimiento"))
        if not ok:
            avisos["fecha_movimiento"] = mensaje

    return errores, avisos


# Orden en el que se listan los errores, para que el resumen siga el orden
# visual del formulario.
ORDEN_CAMPOS = [
    "nombre_completo", "curp", "nss", "rfc", "tipo_movimiento", "fecha_movimiento",
    "tipo_trabajador", "tipo_salario", "tipo_jornada", "sdi", "causa_baja",
]


def validar_movimiento(datos):
    """
    Interfaz estable usada por la aplicación web y por el arnés de pruebas.
    Devuelve (es_valido: bool, errores: list[str]).
    """
    errores, _ = validar_campos(datos)
    ordenados = [errores[campo] for campo in ORDEN_CAMPOS if campo in errores]
    ordenados += [mensaje for campo, mensaje in errores.items() if campo not in ORDEN_CAMPOS]
    return (len(ordenados) == 0), ordenados
