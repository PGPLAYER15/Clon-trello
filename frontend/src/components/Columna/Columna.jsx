import { useDroppable } from '@dnd-kit/core';
import { useState, useRef, useEffect } from 'react';
import Card from '../Card/Card';
import CrearIcon from "../../assets/CrearIcon.svg";
import styles from './TarjetaLista.module.css';

function Columna({ board_id, id, titulo, cards, onAddCard, onDeleteCard, onEditCard, onDeleteColumn, onEditColumn }) {

    const { setNodeRef } = useDroppable({ 
        id: id,
        data: {
            type: 'column',
            columnaId: id
        }
    });
    
    const [mostrarInput, setMostrarInput] = useState(false);
    const [tituloTarjeta, setTituloTarjeta] = useState("");
    
    const [isEditingTitle, setIsEditingTitle] = useState(false);
    const [editedTitle, setEditedTitle] = useState(titulo);
    const [showMenu, setShowMenu] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const titleInputRef = useRef(null);

    useEffect(() => {
        if (isEditingTitle && titleInputRef.current) {
            titleInputRef.current.focus();
            titleInputRef.current.select();
        }
    }, [isEditingTitle]);

    const handleGuardar = () => {
        if (tituloTarjeta.trim()) {
            onAddCard(id, tituloTarjeta); 
            setTituloTarjeta("");
            setMostrarInput(false);
        }
    };

    const handleTitleClick = () => {
        setIsEditingTitle(true);
        setEditedTitle(titulo);
    };

    const handleTitleSave = async () => {
        if (editedTitle.trim() && editedTitle !== titulo) {
            await onEditColumn(id, editedTitle);
        }
        setIsEditingTitle(false);
    };

    const handleTitleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleTitleSave();
        } else if (e.key === 'Escape') {
            setEditedTitle(titulo);
            setIsEditingTitle(false);
        }
    };

    const handleDeleteColumn = async () => {
        await onDeleteColumn(id);
        setShowDeleteConfirm(false);
        setShowMenu(false);
    };

    return (
        <div className={styles.ContenedorColumna} ref={setNodeRef}>
            <div className={styles.columnHeader}>
                {isEditingTitle ? (
                    <input
                        ref={titleInputRef}
                        type="text"
                        value={editedTitle}
                        onChange={(e) => setEditedTitle(e.target.value)}
                        onBlur={handleTitleSave}
                        onKeyDown={handleTitleKeyDown}
                        className={styles.titleInput}
                    />
                ) : (
                    <p className={styles.titulo} onClick={handleTitleClick}>{titulo}</p>
                )}
                
                <div className={styles.menuContainer}>
                    <button 
                        className={styles.menuBtn}
                        onClick={() => setShowMenu(!showMenu)}
                    >
                        ⋮
                    </button>
                    
                    {showMenu && (
                        <div className={styles.menuDropdown}>
                            <button onClick={handleTitleClick} className={styles.menuItem}>
                                Editar título
                            </button>
                            {!showDeleteConfirm ? (
                                <button 
                                    onClick={() => setShowDeleteConfirm(true)} 
                                    className={`${styles.menuItem} ${styles.menuItemDanger}`}
                                >
                                    Eliminar columna
                                </button>
                            ) : (
                                <div className={styles.deleteConfirmColumn}>
                                    <p>¿Eliminar columna y todas sus tarjetas?</p>
                                    <div className={styles.deleteConfirmBtns}>
                                        <button onClick={handleDeleteColumn} className={styles.confirmBtn}>
                                            Sí
                                        </button>
                                        <button onClick={() => setShowDeleteConfirm(false)} className={styles.cancelConfirmBtn}>
                                            No
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className={styles.cardsContainer}>
                {cards?.map((card) => (
                    <Card 
                        key={card.id} 
                        id={card.id} 
                        title={card.title}
                        description={card.description}
                        board_id={board_id} 
                        columnaId={id} 
                        check={card.check}
                        dueDate={card.due_date}
                        onDelete={onDeleteCard}
                        onEdit={onEditCard}
                    />
                ))}
            </div>

            {!mostrarInput ? (
                <button
                    onClick={() => setMostrarInput(true)}
                    className={styles.btn_crear_card}
                >
                    <img src={CrearIcon} alt="" />
                    Añade una tarjeta
                </button>
            ) : (
                <div className={styles.contenedor_input}>
                    <input
                        type="text"
                        placeholder="Título"
                        value={tituloTarjeta}
                        onChange={(e) => setTituloTarjeta(e.target.value)}
                        autoFocus
                    />
                    <div className={styles.contenedor_botones}>
                        <button onClick={handleGuardar} className={styles.btn_guardar_cancelar}>
                            Guardar
                        </button>
                        <button onClick={() => setMostrarInput(false)} className={styles.btn_guardar_cancelar}>
                            Cancelar
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Columna;