from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.api.v1.restaurants import router as restaurants_router


app = FastAPI(
    title=settings.APP_NAME,
    description="API para consultar y administrar restaurantes de FriendlyEats",
    version="1.0.0"
)

# Archivos CSS, JavaScript e imágenes
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Plantillas HTML
templates = Jinja2Templates(directory="app/templates")

# Registrar la API existente
app.include_router(restaurants_router)


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="restaurants.html",
        context={}
    )


# ==========================================
# FORMULARIO PARA REGISTRAR RESTAURANTES
# ==========================================
@app.get("/restaurant/new")
def restaurant_form(request: Request):
    restaurant_id = request.query_params.get("id", "")

    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={
            "mode": "edit" if restaurant_id else "create",
            "restaurant_id": restaurant_id
        }
    )


# ==========================================
# PÁGINA DE DETALLES Y EDICIÓN
# ==========================================
@app.get("/restaurant/{restaurant_id}")
def restaurant_detail(request: Request, restaurant_id: str):
    return templates.TemplateResponse(
        request=request,
        name="restaurant_detail.html",
        context={
            "restaurant_id": restaurant_id
        }
    )





@app.get("/health")
def health_check():
    return {"status": "ok"}