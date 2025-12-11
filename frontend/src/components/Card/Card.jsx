import { useDraggable } from '@dnd-kit/core';
import { useState } from "react";
import { useCard } from "../../hooks/useCard";
import Modal from "../modal/Modal"
import { CSS } from '@dnd-kit/utilities';
import styles from "../Card/Card.module.css";

function Card({ board_id, id, title, description, columnaId, check, onDelete, onEdit }) {

    const { isChecked, toggleCheck, isLoading, error } = useCard(check);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editedTitle, setEditedTitle] = useState(title);
    const [editedDescription, setEditedDescription] = useState(description || '');
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    
    const openModal = (e) => {
        e.stopPropagation();
        setIsModalOpen(true);
        setEditedTitle(title);
        setEditedDescription(description || '');
        setShowDeleteConfirm(false);
    };
    
    const closeModal = () => {
        setIsModalOpen(false);
        setShowDeleteConfirm(false);
    };

    const handleCheckboxChange = async (e) => {
        e.stopPropagation();
        try {
            await toggleCheck(board_id, columnaId, id);
        } catch (error) {
            alert("Hubo un error al actualizar la tarjeta. Por favor, inténtalo de nuevo.");
        }
    };

    const handleSaveEdit = async () => {
        if (!editedTitle.trim()) {
            closeModal();
            return;
        }
        setIsEditing(true);
        try {
            await onEdit(columnaId, id, editedTitle, editedDescription);
            closeModal();
        } catch (error) {
            alert("Error al guardar cambios");
        } finally {
            setIsEditing(false);
        }
    };

    const handleDelete = async () => {
        setIsDeleting(true);
        try {
            await onDelete(columnaId, id);
            closeModal();
        } catch (error) {
            alert("Error al eliminar la tarjeta");
        } finally {
            setIsDeleting(false);
        }
    };

    const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({
        id: id,
        data: {
            type: 'card',
            cardData: { id, title, columnaId }
        },
        disabled: isModalOpen 
    });

    const style = {
        transform: CSS.Translate.toString(transform),
        position: 'relative',
        zIndex: isDragging ? 999 : 'auto',
        opacity: isDragging ? 0.5 : 1
    };

    return (
        <div 
            ref={setNodeRef} 
            style={style} 
            className={styles.contenedor}
        >
            <div 
                className={styles.dragHandle}
                {...listeners} 
                {...attributes}
            >
                ⋮⋮
            </div>

            <input 
                type="checkbox"
                className={styles.checkbox}     
                checked={isChecked}
                onChange={handleCheckboxChange}
                disabled={isLoading}
            />
            
            <p 
                onClick={openModal}
                className={styles.titulo}
            >
                {title}
            </p>

            <Modal isOpen={isModalOpen} onClose={closeModal}>
                <h2>Editar Tarjeta</h2>
                
                <div className={styles.modalContent}>
                    <label>Título:</label>
                    <input
                        type="text"
                        value={editedTitle}
                        onChange={(e) => setEditedTitle(e.target.value)}
                        className={styles.editInput}
                        placeholder="Título de la tarjeta"
                    />
                    
                    <label>Descripción:</label>
                    <textarea
                        value={editedDescription}
                        onChange={(e) => setEditedDescription(e.target.value)}
                        className={styles.descriptionInput}
                        placeholder="Agrega una descripción más detallada...&#10;&#10;Puedes usar formato:&#10;- Listas con guiones&#10;- **Negrita** con asteriscos&#10;- `código` con backticks"
                        rows={6}
                    />
                    
                    <div className={styles.modalActions}>
                        <button 
                            onClick={handleSaveEdit}
                            disabled={isEditing}
                            className={styles.saveBtn}
                        >
                            {isEditing ? "Guardando..." : "Guardar"}
                        </button>
                        
                        {!showDeleteConfirm ? (
                            <button 
                                onClick={() => setShowDeleteConfirm(true)}
                                className={styles.deleteBtn}
                            >
                                Eliminar
                            </button>
                        ) : (
                            <div className={styles.deleteConfirm}>
                                <span>¿Estás seguro?</span>
                                <button 
                                    onClick={handleDelete}
                                    disabled={isDeleting}
                                    className={styles.confirmDeleteBtn}
                                >
                                    {isDeleting ? "Eliminando..." : "Sí, eliminar"}
                                </button>
                                <button 
                                    onClick={() => setShowDeleteConfirm(false)}
                                    className={styles.cancelBtn}
                                >
                                    Cancelar
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            </Modal>
        </div>
    );
}

export default Card;