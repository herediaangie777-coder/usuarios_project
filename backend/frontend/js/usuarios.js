function showMessage(targetId, message, type) {
  const target = document.getElementById(targetId);
  if (!target) return;
  target.className = `alert ${type}`;
  target.textContent = message;
  target.style.display = "block";
}

function getQueryId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

async function loadUsuariosList() {
  try {
    const result = await apiRequest("/usuarios/");
    const tbody = document.getElementById("usuarios-table-body");
    tbody.innerHTML = "";

    result.forEach((usuario) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${usuario.codigo}</td>
        <td>${usuario.nombre_completo}</td>
        <td>${usuario.numero_documento}</td>
        <td>${usuario.username}</td>
        <td>
          <a class="btn" href="usuarios_detalle.html?id=${usuario.id}">Detalle</a>
          <a class="btn secondary" href="usuarios_formulario.html?id=${usuario.id}">Editar</a>
        </td>
      `;
      tbody.appendChild(row);
    });
  } catch (err) {
    showMessage("lista-alert", err.message, "error");
  }
}

function buildPhoneRow(phone = {}) {
  const wrapper = document.createElement("div");
  wrapper.className = "card";
  wrapper.innerHTML = `
    <div class="form-grid">
      <div>
        <label>Numero</label>
        <input type="text" name="telefono_numero" value="${phone.numero || ""}" required />
      </div>
      <div>
        <label>Tipo</label>
        <select name="telefono_tipo" required>
          <option value="movil" ${phone.tipo === "movil" ? "selected" : ""}>Movil</option>
          <option value="fijo" ${phone.tipo === "fijo" ? "selected" : ""}>Fijo</option>
          <option value="trabajo" ${phone.tipo === "trabajo" ? "selected" : ""}>Trabajo</option>
        </select>
      </div>
      <div>
        <label>&nbsp;</label>
        <button type="button" class="btn secondary" data-remove>Quitar</button>
      </div>
    </div>
  `;

  const removeBtn = wrapper.querySelector("[data-remove]");
  removeBtn.addEventListener("click", () => wrapper.remove());
  return wrapper;
}

function collectPhones(container) {
  const phones = [];
  container.querySelectorAll(".card").forEach((card) => {
    const numero = card.querySelector("[name=telefono_numero]").value.trim();
    const tipo = card.querySelector("[name=telefono_tipo]").value;
    if (numero) {
      phones.push({ numero, tipo });
    }
  });
  return phones;
}

async function loadUsuarioForm() {
  const id = getQueryId();
  const form = document.getElementById("usuario-form");
  const phonesContainer = document.getElementById("phones-container");
  const addPhoneBtn = document.getElementById("add-phone");

  addPhoneBtn.addEventListener("click", () => {
    phonesContainer.appendChild(buildPhoneRow());
  });

  if (id) {
    try {
      const result = await apiRequest(`/usuarios/${id}/`);
      const usuario = result;
      form.tipo_documento.value = usuario.tipo_documento;
      form.numero_documento.value = usuario.numero_documento;
      form.nombre_completo.value = usuario.nombre_completo;
      form.edad.value = usuario.edad;
      form.sexo.value = usuario.sexo;
      form.direccion.value = usuario.direccion;
      form.username.value = usuario.username;
      document.getElementById("form-title").textContent = "Editar usuario";
      usuario.telefonos.forEach((tel) => {
        phonesContainer.appendChild(buildPhoneRow(tel));
      });
    } catch (err) {
      showMessage("form-alert", err.message, "error");
    }
  } else {
    phonesContainer.appendChild(buildPhoneRow());
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      tipo_documento: form.tipo_documento.value,
      numero_documento: form.numero_documento.value.trim(),
      nombre_completo: form.nombre_completo.value.trim(),
      edad: Number(form.edad.value),
      sexo: form.sexo.value,
      direccion: form.direccion.value.trim(),
      username: form.username.value.trim(),
      password: form.password.value,
    };

    const phones = collectPhones(phonesContainer);
    if (!id) {
      payload.telefonos = phones;
    }

    try {
      if (id) {
        await apiRequest(`/usuarios/${id}/`, { method: "PUT", body: payload });
        showMessage("form-alert", "Usuario actualizado", "success");
      } else {
        await apiRequest("/usuarios/", { method: "POST", body: payload });
        form.reset();
        phonesContainer.innerHTML = "";
        phonesContainer.appendChild(buildPhoneRow());
        showMessage("form-alert", "Usuario creado", "success");
      }
    } catch (err) {
      showMessage("form-alert", err.message, "error");
    }
  });
}

async function loadUsuarioDetalle() {
  const id = getQueryId();
  if (!id) return;

  try {
    const result = await apiRequest(`/usuarios/${id}/`);
    const usuario = result;
    document.getElementById("detalle-nombre").textContent = usuario.nombre_completo;
    document.getElementById("detalle-documento").textContent = usuario.numero_documento;
    document.getElementById("detalle-username").textContent = usuario.username;
    document.getElementById("detalle-direccion").textContent = usuario.direccion;

    const list = document.getElementById("telefonos-list");
    list.innerHTML = "";
    usuario.telefonos.forEach((tel) => {
      const item = document.createElement("div");
      item.className = "card";
      item.innerHTML = `
        <strong>${tel.numero}</strong> <span>(${tel.tipo})</span>
        <button class="btn secondary" data-delete="${tel.id}">Eliminar</button>
      `;
      list.appendChild(item);
    });

    list.querySelectorAll("[data-delete]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await deleteTelefono(btn.dataset.delete);
          loadUsuarioDetalle();
        } catch (err) {
          showMessage("detalle-alert", err.message, "error");
        }
      });
    });
  } catch (err) {
    showMessage("detalle-alert", err.message, "error");
  }
}

async function setupTelefonoForm() {
  const form = document.getElementById("telefono-form");
  if (!form) return;
  const usuarioId = getQueryId();
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      numero: form.numero.value.trim(),
      tipo: form.tipo.value,
    };
    try {
      await addTelefono(usuarioId, payload);
      form.reset();
      loadUsuarioDetalle();
    } catch (err) {
      showMessage("detalle-alert", err.message, "error");
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("usuarios-table-body")) {
    loadUsuariosList();
  }
  if (document.getElementById("usuario-form")) {
    loadUsuarioForm();
  }
  if (document.getElementById("usuario-detalle")) {
    loadUsuarioDetalle();
    setupTelefonoForm();
  }
});
