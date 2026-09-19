"""CRUD de productos."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Pedido, Producto, ProductoCreate, ProductoPublic, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


def obtener_producto_o_404(producto_id: int, session: Session) -> Producto:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCreate, session: Session = Depends(get_session)):
    producto = Producto.model_validate(datos)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.get("/", response_model=list[ProductoPublic])
def listar_productos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Producto).offset(offset).limit(limit)).all()


@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    return obtener_producto_o_404(producto_id, session)


@router.patch("/{producto_id}", response_model=ProductoPublic)
def actualizar_producto(
    producto_id: int, datos: ProductoUpdate, session: Session = Depends(get_session)
):
    producto = obtener_producto_o_404(producto_id, session)
    # exclude_unset: solo toca los campos que el cliente envió
    producto.sqlmodel_update(datos.model_dump(exclude_unset=True))
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, session: Session = Depends(get_session)):
    producto = obtener_producto_o_404(producto_id, session)
    # SQLite no aplica llaves foráneas por defecto: lo validamos nosotros
    # para no dejar pedidos apuntando a un producto que ya no existe.
    tiene_pedidos = session.exec(
        select(Pedido).where(Pedido.producto_id == producto_id)
    ).first()
    if tiene_pedidos:
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: el producto tiene pedidos asociados",
        )
    session.delete(producto)
    session.commit()
