from app.repositories import restaurant_repository
from app.domain.models import Restaurant
from app.domain.schemas import RestaurantCreate, RestaurantUpdate


# Obtener todos los restaurantes
def get_all_restaurants():
    return restaurant_repository.get_all()


# Obtener un restaurante por su ID
def get_restaurant_by_id(restaurant_id: str):
    return restaurant_repository.get_by_id(restaurant_id)


# Crear un restaurante
def create_restaurant(data: RestaurantCreate):
    restaurant = Restaurant(**data.model_dump())
    return restaurant_repository.create(restaurant)


# Actualizar un restaurante
def update_restaurant(restaurant_id: str, data: RestaurantUpdate):
    changes = data.model_dump(exclude_unset=True)

    if not changes:
        return restaurant_repository.get_by_id(restaurant_id)

    return restaurant_repository.update(restaurant_id, changes)


# Eliminar un restaurante
def delete_restaurant(restaurant_id: str):
    return restaurant_repository.delete(restaurant_id)





# Filtrar restaurantes por ciudad, categoría y precio
def filter_restaurants(
    city: str | None = None,
    category: str | None = None,
    price: int | None = None
):
    return restaurant_repository.filter_restaurants(
        city=city,
        category=category,
        price=price
    )





# Obtener opciones disponibles para los filtros
def get_filter_options():
    return restaurant_repository.get_filter_options()
