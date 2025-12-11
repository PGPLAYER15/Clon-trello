// hooks/useTablero.js
import { useState, useEffect } from "react";
import {
    fetchTablerobyID,
    fetchColumnas,
    crearColumna,
    crearTarjeta,
    actualizarColumna,
    editarTarjeta,
    eliminarTarjeta,
    editarColumna,
    eliminarColumna,
} from "../services/TableroService";

export const useTablero = (boardId) => {
    const [tablero, setTablero] = useState(null);
    const [columnas, setColumnas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    

    useEffect(() => {
        const fetchData = async () => {
            try {
                const tableroData = await fetchTablerobyID(boardId);
                const columnasData = await fetchColumnas(boardId);
                setTablero(tableroData);
                setColumnas(columnasData);
            } catch (error) {
                setError("Error al cargar los datos del tablero.");
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [boardId]);
        
    const agregarColumna = async (titulo) => {
        try {
            const nuevaColumna = await crearColumna(boardId, titulo);
            setColumnas((prev) => [...prev, nuevaColumna]);
        } catch (error) {
            setError("Error al crear la columna.");
            console.error(error);
        }
    };

    const agregarTarjeta = async (columnaId, tituloTarjeta) => {
        try {
            const nuevaTarjeta = await crearTarjeta(boardId, columnaId, tituloTarjeta);
            setColumnas((prev) =>
                prev.map((columna) =>
                    columna.id === columnaId
                        ? { ...columna, cards: [...(columna.cards || []), nuevaTarjeta] }
                        : columna
                )
            );
        } catch (error) {
            setError("Error al crear la tarjeta.");
            console.error(error);
        }
    };

    const editarTarjetaHandler = async (columnaId, cardId, nuevoTitulo, nuevaDescripcion) => {
        try {
            await editarTarjeta(boardId, columnaId, cardId, nuevoTitulo, nuevaDescripcion);
            setColumnas((prev) =>
                prev.map((columna) =>
                    columna.id === columnaId
                        ? {
                            ...columna,
                            cards: columna.cards.map((card) =>
                                card.id === cardId 
                                    ? { ...card, title: nuevoTitulo, description: nuevaDescripcion } 
                                    : card
                            ),
                        }
                        : columna
                )
            );
        } catch (error) {
            setError("Error al editar la tarjeta.");
            console.error(error);
            throw error;
        }
    };

    const eliminarTarjetaHandler = async (columnaId, cardId) => {
        try {
            await eliminarTarjeta(boardId, columnaId, cardId);
            setColumnas((prev) =>
                prev.map((columna) =>
                    columna.id === columnaId
                        ? {
                            ...columna,
                            cards: columna.cards.filter((card) => card.id !== cardId),
                        }
                        : columna
                )
            );
        } catch (error) {
            setError("Error al eliminar la tarjeta.");
            console.error(error);
            throw error;
        }
    };

    const editarColumnaHandler = async (columnaId, nuevoTitulo) => {
        try {
            await editarColumna(boardId, columnaId, nuevoTitulo);
            setColumnas((prev) =>
                prev.map((columna) =>
                    columna.id === columnaId ? { ...columna, title: nuevoTitulo } : columna
                )
            );
        } catch (error) {
            setError("Error al editar la columna.");
            console.error(error);
            throw error;
        }
    };

    const eliminarColumnaHandler = async (columnaId) => {
        try {
            await eliminarColumna(boardId, columnaId);
            setColumnas((prev) => prev.filter((columna) => columna.id !== columnaId));
        } catch (error) {
            setError("Error al eliminar la columna.");
            console.error(error);
            throw error;
        }
    };

    const actualizarOrdenTarjetas = async (columnaId, tarjetas) => {
        try {
            await actualizarColumna(boardId, columnaId, tarjetas);
        } catch (error) {
            setError("Error al actualizar el orden de las tarjetas.");
            console.error(error);
        }
    };

    const moverTarjeta = (sourceColumnId, targetColumnId, activeCard) => {
        setColumnas((prev) => {
            const sourceColumn = prev.find((c) => c.id === sourceColumnId);
            const targetColumn = prev.find((c) => c.id === targetColumnId);

            if (!sourceColumn || !targetColumn || !activeCard) return prev;

            const cardToMove = sourceColumn.cards.find((c) => c?.id === activeCard.id);
            if (!cardToMove) return prev;

            return prev.map((col) => {
                if (col.id === sourceColumnId) {
                    return {
                        ...col,
                        cards: col.cards.filter((c) => c?.id !== activeCard.id)
                    };
                }
                if (col.id === targetColumnId) {
                    return {
                        ...col,
                        cards: [...col.cards, cardToMove]
                    };
                }
                return col;
            });
        });
    };


    return {
        tablero,
        columnas,
        loading,
        error,
        agregarColumna,
        agregarTarjeta,
        editarTarjeta: editarTarjetaHandler,
        eliminarTarjeta: eliminarTarjetaHandler,
        editarColumna: editarColumnaHandler,
        eliminarColumna: eliminarColumnaHandler,
        actualizarOrdenTarjetas,
        moverTarjeta,
    };
};