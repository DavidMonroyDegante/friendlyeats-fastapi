from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.restaurants import router as restaurants_router


app = FastAPI(
    title=settings.APP_NAME,
    description="API para consultar y administrar restaurantes de FriendlyEats",
    version="1.0.0"
)


# Registrar las rutas de restaurantes
app.include_router(restaurants_router)


# Ruta principal para comprobar que la aplicación funciona
@app.get("/")
def home():
    return {
        "mensaje": "Bienvenido a FriendlyEats",
        "estado": "Aplicación funcionando correctamente"
    }