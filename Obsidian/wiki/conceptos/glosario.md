---
tipo: concepto
tags: [glosario, imss, terminos]
fuentes: ["raw/entregables/e1-trl1-problematica.md", "raw/normativa/"]
actualizado: 2026-10-04
---

# Glosario

| Término | Qué significa en Sigma |
|---|---|
| **IMSS** | Instituto Mexicano del Seguro Social |
| **IDSE** | "IMSS desde su empresa": la plataforma donde el patrón presenta los movimientos ([[lote-idse]]) |
| **Movimiento afiliatorio** | Aviso al IMSS de que un trabajador entra (alta 08), sale (baja 02) o cambia de salario (07, no implementado) |
| **Alta / Reingreso (08)** | Inscripción de un trabajador; reingreso si ya había estado en la empresa |
| **Baja (02)** | Fin de la relación laboral; lleva causa de baja ([[catalogos-idse]]) |
| **Patrón / registro patronal** | La empresa ante el IMSS, con una clave de 11 caracteres. La de Sigma (`A1234567890`) es inventada |
| **NSS** | Número de seguridad social, de 11 dígitos ([[nss]]) |
| **CURP** | Clave Única de Registro de Población, de 18 caracteres ([[curp]]) |
| **RFC** | Registro Federal de Contribuyentes: 13 caracteres para persona física con homoclave ([[rfc]]) |
| **SDI** | Salario diario integrado, en pesos por día ([[salario-sdi-y-limites]]) |
| **SBC** | Salario base de cotización: con el que se cotiza; tiene mínimo y tope legal |
| **UMA** | Unidad de Medida y Actualización: $117.31 al día en 2026, desde el 1 de febrero |
| **Tope de 25 UMA** | Máximo SBC: $2,932.75 en 2026 |
| **Plazo legal** | 5 días hábiles para presentar altas y bajas (art. 15 LSS, [[plazo-legal]]) |
| **Días hábiles** | Ni sábado, ni domingo, ni día de descanso obligatorio (art. 74 LFT) |
| **Acuse** | Respuesta del IMSS a un movimiento: aceptado o rechazado |
| **e.firma** | Firma electrónica del patrón con la que se autentica la carga en el IDSE. Sigma no la usa ni la guarda |
| **Lote** | Archivo de texto con varios movimientos para cargarlo en el IDSE |
| **Bitácora** | Registro de auditoría: cada captura, rechazo y exportación, con usuario y hora |
| **Residente de obra** | Encargado en la obra; avisa a la oficina quién entra o sale |
| **Cuadrilla** | Grupo de trabajadores de una obra, que se arma y se disuelve según el proyecto |
| **Capturista** | Quien escribe los movimientos en Sigma (rol "captura") |
| **Error** | Regla que **impide guardar** ([[errores-vs-avisos]]) |
| **Aviso** | Advertencia que **deja guardar** ([[errores-vs-avisos]]) |
| **Folio** | El id del movimiento en Sigma (#N) |
| **TRL** | Technology Readiness Level, nivel de madurez tecnológica ([[niveles-trl]]) |
| **Lazo interno / externo** | Corrección en segundos con la validación, y en días con el acuse ([[sigma-como-sistema-de-control]]) |
| **LSS** | Ley del Seguro Social |
| **RACERF** | Reglamento de la LSS en materia de Afiliación, Clasificación de Empresas, Recaudación y Fiscalización |
| **LFT** | Ley Federal del Trabajo |
| **LFPDPPP** | Ley Federal de Protección de Datos Personales en Posesión de los Particulares (nueva, DOF 20-03-2025) |
| **WCAG** | Pautas de accesibilidad web del W3C ([[accesibilidad]]) |
| **CSRF** | Falsificación de peticiones entre sitios ([[seguridad-web]]) |
| **CSP** | Content-Security-Policy: limita qué scripts puede ejecutar la página ([[seguridad-web]]) |
| **waitress** | Servidor WSGI de producción para Python ([[modulo-servidor]]) |
| **Arnés** | Programa que prueba el sistema de forma automática ([[estrategia-de-pruebas]]) |
| **p95** | Percentil 95: el tiempo dentro del cual se atendió el 95 % de las peticiones |

Ver también: [[inicio]]
