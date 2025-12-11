import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Cabecera.module.css';
import Temporizador from '../Temporizador/Temporizador';
import TemporizadorBotones from '../TemporizadorBotones/TemporizadorBotones';
import Modal from '../modal/Modal';
import useTimer from '../../hooks/useTimer';
import { useBoardCabecera } from '../../hooks/useBoardCabecera';
import { useAuth } from '../../context/AuthContext';

// Trello-style color palette
const colorPalette = [
    { name: 'Azul', value: '#0079bf' },
    { name: 'Naranja', value: '#d29034' },
    { name: 'Verde', value: '#519839' },
    { name: 'Rojo', value: '#b04632' },
    { name: 'Morado', value: '#89609e' },
    { name: 'Rosa', value: '#cd5a91' },
    { name: 'Verde Lima', value: '#4bbf6b' },
    { name: 'Celeste', value: '#00aecc' },
    { name: 'Gris', value: '#838c91' },
];

function Cabecera() {
    const navigate = useNavigate();
    const { minutes, seconds, isWorking, isActive, iniciar, pausar, reiniciar } = useTimer();
    const [isModalOpen, setIsModalOpen] = useState(false);
    const { user, logout } = useAuth();

    const handleBoardCreated = (nuevoTablero) => {
        setIsModalOpen(false);
        navigate(`/tablero/${nuevoTablero.id}`);
    };

    const {
        nombre,
        setNombre,
        descripcion,
        setDescripcion,
        color,
        setColor,
        error,
        isLoading,
        handleCrearTablero,
    } = useBoardCabecera(handleBoardCreated);

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => {
        setIsModalOpen(false);
        setNombre("");
        setDescripcion("");
        setColor("#ffffff");
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        handleCrearTablero();
    };

    return (
        <div className={styles.cabecera}>

            <div className={styles.contenedor}>
                <div className={styles.contenedor_botones}>
                    <button
                        onClick={openModal} 
                        className={styles.btn_menu_arriba}
                        >
                            Crear
                    </button>

                    <TemporizadorBotones
                        iniciar={iniciar}
                        pausar={pausar}
                        reiniciar={reiniciar}
                        isActive={isActive}
                    />
                </div>
                
                <Temporizador
                    minutes={minutes}
                    seconds={seconds}
                    isWorking={isWorking}
                />
                
                <button 
                    onClick={logout}
                    className={styles.btn_espacio}
                    title={user?.username || 'Salir'}
                >
                    Salir
                </button>
            </div>

            <Modal isOpen={isModalOpen} onClose={closeModal}>
                <h2>Crear Tablero</h2>
                <form onSubmit={handleSubmit} className={styles.form_group}>
                    <label>Nombre del Tablero:</label>
                    <input
                        type="text"
                        value={nombre}
                        onChange={(e) => setNombre(e.target.value)}
                        required
                    />
                    <label>Descripción:</label>
                    <input
                        type="text"
                        value={descripcion}
                        onChange={(e) => setDescripcion(e.target.value)}
                    />
                    <label>Color:</label>
                    <div className={styles.colorPalette}>
                        {colorPalette.map((c) => (
                            <button
                                key={c.value}
                                type="button"
                                className={`${styles.colorBtn} ${color === c.value ? styles.colorBtnSelected : ''}`}
                                style={{ backgroundColor: c.value }}
                                onClick={() => setColor(c.value)}
                                title={c.name}
                                aria-label={c.name}
                            />
                        ))}
                    </div>
                    {error && <p style={{ color: "red" }}>{error}</p>}
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? "Creando..." : "Crear Tablero"}
                    </button>
                </form>
            </Modal>
        </div>
    );
}

export default Cabecera;