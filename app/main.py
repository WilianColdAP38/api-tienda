"""Punto de entrada: crea la app, las tablas y registra los routers."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import pedidos, productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="API Tienda",
    description="API RESTful con CRUD de Productos y Pedidos. FastAPI + SQLModel, desplegada en AWS EC2.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/", tags=["Estado"])
def raiz():
    return {"estado": "ok", "docs": "/docs"}
