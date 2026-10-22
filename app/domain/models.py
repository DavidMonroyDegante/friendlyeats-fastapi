from pydantic import BaseModel


class Restaurant(BaseModel):
    id: str | None = None
    name: str
    category: str
    city: str
    price: int
    photoUrl: str | None = None
    avgRating: float = 0
    numRatings: int = 0