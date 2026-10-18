# Usar Sigma entre varias personas

Cómo hacer que varias personas capturen y vean **los mismos datos**, cada quien
desde su computadora.

---

## Por qué cada quien ve datos distintos

Sigma guarda todo (movimientos, trabajadores, usuarios y bitácora) en el archivo
`sigma_imss.db`, dentro de la carpeta `sigma-imss` de **cada computadora**.

Ese archivo **no se sube a GitHub** (`.gitignore` excluye `*.db`), a propósito:
el repositorio es público y la base guarda datos personales. Por eso, si alguien
descarga el proyecto y lo arranca, Sigma le crea una base **nueva y vacía** y no
ve lo que capturaron los demás.

La solución es la misma que en la oficina: **una sola computadora hace de
servidor** y guarda la base; las demás **no instalan nada** y entran con el
navegador a la dirección de esa computadora.

```
   PC de un amigo ──┐
                    ├──►  Tu PC (servidor.py + sigma_imss.db)
   PC de otro ──────┘      todos ven y capturan sobre la misma base
```

| Situación | Opción |
|---|---|
| Están conectados al **mismo Wi-Fi o red** (tu casa, la escuela) | [Opción 1: red local](#opción-1-misma-red-local) |
| Cada quien está **en su casa** | [Opción 2: Tailscale](#opción-2-cada-quien-en-su-casa-con-tailscale) |

---

## Opción 1: misma red local

### En tu PC (la que hace de servidor)

**1. Arranca el servidor** en una terminal abierta en la carpeta `sigma-imss`:

```powershell
python servidor.py
```

Deja esa ventana abierta mientras los demás trabajen.

**2. Busca tu dirección IP:**

```powershell
ipconfig
```

Usa la **Dirección IPv4** de tu Wi-Fi o Ethernet, por ejemplo `192.168.0.8`.

**3. Abre el puerto 5050 en el firewall** (solo la primera vez; PowerShell
**como administrador**):

```powershell
New-NetFirewallRule -DisplayName "Sigma" -Direction Inbound -Protocol TCP -LocalPort 5050 -RemoteAddress LocalSubnet -Action Allow
```

`LocalSubnet` deja entrar solo a equipos de tu misma red.

**4. Crea un usuario para cada persona** (solo la primera vez):

```powershell
python -m sigma.usuarios crear gael captura
python -m sigma.usuarios crear emilio administrador
```

La consola pide la contraseña dos veces (mínimo 8 caracteres) y no la muestra.
`captura` puede capturar y consultar; `administrador` además genera y descarga
los lotes del IDSE.

### En la PC de cada amigo

Abren el navegador (Chrome o Edge) en:

```
http://192.168.0.8:5050
```

con **tu** IP, e inician sesión con su usuario. No instalan nada.

---

## Opción 2: cada quien en su casa (con Tailscale)

La dirección de la opción 1 (`192.168.x.x`) **solo existe dentro de tu red**:
desde otra casa no abre. [Tailscale](https://tailscale.com) es gratis y crea una
red privada y cifrada entre sus computadoras, como si estuvieran en la misma
oficina. No hay que cambiar nada de Sigma.

### Una sola vez

**1. Todos** instalan Tailscale desde <https://tailscale.com/download> e inician
sesión.

**2. Tú** invitas a tus amigos a tu red desde el panel de Tailscale
(<https://login.tailscale.com/admin>): en **Users › Invite users**, o compartiendo
tu equipo en **Machines › Share**.

**3. En tu PC**, saca tu IP de Tailscale:

```powershell
tailscale ip -4
```

Te da algo como `100.101.102.103`.

**4. Abre el puerto para la red de Tailscale** (PowerShell **como
administrador**):

```powershell
New-NetFirewallRule -DisplayName "Sigma Tailscale" -Direction Inbound -Protocol TCP -LocalPort 5050 -RemoteAddress 100.64.0.0/10 -Action Allow
```

`100.64.0.0/10` son solo las direcciones de Tailscale: nadie más entra.

**5. Crea los usuarios** igual que en el paso 4 de la opción 1.

### Cada vez que vayan a trabajar

**En tu PC:** Tailscale conectado y el servidor corriendo:

```powershell
python servidor.py
```

**Tus amigos:** con Tailscale conectado, abren:

```
http://100.101.102.103:5050
```

con **tu** IP de Tailscale. Si en el panel está activado MagicDNS, también
funciona con el nombre de tu equipo: `http://nombre-de-tu-pc:5050`.

---

## Administrar a los usuarios

Todo se hace en tu PC, en la carpeta `sigma-imss`:

```powershell
python -m sigma.usuarios listar                 # quién existe, su rol y su estado
python -m sigma.usuarios contrasena gael        # cambiar su contraseña
python -m sigma.usuarios desbloquear gael       # tras 5 intentos fallidos (si no, espera 15 min)
python -m sigma.usuarios desactivar gael        # quitarle el acceso; su historial se conserva
python -m sigma.usuarios activar gael           # devolvérselo
```

Lo que capture cada quien queda en la bitácora **con su nombre**.

---

## Si algo falla

| Problema | Qué revisar |
|---|---|
| A tu amigo no le abre la página | Que `servidor.py` siga corriendo, que usen tu IP correcta y que exista la regla del firewall |
| Comprobar si llega a tu PC | Desde la PC de tu amigo: `Test-NetConnection 192.168.0.8 -Port 5050` (o tu IP de Tailscale). `TcpTestSucceeded : True` = sí llega |
| Tu IP cambió | Pasa con la red local al reiniciar el módem; vuelve a correr `ipconfig`. La de Tailscale casi no cambia |
| "Usuario o contraseña incorrectos" | La contraseña es la que tú asignaste con `python -m sigma.usuarios`, no la del recuadro "Acceso de prueba" |
| La cuenta se bloqueó | `python -m sigma.usuarios desbloquear <usuario>` |
| Al arrancar sale «el puerto 5050 ya está en uso» | Sigma ya está corriendo en esa PC. `servidor.py` ya no abre un segundo servidor en el mismo puerto (antes Windows lo permitía sin error); usa el que está abierto o ciérralo primero |

Para quitar las reglas del firewall cuando ya no las necesites:

```powershell
Remove-NetFirewallRule -DisplayName "Sigma"
Remove-NetFirewallRule -DisplayName "Sigma Tailscale"
```

---

## Cuidados

- **Tu PC debe estar prendida** y con `servidor.py` abierto mientras los demás
  trabajan. Si lo cierras, no se pierde nada: los datos siguen en tu
  `sigma_imss.db` y vuelven a aparecer al arrancarlo.
- Sigma respalda la base sola al arrancar y cada 24 horas en `respaldos/`.
- **No abras el puerto en tu módem** ni uses programas que generen un link
  público: Sigma quedaría expuesto a cualquiera en internet y, sin HTTPS, los
  datos y las contraseñas viajarían sin cifrar. Tailscale sí cifra la conexión.
- **No subas `sigma_imss.db` a GitHub**: el repositorio es público.
- Si solo quieres pasarle tus datos a alguien (sin trabajar al mismo tiempo),
  mándale una copia de `sigma_imss.db` o de un archivo de `respaldos/` para que
  lo ponga en su carpeta. Es una copia: lo que capture cada uno después ya no lo
  ve el otro.

---

Más detalle: [README.md](README.md) (comandos rápidos) ·
[Ejecutar.md](Ejecutar.md) (instalación y problemas) ·
[Instrucciones.md](Instrucciones.md) (cómo se usa la página).
