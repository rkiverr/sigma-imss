---
tipo: concepto
tags: [errores, avisos, validacion, diseno]
fuentes: ["sigma/validaciones.py", "sigma/templates/index.html", "sigma/static/css/estilos.css"]
actualizado: 2026-10-04
---

# Errores y avisos son cosas distintas

Es una de las ideas centrales del diseño ([[adr-004-errores-y-avisos-son-distintos]]).

| | Error | Aviso |
|---|---|---|
| ¿Deja guardar? | **No**. El servidor responde 422 y devuelve el formulario | **Sí**. Guarda y muestra la advertencia |
| En la interfaz | Borde rojo y mensaje en rojo, más el resumen de errores arriba | Borde ámbar y mensaje en ámbar; *flash* "warning" |
| Para qué | El dato es **imposible** o **ilegal** | El dato es **sospechoso**, pero puede ser real |
| Estructura | Diccionario `errores[campo]` | Diccionario `avisos[campo]` |

## Cuáles son avisos (y por qué)
| Aviso | Por qué no se bloquea |
|---|---|
| Dígito de Luhn del NSS no cuadra | Hay NSS históricos válidos que no lo cumplen ([[nss]]) |
| Dígito de RENAPO de la CURP no cuadra (E5) | Se confirma contra la constancia; el IMSS valida contra RENAPO ([[curp]]) |
| SDI mayor a 25 UMA (E5) | El salario puede ser real; solo se cotiza con el tope ([[salario-sdi-y-limites]]) |
| Plazo vencido o por vencer (E5) | El movimiento igual debe presentarse, y cuanto antes ([[plazo-legal]]) |
| Fecha a más de 1 año al futuro o con más de 5 de antigüedad | Raro, pero posible |
| Baja sin historial en Sigma (E5) | Personal contratado antes de usar el sistema ([[historial-afiliatorio]]) |

## Regla para el futuro
Antes de convertir un aviso en error, pregúntate si existe **algún caso legítimo** que quedaría bloqueado. Si
existe, debe quedarse como aviso. Al revés: lo que la ley prohíbe sin excepción (SDI bajo el mínimo, alta sobre
alta vigente) es **error**.

Ver también: [[reglas-de-validacion]] · [[modulo-validaciones]]
