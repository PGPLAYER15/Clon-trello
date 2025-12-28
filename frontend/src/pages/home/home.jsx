import { useNavigate } from "react-router-dom";
import { useTableros } from "../../hooks/useTableros.js";
import Cabecera from "../../components/Cabecera/Cabecera.jsx";
import Fondo from "../../components/Fondo/Fondo.jsx";
import Menu from "../../components/Menu/Menu.jsx";
import styles from "./home.module.css";

function Home() {
    const navigate = useNavigate();
    const { tableros, loading, error } = useTableros();

    if (loading) return <div>Cargando tableros...</div>;
    if (error) return <div>Error al cargar los tableros</div>;

    return (
        <Fondo>
            <Cabecera />
            <div className={styles.container}>
                <Menu />
                <div className={styles.boardSection}>
                    <h1>Mis Tableros</h1>
                    {tableros.length > 0 ? (
                        <div className={styles.seccionTableros}>
                            {tableros.map(tablero => (
                                <div style={{ background: tablero.color || "#ffffff" }} key={tablero.id} className={styles.boardGrid}>
                                    <div
                                        className={styles.boardCard}
                                        onClick={() => navigate(`/tablero/${tablero.id}`)}
                                    >
                                        <h3>{tablero.title}</h3>
                                        <div className={styles.tableroPreview}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className={styles.container_noneboard}>
                            <p>No tienes tableros creados</p>
                            <img className={styles.noneboard} src="../src/assets/None_boards.png" alt="Sin boards"/>
                        </div>
                    )}
                </div>
            </div>
        </Fondo>
    );
}

export default Home;