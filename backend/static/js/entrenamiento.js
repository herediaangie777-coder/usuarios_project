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

async function csrfFetch(url, options = {}) {
    const headers = {
        ...(options.headers || {}),
        "X-CSRFToken": getCookie("csrftoken"),
    };

    return fetch(url, {
        credentials: "same-origin",
        ...options,
        headers,
    });
}

function syncArbitroSelection() {
    const input = document.getElementById("arbitro-nombre-input");
    const hiddenId = document.getElementById("arbitro-id");
    const datalist = document.getElementById("arbitros-lista");

    if (!input || !hiddenId || !datalist) {
        return;
    }

    const normalizedValue = input.value.trim().toLowerCase();
    const matchedOption = Array.from(datalist.options).find(
        (option) => option.value.trim().toLowerCase() === normalizedValue
    );

    hiddenId.value = matchedOption ? matchedOption.dataset.id : "";
}

async function submitSesionForm(event) {
    event.preventDefault();

    const form = event.currentTarget;
    syncArbitroSelection();
    const formData = new FormData(form);
    const tipoTarget = formData.get("tipo_target");
    const payload = {
        juego: formData.get("juego"),
        fecha: formData.get("fecha"),
        hora_inicio: formData.get("hora_inicio"),
        hora_fin: formData.get("hora_fin"),
        arbitro: formData.get("arbitro") || null,
        arbitro_nombre_input: (formData.get("arbitro_nombre_input") || "").trim(),
        atleta: tipoTarget === "atleta" ? formData.get("atleta") || null : null,
        equipo: tipoTarget === "equipo" ? formData.get("equipo") || null : null,
    };

    const response = await csrfFetch("/sesiones/crear/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const error = await response.json();
        alert(`No fue posible guardar la sesion: ${JSON.stringify(error)}`);
        return;
    }

    window.location.href = "/sesiones/";
}

async function iniciarSesion(id) {
    const response = await csrfFetch(`/sesiones/${id}/iniciar/`, {
        method: "POST",
    });
    if (response.ok) {
        window.location.reload();
    }
}

async function cerrarSesion(id) {
    const response = await csrfFetch(`/sesiones/${id}/cerrar/`, {
        method: "POST",
    });
    if (response.ok) {
        const data = await response.json();
        alert(`Sesion cerrada. XP: ${data.recompensa.puntos_experiencia}. Trofeo: ${data.recompensa.trofeo}`);
        window.location.reload();
    }
}

async function recalcularNivel(equipoId) {
    const response = await csrfFetch(`/api/v1/equipos/${equipoId}/recalcular/`, {
        method: "POST",
    });

    if (response.ok) {
        const data = await response.json();
        alert(`Nivel actualizado: ${data.nivel}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const sesionForm = document.getElementById("sesion-form");
    if (sesionForm) {
        sesionForm.addEventListener("submit", submitSesionForm);
    }
    const arbitroInput = document.getElementById("arbitro-nombre-input");
    if (arbitroInput) {
        arbitroInput.addEventListener("input", syncArbitroSelection);
        arbitroInput.addEventListener("change", syncArbitroSelection);
    }
});

window.iniciarSesion = iniciarSesion;
window.cerrarSesion = cerrarSesion;
window.recalcularNivel = recalcularNivel;
window.iniciar = iniciarSesion;
window.cerrar = cerrarSesion;
