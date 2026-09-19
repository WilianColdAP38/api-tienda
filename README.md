# API Tienda — FastAPI desplegada en AWS EC2

API RESTful con operaciones CRUD completas para **Productos** y **Pedidos**, construida con FastAPI y SQLModel, desplegada en una instancia de AWS EC2 y ejecutándose de forma permanente con pm2.

**URL pública:** http://18.235.4.218:8010/
**Documentación interactiva (Swagger):** http://18.235.4.218:8010/docs

---

## Descripción

Este proyecto expone una API para gestionar el inventario de una tienda y sus pedidos. Implementa dos entidades relacionadas y una regla de negocio central: al crear un pedido se descuenta el stock del producto, y el sistema impide vender más unidades de las disponibles o eliminar productos que ya tienen pedidos asociados.

La API está desplegada en la nube sobre una instancia EC2 con Ubuntu, es accesible públicamente por internet y se mantiene en línea de forma automática incluso tras reinicios del servidor.

---

## Tecnologías

- **Python 3** — lenguaje base
- **FastAPI** — framework de la API REST
- **SQLModel** — ORM sobre SQLite
- **Uvicorn** — servidor ASGI
- **pytest** — pruebas automatizadas (17 tests)
- **AWS EC2** — servidor en la nube (Ubuntu Server, t3.micro)
- **pm2** — gestor de procesos para mantener la API en línea

---

## Entidades y reglas de negocio

### Productos
Campos: `id`, `nombre`, `descripcion`, `precio`, `stock`.

### Pedidos
Campos: `id`, `cliente`, `producto_id`, `cantidad`, `total`, `estado`.

### Reglas implementadas
- Al crear un pedido, el **total se calcula automáticamente** (precio × cantidad).
- Al crear un pedido, se **descuenta el stock** del producto.
- No se puede crear un pedido con **más cantidad que el stock disponible** → responde `409 Conflict`.
- No se puede **eliminar un producto que tiene pedidos asociados** → responde `409 Conflict`.
- Los `id` son **autogenerados** por la base de datos.

---

## Endpoints

### Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/productos/` | Crear producto |
| GET | `/productos/` | Listar productos |
| GET | `/productos/{id}` | Obtener un producto |
| PATCH | `/productos/{id}` | Actualizar producto |
| DELETE | `/productos/{id}` | Eliminar producto |

### Pedidos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/pedidos/` | Crear pedido |
| GET | `/pedidos/` | Listar pedidos |
| GET | `/pedidos/{id}` | Obtener un pedido |
| PATCH | `/pedidos/{id}` | Actualizar estado del pedido |
| DELETE | `/pedidos/{id}` | Eliminar pedido |

---

## Cómo se construyó y desplegó

El desarrollo partió de una API funcional probada en local y se llevó a producción en la nube siguiendo estas fases:

### 1. Desarrollo local
- Código de la API con las dos entidades y la regla de stock.
- Entorno virtual (`venv`) con las dependencias de `requirements.txt`.
- **17 pruebas automatizadas** ejecutadas con `pytest`, todas en verde.
- Repositorio versionado en Git y publicado en GitHub (`venv/` y la base de datos excluidos con `.gitignore`).

### 2. Infraestructura en AWS
- Instancia **EC2 Ubuntu Server (t3.micro, capa gratuita)** en la región `us-east-1`.
- **Grupo de seguridad** con dos reglas: SSH (puerto 22) restringido a la IP del administrador, y puerto **8010 abierto públicamente** (`0.0.0.0/0`) para el acceso a la API.
- **Elastic IP** `18.235.4.218` asociada a la instancia, para tener una dirección pública fija que no cambia al reiniciar.

### 3. Despliegue en el servidor
- Conexión por SSH a la instancia.
- Clonado del repositorio, creación del `venv` e instalación de dependencias.
- Verificación de los 17 tests en el servidor.
- Ejecución permanente con **pm2**, configurado para arrancar automáticamente tras reinicios (`pm2 startup` + `pm2 save`), verificado con un `reboot`.

---

## Cómo ejecutar el proyecto en local

```bash
# Clonar el repositorio
git clone https://github.com/WilianColdAP38/api-tienda.git
cd api-tienda

# Crear y activar el entorno virtual
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# Ejecutar los tests
venv/bin/python -m pytest -q

# Levantar la API
venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8010
```

Luego abrir en el navegador: `http://localhost:8010/docs`

---

## Autor

**Wilian Jami** — Estudiante de Ingeniería en Sistemas, UIDE.
Autonomous Activity: Fastapi on EC2
