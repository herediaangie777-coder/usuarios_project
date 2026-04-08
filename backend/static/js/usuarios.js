function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (const rawCookie of cookies) {
            const cookie = rawCookie.trim();
            if (cookie.startsWith(`${name}=`)) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function parseTelefonos() {
    return Array.from(document.querySelectorAll('input[name="telefonos[]"]')).map((input) => {
        const [tipo, numero] = input.value.split(":");
        return { tipo, numero };
    });
}

function buildAcudientePayload(formData) {
    const tipoUsuario = formData.get("tipo_usuario");
    const edad = Number(formData.get("edad"));
    if (tipoUsuario !== "atleta" || edad >= 18) {
        return null;
    }

    return {
        nombre_completo: formData.get("acudiente_nombre_completo"),
        tipo_documento: formData.get("acudiente_tipo_documento"),
        numero_documento: formData.get("acudiente_numero_documento"),
        telefono: formData.get("acudiente_telefono"),
        parentesco: formData.get("acudiente_parentesco"),
        direccion: formData.get("acudiente_direccion"),
    };
}

function syncEquipoSelection() {
    const input = document.getElementById("equipo-nombre-input");
    const hiddenId = document.getElementById("equipo-id");
    const datalist = document.getElementById("equipos-lista");

    if (!input || !hiddenId || !datalist) {
        return;
    }

    const normalizedValue = input.value.trim().toLowerCase();
    const matchedOption = Array.from(datalist.options).find(
        (option) => option.value.trim().toLowerCase() === normalizedValue
    );

    hiddenId.value = matchedOption ? matchedOption.dataset.id : "";
}

function toggleAcudienteSection() {
    const tipoUsuarioInput = document.getElementById("tipo-usuario");
    const edadInput = document.getElementById("edad");
    const acudienteSection = document.getElementById("acudiente-section");
    const equipoSection = document.getElementById("equipo-section");
    if (!edadInput || !acudienteSection || !tipoUsuarioInput || !equipoSection) {
        return;
    }

    const isAtleta = tipoUsuarioInput.value === "atleta";
    const isMinor = isAtleta && Number(edadInput.value || 0) < 18;
    equipoSection.style.display = isAtleta ? "block" : "none";
    acudienteSection.style.display = isMinor ? "block" : "none";

    acudienteSection.querySelectorAll("input, select").forEach((field) => {
        field.required = isMinor;
    });

    const equipoInput = document.getElementById("equipo-nombre-input");
    const equipoId = document.getElementById("equipo-id");
    if (!isAtleta && equipoInput && equipoId) {
        equipoInput.value = "";
        equipoId.value = "";
    }
}

async function submitUsuarioForm(event) {
    event.preventDefault();

    const form = event.currentTarget;
    const formData = new FormData(form);
    syncEquipoSelection();
    const payload = {
        tipo_documento: formData.get("tipo_documento"),
        numero_documento: formData.get("numero_documento"),
        nombre_completo: formData.get("nombre_completo"),
        tipo_usuario: formData.get("tipo_usuario"),
        edad: Number(formData.get("edad")),
        sexo: formData.get("sexo"),
        direccion: formData.get("direccion"),
        username: formData.get("username"),
        password: formData.get("password"),
        equipo_id: formData.get("equipo_id") || null,
        equipo_nombre_input: (formData.get("equipo_nombre_input") || "").trim(),
        telefonos: parseTelefonos(),
        acudiente: buildAcudientePayload(formData),
    };

    const response = await fetch("/usuarios/crear/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const error = await response.json();
        const alertBox = document.getElementById("form-alert");
        if (alertBox) {
            alertBox.style.display = "block";
            alertBox.textContent = JSON.stringify(error);
        }
        return;
    }

    window.location.href = "/usuarios/";
}

async function loadUsuariosList() {
    const tbody = document.getElementById("usuarios-table-body");
    if (!tbody) {
        return;
    }

    const response = await fetch("/usuarios/data/", {
        credentials: "same-origin",
    });
    if (!response.ok) {
        throw new Error("USER_FETCH_FAILURE");
    }
    const result = await response.json();
    tbody.innerHTML = "";

    if (!result.length) {
        tbody.innerHTML =
            '<tr><td colspan="10" class="text-center text-warning">NO_HAY_USUARIOS_REGISTRADOS</td></tr>';
        return;
    }

    result.forEach((usuario) => {
        const telefonos = (usuario.telefonos || [])
            .map((telefono) => `${telefono.tipo}: ${telefono.numero}`)
            .join("<br>");

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${usuario.codigo || "N/A"}</td>
            <td>${usuario.nombre_completo}</td>
            <td>${usuario.tipo_usuario || "-"}</td>
            <td>${usuario.numero_documento}</td>
            <td>${usuario.username}</td>
            <td>${usuario.equipo_nombre || "-"}</td>
            <td>${usuario.nivel}</td>
            <td>${usuario.puntos_experiencia}</td>
            <td>${telefonos || "-"}</td>
            <td>${usuario.acudiente_detalle ? `${usuario.acudiente_detalle.nombre_completo}<br><span class="text-secondary">${usuario.acudiente_detalle.parentesco} | ${usuario.acudiente_detalle.telefono}</span>` : "-"}</td>
        `;
        tbody.appendChild(row);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("usuario-form");
    if (form) {
        form.addEventListener("submit", submitUsuarioForm);
        toggleAcudienteSection();
        const edadInput = document.getElementById("edad");
        if (edadInput) {
            edadInput.addEventListener("input", toggleAcudienteSection);
        }
        const tipoUsuarioInput = document.getElementById("tipo-usuario");
        if (tipoUsuarioInput) {
            tipoUsuarioInput.addEventListener("change", toggleAcudienteSection);
        }
        const equipoInput = document.getElementById("equipo-nombre-input");
        if (equipoInput) {
            equipoInput.addEventListener("input", syncEquipoSelection);
            equipoInput.addEventListener("change", syncEquipoSelection);
        }
    }

    loadUsuariosList().catch((error) => {
        const tbody = document.getElementById("usuarios-table-body");
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="10" class="text-danger text-center">${error.message}</td></tr>`;
        }
    });
});
