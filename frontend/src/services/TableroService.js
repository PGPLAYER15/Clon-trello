// services/tableroService.js
import axios from "axios";

const API_BASE_URL = "/api";

const api = axios.create({
    baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const crearTablero = async (nombre, descripcion, color) => {
    try {
        const response = await api.post(`/boards`, {
            title: nombre,
            description: descripcion,
            color: color,
        });
        return response.data;
    } catch (error) {
        console.error("Error al crear el tablero:", error);
        throw error;
    }
};

export const fetchTableros = async () => {
    try {
        const response = await api.get(`/boards/`);
        return response.data;
    } catch (error) {
        console.error("Error al obtener los tableros:", error);
        throw error;
    }
}

export const fetchTablerobyID = async (id) => {
    try {
        const response = await api.get(`/boards/${id}`);
        return response.data;
    } catch (error) {
        console.error("Error al obtener el tablero:", error);
        throw error;
    }
};

export const fetchColumnas = async (boardId) => {
    try {
        const response = await api.get(`/boards/${boardId}/lists`);
        return response.data;
    } catch (error) {
        console.error("Error al obtener las columnas:", error);
        throw error;
    }
};

export const crearColumna = async (boardId, titulo) => {
    try {
        const response = await api.post(`/boards/${boardId}/lists`, {
            title: titulo,
            board_id: boardId,
        });
        return response.data;
    } catch (error) {
        console.error("Error al crear la columna:", error);
        throw error;
    }
};

export const crearTarjeta = async (boardId, columnaId, tituloTarjeta) => {
    try {
        const response = await api.post(
            `/boards/${boardId}/lists/${columnaId}/cards/create`,
            {
                title: tituloTarjeta,
                description: null,
                list_id: columnaId,
                check: false,
            }
        );
        return response.data;
    } catch (error) {
        console.error("Error al crear la tarjeta:", error);
        throw error;
    }
};

export const actualizarColumna = async (boardId, columnaId, tarjetas) => {
    try {
        await api.put(`/boards/${boardId}/lists/${columnaId}/cards`, {
            cards: tarjetas.map((tarjeta) => tarjeta.id),
        });
    } catch (error) {
        console.error("Error al actualizar la columna:", error);
        throw error;
    }
};

export const editarTarjeta = async (boardId, columnaId, cardId, nuevoTitulo, nuevaDescripcion) => {
    try {
        const response = await api.put(
            `/boards/${boardId}/lists/${columnaId}/cards/${cardId}`,
            { title: nuevoTitulo, description: nuevaDescripcion }
        );
        return response.data;
    } catch (error) {
        console.error("Error al editar la tarjeta:", error);
        throw error;
    }
};

export const eliminarTarjeta = async (boardId, columnaId, cardId) => {
    try {
        await api.delete(`/boards/${boardId}/lists/${columnaId}/cards/${cardId}`);
    } catch (error) {
        console.error("Error al eliminar la tarjeta:", error);
        throw error;
    }
};

export const editarColumna = async (boardId, columnaId, nuevoTitulo) => {
    try {
        const response = await api.put(
            `/boards/${boardId}/lists/${columnaId}`,
            { title: nuevoTitulo, board_id: boardId }
        );
        return response.data;
    } catch (error) {
        console.error("Error al editar la columna:", error);
        throw error;
    }
};

export const eliminarColumna = async (boardId, columnaId) => {
    try {
        await api.delete(`/boards/${boardId}/lists/${columnaId}`);
    } catch (error) {
        console.error("Error al eliminar la columna:", error);
        throw error;
    }
};