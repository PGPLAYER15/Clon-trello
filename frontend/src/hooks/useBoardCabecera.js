import { useState } from "react";
import { crearTablero } from "../services/BoardService";

export const useBoardCabecera = (onSuccess) => {
    const [nombre, setNombre] = useState("");
    const [descripcion, setDescripcion] = useState("");
    const [color, setColor] = useState("#ffffff");
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleCrearTablero = async () => {
        if (!nombre.trim()) {
            setError("El nombre del tablero es obligatorio.");
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const nuevoTablero = await crearTablero(nombre, descripcion, color);
            console.log("Tablero creado:", nuevoTablero);
            if (onSuccess) {
                onSuccess(nuevoTablero);
            }
        } catch (error) {
            setError("Error al crear el tablero. Por favor, inténtalo de nuevo.");
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    return {
        nombre,
        setNombre,
        descripcion,
        setDescripcion,
        color,
        setColor,
        error,
        isLoading,
        handleCrearTablero,
    };
};