"""
Plazo legal para presentar los movimientos afiliatorios.

El artículo 15, fracción I, de la Ley del Seguro Social obliga al patrón a
comunicar al IMSS las altas y bajas de sus trabajadores "dentro de plazos no
mayores de cinco días hábiles". Presentarlas tarde es infracción (art. 304 A,
fr. II) y se multa con 20 a 350 veces la UMA (art. 304 B, fr. IV).

El plazo se cuenta a partir del día siguiente al del movimiento. Un día es
hábil si no es sábado, domingo ni día de descanso obligatorio del artículo 74
de la Ley Federal del Trabajo. Tres de esos días son móviles (primer lunes de
febrero, tercer lunes de marzo y tercer lunes de noviembre), por eso se
calculan por año en lugar de escribirse en una lista fija.

Lógica tomada de la versión alterna de la Entrega 3 (imss_poc/plazo.py).
"""
from datetime import date, datetime, timedelta

UMBRAL_DIAS_HABILES = 5

# Días inhábiles que el IMSS publique cada año en el DOF y que no estén en el
# artículo 74 de la LFT (por ejemplo, jueves y viernes santos), y los días de
# jornada electoral de la fr. IX del art. 74, que fijan las leyes electorales.
# Se agregan aquí como objetos date.
DIAS_INHABILES_ADICIONALES = set()


def _enesimo_lunes(anio, mes, ocurrencia):
    primero = date(anio, mes, 1)
    return primero + timedelta(days=(0 - primero.weekday()) % 7 + 7 * (ocurrencia - 1))


def dias_de_descanso(anio):
    """Descansos obligatorios del artículo 74 de la LFT para el año indicado."""
    dias = {
        date(anio, 1, 1),                # Año nuevo
        _enesimo_lunes(anio, 2, 1),      # Aniversario de la Constitución
        _enesimo_lunes(anio, 3, 3),      # Natalicio de Benito Juárez
        date(anio, 5, 1),                # Día del Trabajo
        date(anio, 9, 16),               # Independencia
        _enesimo_lunes(anio, 11, 3),     # Revolución Mexicana
        date(anio, 12, 25),              # Navidad
    }
    # Fr. VII, reformada en el DOF del 30-09-2024: el 1 de octubre de cada seis
    # años, cuando hay transmisión del Poder Ejecutivo Federal (2024, 2030…).
    if anio % 6 == 2:
        dias.add(date(anio, 10, 1))      # Transmisión del Poder Ejecutivo Federal
    return dias


def es_dia_habil(dia):
    if dia.weekday() >= 5:
        return False
    return dia not in dias_de_descanso(dia.year) and dia not in DIAS_INHABILES_ADICIONALES


def _a_fecha(ddmmaaaa):
    return datetime.strptime(str(ddmmaaaa), "%d%m%Y").date()


def fecha_limite(fecha_movimiento, umbral=UMBRAL_DIAS_HABILES):
    """Último día en que el movimiento puede presentarse dentro del plazo."""
    dia = _a_fecha(fecha_movimiento)
    habiles = 0
    while habiles < umbral:
        dia += timedelta(days=1)
        if es_dia_habil(dia):
            habiles += 1
    return dia


def dias_habiles_transcurridos(fecha_movimiento, hoy=None):
    inicio = _a_fecha(fecha_movimiento)
    fin = hoy or date.today()
    contador = 0
    dia = inicio + timedelta(days=1)
    while dia <= fin:
        if es_dia_habil(dia):
            contador += 1
        dia += timedelta(days=1)
    return contador


def evaluar(fecha_movimiento, hoy=None, umbral=UMBRAL_DIAS_HABILES):
    """
    Compara los días hábiles transcurridos contra el umbral legal.
    estado: EN_PLAZO | POR_VENCER (último día hábil disponible) | VENCIDO
    """
    transcurridos = dias_habiles_transcurridos(fecha_movimiento, hoy)
    if transcurridos > umbral:
        estado = "VENCIDO"
    elif transcurridos >= umbral - 1:
        estado = "POR_VENCER"
    else:
        estado = "EN_PLAZO"
    return {
        "estado": estado,
        "dias_habiles_transcurridos": transcurridos,
        "dias_habiles_restantes": max(umbral - transcurridos, 0),
        "fecha_limite": fecha_limite(fecha_movimiento, umbral),
    }
