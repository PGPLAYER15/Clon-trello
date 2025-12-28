import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

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
        const response = await api.post(`/boards/`, {
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