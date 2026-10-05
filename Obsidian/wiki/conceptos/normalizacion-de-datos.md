---
tipo: concepto
tags: [normalizacion, mascaras, captura, data-longitud]
fuentes: ["sigma/validaciones.py", "sigma/app.py", "sigma/static/js/app.js", "sigma/templates/index.html"]
actualizado: 2026-10-04
---

# Normalización de lo capturado

Antes de validar, el sistema **limpia** lo que escribió o pegó el usuario. Hay dos lugares que deben coincidir:
el **servidor** y las **máscaras del navegador**.

## En el servidor: `validaciones.normalizar_datos()` (E5)
La usan **los dos** caminos: `POST /capturar` (`_leer_formulario`) y `POST /api/validar`.

| Campo | Limpieza |
|---|---|
| Todos | `strip()` |
| Nombre | Colapsa los espacios repetidos |
| CURP, RFC | Quita espacios, guiones y puntos; mayúsculas |
| NSS, fecha | Deja **solo dígitos**: "05/09/2026" → "05092026"; "43 16 89 1234 5" → "43168912345" |
| Catálogos | Mayúsculas |

**Antes del E5**, la API no quitaba los espacios del NSS ni las diagonales de la fecha. La validación en vivo
decía "error" en datos que el servidor sí aceptaba (E-07).

## En el navegador: máscaras de `app.js`
- NSS y fecha: elimina todo lo que no sea dígito.
- CURP y RFC: mayúsculas; elimina todo lo que no sea `A-Z`, `Ñ`, `&` o un dígito.
- **Primero limpia y después recorta** a la longitud de `data-longitud` (18, 11, 13 y 8).

### Por qué `data-longitud` y no `maxlength` ([[adr-011-normalizacion-unica-y-data-longitud]])
Con `maxlength="11"`, al pegar "43 16 89 1234 5" (15 caracteres) el navegador **recortaba primero** a
"43 16 89 12" y luego la máscara dejaba "43168912": se perdían 3 dígitos y el servidor rechazaba un NSS válido.
En el E5 fallaron así **24 de 24** capturas válidas pegadas (E-06). Ahora la máscara limpia todo y recorta al
final.

## Sin JavaScript
El servidor normaliza igual, así que la página funciona aunque el navegador no ejecute JS.

## Trampa
Si cambias la limpieza, **actualiza las tres cosas a la vez**: `normalizar_datos()`, las máscaras de `app.js` y
`emular_navegador()` del arnés ([[arnes-ambiente-relevante]]).

Ver también: [[modulo-validaciones]] · [[modulo-interfaz]]
