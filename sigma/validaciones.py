"""
Módulo de validación algorítmica.

Implementa las reglas descritas en la Entrega 1 / Entrega 3 y agrega las
validaciones de coherencia que exige el IMSS al capturar un movimiento
afiliatorio:

  * Formato de CURP, NSS, RFC, fecha y tipo de movimiento.
  * Fecha de nacimiento embebida en la CURP realmente existente.
  * Coherencia entre CURP y RFC (mismas iniciales y misma fecha).
  * Reglas por tipo de movimiento (SDI y UMF obligatorios en altas, causa en bajas).
  * Límites legales del salario base de cotización (art. 28 LSS).
  * Plazo de cinco días hábiles para presentar el movimiento (art. 15 LSS).
  * Nombre separado en apellido paterno, materno y nombre(s), como lo pide la
    estructura oficial del IMSS, y su concordancia con las iniciales de la CURP.

La función principal devuelve los errores indexados por campo, para que la
interfaz pueda señalar exactamente el campo que hay que corregir.
"""
import re
import unicodedata
from datetime import datetime, date

from . import plazo

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
# "Semana o jornada reducida" de la estructura oficial de movimientos del IMSS
# (posición 118): 0 es la jornada normal; 1 a 5, los días que se trabajan en una
# semana reducida; 6, la jornada reducida. Hasta la Entrega 5 Sigma usaba 1 para
# la jornada normal, que el IMSS lee como "un día a la semana".
TIPOS_JORNADA = {
    "0": "0 — Jornada normal",
    "1": "1 — Semana reducida: un día",
    "2": "2 — Semana reducida: dos días",
    "3": "3 — Semana reducida: tres días",
    "4": "4 — Semana reducida: cuatro días",
    "5": "5 — Semana reducida: cinco días",
    "6": "6 — Jornada reducida",
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

# Límites del salario base de cotización (art. 28 LSS): el inferior es el
# salario mínimo general del área geográfica (Nuevo León está en la zona
# general) y el superior 25 veces la UMA. Ambos cambian cada año: el salario
# mínimo el 1 de enero (CONASAMI) y la UMA el 1 de febrero (INEGI, DOF).
SALARIO_MINIMO_GENERAL = {2025: 278.80, 2026: 315.04}
UMA_DIARIA = {2025: 113.14, 2026: 117.31}
VECES_UMA_TOPE = 25

# Arriba de este monto el dato casi seguro trae un error de captura (un punto
# decimal omitido, por ejemplo), aunque ya se cotice con el tope.
SDI_MAXIMO = 10000.0

# Nombres: letras (con acentos y ñ), espacios, punto, guion y apóstrofo.
NOMBRE_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ .'\-]*$")

# El IMSS recibe el nombre en tres campos de 27 posiciones cada uno.
CAMPOS_NOMBRE = ("apellido_paterno", "apellido_materno", "nombres")
LONGITUD_NOMBRE = 27

# Unidad de medicina familiar (clínica de adscripción): 3 dígitos en el alta.
UMF_REGEX = re.compile(r"^\d{3}$")

ALFABETO_CURP = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

# Reglas de RENAPO para las cuatro primeras letras de la CURP: se omiten las
# partículas de los apellidos y, en un nombre compuesto que empieza con José o
# María, se usa el segundo nombre.
PARTICULAS = {"DA", "DAS", "DE", "DEL", "DER", "DI", "DIE", "DD", "EL", "LA", "LOS", "LAS",
              "LE", "LES", "MAC", "MC", "VAN", "VON", "Y"}
NOMBRES_COMUNES = {"JOSE", "J", "J.", "MARIA", "MA", "MA."}

# Ventana razonable para una fecha de movimiento, en días.
DIAS_ANTIGUEDAD_MAXIMA = 365 * 5
DIAS_FUTURO_MAXIMO = 365


# --------------------------------------------------------------------------
# Normalización: la misma para el formulario y para la validación en vivo
# --------------------------------------------------------------------------
def normalizar_datos(datos):
    """
    Limpia lo capturado antes de validar. La usan POST /capturar y
    /api/validar, para que la validación en vivo y la del servidor reciban
    exactamente el mismo texto. Quita los espacios y guiones con los que se
    suelen pegar la CURP, el RFC y el NSS, y deja la fecha solo con dígitos.
    """
    limpio = {campo: str(valor if valor is not None else "").strip()
              for campo, valor in datos.items()}
    for campo in CAMPOS_NOMBRE + ("nombre_completo",):
        if campo in limpio:
            limpio[campo] = re.sub(r"\s+", " ", limpio[campo])
    # El nombre completo se deriva de los tres campos que pide el IMSS; se
    # conserva para la tabla, la búsqueda y la bitácora.
    if any(campo in limpio for campo in CAMPOS_NOMBRE):
        limpio["nombre_completo"] = " ".join(
            limpio.get(campo, "") for campo in CAMPOS_NOMBRE if limpio.get(campo))
    if "umf" in limpio:
        limpio["umf"] = re.sub(r"\D", "", limpio["umf"])
        if 0 < len(limpio["umf"]) < 3:
            limpio["umf"] = limpio["umf"].zfill(3)
    for campo in ("curp", "rfc"):
        if campo in limpio:
            limpio[campo] = re.sub(r"[\s\-.]", "", limpio[campo]).upper()
    for campo in ("nss", "fecha_movimiento"):
        if campo in limpio:
            limpio[campo] = re.sub(r"\D", "", limpio[campo])
    for campo in ("causa_baja", "tipo_trabajador", "tipo_salario", "tipo_jornada"):
        if campo in limpio:
            limpio[campo] = limpio[campo].upper()
    return limpio


def limites_sbc(fecha_ddmmaaaa=None):
    """
    (mínimo, tope) del salario base de cotización vigentes en la fecha del
    movimiento. La UMA nueva rige desde el 1 de febrero; en enero aplica la
    del año anterior. Si el año no está en las tablas se usa el más reciente.
    """
    try:
        fecha = datetime.strptime(str(fecha_ddmmaaaa), "%d%m%Y").date()
    except ValueError:
        fecha = date.today()
    anio_sm = min(max(fecha.year, min(SALARIO_MINIMO_GENERAL)), max(SALARIO_MINIMO_GENERAL))
    anio_uma = fecha.year if fecha.month >= 2 else fecha.year - 1
    anio_uma = min(max(anio_uma, min(UMA_DIARIA)), max(UMA_DIARIA))
    return SALARIO_MINIMO_GENERAL[anio_sm], round(UMA_DIARIA[anio_uma] * VECES_UMA_TOPE, 2)


def aviso_montos_sin_cargar(anio):
    """
    Los montos legales cambian cada año (salario mínimo en enero, UMA en
    febrero). Si el año todavía no está en las tablas, limites_sbc() usa el
    más reciente; aquí se avisa para que nadie lo pase por alto. Los montos
    nuevos no se suponen: se cargan cuando se publican.
    """
    ultimo = max(SALARIO_MINIMO_GENERAL)
    if anio > ultimo:
        return (f"Los montos legales de {anio} (salario mínimo y UMA) todavía no están cargados en "
                f"Sigma; se usaron los de {ultimo}. Hay que actualizarlos en validaciones.py.")
    return None


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


def _digito_verificador_curp(curp):
    """Dígito verificador de la CURP (posición 18), según el algoritmo de RENAPO."""
    suma = sum(ALFABETO_CURP.index(c) * (18 - i) for i, c in enumerate(curp[:17]))
    return (10 - suma % 10) % 10


def verificar_digito_curp(valor):
    """
    Detecta una letra o un número cambiado que conserva el formato de la CURP
    (por ejemplo, una consonante mal tecleada). Igual que el dígito del NSS, se
    reporta como AVISO: el IMSS valida la CURP contra RENAPO y quien captura
    debe confirmarla contra la constancia del trabajador.
    """
    valor = (valor or "").strip().upper()
    if not CURP_REGEX.match(valor):
        return True, None
    esperado = _digito_verificador_curp(valor)
    if int(valor[17]) != esperado:
        return False, (f"El dígito verificador de la CURP no coincide (se esperaba {esperado}): "
                       "es probable que una letra o un número esté mal tecleado. "
                       "Confírmala contra la constancia de CURP del trabajador.")
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


def validar_sdi(valor, obligatorio, fecha=None):
    """
    Devuelve (ok, mensaje, aviso). El SDI menor al salario mínimo es error,
    porque el art. 28 de la LSS no permite cotizar por debajo; el mayor al
    tope de 25 UMA es aviso, porque el salario puede ser real pero ante el IMSS
    se cotiza con el tope (art. 45 del RACERF).
    """
    valor = (valor or "").strip()
    if not valor:
        if obligatorio:
            return False, "El salario diario integrado es obligatorio en un alta.", None
        return True, None, None
    try:
        monto = float(valor.replace(",", ""))
    except ValueError:
        return False, "El salario diario integrado debe ser un número (por ejemplo 450.50).", None
    minimo, tope = limites_sbc(fecha)
    if monto < minimo:
        return False, (f"El salario diario integrado ({monto:,.2f}) es menor al salario mínimo "
                       f"general ({minimo:,.2f}); la LSS no permite cotizar por debajo de él. "
                       "Revisa si se corrió el punto decimal."), None
    if monto > SDI_MAXIMO:
        return False, (f"El salario diario integrado ({monto:,.2f}) parece un error de captura: "
                       "revisa el punto decimal."), None
    avisos = []
    if monto > tope:
        avisos.append(f"El salario diario integrado rebasa el tope de 25 UMA ({tope:,.2f}); "
                      "ante el IMSS se cotizará con el tope (art. 28 LSS).")
    if FECHA_REGEX.match(str(fecha or "")):
        sin_montos = aviso_montos_sin_cargar(int(str(fecha)[4:8]))
        if sin_montos:
            avisos.append(sin_montos)
    return True, None, " ".join(avisos) or None


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


def validar_nombre(datos):
    """
    El IMSS recibe el apellido paterno, el materno y el nombre(s) por separado,
    en 27 posiciones cada uno. El paterno y el nombre son obligatorios; el
    materno puede faltar (personas con un solo apellido). Devuelve los errores
    indexados por campo.
    """
    errores = {}
    etiquetas = {"apellido_paterno": "El apellido paterno", "apellido_materno": "El apellido materno",
                 "nombres": "El nombre"}
    for campo in CAMPOS_NOMBRE:
        valor = (datos.get(campo) or "").strip()
        if not valor:
            if campo != "apellido_materno":
                errores[campo] = f"{etiquetas[campo]} del trabajador es obligatorio."
            continue
        if not NOMBRE_REGEX.match(valor):
            errores[campo] = (f"{etiquetas[campo]} solo admite letras, espacios, punto, guion y "
                              "apóstrofo: revisa si se tecleó un número o un símbolo "
                              "(por ejemplo, un cero en lugar de la letra O).")
        elif len(valor) > LONGITUD_NOMBRE:
            errores[campo] = (f"{etiquetas[campo]} tiene {len(valor)} caracteres; el IMSS admite "
                              f"{LONGITUD_NOMBRE} como máximo. Usa la forma abreviada que aparece en "
                              "la constancia del IMSS.")
    return errores


def _sin_acentos(texto):
    texto = (texto or "").upper().replace("Ñ", "X")
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")


def _palabra_clave(texto, particulas=PARTICULAS):
    palabras = [p for p in re.split(r"[\s\-]+", _sin_acentos(texto)) if p and p not in particulas]
    return palabras[0] if palabras else ""


def _nombre_clave(nombres):
    palabras = [p for p in re.split(r"[\s\-]+", _sin_acentos(nombres)) if p and p not in PARTICULAS]
    if len(palabras) > 1 and palabras[0] in NOMBRES_COMUNES:
        return palabras[1]
    return palabras[0] if palabras else ""


def iniciales_curp(paterno, materno, nombres):
    """
    Las cuatro primeras letras de la CURP según RENAPO: inicial y primera vocal
    interna del apellido paterno, inicial del materno (X si no tiene) e inicial
    del nombre. Devuelve "" si falta el paterno o el nombre.
    """
    pat, mat, nom = _palabra_clave(paterno), _palabra_clave(materno), _nombre_clave(nombres)
    if not pat or not nom:
        return ""
    vocal = next((c for c in pat[1:] if c in "AEIOU"), "X")
    return pat[0] + vocal + (mat[0] if mat else "X") + nom[0]


def verificar_iniciales_curp(curp, paterno, materno, nombres):
    """
    AVISO cuando las iniciales de la CURP no corresponden al nombre capturado:
    suele ser un apellido en el campo equivocado, una letra mal tecleada en la
    CURP o la CURP de otra persona. Las palabras altisonantes llevan una X en la
    segunda posición (regla de RENAPO), así que esa variante también se acepta.
    """
    curp = (curp or "").strip().upper()
    if not CURP_REGEX.match(curp):
        return True, None
    esperado = iniciales_curp(paterno, materno, nombres)
    if not esperado:
        return True, None
    capturado = curp[:4].replace("Ñ", "X")
    if capturado in (esperado, esperado[0] + "X" + esperado[2:]):
        return True, None
    return False, (f"Las iniciales de la CURP ({curp[:4]}) no corresponden al nombre capturado "
                   f"(se esperaba {esperado}): revisa que cada apellido esté en su campo y que la "
                   "CURP sea la del trabajador.")


def validar_umf(valor, obligatorio):
    valor = (valor or "").strip()
    if not valor:
        if obligatorio:
            return False, ("Falta la unidad de medicina familiar (UMF): el IMSS la pide en cada alta. "
                           "Está en la constancia de vigencia o en el carnet del trabajador.")
        return True, None
    if not UMF_REGEX.match(valor) or valor == "000":
        return False, "La unidad de medicina familiar es un número de 1 a 3 dígitos (por ejemplo 035)."
    return True, None


def validar_catalogo(valor, catalogo, etiqueta, obligatorio):
    valor = (valor or "").strip().upper()
    if not valor:
        if obligatorio:
            return False, (f"Falta capturar {etiqueta[0].lower() + etiqueta[1:]}: es un dato "
                           "obligatorio para este tipo de movimiento.")
        return True, None
    if valor not in catalogo:
        opciones = ", ".join(sorted(catalogo))
        return False, f"{etiqueta} no está en el catálogo del IDSE. Valores permitidos: {opciones}."
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

    errores.update(validar_nombre(datos))

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

    ok, mensaje, aviso_sdi = validar_sdi(datos.get("sdi"), obligatorio=es_alta,
                                         fecha=datos.get("fecha_movimiento"))
    if not ok:
        errores["sdi"] = mensaje
    elif aviso_sdi:
        avisos["sdi"] = aviso_sdi

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

    ok, mensaje = validar_umf(datos.get("umf"), obligatorio=es_alta)
    if not ok:
        errores["umf"] = mensaje

    ok, mensaje = validar_catalogo(datos.get("causa_baja"), CAUSAS_BAJA,
                                   "La causa de baja", obligatorio=es_baja)
    if not ok:
        errores["causa_baja"] = mensaje
    elif es_alta and (datos.get("causa_baja") or "").strip():
        errores["causa_baja"] = "Un alta (08) no debe llevar causa de baja."

    # Avisos: no bloquean, solo advierten al capturista.
    if "curp" not in errores:
        avisos_curp = []
        ok, mensaje = verificar_digito_curp(datos.get("curp"))
        if not ok:
            avisos_curp.append(mensaje)
        if not any(campo in errores for campo in CAMPOS_NOMBRE):
            ok, mensaje = verificar_iniciales_curp(datos.get("curp"), datos.get("apellido_paterno"),
                                                   datos.get("apellido_materno"), datos.get("nombres"))
            if not ok:
                avisos_curp.append(mensaje)
        if avisos_curp:
            avisos["curp"] = " ".join(avisos_curp)

    if "nss" not in errores:
        ok, mensaje = verificar_digito_nss(datos.get("nss"))
        if not ok:
            avisos["nss"] = mensaje

    if "fecha_movimiento" not in errores:
        ok, mensaje = verificar_rango_fecha(datos.get("fecha_movimiento"))
        if not ok:
            avisos["fecha_movimiento"] = mensaje
        else:
            mensaje = verificar_plazo(datos.get("fecha_movimiento"))
            if mensaje:
                avisos["fecha_movimiento"] = mensaje

    return errores, avisos


def verificar_plazo(fecha_movimiento, hoy=None):
    """
    Aviso cuando el movimiento ya rebasó, o está por rebasar, el plazo de
    cinco días hábiles del art. 15, fr. I, de la LSS. No bloquea: un aviso
    extemporáneo se tiene que presentar de todos modos, y cuanto antes.
    """
    resultado = plazo.evaluar(fecha_movimiento, hoy)
    limite = resultado["fecha_limite"].strftime("%d/%m/%Y")
    if resultado["estado"] == "VENCIDO":
        return (f"El plazo legal de 5 días hábiles venció el {limite} (art. 15, fr. I, LSS): "
                "preséntalo en IDSE cuanto antes; el aviso extemporáneo puede multarse.")
    if resultado["estado"] == "POR_VENCER":
        return f"El plazo legal de 5 días hábiles vence el {limite}: preséntalo en IDSE hoy."
    return None


# Orden en el que se listan los errores, para que el resumen siga el orden
# visual del formulario.
ORDEN_CAMPOS = [
    "apellido_paterno", "apellido_materno", "nombres", "curp", "nss", "rfc", "tipo_movimiento",
    "fecha_movimiento", "tipo_trabajador", "tipo_salario", "tipo_jornada", "sdi", "umf", "causa_baja",
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
