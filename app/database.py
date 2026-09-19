"""Conexión a la base de datos y dependencia de sesión."""
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

# Ruta absoluta: la BD siempre queda en la raíz del proyecto,
# sin importar desde qué carpeta se lance uvicorn o pm2.
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'tienda.db'}"

# check_same_thread=False: FastAPI atiende peticiones en varios hilos
# y SQLite por defecto solo permite usar la conexión en el hilo que la creó.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
