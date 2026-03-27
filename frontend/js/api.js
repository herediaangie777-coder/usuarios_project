const API_BASE = "/api";

async function apiRequest(path, options = {}) {
  const config = {
    headers: { "Content-Type": "application/json" },
    ...options,
  };

  if (config.body && typeof config.body !== "string") {
    config.body = JSON.stringify(config.body);
  }

  const response = await fetch(`${API_BASE}${path}`, config);
  let payload = null;

  try {
    payload = await response.json();
  } catch (err) {
    payload = { status: "error", message: "Respuesta invalida del servidor" };
  }

  if (!response.ok || payload.status === "error") {
    const error = new Error(payload.message || "Error en la solicitud");
    error.data = payload.data || {};
    throw error;
  }

  return payload;
}
