
import { useState, useEffect, useCallback } from "react";
import { fetchTableros } from "../services/TableroService";

export const useTableros = () => {

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [tableros, setTableros] = useState([]);

    const fetchTableroData = useCallback(async () => {
        setLoading(true);
        try {
            const tablerosData = await fetchTableros();
            setTableros(tablerosData);
            console.log("Se cargaron los tableros");
        } catch (error) {
            setError("Error al cargar los tablero.");
            console.error(error);
        } finally {
            setLoading(false);
        }
    }, []);
        
    useEffect(() => {
        fetchTableroData();
    }, [fetchTableroData]);

    const addTablero = useCallback((nuevoTablero) => {
        setTableros(prev => [...prev, nuevoTablero]);
    }, []);
        
    return { tableros, loading, error, refetch: fetchTableroData, addTablero };
}