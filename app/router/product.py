from uuid import UUID
from sqlmodel import select
from fastapi import APIRouter, Depends, Header, status, HTTPException

from app.models.database import Product
from app.schema.product import ProductRequest
from app.utils.query_params import pagination
from app.models.engine import get_session

product_router = APIRouter(tags=['product'])

@product_router.get(path='/products', status_code=status.HTTP_200_OK)
def get_products(params = Depends(pagination), db = Depends(get_session), request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a")):
  stmt = select(Product)
  result = db.exec(stmt.offset(params["offset"]).limit(params["limit"])).all()

  return {
    "data": result,
    "message": "Success retrieve products"
  }

@product_router.post(path='/products')
def post_products(body:ProductRequest, db = Depends(get_session), request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a")):
  try:
    product = Product(**body.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    return {
      "data": product,
      "message": "Success create product"
    }
  
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
