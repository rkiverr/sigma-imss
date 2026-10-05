---
tipo: concepto
tags: [rfc, sat, identificadores, coherencia]
fuentes: ["sigma/validaciones.py"]
actualizado: 2026-10-04
---

# RFC y su coherencia con la CURP

El **Registro Federal de Contribuyentes** de una persona física tiene **13 caracteres**:
- 4 letras.
- 6 dígitos con la fecha AAMMDD.
- 3 de homoclave.

El de una persona moral tiene 12. Puede incluir **Ñ** y **&**.

## Cómo lo valida Sigma
1. **Normalización:** mayúsculas, sin espacios, guiones ni puntos.
2. **Error:** obligatorio y `RFC_REGEX` = `^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$`.
3. **Error, coherencia con la CURP** (`validar_coherencia_curp_rfc`), solo si ambos pasaron el formato:
   - Si el RFC tiene 13 caracteres, sus **primeras 4 letras** deben ser iguales a las de la CURP.
   - Su **fecha** (`rfc[-9:-3]`) debe ser igual a la de la CURP (`curp[4:10]`).

**Por qué:** el RFC de una persona física se construye con las mismas iniciales y la misma fecha que su CURP. Si
los dos tienen formato válido pero no concuerdan, uno de los dos está mal tecleado.

## Limitación
La **homoclave** y su dígito verificador **no se validan**: el cálculo depende de un algoritmo del SAT sobre el
nombre completo. En el E5, un RFC con la fecha cambiada se bloqueó en 8 de 8 casos (categoría B09).

Ver también: [[curp]] · [[reglas-de-validacion]]
