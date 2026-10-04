---
tipo: concepto
tags: [nss, luhn, digito-verificador, identificadores]
fuentes: ["validaciones.py"]
actualizado: 2026-10-04
---

# NSS: número de seguridad social y dígito de Luhn

Son **11 dígitos**:
- 2 de subdelegación.
- 2 del año de afiliación.
- 2 del año de nacimiento.
- 4 de consecutivo.
- **1 dígito verificador.**

## Cómo lo valida Sigma
1. **Normalización:** se quitan los espacios, guiones y cualquier otro carácter que no sea dígito
   ([[normalizacion-de-datos]]). "43 16 89 1234 5" se vuelve "43168912345".
2. **Error:** obligatorio, solo dígitos y exactamente 11 (`NSS_REGEX`).
3. **Error (con la base):** no puede pertenecer a otro trabajador, y una CURP ya registrada no puede venir con
   otro NSS (`conflicto_de_identidad`).
4. **Aviso:** dígito verificador de **Luhn** (`verificar_digito_nss`).

## Algoritmo (`_digito_verificador_nss`)
```python
suma = 0
for i, c in enumerate(nss[:10]):
    d = int(c)
    if i % 2:            # posiciones impares (base 0): 1, 3, 5, 7, 9 se duplican
        d *= 2
        if d > 9:
            d -= 9
    suma += d
digito = (10 - suma % 10) % 10
```
Luhn detecta **cualquier dígito equivocado** y **casi cualquier par de dígitos adyacentes transpuestos**; la
excepción es 09↔90. En el E5 avisó en 8 de 8 transposiciones y en 8 de 8 dígitos cambiados.

## ¿Por qué es aviso y no error?
**Existen NSS históricos**, emitidos antes de que se estandarizara el dígito, que no cumplen Luhn y son
perfectamente válidos. Bloquearlos impediría capturar movimientos legítimos ([[errores-vs-avisos]],
[[adr-004-errores-y-avisos-son-distintos]]).

Ver también: [[curp]] · [[reglas-de-validacion]]
