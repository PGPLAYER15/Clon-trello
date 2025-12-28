import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const api = axios.create({
    baseURL: API_BASE_URL
});

export const updateCardCheckStatus = async (board_id, columnaId, id, check) => {
    try {
        await api.put(`/boards/${board_id}/lists/${columnaId}/cards/${id}/`, {
            check: check
        });
    } catch (error) {
        console.error("Error al actualizar el estado de la tarjeta:", error);
        throw error;
    }
};  