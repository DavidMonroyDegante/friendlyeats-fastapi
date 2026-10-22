from app.core.firebase import db
from app.domain.models import Restaurant


# Nombre de la colección en Firestore
COLLECTION_NAME = "restaurants"


# Obtener todos los restaurantes
def get_all():
    restaurants = []

    documents = db.collection(COLLECTION_NAME).stream()

    for document in documents:
        data = document.to_dict()
        data["id"] = document.id

        restaurants.append(Restaurant(**data))

    return restaurants


# Obtener un restaurante por su ID
def get_by_id(restaurant_id: str):
    document = (
        db.collection(COLLECTION_NAME)
        .document(restaurant_id)
        .get()
    )

    if not document.exists:
        return None

    data = document.to_dict()
    data["id"] = document.id

    return Restaurant(**data)


# Crear un restaurante
def create(restaurant: Restaurant):
    data = restaurant.model_dump(exclude={"id"})

    document = db.collection(COLLECTION_NAME).document()
    document.set(data)

    data["id"] = document.id

    return Restaurant(**data)


# Actualizar un restaurante
def update(restaurant_id: str, changes: dict):
    document = (
        db.collection(COLLECTION_NAME)
        .document(restaurant_id)
    )

    if not document.get().exists:
        return None

    document.update(changes)

    return get_by_id(restaurant_id)


# Eliminar un restaurante
def delete(restaurant_id: str):
    document = (
        db.collection(COLLECTION_NAME)
        .document(restaurant_id)
    )

    if not document.get().exists:
        return False

    document.delete()

    return True





# Filtrar restaurantes por ciudad, categoría y precio
def filter_restaurants(
    city: str | None = None,
    category: str | None = None,
    price: int | None = None
):
    query = db.collection(COLLECTION_NAME)

    if city:
        query = query.where("city", "==", city)

    if category:
        query = query.where("category", "==", category)

    if price is not None:
        query = query.where("price", "==", price)

    restaurants = []

    for document in query.stream():
        data = document.to_dict()
        data["id"] = document.id

        restaurants.append(Restaurant(**data))

    return restaurants
