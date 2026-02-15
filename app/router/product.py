from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.database import Product
from app.models.engine import get_session
from app.schema.product import (
    ProductCreateResponse,
    ProductListResponse,
    ProductRequest,
    ProductResponse,
    ProductUpdate,
)
from app.utils.query_params import pagination

product_router = APIRouter(tags=["Product"])


@product_router.get(path="/products", status_code=status.HTTP_200_OK, response_model=ProductListResponse)
def get_products(params=Depends(pagination), db=Depends(get_session)):
    stmt = select(Product).options(selectinload(Product.categories))
    result = db.exec(stmt.offset(params["offset"]).limit(params["limit"])).all()

    return {"data": result, "message": "Success retrieve products"}


@product_router.get(path="/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product_by_id(product_id: UUID, db=Depends(get_session)):
    result = db.get(Product, product_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return result


@product_router.delete(path="/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(
    product_id: UUID,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    result = db.get(Product, product_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    db.delete(result)
    db.commit()
    return None


@product_router.put(path="/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductCreateResponse)
def update_product_by_id(
    product_id: UUID,
    product: ProductUpdate,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    result = db.get(Product, product_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_product = product.model_dump(exclude_unset=True)
    for key, value in update_product.items():
        setattr(result, key, value)

    db.add(result)
    db.commit()
    db.refresh(result)

    return {"data": result, "message": "Success update product"}


@product_router.post(path="/products", response_model=ProductCreateResponse)
def post_products(
    body: ProductRequest,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    try:
        product = Product(**body.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)

        return {"data": product, "message": "Success create product"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU already exists")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
