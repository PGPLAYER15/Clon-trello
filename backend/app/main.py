from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.database import engine, Base, SessionLocal
from app.api.v1 import auth, boards, lists, cards
from app.domain.entities.board import Board
from app.domain.entities.list import List
from app.domain.entities.card import Card
from app.domain.entities.user import User

app = FastAPI(title="Trello Clone API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if not db.query(Board).first():
            demo_board = Board(
                title="Mi Primer Tablero",
                description="Tablero de ejemplo creado automáticamente",
                color="#0079BF"
            )
            db.add(demo_board)
            db.commit()
            db.refresh(demo_board)
            
            lista_todo = List(title="Por Hacer", board_id=demo_board.id)
            lista_progreso = List(title="En Progreso", board_id=demo_board.id)
            lista_hecho = List(title="Hecho", board_id=demo_board.id)
            
            db.add_all([lista_todo, lista_progreso, lista_hecho])
            db.commit()
            
            tarjeta_1 = Card(title="Configurar proyecto", list_id=lista_todo.id)
            tarjeta_2 = Card(title="Diseñar interfaz", list_id=lista_todo.id)
            
            db.add_all([tarjeta_1, tarjeta_2])
            db.commit()
                        
    except Exception as e:
        print(f" Error al crear datos iniciales: {str(e)}")
        db.rollback()
    finally:
        db.close()

# Auth routes
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["auth"]
)

# Board routes
app.include_router(
    boards.router, 
    prefix="/api/boards",
    tags=["boards"]
)

app.include_router(
    lists.router, 
    prefix="/api/boards/{board_id}/lists",
    tags=["lists"]
)

app.include_router(
    cards.router, 
    prefix="/api/boards/{board_id}/lists/{list_id}/cards",
    tags=["cards"]
)

@app.get("/")
def read_root():
    return {"message": "API de Trello Clone - Clean Architecture v2.0"}