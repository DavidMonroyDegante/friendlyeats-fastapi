
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
