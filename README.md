# 📝 Clon de Trello

**Clon Trello** es una aplicación tipo *To-Do* que permite a los usuarios enlistar, organizar y mover tareas entre diferentes columnas, al estilo del conocido gestor Trello.

## 🚀 Funcionalidades principales

- Crear tareas en columnas (como "Por hacer", "En progreso", "Hecho").
- Arrastrar y soltar tareas entre columnas gracias a **dnd-kit**.
- Backend robusto con **FastAPI** para gestionar tareas y columnas.
- Interfaz interactiva y dinámica con **React** y **JavaScript**.

## 🛠️ Tecnologías utilizadas

- 🐍 **Python** (FastAPI)
- ⚛️ **React**
- 📦 **dnd-kit**
- 💡 **JavaScript**

## 🔧 Instalación y ejecución

### Requisitos

- Node.js
- Python 3.9+
- pip

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

````
### Frontend (React)

```bash
cd frontend
npm install
npm run dev
`````
## 🖼️ Demo

<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1Xeq2xOE_q1JpyrJyo1G_KH8hTV0eWKLV" alt="Captura del proyecto 1" width="600"/>
</div>
<br/>
<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1QEomySE5Ggf36SoSY030lAGyzBKzLqFY" alt="Captura del proyecto 4" width="600"/>
</div>
<br/>
<div align="center">
  <img src="https://drive.google.com/uc?export=view&id=1f-vm0omBTYjV4bD4INdzks_DG1ax84os" alt="Captura del proyecto 3" width="600"/>
</div>

## 📂 Estructura del proyecto

```bash
├── backend/
│   ├── app/
│   │   ├── models/       # Modelos SQLAlchemy (Card, Board, List)
│   │   ├── routes/       # Rutas de la API para cada entidad
│   │   ├── schemas/      # Esquemas Pydantic para validación
│   ├── main.py           # Punto de entrada para FastAPI
│   └── trello.db         # Base de datos SQLite
│
├── frontend/
│   ├── config/           # Configuración del cliente HTTP
│   ├── src/
│   │   ├── assets/       # Recursos gráficos (si aplica)
│   │   ├── components/   # Componentes reutilizables
│   │   ├── hooks/        # Custom hooks (lógica compartida)
│   │   ├── pages/        # Páginas principales (Home, Board)
│   │   ├── services/     # Conexiones con la API
│   │   ├── App.jsx       # Componente principal
│   │   └── main.jsx      # Punto de entrada
└── README.md

````

## 📡 Endpoints de la API

A continuación se describen los principales endpoints RESTful disponibles en el backend (FastAPI):

### 📁 Boards

| Método | Endpoint                      | Descripción               |
|--------|-------------------------------|---------------------------|
| GET    | `/api/boards/`                | Obtener todos los tableros |
| POST   | `/api/boards/`                | Crear un nuevo tablero    |
| GET    | `/api/boards/{board_id}`      | Obtener un tablero por ID |
| DELETE | `/api/boards/{board_id}`      | Eliminar un tablero       |

### 🗂️ Lists

| Método | Endpoint                                                | Descripción                        |
|--------|---------------------------------------------------------|------------------------------------|
| POST   | `/api/boards/{board_id}/lists/`                         | Crear lista en un tablero          |
| GET    | `/api/boards/{board_id}/lists/`                         | Obtener listas de un tablero       |
| GET    | `/api/boards/{board_id}/lists/{list_id}`               | Obtener lista por ID               |
| PUT    | `/api/boards/{board_id}/lists/{list_id}`               | Actualizar lista                   |
| DELETE | `/api/boards/{board_id}/lists/{list_id}`               | Eliminar lista                     |
| PUT    | `/api/boards/{board_id}/lists/{list_id}/cards`         | Actualizar las tarjetas de la lista|

### 🗃️ Cards

| Método | Endpoint                                                                      | Descripción            |
|--------|-------------------------------------------------------------------------------|------------------------|
| POST   | `/api/boards/{board_id}/lists/{list_id}/cards/create`                        | Crear tarjeta          |
| GET    | `/api/boards/{board_id}/lists/{list_id}/cards/`                              | Obtener tarjetas       |
| GET    | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`                     | Obtener tarjeta por ID |
| PUT    | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`                     | Actualizar tarjeta     |
| DELETE | `/api/boards/{board_id}/lists/{list_id}/cards/{card_id}`                     | Eliminar tarjeta       |
