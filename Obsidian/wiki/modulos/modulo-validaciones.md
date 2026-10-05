---
tipo: modulo
tags: [validaciones, regex, reglas, comparador]
fuentes: ["sigma/validaciones.py"]
actualizado: 2026-10-04
---

# `sigma/validaciones.py` — validación algorítmica (el comparador)

Tiene 462 líneas. Es la **única fuente de verdad** de las reglas de captura: la usan `POST /capturar` y
`POST /api/validar` ([[adr-003-un-solo-validador]]). No toca la base de datos; las reglas que necesitan la
base viven en `app.py` y `database.py`.

## Constantes
| Nombre | Contenido |
|---|---|
| `CURP_REGEX` | `^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$` ([[curp]]) |
| `NSS_REGEX` | `^\d{11}$` ([[nss]]) |
| `RFC_REGEX` | `^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$` ([[rfc]]) |
| `FECHA_REGEX` | DDMMAAAA con día 01–31 y mes 01–12 |
| `TIPOS_MOVIMIENTO_VALIDOS`, `TIPO_ALTA`, `TIPO_BAJA` | `{"08","02"}`, `"08"`, `"02"` |
| `TIPOS_TRABAJADOR`, `TIPOS_SALARIO`, `TIPOS_JORNADA`, `CAUSAS_BAJA` | Catálogos IDSE ([[catalogos-idse]]) |
| `SALARIO_MINIMO_GENERAL` | `{2025: 278.80, 2026: 315.04}`. **Se actualiza cada año** ([[mantenimiento-anual]]) |
| `UMA_DIARIA` | `{2025: 113.14, 2026: 117.31}`. Rige desde el 1 de febrero |
| `VECES_UMA_TOPE` | 25 |
| `SDI_MAXIMO` | 10,000.00: arriba de eso casi siempre es un punto decimal omitido |
| `NOMBRE_REGEX` | Letras con acentos y ñ, espacio, punto, guion y apóstrofo |
| `ALFABETO_CURP` | `0-9A-NÑO-Z`, para el dígito verificador |
| `DIAS_ANTIGUEDAD_MAXIMA`, `DIAS_FUTURO_MAXIMO` | 5 años y 1 año, para el aviso de fecha lejana |
| `ORDEN_CAMPOS` | Orden visual de los campos, para listar los errores |

## Funciones
| Función | Qué hace | Devuelve |
|---|---|---|
| `normalizar_datos(datos)` | Limpia lo capturado: espacios del nombre, quita `\s - .` en CURP/RFC, solo dígitos en NSS y fecha, mayúsculas en catálogos ([[normalizacion-de-datos]]) | dict |
| `limites_sbc(fecha)` | (mínimo, tope) vigentes en la fecha del movimiento; en enero usa la UMA del año anterior ([[salario-sdi-y-limites]]) | tupla |
| `validar_curp`, `validar_nss`, `validar_rfc`, `validar_fecha`, `validar_tipo_movimiento` | Formato; la CURP también exige que su fecha exista (`_fecha_desde_aammdd`) | `(ok, mensaje)` |
| `verificar_digito_curp` | Dígito de RENAPO → **aviso** | `(ok, mensaje)` |
| `verificar_digito_nss` | Luhn → **aviso** | `(ok, mensaje)` |
| `verificar_rango_fecha` | Más de 1 año al futuro o más de 5 de antigüedad → **aviso** | `(ok, mensaje)` |
| `verificar_plazo(fecha, hoy)` | Usa `plazo.evaluar()`: VENCIDO o POR_VENCER → texto del **aviso** ([[plazo-legal]]) | str o None |
| `validar_sdi(valor, obligatorio, fecha)` | Error si falta en un alta, si no es número, si es menor al salario mínimo o mayor a 10,000; **aviso** si pasa de 25 UMA | `(ok, mensaje, aviso)` |
| `validar_coherencia_curp_rfc` | Las 4 letras (si el RFC tiene 13) y la fecha deben coincidir | `(ok, mensaje)` |
| `validar_catalogo(valor, catalogo, etiqueta, obligatorio)` | Obligatorio según el tipo; la clave debe estar en el catálogo | `(ok, mensaje)` |
| **`validar_campos(datos)`** | **Aplica todo** y separa errores de avisos ([[reglas-de-validacion]]) | `(errores, avisos)` |
| `validar_movimiento(datos)` | Interfaz estable `(bool, list[str])` que usa `test_prueba_concepto.py`. **No cambiar su firma** | `(es_valido, errores)` |

## Orden de evaluación dentro de `validar_campos`
1. Nombre: obligatorio, mínimo 5 caracteres y `NOMBRE_REGEX`.
2. CURP, NSS, RFC, fecha y tipo de movimiento.
3. Coherencia CURP↔RFC, solo si ambos pasaron el formato.
4. SDI, que es obligatorio en un alta.
5. Catálogos: tipo de trabajador, de salario y de jornada (obligatorios en un alta); causa de baja
   (obligatoria en una baja; error si un alta trae causa).
6. Avisos: dígito de la CURP, dígito del NSS, y para la fecha, el aviso de fecha lejana **o** el de plazo, nunca
   los dos.

## Trampas al modificarlo
- Si cambias reglas, **vuelve a correr** `python pruebas/test_prueba_concepto.py`: C1 y C2 deben seguir válidos y C3–C8
  rechazados ([[arnes-prueba-de-concepto]]). Corre también el bloque B de [[arnes-ambiente-relevante]].
- Si cambias la limpieza, **actualiza `emular_navegador()`** del arnés y las máscaras de `app.js`.
- Un error bloquea y un aviso no. Antes de convertir un aviso en error, lee [[errores-vs-avisos]].
- Los montos legales cambian cada año ([[mantenimiento-anual]]).

Ver también: [[reglas-de-validacion]] · [[modulo-plazo]] · [[modulo-app]]
