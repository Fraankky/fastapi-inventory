from app.routers.stock_movement_router import movement_router
from app.routers.category_router import category_router
from app.routers.product_router import product_router
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION
)

app.include_router(category_router)
app.include_router(product_router)
app.include_router(movement_router)

@app.get("/")
def root():
    return {"message": "Inventory API is running"}

@app.get("/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)