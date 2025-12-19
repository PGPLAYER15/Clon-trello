import { useDraggable } from '@dnd-kit/core';
import { useState, useMemo } from "react";
import { useCard } from "../../hooks/useCard";
import Modal from "../modal/Modal"
import { CSS } from '@dnd-kit/utilities';
import styles from "../Card/Card.module.css";

const getUrgencyClass = (dueDate, isCompleted) => {
    if (!dueDate) return null;
    if (isCompleted) return styles.dueGray;
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);
    
    const diffTime = due - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return styles.dueRed;      
    if (diffDays <= 1) return styles.dueRed;    
    if (diffDays <= 3) return styles.dueYellow;  
    return styles.dueGreen;                      
};

const formatDueDate = (dueDate) => {
    if (!dueDate) return null;
    const date = new Date(dueDate);
    return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
};

function Card({ board_id, id, title, description, columnaId, check, onDelete, onEdit,dueDate }) {

    const { isChecked, toggleCheck, isLoading, error } = useCard(check);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [editedTitle, setEditedTitle] = useState(title);
    const [editedDescription, setEditedDescription] = useState(description || '');
    const [editedDueDate, setEditedDueDate] = useState('');
    const [isEditing, setIsEditing] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    
    const openModal = (e) => {
        e.stopPropagation();
        setIsModalOpen(true);
        setEditedTitle(title);
        setEditedDescription(description || '');
        setEditedDueDate(dueDate ? dueDate.split('T')[0] : '');
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
            await onEdit(columnaId, id, editedTitle, editedDescription, editedDueDate || null);
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
            
            <div className={styles.cardContent} onClick={openModal}>
                <p className={styles.titulo}>
                    {title}
                </p>
                {dueDate && (
                    <span className={`${styles.dueDateBadge} ${getUrgencyClass(dueDate, isChecked)}`}>
                        {formatDueDate(dueDate)}
                    </span>
                )}
            </div>

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
                    
                    <div className={styles.datePickerContainer}>
                        <label className={styles.datePickerLabel}>Fecha de vencimiento</label>
                        <input
                            type="date"
                            value={editedDueDate}
                            onChange={(e) => setEditedDueDate(e.target.value)}
                            className={styles.dateInput}
                        />
                    </div>  
                    
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