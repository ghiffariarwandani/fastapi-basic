from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.models.database import Category
from app.models.engine import get_session
from app.schema.category import CategoryCreateResponse, CategoryListResponse, CategoryRequest, CategoryUpdate
from app.utils.query_params import pagination

category_router = APIRouter(tags=["Category"])


@category_router.get(path="/categories", status_code=status.HTTP_200_OK, response_model=CategoryListResponse)
def get_categories(params=Depends(pagination), db=Depends(get_session)):
    stmt = select(Category)
    result = db.exec(stmt.offset(params["offset"]).limit(params["limit"])).all()

    return {"data": result, "message": "Success retrieve categories"}


@category_router.get(
    path="/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryCreateResponse
)
def get_category_by_id(category_id: UUID, db=Depends(get_session)):
    result = db.get(Category, category_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    return {"data": result, "message": "Success retrieve category"}


@category_router.post(path="/categories", response_model=CategoryCreateResponse, status_code=status.HTTP_201_CREATED)
def post_categories(
    body: CategoryRequest,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    try:
        category = Category(**body.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)

        return {"data": category, "message": "Success create category"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@category_router.delete(path="/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_by_id(
    category_id: UUID,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    result = db.get(Category, category_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(result)
    db.commit()
    return None


@category_router.put(
    path="/categories/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryCreateResponse
)
def update_category_by_id(
    category_id: UUID,
    category: CategoryUpdate,
    db=Depends(get_session),
    request_id: UUID = Header(..., alias="X-Request-ID", example="25769c6cd34d4bfeba98e0ee856f3e7a"),
):
    result = db.get(Category, category_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_category = category.model_dump(exclude_unset=True)
    for key, value in update_category.items():
        setattr(result, key, value)

    try:
        db.add(result)
        db.commit()
        db.refresh(result)

        return {"data": result, "message": "Success update category"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
