/* ==========================================================================
   Sigma — lógica de interfaz.

   Todo el archivo es progresivo: si el navegador no ejecuta JavaScript, el
   formulario sigue funcionando porque el servidor valida y responde igual.
   Aquí solo se agrega retroalimentación inmediata y comodidad de captura.
   ========================================================================== */
(function () {
  "use strict";

  /* ----------------------------------------------------------------------
     Tema claro / oscuro
     ---------------------------------------------------------------------- */
  var LLAVE_TEMA = "sigma-tema";

  function temaGuardado() {
    try {
      return localStorage.getItem(LLAVE_TEMA);
    } catch (e) {
      return null; // modo privado o almacenamiento bloqueado
    }
  }

  function temaEfectivo() {
    var elegido = document.documentElement.getAttribute("data-tema");
    if (elegido) return elegido;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "oscuro" : "claro";
  }

  function sincronizarBoton(tema) {
    var boton = document.getElementById("interruptor-tema");
    if (!boton) return;
    boton.setAttribute("aria-pressed", String(tema === "oscuro"));
    boton.setAttribute("title", tema === "oscuro"
      ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
  }

  function aplicarTema(tema) {
    document.documentElement.setAttribute("data-tema", tema);
    try {
      localStorage.setItem(LLAVE_TEMA, tema);
    } catch (e) { /* sin persistencia, el tema dura la sesión */ }
    sincronizarBoton(tema);
  }

  function iniciarTema() {
    var boton = document.getElementById("interruptor-tema");
    if (!boton) return;
    // Mientras el usuario no elija, no se escribe nada: el tema del sistema
    // manda y el CSS ya lo resuelve solo.
    sincronizarBoton(temaEfectivo());
    boton.addEventListener("click", function () {
      aplicarTema(temaEfectivo() === "oscuro" ? "claro" : "oscuro");
    });
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (evento) {
      if (!temaGuardado()) sincronizarBoton(evento.matches ? "oscuro" : "claro");
    });
  }

  /* ----------------------------------------------------------------------
     Notificaciones flotantes
     ---------------------------------------------------------------------- */
  function iniciarNotificaciones() {
    document.querySelectorAll(".notificacion").forEach(function (nota) {
      var cerrar = nota.querySelector("button");
      if (cerrar) cerrar.addEventListener("click", function () { desvanecer(nota); });
      if (!nota.classList.contains("notificacion-error")) {
        setTimeout(function () { desvanecer(nota); }, 7000);
      }
    });
  }

  function desvanecer(elemento) {
    elemento.style.transition = "opacity 200ms, transform 200ms";
    elemento.style.opacity = "0";
    elemento.style.transform = "translateY(8px)";
    setTimeout(function () { elemento.remove(); }, 220);
  }

  /* ----------------------------------------------------------------------
     Formulario de captura
     ---------------------------------------------------------------------- */
  var formulario = document.getElementById("formulario-captura");
  var tocados = new Set();
  var temporizador = null;

  function contenedorDe(nombre) {
    return document.querySelector('.campo[data-campo="' + nombre + '"]');
  }

  function pintarCampo(nombre, estado, mensaje) {
    var contenedor = contenedorDe(nombre);
    if (!contenedor) return;
    var control = contenedor.querySelector("input, select");
    var texto = contenedor.querySelector(".mensaje");

    if (estado) {
      contenedor.setAttribute("data-estado", estado);
    } else {
      contenedor.removeAttribute("data-estado");
    }
    if (texto) texto.textContent = mensaje || "";
    if (control) {
      if (estado === "error") {
        control.setAttribute("aria-invalid", "true");
      } else {
        control.removeAttribute("aria-invalid");
      }
    }
  }

  function datosDelFormulario() {
    var datos = {};
    new FormData(formulario).forEach(function (valor, clave) {
      datos[clave] = valor;
    });
    return datos;
  }

  function validarEnServidor(mostrarTodo) {
    if (!formulario) return Promise.resolve(true);
    return fetch("/api/validar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datosDelFormulario())
    })
      .then(function (respuesta) { return respuesta.json(); })
      .then(function (resultado) {
        formulario.querySelectorAll(".campo[data-campo]").forEach(function (contenedor) {
          var nombre = contenedor.getAttribute("data-campo");
          if (!mostrarTodo && !tocados.has(nombre)) return;

          if (resultado.errores[nombre]) {
            pintarCampo(nombre, "error", resultado.errores[nombre]);
          } else if (resultado.avisos[nombre]) {
            pintarCampo(nombre, "aviso", resultado.avisos[nombre]);
          } else {
            var control = contenedor.querySelector("input, select");
            var lleno = control && String(control.value || "").trim() !== "";
            pintarCampo(nombre, lleno ? "ok" : null, "");
          }
        });
        return resultado.valido;
      })
      .catch(function () {
        // Sin conexión con el servidor no bloqueamos: el envío normal validará.
        return true;
      });
  }

  function programarValidacion(mostrarTodo) {
    clearTimeout(temporizador);
    temporizador = setTimeout(function () { validarEnServidor(mostrarTodo); }, 260);
  }

  /* Máscaras de captura: evitan el error antes de que ocurra. */
  function aplicarMascaras() {
    var soloDigitos = ["nss", "fecha_movimiento"];
    var mayusculas = ["curp", "rfc"];

    soloDigitos.forEach(function (nombre) {
      var control = formulario.elements[nombre];
      if (!control) return;
      control.addEventListener("input", function () {
        var limpio = control.value.replace(/\D/g, "");
        if (limpio !== control.value) control.value = limpio;
        actualizarContador(nombre);
      });
    });

    mayusculas.forEach(function (nombre) {
      var control = formulario.elements[nombre];
      if (!control) return;
      control.addEventListener("input", function () {
        var posicion = control.selectionStart;
        var limpio = control.value.toUpperCase().replace(/[^A-ZÑ&0-9]/g, "");
        if (limpio !== control.value) {
          control.value = limpio;
          try { control.setSelectionRange(posicion, posicion); } catch (e) { /* ignorado */ }
        }
        actualizarContador(nombre);
      });
    });

    var nombreCompleto = formulario.elements.nombre_completo;
    if (nombreCompleto) {
      nombreCompleto.addEventListener("blur", function () {
        nombreCompleto.value = nombreCompleto.value.replace(/\s+/g, " ").trim();
      });
    }
  }

  function actualizarContador(nombre) {
    var contenedor = contenedorDe(nombre);
    if (!contenedor) return;
    var contador = contenedor.querySelector(".contador");
    var control = contenedor.querySelector("input");
    if (!contador || !control || !control.maxLength || control.maxLength < 0) return;
    contador.textContent = control.value.length + "/" + control.maxLength;
  }

  /* Selector de fecha nativo sincronizado con el campo DDMMAAAA que pide IDSE. */
  function iniciarFecha() {
    var texto = formulario.elements.fecha_movimiento;
    var calendario = document.getElementById("selector-fecha");
    if (!texto || !calendario) return;

    calendario.addEventListener("change", function () {
      if (!calendario.value) return;
      var partes = calendario.value.split("-"); // AAAA-MM-DD
      texto.value = partes[2] + partes[1] + partes[0];
      actualizarContador("fecha_movimiento");
      tocados.add("fecha_movimiento");
      programarValidacion(false);
    });

    texto.addEventListener("input", function () {
      var valor = texto.value;
      if (/^\d{8}$/.test(valor)) {
        calendario.value = valor.slice(4, 8) + "-" + valor.slice(2, 4) + "-" + valor.slice(0, 2);
      } else {
        calendario.value = "";
      }
    });

    if (/^\d{8}$/.test(texto.value)) {
      calendario.value = texto.value.slice(4, 8) + "-" + texto.value.slice(2, 4) + "-" + texto.value.slice(0, 2);
    }
  }

  /* Los campos de alta y de baja son excluyentes: se muestran según el tipo. */
  function iniciarCamposCondicionales() {
    var tipo = formulario.elements.tipo_movimiento;
    if (!tipo) return;

    function refrescar() {
      var esAlta = tipo.value === "08";
      document.querySelectorAll("[data-visible-en]").forEach(function (bloque) {
        var visible = bloque.getAttribute("data-visible-en") === (esAlta ? "08" : "02");
        bloque.hidden = !visible;
        bloque.querySelectorAll("input, select").forEach(function (control) {
          control.disabled = !visible;
          if (!visible) {
            control.value = "";
            pintarCampo(control.name, null, "");
            tocados.delete(control.name);
          }
        });
      });
      document.querySelectorAll("[data-requerido-en]").forEach(function (etiqueta) {
        etiqueta.hidden = etiqueta.getAttribute("data-requerido-en") !== (esAlta ? "08" : "02");
      });
    }

    tipo.addEventListener("change", function () {
      refrescar();
      programarValidacion(false);
    });
    refrescar();
  }

  function iniciarFormulario() {
    if (!formulario) return;

    aplicarMascaras();
    iniciarFecha();
    iniciarCamposCondicionales();

    formulario.querySelectorAll(".campo[data-campo]").forEach(function (contenedor) {
      var nombre = contenedor.getAttribute("data-campo");
      var control = contenedor.querySelector("input, select");
      if (!control) return;
      actualizarContador(nombre);

      control.addEventListener("blur", function () {
        tocados.add(nombre);
        programarValidacion(false);
      });
      control.addEventListener("input", function () {
        if (tocados.has(nombre)) programarValidacion(false);
      });
      control.addEventListener("change", function () {
        tocados.add(nombre);
        programarValidacion(false);
      });
    });

    var boton = document.getElementById("boton-capturar");
    formulario.addEventListener("submit", function () {
      if (boton) {
        boton.disabled = true;                       // evita el doble envío
        boton.textContent = "Guardando…";
        // Si el servidor devuelve la página con errores, el botón vuelve solo
        // porque se recarga el documento completo.
        setTimeout(function () {
          boton.disabled = false;
          boton.textContent = "Capturar movimiento";
        }, 6000);
      }
    });

    var limpiar = document.getElementById("boton-limpiar");
    if (limpiar) {
      limpiar.addEventListener("click", function () {
        formulario.reset();
        tocados.clear();
        formulario.querySelectorAll(".campo[data-campo]").forEach(function (contenedor) {
          pintarCampo(contenedor.getAttribute("data-campo"), null, "");
          actualizarContador(contenedor.getAttribute("data-campo"));
        });
        var calendario = document.getElementById("selector-fecha");
        if (calendario) calendario.value = "";
        formulario.elements.nombre_completo.focus();
      });
    }

    // Si el servidor devolvió errores, ya son campos "tocados".
    formulario.querySelectorAll('.campo[data-estado="error"], .campo[data-estado="aviso"]')
      .forEach(function (contenedor) { tocados.add(contenedor.getAttribute("data-campo")); });
  }

  /* ----------------------------------------------------------------------
     Filtros de la tabla
     ---------------------------------------------------------------------- */
  function iniciarFiltros() {
    var filtros = document.getElementById("formulario-filtros");
    if (!filtros) return;
    var espera = null;

    filtros.querySelectorAll("select").forEach(function (control) {
      control.addEventListener("change", function () { filtros.submit(); });
    });

    var busqueda = filtros.elements.q;
    if (busqueda) {
      busqueda.addEventListener("input", function () {
        clearTimeout(espera);
        espera = setTimeout(function () { filtros.submit(); }, 480);
      });
    }
  }

  /* ----------------------------------------------------------------------
     Detalle de un movimiento
     ---------------------------------------------------------------------- */
  function iniciarDetalle() {
    var dialogo = document.getElementById("dialogo-detalle");
    if (!dialogo || typeof dialogo.showModal !== "function") return;
    var cuerpo = document.getElementById("dialogo-cuerpo");
    var titulo = document.getElementById("dialogo-titulo");

    document.querySelectorAll("tr[data-movimiento]").forEach(function (fila) {
      function abrir() { mostrar(fila.getAttribute("data-movimiento")); }
      fila.addEventListener("click", abrir);
      fila.addEventListener("keydown", function (evento) {
        if (evento.key === "Enter" || evento.key === " ") {
          evento.preventDefault();
          abrir();
        }
      });
    });

    dialogo.querySelector(".dialogo-cerrar").addEventListener("click", function () {
      dialogo.close();
    });

    function fila(etiqueta, valor, mono) {
      if (valor === null || valor === undefined || valor === "") return "";
      return "<dt>" + escapar(etiqueta) + "</dt><dd" + (mono ? ' class="mono"' : "") + ">"
        + escapar(String(valor)) + "</dd>";
    }

    function mostrar(id) {
      titulo.textContent = "Movimiento #" + id;
      cuerpo.innerHTML = '<p class="ayuda">Cargando…</p>';
      dialogo.showModal();

      fetch("/api/movimiento/" + encodeURIComponent(id))
        .then(function (respuesta) {
          if (!respuesta.ok) throw new Error("No disponible");
          return respuesta.json();
        })
        .then(function (m) {
          var html = '<dl class="definiciones">'
            + fila("Trabajador", m.nombre_completo)
            + fila("CURP", m.curp, true)
            + fila("NSS", m.nss, true)
            + fila("RFC", m.rfc, true)
            + fila("Tipo", m.tipo_movimiento + " — " + m.tipo_etiqueta)
            + fila("Fecha", m.fecha_legible)
            + fila("Estado", m.estado)
            + fila("Tipo de trabajador", m.tipo_trabajador_etiqueta || m.tipo_trabajador)
            + fila("Tipo de salario", m.tipo_salario_etiqueta || m.tipo_salario)
            + fila("Tipo de jornada", m.tipo_jornada_etiqueta || m.tipo_jornada)
            + fila("Salario diario integrado", m.sdi)
            + fila("Causa de baja", m.causa_baja_etiqueta || m.causa_baja)
            + fila("Registro patronal", m.registro_patronal, true)
            + fila("Razón social", m.razon_social)
            + fila("Capturado", m.creado_en)
            + "</dl>";

          if (m.historial && m.historial.length) {
            html += '<h3 class="subtitulo-dialogo">Bitácora del movimiento</h3>';
            html += '<ul class="linea-tiempo">';
            m.historial.forEach(function (registro) {
              html += "<li><span class=\"accion\">" + escapar(registro.accion) + "</span>"
                + '<span class="meta">' + escapar(registro.timestamp) + " · "
                + escapar(registro.usuario) + "</span>"
                + (registro.detalle
                  ? '<span class="detalle">' + escapar(registro.detalle) + "</span>" : "")
                + "</li>";
            });
            html += "</ul>";
          }
          cuerpo.innerHTML = html;
        })
        .catch(function () {
          cuerpo.innerHTML = '<p class="ayuda">No fue posible cargar el detalle del movimiento.</p>';
        });
    }
  }

  function escapar(texto) {
    var div = document.createElement("div");
    div.textContent = texto;
    return div.innerHTML;
  }

  /* ---------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    iniciarTema();
    iniciarNotificaciones();
    iniciarFormulario();
    iniciarFiltros();
    iniciarDetalle();
  });
})();
