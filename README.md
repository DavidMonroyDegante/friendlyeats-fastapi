# FriendlyEats — Sprint 1

Aplicación web para consultar, registrar, editar, filtrar y eliminar restaurantes. El proyecto utiliza FastAPI para la API y Firebase Firestore como base de datos, con el emulador local para el desarrollo y las pruebas.

## Tecnologías utilizadas

- Python 3.12
- FastAPI
- Firebase Firestore Emulator
- HTML5
- CSS3
- JavaScript
- Jinja2
- Pytest

## Requisitos previos

- Python 3.12 instalado.
- Node.js instalado.
- Firebase CLI instalado.
- Java instalado para ejecutar el emulador de Firestore.
- Visual Studio Code (recomendado).

## Estructura del proyecto

```text
friendlyeats-fastapi/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── restaurants.py
│   ├── core/
│   │   ├── config.py
│   │   └── firebase.py
│   ├── domain/
│   ├── repositories/
│   ├── services/
│   ├── templates/
│   └── main.py
├── scripts/
│   └── seed.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── tests/
│   └── test_restaurants.py
├── firebase.json
├── firestore.rules
├── pytest.ini
├── requirements.txt
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/DavidMonroyDegante/friendlyeats-fastapi.git
cd friendlyeats-fastapi
```

### 2. Crear un entorno virtual

En Windows PowerShell, ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

Con el entorno virtual activo, ejecuta:

```powershell
pip install -r requirements.txt
```

## Configuración y ejecución

### 1. Iniciar Firestore Emulator

Desde la raíz del proyecto, ejecuta:

```powershell
firebase.cmd emulators:start --only firestore
```

Mantén esta terminal abierta mientras utilizas la aplicación.

La configuración utiliza el emulador local de Firestore. Los puertos y el identificador del proyecto se configuran en `firebase.json` y `app/core/config.py`.

### 2. Cargar los restaurantes de ejemplo

Con el emulador de Firestore en funcionamiento, abre otra terminal en la raíz del proyecto, activa el entorno virtual y ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
python -m scripts.seed
```

El script `scripts/seed.py` contiene diez restaurantes de ejemplo para la colección `restaurants`.

Antes de agregar cada restaurante, comprueba si ya existe uno con el mismo nombre. Si lo encuentra, lo omite para evitar duplicados y no modifica los datos existentes. Por esta razón, al ejecutar el script por segunda vez, no necesariamente se agregarán restaurantes nuevos.

### 3. Iniciar FastAPI

Abre otra terminal en la raíz del proyecto y ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Mantén esta terminal abierta mientras utilizas la aplicación.

### 4. Abrir la aplicación

- **Aplicación web:** http://127.0.0.1:8000/
- **Documentación de la API:** http://127.0.0.1:8000/docs
- **Consola del emulador:** http://127.0.0.1:4000

## Funcionalidades

- Listado de restaurantes.
- Búsqueda por ciudad, categoría y precio.
- Opciones de filtros obtenidas de los datos disponibles.
- Visualización de los detalles de cada restaurante.
- Registro de restaurantes.
- Edición de restaurantes.
- Eliminación de restaurantes con confirmación.
- Paginación visual de los resultados.
- API REST para operaciones CRUD.
- Validación de los datos de entrada.

## Endpoints principales

| Método | Endpoint | Función |
|---|---|---|
| GET | `/health` | Verificar que la aplicación está funcionando. |
| GET | `/api/v1/restaurants/` | Consultar restaurantes con paginación. |
| GET | `/api/v1/restaurants/filter` | Filtrar por ciudad, categoría y precio. |
| GET | `/api/v1/restaurants/filter-options` | Obtener ciudades y categorías disponibles. |
| GET | `/api/v1/restaurants/{restaurant_id}` | Consultar los detalles de un restaurante. |
| POST | `/api/v1/restaurants/` | Registrar un restaurante. |
| PUT | `/api/v1/restaurants/{restaurant_id}` | Actualizar un restaurante. |
| PATCH | `/api/v1/restaurants/{restaurant_id}` | Actualizar únicamente los campos enviados. |
| DELETE | `/api/v1/restaurants/{restaurant_id}` | Eliminar un restaurante; devuelve `204` si se elimina correctamente. |

### Parámetros de paginación

El endpoint de consulta admite los siguientes parámetros:

- `limit`: cantidad máxima de restaurantes por consulta. Su valor predeterminado es `20` y admite valores de `1` a `100`.
- `start_after`: identificador del último restaurante de la página anterior, para continuar la consulta.
- `order_by`: campo de ordenamiento. Admite `name` o `avgRating`; por defecto utiliza `name`.

Ejemplo de consulta:

```text
/api/v1/restaurants/?limit=5&order_by=name
```

La API utiliza paginación en las consultas a Firestore. Por separado, la interfaz web muestra cinco restaurantes por página.

## Pruebas automáticas

Con el entorno virtual activo, ejecuta:

```powershell
pytest -v
```

La suite contiene **21 pruebas aprobadas en la última ejecución local**. Estas pruebas verifican diferentes comportamientos de la aplicación, entre ellos:

- Visualización de páginas web.
- Consultas y operaciones CRUD de la API.
- Validación de los datos de entrada.
- Consulta de restaurantes existentes y manejo de registros inexistentes.
- Actualización parcial mediante `PATCH`.
- Actualización mediante `PUT`.
- Eliminación con respuesta `204`.
- Validación de los parámetros de paginación.

Para comprobar el resultado más reciente, ejecuta nuevamente `pytest -v`.

## Estado del proyecto

El proyecto cuenta con una interfaz web para listar, filtrar, consultar detalles, registrar, editar y eliminar restaurantes. La API REST está conectada con Firestore y dispone de operaciones CRUD, validación de datos, filtros y paginación.

La interfaz web muestra cinco restaurantes por página, mientras que la API permite consultar hasta 100 restaurantes por solicitud, con un límite predeterminado de 20.

También se incluye un script para cargar diez restaurantes de ejemplo en la colección `restaurants`, evitando agregar registros con nombres que ya existan.

La suite de pruebas contiene 21 pruebas aprobadas en la última ejecución local. El proyecto utiliza el emulador de Firestore para facilitar el desarrollo y las pruebas sin depender de una base de datos de producción.

## Decisiones de desarrollo

- **Separación por capas:** la API, los servicios, los repositorios y los modelos se organizan en módulos distintos para facilitar el mantenimiento.
- **Validación de datos:** se utilizan esquemas de Pydantic para validar la información recibida por la API.
- **Persistencia:** Firestore se utiliza como base de datos NoSQL.
- **Entorno local:** el emulador de Firestore permite realizar pruebas durante el desarrollo sin utilizar una base de datos de producción.
- **Carga inicial:** el script de datos de ejemplo comprueba los nombres existentes antes de insertar nuevos registros.
- **Pruebas automatizadas:** Pytest permite comprobar las respuestas y validaciones de la aplicación.