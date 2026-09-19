PRODUCTO = {"nombre": "Teclado", "descripcion": "Mecánico", "precio": 45.5, "stock": 10}


def test_crear_producto(client):
    r = client.post("/productos/", json=PRODUCTO)
    assert r.status_code == 201
    assert r.json() == {"id": 1, **PRODUCTO}


def test_crear_producto_precio_invalido(client):
    r = client.post("/productos/", json={**PRODUCTO, "precio": -1})
    assert r.status_code == 422


def test_listar_productos(client):
    client.post("/productos/", json=PRODUCTO)
    client.post("/productos/", json={**PRODUCTO, "nombre": "Mouse"})
    r = client.get("/productos/")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_obtener_producto(client):
    client.post("/productos/", json=PRODUCTO)
    r = client.get("/productos/1")
    assert r.status_code == 200
    assert r.json()["nombre"] == "Teclado"


def test_obtener_producto_inexistente(client):
    assert client.get("/productos/999").status_code == 404


def test_actualizar_producto_parcial(client):
    client.post("/productos/", json=PRODUCTO)
    r = client.patch("/productos/1", json={"precio": 50})
    assert r.status_code == 200
    assert r.json()["precio"] == 50
    assert r.json()["nombre"] == "Teclado"  # lo no enviado no cambia


def test_eliminar_producto(client):
    client.post("/productos/", json=PRODUCTO)
    assert client.delete("/productos/1").status_code == 204
    assert client.get("/productos/1").status_code == 404


def test_eliminar_producto_con_pedidos(client):
    client.post("/productos/", json=PRODUCTO)
    client.post("/pedidos/", json={"cliente": "Ana", "cantidad": 1, "producto_id": 1})
    assert client.delete("/productos/1").status_code == 409
