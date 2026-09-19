"""CRUD de pedidos. Crear un pedido descuenta stock y calcula el total."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Pedido, PedidoCreate, PedidoPublic, PedidoUpdate, Producto

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def obtener_pedido_o_404(pedido_id: int, session: Session) -> Pedido:
    pedido = session.get(Pedido, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.post("/", response_model=PedidoPublic, status_code=status.HTTP_201_CREATED)
def crear_pedido(datos: PedidoCreate, session: Session = Depends(get_session)):
    producto = session.get(Producto, datos.producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if producto.stock < datos.cantidad:
        raise HTTPException(
            status_code=409,
            detail=f"Stock insuficiente: disponible {producto.stock}",
        )

    producto.stock -= datos.cantidad
    pedido = Pedido(
        cliente=datos.cliente,
        cantidad=datos.cantidad,
        producto_id=datos.producto_id,
        total=round(producto.precio * datos.cantidad, 2),
    )
    session.add(producto)
    session.add(pedido)
    session.commit()  # un solo commit: stock y pedido se guardan juntos o ninguno
    session.refresh(pedido)
    return pedido


@router.get("/", response_model=list[PedidoPublic])
def listar_pedidos(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Pedido).offset(offset).limit(limit)).all()


@router.get("/{pedido_id}", response_model=PedidoPublic)
def obtener_pedido(pedido_id: int, session: Session = Depends(get_session)):
    return obtener_pedido_o_404(pedido_id, session)


@router.patch("/{pedido_id}", response_model=PedidoPublic)
def actualizar_pedido(
    pedido_id: int, datos: PedidoUpdate, session: Session = Depends(get_session)
):
    pedido = obtener_pedido_o_404(pedido_id, session)
    pedido.sqlmodel_update(datos.model_dump(exclude_unset=True))
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = obtener_pedido_o_404(pedido_id, session)
    session.delete(pedido)
    session.commit()
