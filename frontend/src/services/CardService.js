import axios from "axios";

export const updateCardCheckStatus = async (board_id, columnaId, id, check) => {
    try {
        await axios.put(`/api/boards/${board_id}/lists/${columnaId}/cards/${id}`, {
            check: check
        });
    } catch (error) {
        console.error("Error al actualizar el estado de la tarjeta:", error);
        throw error;
    }
};