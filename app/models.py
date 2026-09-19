"""Modelos de tabla y esquemas de entrada/salida de las dos entidades."""
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


# ---------- Producto ----------
class ProductoBase(SQLModel):
    nombre: str = Field(min_length=1, max_length=100, index=True)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float = Field(gt=0)
    stock: int = Field(default=0, ge=0)


class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductoCreate(ProductoBase):
    pass


class ProductoPublic(ProductoBase):
    id: int


class ProductoUpdate(SQLModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=300)
    precio: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


# ---------- Pedido ----------
class EstadoPedido(str, Enum):
    pendiente = "pendiente"
    pagado = "pagado"
    enviado = "enviado"
    cancelado = "cancelado"


class PedidoBase(SQLModel):
    cliente: str = Field(min_length=1, max_length=100)
    cantidad: int = Field(gt=0)
    producto_id: int = Field(foreign_key="producto.id")


class Pedido(PedidoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    total: float
    estado: EstadoPedido = Field(default=EstadoPedido.pendiente)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PedidoCreate(PedidoBase):
    pass


class PedidoPublic(PedidoBase):
    id: int
    total: float
    estado: EstadoPedido
    fecha: datetime


class PedidoUpdate(SQLModel):
    cliente: str | None = Field(default=None, min_length=1, max_length=100)
    estado: EstadoPedido | None = None
