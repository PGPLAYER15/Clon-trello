import { useState } from "react";
import { useTablero } from "../../hooks/useTablero";
import Btn_crear from "../Btn_crear/Btn_crear";
import Columna from "../Columna/Columna";
import styles from "../Tablero/Tablero.module.css";
import { DndContext, DragOverlay, PointerSensor, useSensor, useSensors } from "@dnd-kit/core";
import { SortableContext, arrayMove, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { restrictToWindowEdges } from "@dnd-kit/modifiers";

const Tablero = ({ id }) => {
    const [activeCard, setActiveCard] = useState(null);

    const {
        tablero,
        columnas,
        loading,
        error,
        agregarColumna,
        agregarTarjeta,
        editarTarjeta,
        eliminarTarjeta,
        editarColumna,
        eliminarColumna,
        actualizarOrdenTarjetas,
        moverTarjeta,
    } = useTablero(id);

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        })
    );

    const handleDragStart = ({ active }) => {
        const cardData = active.data.current?.cardData;
        if (cardData) {
            setActiveCard(cardData);
        }
    };

    const handleDragEnd = async ({ active, over }) => {
        setActiveCard(null);
        
        if (!over) return;

        const activeCardData = active.data.current?.cardData;
        const overCard = over.data.current?.cardData;
        const sourceColumnId = activeCardData?.columnaId;
        const targetColumnId = over.data.current?.columnaId || overCard?.columnaId;

        if (!activeCardData || !sourceColumnId || !targetColumnId) return;

        try {
            if (sourceColumnId === targetColumnId) {
                const column = columnas.find((c) => c.id === sourceColumnId);
                if (column && column.cards) {
                    const oldIndex = column.cards.findIndex((c) => c?.id === activeCardData.id);
                    const newIndex = column.cards.findIndex((c) => c?.id === (overCard?.id || over.id));
                    
                    if (oldIndex !== -1 && newIndex !== -1 && oldIndex !== newIndex) {
                        const reorderedCards = arrayMove(column.cards, oldIndex, newIndex);
                        await actualizarOrdenTarjetas(sourceColumnId, reorderedCards);
                    }
                }
            } else {
                moverTarjeta(sourceColumnId, targetColumnId, activeCardData);
            }
        } catch (error) {
            console.error("Error al mover la tarjeta:", error);
        }
    };

    if (loading) return <div>Cargando columnas...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className={styles.tablero} style={{ backgroundColor: tablero?.color }}>
            <h1>{tablero?.title}</h1>
            <div className={styles.columnas}>
                <DndContext
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                    sensors={sensors}
                    modifiers={[restrictToWindowEdges]}
                >
                    {columnas.map((columna) => (
                        <SortableContext
                            key={columna.id}
                            items={(columna.cards || []).filter(c => c).map((card) => card.id)}
                            strategy={verticalListSortingStrategy}
                        >
                            <Columna
                                board_id={id}
                                key={columna.id}
                                id={columna.id}
                                titulo={columna.title}
                                cards={(columna.cards || []).filter(c => c)}
                                onAddCard={agregarTarjeta}
                                onDeleteCard={eliminarTarjeta}
                                onEditCard={editarTarjeta}
                                onDeleteColumn={eliminarColumna}
                                onEditColumn={editarColumna}
                            />
                        </SortableContext>
                    ))}
                    
                    <DragOverlay>
                        {activeCard ? (
                            <div className={styles.dragPreview}>
                                {activeCard.title}
                            </div>
                        ) : null}
                    </DragOverlay>
                </DndContext>
                <Btn_crear agregarColumna={agregarColumna} />
            </div>
        </div>
    );
};

export default Tablero;