import pytest

PRODUCTO = {"nombre": "Teclado", "descripcion": "Mecánico", "precio": 45.5, "stock": 10}
PEDIDO = {"cliente": "Ana", "cantidad": 2, "producto_id": 1}


@pytest.fixture(autouse=True)
def producto_base(client):
    client.post("/productos/", json=PRODUCTO)


def test_crear_pedido_calcula_total_y_descuenta_stock(client):
    r = client.post("/pedidos/", json=PEDIDO)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["total"] == 91.0
    assert cuerpo["estado"] == "pendiente"
    assert client.get("/productos/1").json()["stock"] == 8


def test_crear_pedido_producto_inexistente(client):
    r = client.post("/pedidos/", json={**PEDIDO, "producto_id": 999})
    assert r.status_code == 404


def test_crear_pedido_stock_insuficiente(client):
    r = client.post("/pedidos/", json={**PEDIDO, "cantidad": 11})
    assert r.status_code == 409
    assert client.get("/productos/1").json()["stock"] == 10  # no se tocó


def test_listar_pedidos(client):
    client.post("/pedidos/", json=PEDIDO)
    r = client.get("/pedidos/")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_obtener_pedido_inexistente(client):
    assert client.get("/pedidos/999").status_code == 404


def test_actualizar_estado_pedido(client):
    client.post("/pedidos/", json=PEDIDO)
    r = client.patch("/pedidos/1", json={"estado": "pagado"})
    assert r.status_code == 200
    assert r.json()["estado"] == "pagado"


def test_actualizar_estado_invalido(client):
    client.post("/pedidos/", json=PEDIDO)
    assert client.patch("/pedidos/1", json={"estado": "volando"}).status_code == 422


def test_eliminar_pedido(client):
    client.post("/pedidos/", json=PEDIDO)
    assert client.delete("/pedidos/1").status_code == 204
    assert client.get("/pedidos/1").status_code == 404
