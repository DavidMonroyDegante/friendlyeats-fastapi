
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "FriendlyEats" in response.text


def test_restaurants_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "restaurantsList" in response.text


def test_restaurant_form_page():
    response = client.get("/restaurant/new")

    assert response.status_code == 200
    assert "restaurantForm" in response.text


def test_api_list_restaurants():
    response = client.get("/api/v1/restaurants/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_filter_options():
    response = client.get("/api/v1/restaurants/filter-options")

    assert response.status_code == 200

    data = response.json()

    assert "cities" in data
    assert "categories" in data
    assert isinstance(data["cities"], list)
    assert isinstance(data["categories"], list)


def test_api_filter_invalid_price():
    response = client.get(
        "/api/v1/restaurants/filter",
        params={"price": 4}
    )

    assert response.status_code == 422


def test_api_restaurant_not_found():
    response = client.get(
        "/api/v1/restaurants/restaurant_que_no_existe_12345"
    )

    assert response.status_code == 404


def test_api_delete_nonexistent_restaurant():
    response = client.delete(
        "/api/v1/restaurants/restaurant_que_no_existe_12345"
    )

    assert response.status_code == 404


# ==========================================
# PRUEBAS DE ACTUALIZACIÃ“N PARCIAL (PATCH)
# ==========================================

def test_api_patch_restaurant_partial(monkeypatch):
    cambios_recibidos = {}

    def fake_update(restaurant_id, data):
        cambios_recibidos.update(
            data.model_dump(exclude_unset=True)
        )

        return {
            "id": restaurant_id,
            "name": "Tacos",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 2,
            "photoUrl": None,
            "avgRating": 0,
            "numRatings": 0
        }

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.update_restaurant",
        fake_update
    )

    response = client.patch(
        "/api/v1/restaurants/restaurante_prueba",
        json={"city": "Puebla"}
    )

    assert response.status_code == 200
    assert response.json()["city"] == "Puebla"
    assert cambios_recibidos == {"city": "Puebla"}


def test_api_patch_restaurant_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.update_restaurant",
        lambda restaurant_id, data: None
    )

    response = client.patch(
        "/api/v1/restaurants/restaurante_inexistente",
        json={"city": "Puebla"}
    )

    assert response.status_code == 404


# ==========================================
# PRUEBA DE ELIMINACIÃ“N EXITOSA (DELETE)
# ==========================================

def test_api_delete_restaurant_returns_204(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.delete_restaurant",
        lambda restaurant_id: True
    )

    response = client.delete(
        "/api/v1/restaurants/restaurante_prueba"
    )

    assert response.status_code == 204
    assert response.content == b""


# ==========================================
# PRUEBAS DE PAGINACIÃ“N DE LA API
# ==========================================

def test_api_pagination_default_parameters(monkeypatch):
    received = {}

    def fake_paginated(limit, start_after, order_by):
        received["limit"] = limit
        received["start_after"] = start_after
        received["order_by"] = order_by
        return []

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.get_paginated_restaurants",
        fake_paginated
    )

    response = client.get("/api/v1/restaurants/")

    assert response.status_code == 200
    assert received == {
        "limit": 20,
        "start_after": None,
        "order_by": "name"
    }


def test_api_pagination_custom_parameters(monkeypatch):
    received = {}

    def fake_paginated(limit, start_after, order_by):
        received["limit"] = limit
        received["start_after"] = start_after
        received["order_by"] = order_by
        return []

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.get_paginated_restaurants",
        fake_paginated
    )

    response = client.get(
        "/api/v1/restaurants/",
        params={
            "limit": 5,
            "start_after": "ultimo_restaurante",
            "order_by": "avgRating"
        }
    )

    assert response.status_code == 200
    assert received == {
        "limit": 5,
        "start_after": "ultimo_restaurante",
        "order_by": "avgRating"
    }


def test_api_pagination_invalid_limit():
    response = client.get(
        "/api/v1/restaurants/",
        params={"limit": 101}
    )

    assert response.status_code == 422


def test_api_pagination_invalid_order():
    response = client.get(
        "/api/v1/restaurants/",
        params={"order_by": "categoria"}
    )

    assert response.status_code == 422

# ==========================================
# PRUEBAS DE CREACION (POST)
# ==========================================

def test_api_create_restaurant(monkeypatch):
    def fake_create(data):
        return {
            "id": "restaurante_nuevo",
            "name": data.name,
            "category": data.category,
            "city": data.city,
            "price": data.price,
            "photoUrl": data.photoUrl,
            "avgRating": 0,
            "numRatings": 0
        }

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.create_restaurant",
        fake_create
    )

    response = client.post(
        "/api/v1/restaurants/",
        json={
            "name": "Tacos de prueba",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 2
        }
    )

    assert response.status_code == 201
    assert response.json()["id"] == "restaurante_nuevo"
    assert response.json()["name"] == "Tacos de prueba"


def test_api_create_restaurant_invalid_price():
    response = client.post(
        "/api/v1/restaurants/",
        json={
            "name": "Tacos de prueba",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 4
        }
    )

    assert response.status_code == 422


# ==========================================
# PRUEBAS DE ACTUALIZACION (PUT)
# ==========================================

def test_api_update_restaurant(monkeypatch):
    def fake_update(restaurant_id, data):
        return {
            "id": restaurant_id,
            "name": data.name,
            "category": data.category,
            "city": data.city,
            "price": data.price,
            "photoUrl": data.photoUrl,
            "avgRating": 0,
            "numRatings": 0
        }

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.update_restaurant",
        fake_update
    )

    response = client.put(
        "/api/v1/restaurants/restaurante_prueba",
        json={
            "name": "Tacos actualizados",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 2
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Tacos actualizados"


def test_api_update_restaurant_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.update_restaurant",
        lambda restaurant_id, data: None
    )

    response = client.put(
        "/api/v1/restaurants/inexistente",
        json={"name": "Tacos actualizados"}
    )

    assert response.status_code == 404


# ==========================================
# PRUEBA DE CONSULTA POR ID
# ==========================================

def test_api_get_existing_restaurant(monkeypatch):
    def fake_get(restaurant_id):
        return {
            "id": restaurant_id,
            "name": "Tacos de prueba",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 2,
            "photoUrl": None,
            "avgRating": 4.5,
            "numRatings": 10
        }

    monkeypatch.setattr(
        "app.api.v1.restaurants.restaurant_service.get_restaurant_by_id",
        fake_get
    )

    response = client.get(
        "/api/v1/restaurants/restaurante_prueba"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Tacos de prueba"
    assert response.json()["avgRating"] == 4.5


# ==========================================
# PRUEBA DE VALIDACION DE NOMBRE
# ==========================================

def test_api_create_restaurant_empty_name():
    response = client.post(
        "/api/v1/restaurants/",
        json={
            "name": "",
            "category": "Mexicana",
            "city": "Puebla",
            "price": 2
        }
    )

    assert response.status_code == 422