
from app.core.firebase import db


# Diez restaurantes de ejemplo para FriendlyEats
restaurants = [
    {
        "name": "La Abuela",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        "avgRating": 4.5,
        "numRatings": 20
    },
    {
        "name": "Pizza Central",
        "category": "Pizza",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
        "avgRating": 4.0,
        "numRatings": 12
    },
    {
        "name": "Sushi House",
        "category": "Japonesa",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c",
        "avgRating": 4.7,
        "numRatings": 35
    },
    {
        "name": "Burger Town",
        "category": "Hamburguesas",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
        "avgRating": 4.2,
        "numRatings": 18
    },
    {
        "name": "El Buen Taco",
        "category": "Mexicana",
        "city": "Cholula",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b",
        "avgRating": 4.3,
        "numRatings": 25
    },
    {
        "name": "Pasta Bella",
        "category": "Italiana",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601",
        "avgRating": 4.6,
        "numRatings": 30
    },
    {
        "name": "Café del Parque",
        "category": "Cafetería",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb",
        "avgRating": 4.1,
        "numRatings": 14
    },
    {
        "name": "Mar y Tierra",
        "category": "Mariscos",
        "city": "Veracruz",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b",
        "avgRating": 4.4,
        "numRatings": 22
    },
    {
        "name": "Verde Natural",
        "category": "Saludable",
        "city": "Cholula",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "avgRating": 4.5,
        "numRatings": 16
    },
    {
        "name": "Dulce Tentación",
        "category": "Postres",
        "city": "CDMX",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1551024506-0bccd828d307",
        "avgRating": 4.8,
        "numRatings": 40
    }
]


def seed_restaurants():
    collection = db.collection("restaurants")
    created = 0
    skipped = 0

    for restaurant in restaurants:
        existing = (
            collection
            .where("name", "==", restaurant["name"])
            .limit(1)
            .stream()
        )

        if next(existing, None):
            print(f"Ya existe: {restaurant['name']}")
            skipped += 1
            continue

        collection.add(restaurant)
        print(f"Creado: {restaurant['name']}")
        created += 1

    print("\nCarga de datos finalizada.")
    print(f"Restaurantes nuevos: {created}")
    print(f"Restaurantes omitidos: {skipped}")


if __name__ == "__main__":
    seed_restaurants()
