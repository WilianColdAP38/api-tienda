# API Tienda

API RESTful con CRUD de **Productos** y **Pedidos**, hecha con FastAPI + SQLModel (SQLite) y desplegada en AWS EC2 con pm2 en el puerto **8010**.

- URL pública: `http://<ip-publica>:8010/`
- Documentación interactiva: `http://<ip-publica>:8010/docs`

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/productos/` | Crear producto |
| GET | `/productos/` | Listar productos (`offset`, `limit`) |
| GET | `/productos/{id}` | Obtener un producto |
| PATCH | `/productos/{id}` | Actualizar parcialmente |
| DELETE | `/productos/{id}` | Eliminar (409 si tiene pedidos) |
| POST | `/pedidos/` | Crear pedido: valida stock, lo descuenta y calcula el total |
| GET | `/pedidos/` | Listar pedidos (`offset`, `limit`) |
| GET | `/pedidos/{id}` | Obtener un pedido |
| PATCH | `/pedidos/{id}` | Cambiar `cliente` o `estado` |
| DELETE | `/pedidos/{id}` | Eliminar pedido |

## Ejecutar en local

```bash
python -m venv venv
# Windows PowerShell:  .\venv\Scripts\Activate.ps1
# Linux / macOS:       source venv/bin/activate
pip install -r requirements.txt
python -m pytest -v
uvicorn app.main:app --reload --port 8010
```

## Desplegar / actualizar en EC2 (Ubuntu)

```bash
cd ~/api-tienda
git pull
venv/bin/pip install -r requirements.txt
pm2 restart api-tienda
```


