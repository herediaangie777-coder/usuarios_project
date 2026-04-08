const API_BASE = "http://localhost:8000/api/v1";

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    let payload = null;
    try {
        payload = await response.json();
    } catch (error) {
        payload = null;
    }

    if (!response.ok) {
        const message = payload ? JSON.stringify(payload) : `HTTP ${response.status}`;
        throw new Error(message);
    }

    return payload;
}

function renderMessage(message, isError = false) {
    const node = document.getElementById("platform-message");
    node.textContent = message;
    node.style.color = isError ? "#ff9a8b" : "#9bc5d1";
}

function setPlatformForm(item = null) {
    document.getElementById("platform-id").value = item?.id || "";
    document.getElementById("platform-name").value = item?.nombre || "";
    document.getElementById("platform-brand").value = item?.marca || "";
}

async function loadPlataformas() {
    const items = await requestJson(`${API_BASE}/plataformas/`);
    const container = document.getElementById("platform-list");
    container.innerHTML = "";

    if (!items.length) {
        container.innerHTML = `<p class="message">No hay plataformas registradas.</p>`;
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "card";
        card.innerHTML = `
            <h3>${item.nombre}</h3>
            <p>Marca: ${item.marca}</p>
            <div class="card-actions">
                <button type="button" data-edit="${item.id}">Editar</button>
                <button type="button" class="danger" data-delete="${item.id}">Eliminar</button>
            </div>
        `;
        card.querySelector("[data-edit]").addEventListener("click", () => setPlatformForm(item));
        card.querySelector("[data-delete]").addEventListener("click", async () => {
            try {
                await requestJson(`${API_BASE}/plataformas/${item.id}/`, { method: "DELETE" });
                renderMessage("Plataforma eliminada.");
                await loadPlataformas();
            } catch (error) {
                renderMessage(`Error al eliminar: ${error.message}`, true);
            }
        });
        container.appendChild(card);
    });
}

async function loadJuegos() {
    const items = await requestJson(`${API_BASE}/juegos/`);
    const container = document.getElementById("game-list");
    container.innerHTML = "";

    if (!items.length) {
        container.innerHTML = `<p class="message">No hay juegos registrados.</p>`;
        return;
    }

    items.forEach((item) => {
        const plataformas = (item.plataformas || []).map((p) => p.nombre).join(", ") || "Sin plataformas";
        const card = document.createElement("article");
        card.className = "card";
        card.innerHTML = `
            <h3>${item.nombre}</h3>
            <p>ESRB: ${item.clasificacion_esrb}</p>
            <p>Desarrollador: ${item.desarrollador}</p>
            <p>Plataformas: ${plataformas}</p>
        `;
        container.appendChild(card);
    });
}

async function loadEquipos() {
    const items = await requestJson(`${API_BASE}/equipos/`);
    const container = document.getElementById("team-list");
    container.innerHTML = "";

    if (!items.length) {
        container.innerHTML = `<p class="message">No hay equipos registrados.</p>`;
        return;
    }

    items.forEach((item) => {
        const card = document.createElement("article");
        card.className = "card";
        card.innerHTML = `
            <h3>${item.nombre}</h3>
            <p>Juego: ${item.juego || "No asociado"}</p>
            <p>Nivel: ${item.nivel}</p>
            <p>Horas de juego: ${item.horas_juego || "0"}</p>
        `;
        container.appendChild(card);
    });
}

async function submitPlatform(event) {
    event.preventDefault();
    const id = document.getElementById("platform-id").value;
    const payload = {
        nombre: document.getElementById("platform-name").value.trim(),
        marca: document.getElementById("platform-brand").value.trim(),
    };

    try {
        await requestJson(
            id ? `${API_BASE}/plataformas/${id}/` : `${API_BASE}/plataformas/`,
            {
                method: id ? "PATCH" : "POST",
                body: JSON.stringify(payload),
            }
        );
        renderMessage(id ? "Plataforma actualizada." : "Plataforma creada.");
        setPlatformForm();
        await loadPlataformas();
    } catch (error) {
        renderMessage(`Error al guardar: ${error.message}`, true);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("platform-form").addEventListener("submit", submitPlatform);
    document.getElementById("platform-reset").addEventListener("click", () => setPlatformForm());

    try {
        await Promise.all([loadPlataformas(), loadJuegos(), loadEquipos()]);
        renderMessage("Datos cargados correctamente.");
    } catch (error) {
        renderMessage(`Error de red o servidor: ${error.message}`, true);
    }
});
