async function listTelefonos(usuarioId) {
  const result = await apiRequest(`/usuarios/${usuarioId}/telefonos/`);
  return result.data;
}

async function addTelefono(usuarioId, payload) {
  const result = await apiRequest(`/usuarios/${usuarioId}/telefonos/`, {
    method: "POST",
    body: payload,
  });
  return result.data;
}

async function deleteTelefono(telefonoId) {
  await apiRequest(`/telefonos/${telefonoId}/`, { method: "DELETE" });
}
