---
tipo: consulta
tags: [preguntas, faq, dudas-resueltas]
fuentes: ["sigma/database.py", "sigma/app.py", "sigma/templates/base.html", "raw/historial/git-log.md"]
actualizado: 2026-10-04
---

# Preguntas frecuentes

Preguntas que ya se hicieron, con su respuesta. Si una respuesta cambia, se corrige aquí y se anota en el log.

## Sobre la interfaz
**¿Qué hacen los dos usuarios del desplegable "Usuario responsable"?**
Solo firman la bitácora. Los roles `administrador` y `captura` son etiquetas: no hay permisos ni login. Es una
limitación conocida (E-17, [[bugs-conocidos]]); en TRL 6 entra la autenticación ([[hoja-de-ruta-trl6]]).

**¿Qué es la insignia `A1234567890 · Desarrollos Eléctricos…`?**
- Es el **patrón**: el registro patronal y la razón social.
- Es **dato semilla inventado** (`PATRON_SEMILLA` en `database.py`) y va como primer campo de cada línea del lote
  IDSE ([[lote-idse]]).
- **Para cambiarlo:** edita esa constante y borra `sigma_imss.db` para que se vuelva a sembrar.
- Hoy la interfaz usa solo el primer patrón.

**¿El punto verde junto a "SQLite · sigma_imss.db" significa que la base está activa?**
No: es decorativo y no monitorea nada. Lo que sí garantiza que la base respondió es que la página cargue; si no
respondiera, saldría la página 503 ([[modulo-app]]). Una mejora opcional sería colorearlo según el motor.

**¿Por qué el formulario acepta un movimiento que tiene avisos amarillos?**
Porque los avisos no bloquean: hay NSS históricos legítimos que no pasan Luhn, y un movimiento fuera de plazo
igual se debe presentar, solo que con riesgo de multa ([[errores-vs-avisos]]).

## Sobre los datos
**¿Sigma tiene base de datos?**
Sí: 5 tablas ([[modelo-de-datos]]), con PostgreSQL desde el E3. Lo que se agregó en el E4 es que elija el motor
solo y use SQLite si no hay PostgreSQL ([[doble-motor-de-base-de-datos]]).

**¿Por qué no veo lo que capturó mi compañero?**
La base es **local de cada quien**: `sigma_imss.db` está en `.gitignore`. Para compartir datos haría falta un
PostgreSQL hospedado y apuntar `DATABASE_URL` hacia él ([[configuracion]]).

**¿Por qué el E5 no se probó con datos reales de la empresa?**
- La LFPDPPP protege la CURP, el NSS y el salario, y para usarlos hace falta el aviso de privacidad y el
  consentimiento.
- El envío real al IDSE exige la e.firma del patrón.

Por eso el TRL 5 usa un **ambiente emulado** con supuestos declarados; la operación real es TRL 6–7
([[entregable-5-trl5]]).

## Sobre el código y las ramas
**¿Por qué la rama aparece dos veces en GitHub?**
Es una sola. "Your branches" y "Active branches" son dos vistas de la misma lista.

**¿Por qué sigue existiendo `trl5/ambiente-relevante` si ya está en `main`?**
Porque el informe del E5 la cita por nombre. Se dejó en GitHub para que la cita no quede rota ([[cronologia]]).

**¿Arranco con `app.py` o con `servidor.py`?**
- Para usarlo en la red de la oficina: **`python servidor.py`** (waitress).
- El servidor de desarrollo escucha en `127.0.0.1` y depura solo con `SIGMA_DEBUG=1`. Con la estructura de
  `sigma/` (PR #2) se arranca con **`python -m sigma`**; antes era `python app.py`.

Ver [[como-arrancar]] y [[adr-009-servidor-de-produccion-waitress]].

**¿Puedo escribir SQL con `?`?**
No. Todo SQL va con `%s`; el envoltorio de SQLite lo traduce en un solo sentido
([[adr-008-sql-con-marcadores-psycopg2]]).

**¿Dónde está el script que generó los informes?**
- **E4:** se descartó porque Pedro no quiso archivos extra en el repo.
- **E5:** la receta completa, con fragmentos de código, está en [[como-se-hizo-el-entregable-5]].

**¿Los cambios del E5 pasaron por un PR?**
No. Pedro pidió integrarlos directo a `main` (`cffd375`). Queda pendiente avisarle a Gael
([[sesion-2026-10-04-entregable-5]]).

**¿Y la reorganización en carpetas?**
Se abrió el PR #2, pero Pedro pidió integrarla directo a `main` (`fb3a4a8`) sin esperar la revisión. El PR quedó
cerrado como integrado, porque GitHub no deja borrarlos. También falta avisarle a Gael
([[sesion-2026-10-04-estructura-de-carpetas]]).

**Ahora que la reorganización está en `main`, ¿la computadora de cada quien se reorganiza sola?**
No. **GitHub** ya tiene la estructura nueva (merge `fb3a4a8`), pero cada copia local cambia hasta que se baja:
```bash
git switch main
git pull
```
- Git mueve solo los archivos a `sigma/` y `pruebas/` y conserva su historial.
- Antes: detener Sigma y hacer commit o `git stash` de los cambios sin guardar. Si sale "Permission denied" al
  mover una carpeta, cerrar VS Code y repetir el `git pull`.
- `sigma_imss.db` y `exportaciones/` se quedan donde estaban: no se pierde lo capturado.
- Los reportes viejos sueltos en la raíz (`resultados_*`) ya no están en `.gitignore` y aparecen en `git status`;
  se pueden borrar.
- Para programar, `python app.py` pasa a ser `python -m sigma`.

Ver [[adr-017-paquete-sigma-y-carpeta-de-pruebas]].

**¿Cómo sé que la reorganización funciona igual que antes?**
Se comparó contra `main` con el mismo arnés: 10/10 criterios en las dos versiones, 0 diferencias funcionales y
18/18 respuestas HTTP idénticas. El método se puede repetir: [[verificar-un-cambio-contra-main]].

## Sobre la clasificación del sistema
**¿Sigma es de lazo abierto o de lazo cerrado?**
De **lazo cerrado**: lo decidió Pedro el 19 de sep. El E4 decía "abierto con retroalimentación al operador", pero
lo vigente es cerrado ([[adr-015-lazo-cerrado]], [[sigma-como-sistema-de-control]]).

Ver también: [[problemas-frecuentes]] · [[glosario]]
