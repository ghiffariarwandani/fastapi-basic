from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.router.category import category_router
from app.router.product import product_router

app = FastAPI(title=settings.app_name, version=settings.version)

app.include_router(product_router)
app.include_router(category_router)


@app.get(path="/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
