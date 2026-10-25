from fastapi import APIRouter, HTTPException, status

from app.domain.schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.services import restaurant_service


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurantes"]
)


# Obtener todos los restaurantes
@router.get("/", response_model=list[RestaurantResponse])
def get_restaurants():
    return restaurant_service.get_all_restaurants()



# Filtrar restaurantes por ciudad, categoría y precio
@router.get("/filter", response_model=list[RestaurantResponse])
def filter_restaurants(
    city: str | None = None,
    category: str | None = None,
    price: int | None = None
):
    if price is not None and price not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El precio debe ser 1, 2 o 3"
        )

    return restaurant_service.filter_restaurants(
        city=city,
        category=category,
        price=price
    )






# Obtener ciudades y categorías para los filtros
@router.get("/filter-options")
def get_filter_options():
    return restaurant_service.get_filter_options()





# Obtener un restaurante por su ID
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: str):
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado"
        )

    return restaurant


# Crear un restaurante
@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(data: RestaurantCreate):
    return restaurant_service.create_restaurant(data)


# Actualizar un restaurante
@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(restaurant_id: str, data: RestaurantUpdate):
    restaurant = restaurant_service.update_restaurant(restaurant_id, data)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado"
        )

    return restaurant


# Eliminar un restaurante
@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: str):
    deleted = restaurant_service.delete_restaurant(restaurant_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado"
        )

    return {
        "mensaje": "Restaurante eliminado correctamente"
    }
