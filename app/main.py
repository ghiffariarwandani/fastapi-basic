from scalar_fastapi import get_scalar_api_reference
from fastapi import FastAPI

from app.core.settings import settings
from app.router.product import product_router

app = FastAPI(
    title=settings.app_name,
    version=settings.version
)

app.include_router(product_router)

@app.get(path="/scalar")

def get_scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title
    )