# 📝 Clon de Trello

**Clon Trello** es una aplicación tipo *To-Do* que permite a los usuarios enlistar, organizar y mover tareas entre diferentes columnas, al estilo del conocido gestor Trello.

## 🚀 Funcionalidades principales

### ✨ Gestión de Tableros
- Crear, editar y eliminar tableros personalizados
- Cada usuario solo ve sus propios tableros (autenticación)
- Personalizar tableros con colores

### 📋 Gestión de Columnas
- Crear columnas para organizar tareas
- Edición de título inline (clic para editar)
- Menú de opciones con eliminación y confirmación

### 🎴 Gestión de Tarjetas
- Crear tarjetas con título y descripción
- Editar tarjetas a través de un modal interactivo
- Eliminar tarjetas con confirmación
- Soporte para descripciones con Markdown

### 🖱️ Drag and Drop Avanzado
- Arrastrar y soltar tarjetas entre columnas con **dnd-kit**
- Preview visual mejorada al arrastrar (rotación y sombra)
- Drag handle dedicado para evitar conflictos con clics

### 🔐 Sistema de Autenticación
- Registro de usuarios con email y contraseña
- Login con JWT (JSON Web Tokens)
- Rutas protegidas para usuarios autenticados
- Sesiones persistentes con tokens

## 🛠️ Tecnologías utilizadas

### Backend
- 🐍 **Python 3.9+**
- ⚡ **FastAPI** - Framework web moderno
- 🔒 **JWT** - Autenticación con tokens
- 🗄️ **SQLAlchemy** - ORM para base de datos
- 📦 **Pydantic** - Validación de datos
- 🔑 **bcrypt** - Hashing de contraseñas

### Frontend
- ⚛️ **React 18** - UI interactiva
- 📦 **dnd-kit** - Drag and drop
- 🎨 **CSS Modules** - Estilos aislados
- 🔄 **Axios** - Cliente HTTP
- �️ **React Router** - Navegación SPA

## 🔧 Instalación y ejecución

### Requisitos

- Node.js 18+
- Python 3.9+
- pip

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8002
- **Documentación API:** http://localhost:8002/docs

## 🖼️ Demo

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1Xeq2xOE_q1JpyrJyo1G_KH8hTV0eWKLV" alt="Vista de tableros" width="600"/>
</div>
<br/>
<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1QEomySE5Ggf36SoSY030lAGyzBKzLqFY" alt="Tablero con columnas" width="600"/>
</div>
<br/>
<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1f-vm0omBTYjV4bD4INdzks_DG1ax84os" alt="Drag and drop" width="600"/>
</div>

## 📂 Estructura del proyecto

```
├── backend/
│   ├── app/
│   │   ├── core/         # Configuración y seguridad
│   │   │   ├── config.py # Variables de entorno
│   │   │   └── security.py # JWT y autenticación
│   │   ├── models/       # Modelos SQLAlchemy
│   │   │   ├── board.py
│   │   │   ├── card.py
│   │   │   ├── list.py
│   │   │   └── user.py
│   │   ├── routes/       # Rutas de la API
│   │   │   ├── auth.py   # Login y registro
│   │   │   ├── boards.py
│   │   │   ├── cards.py
│   │   │   └── lists.py
│   │   ├── schemas/      # Esquemas Pydantic
│   │   └── main.py       # Punto de entrada
│   ├── .env              # Variables de entorno
│   └── trello.db         # Base de datos SQLite
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   │   ├── Card/
│   │   │   ├── Columna/
│   │   │   ├── Tablero/
│   │   │   └── modal/
│   │   ├── context/      # AuthContext (estado global)
│   │   ├── hooks/        # Custom hooks
│   │   ├── pages/        # Páginas (home, login, register)
│   │   ├── services/     # Conexiones con la API
│   │   └── App.jsx       # Componente principal
│   └── vite.config.js
│
├── CHANGELOG.md          # Historial de cambios
└── README.md
```

## 📡 Endpoints de la API

### 🔐 Autenticación

| Método | Endpoint             | Descripción                    |
|--------|----------------------|--------------------------------|
| POST   | `/api/auth/register` | Registrar nuevo usuario        |
| POST   | `/api/auth/login`    | Iniciar sesión (obtener token) |
| GET    | `/api/auth/me`       | Obtener usuario actual         |

### 📁 Boards (requiere autenticación)

| Método | Endpoint                 | Descripción                    |
|--------|--------------------------|--------------------------------|
| GET    | `/api/boards/`           | Obtener tableros del usuario   |
| POST   | `/api/boards/`           | Crear un nuevo tablero         |
| GET    | `/api/boards/{board_id}` | Obtener un tablero por ID      |
| DELETE | `/api/boards/{board_id}` | Eliminar un tablero            |

### 🗂️ Lists

| Método | Endpoint                                        | Descripción                         |
|--------|-------------------------------------------------|-------------------------------------|
| POST   | `/api/boards/{board_id}/lists/`                 | Crear lista en un tablero           |
| GET    | `/api/boards/{board_id}/lists/`                 | Obtener listas de un tablero        |
| GET    | `/api/boards/{board_id}/lists/{list_id}`        | Obtener lista por ID                |
| PUT    | `/api/boards/{board_id}/lists/{list_id}`        | Actualizar lista                    |
| DELETE | `/api/boards/{board_id}/lists/{list_id}`        | Eliminar lista                      |
| PUT    | `/api/boards/{board_id}/lists/{list_id}/cards`  | Actualizar las tarjetas de la lista |

### 🗃️ Cards

| Método | Endpoint                                                    | Descripción            |
|--------|-------------------------------------------------------------|------------------------|
| POST   | `/api/boards/{board_id}/lists/{list_id}/cards/create`       | Crear tarjeta          |
| GET    | `/api/boards/{board_id}/lists/{list_id}/cards/`             | Obtener tarjetas       |
| GET    | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`    | Obtener tarjeta por ID |
| PUT    | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`    | Actualizar tarjeta     |
| DELETE | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`    | Eliminar tarjeta       |

## 🔒 Configuración de Entorno

Crea un archivo `.env` en la carpeta `backend/`:

```env
SECRET_KEY=tu-clave-secreta-muy-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///./trello.db
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

Hecho con ❤️ por [PGPLAYER15](https://github.com/PGPLAYER15)
