from fastapi import APIRouter, HTTPException, Response, status

from app.domain.schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.services import restaurant_service


router = APIRouter(
    prefix="/api/v1/restaurants",
    tags=["Restaurantes"]
)


# Obtener restaurantes con paginación y ordenamiento
@router.get("/", response_model=list[RestaurantResponse])
def get_restaurants(
    limit: int = 20,
    start_after: str | None = None,
    order_by: str = "name"
):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El límite debe estar entre 1 y 100"
        )

    if order_by not in ("name", "avgRating"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El orden debe ser name o avgRating"
        )

    return restaurant_service.get_paginated_restaurants(
        limit=limit,
        start_after=start_after,
        order_by=order_by
    )



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



# Actualizar parcialmente un restaurante
@router.patch("/{restaurant_id}", response_model=RestaurantResponse)
def patch_restaurant(restaurant_id: str, data: RestaurantUpdate):
    restaurant = restaurant_service.update_restaurant(restaurant_id, data)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado"
        )

    return restaurant


# Eliminar un restaurante
@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_restaurant(restaurant_id: str):
    deleted = restaurant_service.delete_restaurant(restaurant_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
