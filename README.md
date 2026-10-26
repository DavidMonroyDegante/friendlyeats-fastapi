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
| GET | `/health` | Verificar que la aplicación está funcionando |
| GET | `/api/v1/restaurants/` | Consultar restaurantes con paginación |
| GET | `/api/v1/restaurants/filter` | Filtrar por ciudad, categoría y precio |
| GET | `/api/v1/restaurants/filter-options` | Obtener ciudades y categorías disponibles |
| GET | `/api/v1/restaurants/{restaurant_id}` | Consultar los detalles de un restaurante |
| POST | `/api/v1/restaurants/` | Registrar un restaurante |
| PUT | `/api/v1/restaurants/{restaurant_id}` | Actualizar un restaurante |
| PATCH | `/api/v1/restaurants/{restaurant_id}` | Actualizar únicamente los campos enviados |
| DELETE | `/api/v1/restaurants/{restaurant_id}` | Eliminar un restaurante; devuelve 204 si se elimina correctamente |

### Parámetros de paginación

El endpoint de consulta admite los siguientes parámetros:
- `limit`: cantidad máxima de restaurantes por consulta. Su valor predeterminado es 20 y admite valores de 1 a 100.
- `start_after`: identificador del último restaurante de la página anterior, para continuar la consulta.
- `order_by`: campo de ordenamiento. Admite `name` o `avgRating`; por defecto utiliza `name`.

Ejemplo:

`/api/v1/restaurants/?limit=5&order_by=name`

La API utiliza paginación sobre las consultas a Firestore. Por separado, la interfaz web muestra cinco restaurantes por página.


## Pruebas automáticas

Con el entorno virtual activo, ejecuta:

```powershell
pytest -v
```

Las pruebas verifican diferentes comportamientos de la aplicación, incluyendo páginas web, consultas y validaciones de la API, actualización parcial mediante PATCH, eliminación con respuesta 204 y validación de los parámetros de paginación.

En la última ejecución se obtuvieron 15 pruebas aprobadas.



## Estado del proyecto

El proyecto cuenta con una interfaz web para listar, filtrar, consultar detalles, registrar, editar y eliminar restaurantes. La API REST está conectada con Firestore y dispone de operaciones CRUD, validación de datos, filtros y paginación.

La interfaz web muestra cinco restaurantes por página, mientras que la API permite consultar hasta 100 restaurantes por solicitud, con un límite predeterminado de 20.

La suite de pruebas contiene 15 pruebas aprobadas en la última ejecución local. El proyecto utiliza el emulador de Firestore para facilitar el desarrollo y las pruebas sin depender de una base de datos de producción.
