from pydantic import BaseModel, Field


# Datos básicos de un restaurante
class RestaurantBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    city: str = Field(min_length=1, max_length=50)
    price: int = Field(ge=1, le=3)
    photoUrl: str | None = None


# Datos necesarios para registrar un restaurante
class RestaurantCreate(RestaurantBase):
    pass


# Datos que se pueden modificar
class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    city: str | None = Field(default=None, min_length=1, max_length=50)
    price: int | None = Field(default=None, ge=1, le=3)
    photoUrl: str | None = None


# Datos que devolverá la aplicación
class RestaurantResponse(RestaurantBase):
    id: str
    avgRating: float = 0
    numRatings: int = 0