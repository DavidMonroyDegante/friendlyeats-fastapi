# FriendlyEats — Sprint 1

Aplicación web para consultar, registrar, editar, filtrar y eliminar restaurantes. El proyecto utiliza FastAPI como API y Firebase Firestore como base de datos, con el emulador local para desarrollo y pruebas.

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

En Windows PowerShell:

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

```powershell
pip install -r requirements.txt
```

## Configuración y ejecución

### 1. Iniciar Firestore Emulator

Desde la raíz del proyecto:

```powershell
firebase.cmd emulators:start --only firestore
```

Mantén esta terminal abierta.

La configuración del proyecto utiliza el emulador local de Firestore. Revisa `firebase.json` y `app/core/config.py` para confirmar los puertos y el identificador del proyecto.

### 2. Iniciar FastAPI

Abre una segunda terminal, activa el entorno virtual y ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

### 3. Abrir la aplicación

- Aplicación web: http://127.0.0.1:8000/
- Documentación de la API: http://127.0.0.1:8000/docs
- Consola del emulador: http://127.0.0.1:4000

## Funcionalidades

- Listado de restaurantes.
- Búsqueda por ciudad, categoría y precio.
- Opciones de filtros obtenidas de los datos disponibles.
- Visualización de detalles de cada restaurante.
- Registro de restaurantes.
- Edición de restaurantes.
- Eliminación de restaurantes con confirmación.
- Paginación visual de los resultados.
- API REST para operaciones CRUD.
- Validación de los datos de entrada.

## Endpoints principales

| Método | Endpoint | Función |
|---|---|---|
| GET | `/api/v1/restaurants/` | Consultar restaurantes |
| GET | `/api/v1/restaurants/filter` | Filtrar restaurantes |
| GET | `/api/v1/restaurants/filter-options` | Obtener ciudades y categorías |
| GET | `/api/v1/restaurants/{restaurant_id}` | Consultar un restaurante |
| POST | `/api/v1/restaurants/` | Registrar un restaurante |
| PUT | `/api/v1/restaurants/{restaurant_id}` | Actualizar un restaurante |
| DELETE | `/api/v1/restaurants/{restaurant_id}` | Eliminar un restaurante |

## Pruebas automáticas

Con el entorno virtual activo, ejecuta:

```powershell
pytest -v
```

Las pruebas verifican páginas web, consulta de restaurantes, opciones de filtros y respuestas de error de la API.

## Estado del proyecto

La interfaz web, las operaciones CRUD y los filtros están implementados. La suite inicial de pruebas contiene ocho pruebas aprobadas en el entorno local.

La paginación actual se realiza en la interfaz después de consultar los resultados de la API; no corresponde a paginación del lado de Firestore.