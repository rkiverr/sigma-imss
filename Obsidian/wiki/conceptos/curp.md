---
tipo: concepto
tags: [curp, renapo, digito-verificador, identificadores]
fuentes: ["validaciones.py", "prueba_ambiente_relevante.py"]
actualizado: 2026-10-04
---

# CURP: estructura y dígito verificador

La **Clave Única de Registro de Población** tiene 18 caracteres y la emite RENAPO.

```text
G O M F 8 8 0 3 2 3 H D G N R R 0 0
└─┬───┘ └────┬────┘ │ └┬┘ └─┬─┘ │ │
  │          │      │  │    │   │ └ 18: dígito verificador
  │          │      │  │    │   └── 17: homoclave (0-9 si nació antes de 2000; A-Z desde 2000)
  │          │      │  │    └────── 14-16: primeras consonantes internas de apellido paterno, materno y nombre
  │          │      │  └─────────── 12-13: entidad de nacimiento (NL, CL, TS, …)
  │          │      └────────────── 11: sexo (H o M)
  │          └───────────────────── 5-10: fecha de nacimiento AAMMDD
  └──────────────────────────────── 1-4: inicial y primera vocal interna del paterno, inicial del materno, inicial del nombre
```

## Cómo la valida Sigma (`validaciones.py`)
1. **Error:** debe tener 18 caracteres y cumplir `CURP_REGEX` (`^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$`).
2. **Error:** la fecha AAMMDD debe existir (`_fecha_desde_aammdd`). Los años de 00 al año actual mod 100 se toman
   como 2000s; el resto, como 1900s.
3. **Error:** debe coincidir con el RFC en las primeras 4 letras (si el RFC tiene 13) y en la fecha ([[rfc]]).
4. **Aviso (E5):** dígito verificador (`verificar_digito_curp`).

## Algoritmo del dígito verificador (RENAPO)
```python
ALFABETO = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"   # valor = posición
suma = sum(ALFABETO.index(c) * (18 - i) for i, c in enumerate(curp[:17]))
digito = (10 - suma % 10) % 10
```
Se verificó contra el ejemplo de RENAPO **HEGG560427MVZRRL04**: el algoritmo da 4.

### ⚠ Límite del algoritmo
Los pesos van de 18 a 2 y se toma la suma **módulo 10**, así que **no todos los cambios de una letra se
detectan**:
- En la posición 14 (peso 5), un cambio de valor par da el mismo dígito.
- En la 15 (peso 4), un cambio múltiplo de 5.
- En la 16 (peso 3), uno múltiplo de 10.

En el E5, de 8 CURP con una consonante cambiada, **4 se detectaron y 4 no**. Confirmar esos casos exige
consultar RENAPO, que no tiene una API pública ([[bugs-corregidos]], E-13).

**¿Por qué es aviso y no error?** Por la misma razón que con el NSS: el capturista debe confirmarla contra la
constancia de CURP, y el IMSS es quien la valida contra RENAPO ([[errores-vs-avisos]]).

## Cómo la construye el arnés (datos sintéticos)
`prueba_ambiente_relevante.Plantilla` aplica las reglas de RENAPO:
- Ñ→X y sin acentos.
- Se saltan las partículas (DE, LA, DEL…).
- En nombres compuestos con José o María, usa el segundo nombre.
- Primera vocal y consonantes internas.
- Entidad aleatoria (NL en el 54 % de los casos).
- Homoclave 0 o A.
- **Dígito verificador correcto.**

Ver [[arnes-ambiente-relevante]].

Ver también: [[nss]] · [[rfc]] · [[reglas-de-validacion]]
