"""
Módulo de abstracción de datos: traduce los movimientos válidos, almacenados
en la base de datos relacional, al formato de texto plano de ancho fijo que
exige la plataforma IDSE para su carga masiva.

NOTA: la estructura exacta de columnas/posiciones debe confirmarse contra el
layout oficial vigente publicado por el IMSS; aquí se usa una estructura de
campos delimitados por '|' como representación del principio de exportación
(abstracción de datos), suficiente para demostrar la prueba de concepto.
"""

CAMPOS_EXPORTACION = [
    "registro_patronal", "tipo_movimiento", "curp", "nss", "rfc",
    "fecha_movimiento", "tipo_trabajador", "tipo_salario", "tipo_jornada",
    "sdi", "causa_baja",
]


def generar_linea_idse(registro: dict) -> str:
    valores = [str(registro.get(campo, "") or "") for campo in CAMPOS_EXPORTACION]
    return "|".join(valores)


def generar_lote_idse(registros: list) -> str:
    lineas = [generar_linea_idse(r) for r in registros]
    return "\n".join(lineas)


def exportar_a_archivo(registros: list, ruta_salida: str) -> str:
    contenido = generar_lote_idse(registros)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(contenido + "\n")
    return ruta_salida
