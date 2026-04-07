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
    throw new Error("Respuesta inválida del servidor");
  }

  if (!response.ok) {
    throw new Error(JSON.stringify(payload));
  }

  return payload; // 👈 ahora devuelve directo el JSON real
}
