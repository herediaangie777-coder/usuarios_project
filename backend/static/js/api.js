const API_BASE_URL = "/api/v1/";

const api = {
    async getPlataformas() {
        const response = await fetch(`${API_BASE_URL}plataformas/`, {
            credentials: "same-origin",
        });
        if (!response.ok) {
            throw new Error("PLATFORM_FETCH_FAILURE");
        }
        return response.json();
    },

    async getJuegos() {
        const response = await fetch(`${API_BASE_URL}juegos/`, {
            credentials: "same-origin",
        });
        if (!response.ok) {
            throw new Error("GAME_FETCH_FAILURE");
        }
        return response.json();
    },

    async getEquipos() {
        const response = await fetch(`${API_BASE_URL}equipos/`, {
            credentials: "same-origin",
        });
        if (!response.ok) {
            throw new Error("TEAM_FETCH_FAILURE");
        }
        return response.json();
    },
};
